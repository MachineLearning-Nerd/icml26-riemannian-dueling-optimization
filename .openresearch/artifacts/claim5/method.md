# Method

The attack pins a public CIFAR-10 VGG11-BN weight file by SHA-256, selects the
first two correctly classified test examples from the first 128 indices, and
rejects a random sphere start if it is already adversarial. At each step the
optimizer receives only ten signs comparing symmetric exponential-map probes;
function values are retained only by the experiment harness.

The horizon route spans 19 tilts from -0.45 to 0.45 radians. It uses exactly the
paper's step count, probe radius, and step size. Reversed comparison signs are
the negative control.
