# Method

Execute Algorithm 2 literally on `f(x)=x²/2`, `X=[-2,2]`, then rerun the same
oracle sequence with the Appendix-F schedule as an independent control.

Independently execute eight proof-consistent recurrent phases with ten seeds at
each `d=4,8,16`. Regress the median log2 suboptimality against phase and count
every two-probe comparison. The predeclared verification interval is
`[-1.2,-0.8]` bits per phase; comparison counts must be dimension-linear.
