# Method

The attack pins a public CIFAR-10 VGG11-BN weight file by SHA-256, fetches the
first 16 test rows from the revision-pinned Hugging Face Dataset Viewer API,
selects the first two correctly classified examples, and rejects a random
sphere start if it is already adversarial. Every image and the row response are
hashed. At each step the optimizer receives only ten signs comparing symmetric
exponential-map probes; function values are retained only by the experiment
harness.

The horizon route spans 19 tilts from -0.45 to 0.45 radians. It uses exactly the
paper's step count, probe radius, and step size. Reversed comparison signs are
the negative control.

The exact attack route retains `nu=eta=1e-6` and cross-entropy. A separate
calibration route uses `nu=0.01`, `eta=0.04`, radius 0.5, and the standard
true-label logit margin on four inputs. A fifth, duplicated input receives
reversed signs as a simultaneous negative control. The calibration values are
fixed in committed code before the held-out run.
