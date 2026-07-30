# Method

At each dimension, draw 80,000 standard Gaussian vectors, normalize them to
the tangent unit sphere, and average `sign(<v,u>)u`. Project the mean parallel
and perpendicular to an independently sampled unit vector `v`.

The checker independently computes the exact spherical constant
`sqrt(d) Gamma(d/2) / (sqrt(pi) Gamma((d+1)/2))`. The negative control removes
the sign and pairs every direction with its antipode, forcing a zero mean.
