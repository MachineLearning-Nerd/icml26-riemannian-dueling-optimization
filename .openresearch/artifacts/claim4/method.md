# Method

At each dimension, draw 80,000 standard Gaussian vectors, normalize them to
the tangent unit sphere, and average `sign(<v,u>)u`. Project the mean parallel
and perpendicular to an independently sampled unit vector `v`.

The checker independently computes the exact spherical constant
`sqrt(d) Gamma(d/2) / (sqrt(pi) Gamma((d+1)/2))`. The negative control removes
the sign and pairs every direction with its antipode, forcing a zero mean.

For finite perturbations, independently draw 200,000 unit directions at each
of `d=2,5,10,50`. On the Euclidean unit ball at `x=0`, use
`f(z)=e1^T z + (20d/6)(a^T z)^3`, where
`a=(e1+e2)/sqrt(2)`. This objective is smooth on the bounded domain, has
nonzero gradient, curvature zero, and keeps both probes in the domain.

Compare the actual central-difference sign with `sign(<grad f(0),u>)` at
`nu=1e-4` and `nu=0.5`. Forty blocked paired means estimate the orthogonal
bias and its 95% lower bound. A linear-objective control at `nu=0.5` must have
zero disagreement.
