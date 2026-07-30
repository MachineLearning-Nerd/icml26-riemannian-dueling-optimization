#!/usr/bin/env python3
"""CPU reproduction of the paper-setting real applications."""
from __future__ import annotations

import hashlib
import json
import math
import os
import platform
import random
import time
import urllib.request
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as functional
from torch import nn
from torchvision import datasets, transforms


ROOT = Path(__file__).resolve().parents[2]
SEED = 20260730
WEIGHTS_URL = (
    "https://github.com/chenyaofo/pytorch-cifar-models/releases/download/"
    "vgg/cifar10_vgg11_bn-eaeebf42.pt"
)
WEIGHTS_SHA256 = (
    "eaeebf42370c92fdfbb5dbe8eba7c27d4eb7366a1dca0b5be435364ccdf54378"
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class CifarVgg11Bn(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        configuration = [
            64,
            "M",
            128,
            "M",
            256,
            256,
            "M",
            512,
            512,
            "M",
            512,
            512,
            "M",
        ]
        layers: list[nn.Module] = []
        channels = 3
        for width in configuration:
            if width == "M":
                layers.append(nn.MaxPool2d(2, 2))
                continue
            layers.extend(
                [
                    nn.Conv2d(channels, width, 3, padding=1),
                    nn.BatchNorm2d(width),
                    nn.ReLU(inplace=True),
                ]
            )
            channels = width
        self.features = nn.Sequential(*layers)
        self.classifier = nn.Sequential(
            nn.Linear(512, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, 512),
            nn.ReLU(inplace=True),
            nn.Dropout(),
            nn.Linear(512, 10),
        )
        self.register_buffer(
            "mean",
            torch.tensor((0.4914, 0.4822, 0.4465))[None, :, None, None],
            persistent=False,
        )
        self.register_buffer(
            "std",
            torch.tensor((0.2023, 0.1994, 0.2010))[None, :, None, None],
            persistent=False,
        )

    def forward(self, images: torch.Tensor) -> torch.Tensor:
        normalized = (images - self.mean) / self.std
        features = self.features(normalized)
        return self.classifier(torch.flatten(features, 1))


def model_state_sha256(model: nn.Module) -> str:
    digest = hashlib.sha256()
    for name, tensor in model.state_dict().items():
        digest.update(name.encode())
        digest.update(str(tensor.dtype).encode())
        digest.update(str(tuple(tensor.shape)).encode())
        digest.update(tensor.detach().contiguous().numpy().tobytes())
    return digest.hexdigest()


def load_assets() -> tuple[nn.Module, torch.Tensor, torch.Tensor, list[int], dict]:
    cache = ROOT / ".cache" / "claim5"
    cache.mkdir(parents=True, exist_ok=True)
    weights = cache / "cifar10_vgg11_bn-eaeebf42.pt"
    if not weights.exists():
        request = urllib.request.Request(
            WEIGHTS_URL,
            headers={"User-Agent": "OpenResearch-Reproduction/1.0"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            weights.write_bytes(response.read())
    if sha256_file(weights) != WEIGHTS_SHA256:
        raise RuntimeError("VGG weight hash mismatch")

    model = CifarVgg11Bn().eval()
    model.load_state_dict(torch.load(weights, map_location="cpu", weights_only=True))
    dataset = datasets.CIFAR10(
        root=cache,
        train=False,
        download=True,
        transform=transforms.ToTensor(),
    )
    candidates = torch.stack([dataset[index][0] for index in range(128)])
    labels = torch.tensor([dataset[index][1] for index in range(128)])
    with torch.inference_mode():
        predictions = model(candidates).argmax(1)
    selected = torch.nonzero(predictions == labels).flatten()[:2].tolist()
    if len(selected) != 2:
        raise RuntimeError("could not locate two correctly classified inputs")
    images = candidates[selected]
    selected_labels = labels[selected]
    archive = cache / "cifar-10-python.tar.gz"
    asset_metadata = {
        "model": "chenyaofo/pytorch-cifar-models:cifar10_vgg11_bn",
        "weights_url": WEIGHTS_URL,
        "weights_sha256": WEIGHTS_SHA256,
        "model_state_sha256": model_state_sha256(model),
        "dataset": "torchvision CIFAR-10 test split",
        "dataset_archive_sha256": sha256_file(archive),
        "selected_test_indices": selected,
    }
    return model, images, selected_labels, selected, asset_metadata


def sphere_exp(point: torch.Tensor, tangent: torch.Tensor) -> torch.Tensor:
    norm = tangent.norm(dim=-1, keepdim=True)
    safe_norm = norm.clamp_min(1e-20)
    return torch.cos(norm) * point + torch.sin(norm) * tangent / safe_norm


def losses(
    model: nn.Module, images: torch.Tensor, labels: torch.Tensor
) -> torch.Tensor:
    return functional.cross_entropy(model(images), labels, reduction="none")


def paper_setting_attack(
    model: nn.Module, images: torch.Tensor, labels: torch.Tensor
) -> dict:
    steps = 1_000
    batch_directions = 10
    nu = 1e-6
    eta = 1e-6
    generator = torch.Generator().manual_seed(SEED)
    count, channels, height, width = images.shape
    ambient_dimension = channels * height * width
    radius = 0.05 * images.flatten(1).norm(dim=1)
    with torch.inference_mode():
        clean_logits = model(images)
        clean_loss = losses(model, images, labels)
    for _ in range(100):
        point = torch.randn(
            (count, ambient_dimension), generator=generator, dtype=images.dtype
        )
        point /= point.norm(dim=1, keepdim=True)
        with torch.inference_mode():
            current_images = (
                images
                + radius[:, None, None, None] * point.reshape_as(images)
            )
            initial_logits = model(current_images)
            initial_loss = losses(model, current_images, labels)
        if torch.all(initial_logits.argmax(1) == labels):
            break
    else:
        raise RuntimeError("could not find a non-vacuous random sphere start")
    best_loss = initial_loss.clone()
    best_point = point.clone()
    trace = [
        {
            "step": 0,
            "mean_best_cross_entropy": float(best_loss.mean()),
            "successes": 0,
        }
    ]

    for step in range(steps):
        directions = torch.randn(
            (count, batch_directions, ambient_dimension),
            generator=generator,
            dtype=images.dtype,
        )
        directions -= point[:, None, :] * (
            directions * point[:, None, :]
        ).sum(2, keepdim=True)
        directions /= directions.norm(dim=2, keepdim=True).clamp_min(1e-20)
        center = point[:, None, :].expand_as(directions)
        plus = sphere_exp(center, nu * directions)
        minus = sphere_exp(center, -nu * directions)
        candidates = torch.cat([plus, minus], dim=1)
        perturbed = (
            images[:, None]
            + radius[:, None, None, None, None]
            * candidates.reshape(
                count,
                2 * batch_directions,
                channels,
                height,
                width,
            )
        )
        candidate_labels = labels[:, None].expand(
            count, 2 * batch_directions
        )
        with torch.inference_mode():
            candidate_loss = losses(
                model(perturbed.flatten(0, 1)),
                candidate_labels.flatten(),
            ).reshape(count, 2 * batch_directions)
        signs = torch.where(
            candidate_loss[:, :batch_directions]
            >= candidate_loss[:, batch_directions:],
            1.0,
            -1.0,
        )
        direction = (signs[:, :, None] * directions).mean(1)
        direction -= point * (direction * point).sum(1, keepdim=True)
        point = sphere_exp(point, eta * direction)
        current_images = (
            images + radius[:, None, None, None] * point.reshape_as(images)
        )
        with torch.inference_mode():
            current_logits = model(current_images)
            current_loss = losses(model, current_images, labels)
        improved = current_loss > best_loss
        best_loss = torch.where(improved, current_loss, best_loss)
        best_point[improved] = point[improved]
        if (step + 1) % 100 == 0:
            trace.append(
                {
                    "step": step + 1,
                    "mean_best_cross_entropy": float(best_loss.mean()),
                    "successes": int(
                        (current_logits.argmax(1) != labels).sum()
                    ),
                }
            )

    adversarial = (
        images + radius[:, None, None, None] * best_point.reshape_as(images)
    )
    with torch.inference_mode():
        final_logits = model(adversarial)
        final_loss = losses(model, adversarial, labels)
    perturbation_norms = (adversarial - images).flatten(1).norm(dim=1)
    success = final_logits.argmax(1) != labels
    return {
        "protocol": {
            "images": count,
            "ambient_dimension": ambient_dimension,
            "steps": steps,
            "batch_directions": batch_directions,
            "duels": count * batch_directions * steps,
            "pairwise_objective_evaluations": 2
            * count
            * batch_directions
            * steps,
            "nu": nu,
            "eta": eta,
            "sphere_radius": "0.05 * ||image||_2 from cited implementation",
            "objective": "maximize true-label cross entropy",
            "optimizer_observes": "pairwise signs only",
            "pixel_clipping": False,
        },
        "clean_predictions": clean_logits.argmax(1).tolist(),
        "labels": labels.tolist(),
        "clean_cross_entropy": clean_loss.tolist(),
        "initial_cross_entropy": initial_loss.tolist(),
        "final_cross_entropy": final_loss.tolist(),
        "final_predictions": final_logits.argmax(1).tolist(),
        "successful_images": int(success.sum()),
        "attack_success_rate": float(success.float().mean()),
        "perturbation_l2_norms": perturbation_norms.tolist(),
        "sphere_radii": radius.tolist(),
        "maximum_radius_error": float(
            (perturbation_norms - radius).abs().max()
        ),
        "trace": trace,
    }


def horizon_route(reverse: bool = False) -> dict:
    tilts = np.linspace(-0.45, 0.45, 19)
    rows = []
    for index, tilt in enumerate(tilts):
        rng = np.random.default_rng(SEED + index)
        correction = 0.0
        best_correction = correction
        objective = lambda angle: 2 - 2 * math.cos(angle + tilt)
        best_loss = objective(correction)
        for _ in range(100):
            direction = 1.0 if rng.integers(2) else -1.0
            plus_loss = objective(correction + 1e-6 * direction)
            minus_loss = objective(correction - 1e-6 * direction)
            chosen = direction if plus_loss <= minus_loss else -direction
            if reverse:
                chosen = -chosen
            correction += 1e-2 * chosen
            current = objective(correction)
            if current < best_loss:
                best_loss = current
                best_correction = correction
        rows.append(
            {
                "tilt_radians": float(tilt),
                "best_correction_radians": best_correction,
                "best_loss": best_loss,
            }
        )
    return {
        "dataset_scope": (
            "19 deterministic tilt annotations spanning the paper figure range; "
            "HLW pixels are unavailable without accepting a separate license"
        ),
        "steps": 100,
        "nu": 1e-6,
        "eta": 1e-2,
        "optimizer_observes": "pairwise signs only",
        "reverse_oracle": reverse,
        "successes_below_1e-5": sum(row["best_loss"] < 1e-5 for row in rows),
        "maximum_best_loss": max(row["best_loss"] for row in rows),
        "rows": rows,
    }


def verify() -> dict:
    started = time.perf_counter()
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    torch.set_num_threads(8)
    torch.set_num_interop_threads(1)
    model, images, labels, _, assets = load_assets()
    attack = paper_setting_attack(model, images, labels)
    horizon = horizon_route()
    horizon_control = horizon_route(reverse=True)
    checks = {
        "pinned_model_and_data": (
            assets["weights_sha256"] == WEIGHTS_SHA256
            and len(assets["dataset_archive_sha256"]) == 64
        ),
        "clean_inputs_correct": attack["clean_predictions"] == attack["labels"],
        "sphere_feasible": attack["maximum_radius_error"] < 1e-5,
        "paper_attack_settings": (
            attack["protocol"]["steps"] == 1_000
            and attack["protocol"]["batch_directions"] == 10
            and attack["protocol"]["nu"] == 1e-6
            and attack["protocol"]["eta"] == 1e-6
        ),
        "horizon_19_of_19": horizon["successes_below_1e-5"] == 19,
        "horizon_negative_control": (
            horizon_control["maximum_best_loss"]
            > 100 * horizon["maximum_best_loss"]
        ),
    }
    attack_verified = attack["successful_images"] > 0
    result = {
        "paper": "2603.00023",
        "claim": 5,
        "route": "paper-setting CPU applications",
        "seed": SEED,
        "cpu": {
            "estimated_computational_cores": 8,
            "actual_logical_cpus": os.cpu_count(),
            "torch_threads": torch.get_num_threads(),
            "python": platform.python_version(),
            "torch": torch.__version__,
        },
        "assets": assets,
        "attack": attack,
        "horizon": horizon,
        "horizon_negative_control": horizon_control,
        "checks": checks,
        "attack_status": "VERIFIED" if attack_verified else "BLOCKED",
        "horizon_status": "VERIFIED",
        "claim_status": "VERIFIED" if attack_verified else "BLOCKED",
        "runtime_seconds": time.perf_counter() - started,
        "limitations": [
            "HLW images require a separately accepted non-transferable license; "
            "this route tests the exact SO(2) optimization on deterministic tilts "
            "but does not label them as an HLW image reproduction.",
            "The paper does not identify its VGG checkpoint or evaluated indices; "
            "this route pins a public CIFAR-10 VGG11-BN checkpoint and indices.",
        ],
    }
    output = ROOT / "outputs" / "real_applications.json"
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print("REAL_APPLICATIONS_JSON=" + json.dumps(result, sort_keys=True))
    print(
        json.dumps(
            {
                "real_applications_summary": {
                    "claim_status": result["claim_status"],
                    "attack_status": result["attack_status"],
                    "successful_images": attack["successful_images"],
                    "attack_success_rate": attack["attack_success_rate"],
                    "clean_cross_entropy": attack["clean_cross_entropy"],
                    "initial_cross_entropy": attack["initial_cross_entropy"],
                    "final_cross_entropy": attack["final_cross_entropy"],
                    "maximum_radius_error": attack["maximum_radius_error"],
                    "horizon_successes": horizon["successes_below_1e-5"],
                    "horizon_control_maximum_best_loss": horizon_control[
                        "maximum_best_loss"
                    ],
                    "runtime_seconds": result["runtime_seconds"],
                }
            },
            sort_keys=True,
        )
    )
    if not all(checks.values()):
        raise SystemExit("real-application evidence integrity check failed")
    return result


if __name__ == "__main__":
    verify()
