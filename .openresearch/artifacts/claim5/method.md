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
