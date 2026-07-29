# STATUS — nDfDnsyllY

**State: PUBLIC + QUEUED — awaiting shared HF Space drain.**

- Six anchored claims, five source-complete CPU targets (C1–C4, C6).
- Pinned arXiv `2603.00023` source SHA-256:
  `1df1a267c036a4ef161c02719c4b88bb4cb321099d10b5ac3485a97a51e1a71d`.
- C5 is a CIFAR-10/VGG attack whose source references an external baseline
  repository but does not release the authors' RDNGD implementation,
  checkpoint, exact images, or processed data. It is not eligible for a proxy.
- C1–C4/C6 pass with schedule/reduction, Monte Carlo, wrong-oracle, and
  geometry controls. Rayleigh uses the paper's full 50,000 iterations at
  `d=100,150`; SPD/Karcher uses `n=5,10,m=50`.
- The fail-closed gate passes; Trackio contains five verified claim pages, the
  excluded-C5 page, Methods, Negative controls, full verifier/gate runs, and a
  pinned Conclusion. Secret scan found only bundled Trackio JavaScript names.
- Public GitHub repository is live at commit `1ed657d`; the full local gate
  preceded the canonical atomic backlog entry.
- The shared drain is the sole HF Space publisher. Next action is public Space
  readback after the quota permits creation.
