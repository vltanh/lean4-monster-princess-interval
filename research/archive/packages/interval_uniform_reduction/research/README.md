# Discovery code and unfinished searches — NOT exact certificates

These files record the search performed during this turn. None establishes a full-game saddle point. Numerical objectives, near-equalities, and floating-point pruning in this directory must not be read as proof certificates. Use the parent directory's `verify.py` for the exact assertions.

## Main path-network search

`network_transport.py` builds a planar spacetime graph from basis hider paths, allowing all routes obtained by switching at intersections. Face CDF potentials describe probability flows. For each candidate flow, `adaptive_batch.py` generates unrestricted monster responses; after a graph equilibrium is reached numerically, it tests the dual monster mixture against unrestricted princess paths and adds violating paths.

`integer_geometry.py` and `integer_deadline.py` retain integer geometry. The C++ discovery responses also retain exact geometry, but use floating-point objective comparisons. Their `complete` flag means the configured search finished under those comparisons; it does NOT mean an exact rational certificate was obtained. Iteration and node limits are explicit.

The Python discovery dependencies used were NumPy, SciPy, and Numba; versions are in `search_status.json`. The code uses SciPy's private HiGHS wrapper, so its API may vary across versions. A C++17 compiler and Boost multiprecision headers are needed for discovery response helpers.

From this directory:

```sh
g++ -O3 -std=c++17 fast_ordered.cpp -o ordered_monster
g++ -O3 -std=c++17 fast_batch.cpp -o ordered_batch
python adaptive_batch.py --inner
```

`--inner` resumes the latest unfinished graph optimization. `--resume` instead starts from the last numerically closed graph in `adaptive_checkpoint.json` and adds unrestricted princess responses. No run is promised to terminate with a saddle point. These commands may require substantial memory and computation.

The supplied `adaptive_checkpoint.json` is the completed graph iteration 3. Its numerically optimized matrix value is approximately 1.417589847; the dual monster's unrestricted princess response is approximately 1.635248228. Thus that dual is NOT an unrestricted matching upper strategy. The exact rational hider-response certificate extracted from this graph is in the parent directory, independently verified there.

`adaptive_inner.json` is a later, unfinished graph iteration. It is saved for reproducibility, not counted as a closed result. All active search processes were stopped before packaging.

## Other experiments

The `beam_grid_8` experiment used a broader line-intersection network. It closed numerically on its network, but failed the unrestricted princess check.

The `out_plateau_16` experiment tested waiting and outward–inward–outward variants against a larger two-turn monster family; it did not yield a saddle point.

The `upper_continuum_32` experiment optimized a denser sampled monster family against the unrestricted deadline-response oracle. Its floating result was NOT converted into a rational flow certificate in this run and is not part of the exact result.

`shape_search.py` and `dither.py` are support modules; some standalone entry points expect earlier experimental data not included here. They need not be run to resume the main adaptive search.
