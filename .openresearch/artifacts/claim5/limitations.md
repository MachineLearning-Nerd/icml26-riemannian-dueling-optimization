# Limitations and deviations

The paper does not identify its VGG checkpoint, CIFAR indices, random seeds, or
exact attack radius. This route pins defensible public choices and records
them. The official HLW images require accepting a separate non-transferable
research license; no acceptance is inferred. The SO(2) optimizer is therefore
tested on deterministic tilt annotations without claiming that the pixels are
from HLW.

The exact paper-setting attack did not misclassify either tested input. The
calibrated route changes probe radius, step size, sphere radius, and objective,
so it tests the claimed application mechanism rather than numerical identity
to Figure 4.
