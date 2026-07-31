# Limitations and deviations

- Lemma 3.2's constant is settled exactly in closed form for every dimension;
  the Monte Carlo rows are corroboration of that closed form, not its source.
- Lemma 3.1 is universally quantified over `x`, `v`, `nu` and `f`. The 13-cell
  `gamma_x < 1` sweep independently varies `d`, `nu`, `L` and
  `||grad f(x)||` and reproduces the bound's functional form, but a finite
  sweep corroborates a universal statement rather than proving it.
- The sweep uses Euclidean `R^d`, a zero-curvature Hadamard manifold covered by
  the paper's assumptions. Positively curved cases are not covered here; the
  sphere and SPD routes appear under Claims 5 and 6.
- The measured disagreement rate sits at `gamma_x/(2d)`, so `gamma_x` is a
  valid but conservative bound. This is reported, not treated as a defect: the
  lemma states an upper bound, not an equality.
- **Withdrawn:** an earlier revision reported a finite-`nu` falsification. Its
  cells had `gamma_x` between 11.28 and 1410.47, where Lemma 3.1 guarantees
  nothing, so they were never a valid counterexample. They are retained as a
  consistency record.
- Runtime figures are for the cumulative suite, not Claim 4 in isolation.
