# Bootstrapping Execution Guide

Complete the [installation and build steps](README.md) first. Run the commands below from the repository root.

<a id="cpp"></a>

## 1. Running the C++ example

Set the shared library path:

```bash
export LD_LIBRARY_PATH="$PWD/build-bootstrap/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
```

Run the CoeffsToSlots-first variant:

```bash
./build-bootstrap/bin/bootstrap simple
```

Run the SlotsToCoeffs-first variant:

```bash
./build-bootstrap/bin/bootstrap stc
```

The C++ executable uses `stc`, while the Python example uses `stoc`. Running the C++ executable without an argument prints usage information and exits with code 1.

### Reading the output

The example generates and encrypts a message, consumes levels, performs bootstrapping, and prints the decrypted result and timings.

- `Message vector` / `Result vector`: samples of the input and decrypted output
- `Before Bootstrapping` / `After Bootstrapping`: remaining levels before and after bootstrapping, as calculated by the example
- `avg`: average bit precision based on relative error, excluding inputs close to zero
- Timer output: time spent creating the context, running setup, generating keys, and performing bootstrapping

Accuracy and runtime depend on the GPU, build options, and input. Check the decrypted values and precision as well as whether the process completes.

### Sparse example status

The executable also accepts `sparse`, but `SparseBootStrapping()` is currently marked `Doesn't work yet` in the source. Use `simple` or `stc` for initial validation. The sparse example also hardcodes GPU index `2`.

<a id="python"></a>

## 2. Running the Python example

After building the Python bindings as described in the README, run:

```bash
source .venv/bin/activate
export PYTHONPATH="$PWD/build-python/lib${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$PWD/build-python/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"

python python/examples/ckks_bootstrapping.py --order ctos
python python/examples/ckks_bootstrapping.py --order stoc
```

If `--order` is omitted, the example defaults to `ctos`.

### Reading the output

- `order`: selected stage order
- `chain index`: chain indices of the input and output ciphertexts
- `setup/key generation`: elapsed time for setup and key generation
- `bootstrap`: elapsed time for the bootstrapping call, as measured by the Python example
- `MSE` / `max error`: mean squared error and maximum absolute error between the input and decrypted output
- `first 8 values`: the first eight input and output values

The chain index is not the number of remaining levels, so it should not be interpreted as the C++ example's level count. Python timings use `time.perf_counter()` and may cover a different scope from the C++ GPU timers.

## 3. Selecting a GPU

The regular C++ example uses CUDA device 0. To select another GPU, control which GPU is visible to the process. This example exposes GPU 1 as device 0 within the process:

```bash
CUDA_VISIBLE_DEVICES=1 ./build-bootstrap/bin/bootstrap simple
CUDA_VISIBLE_DEVICES=1 python python/examples/ckks_bootstrapping.py --order ctos
```

## 4. Changing the default parameters

The regular C++ and Python examples use these defaults:

| Parameter | Default |
| --- | --- |
| Ring dimension | `2^16` (65536) |
| Slots | `N / 2` (32768) |
| Scale | `2^59` |
| Level budget | `[2, 2]` |
| Levels after bootstrap setting | `11` |
| Number of special moduli | `10` |

For the regular examples, the CLI selects the stage order. To change parameters, edit the source:

- C++: `SimpleBootstrapExample()` in [bootstrapping_example.cu](bootstrapping/bootstrapping_example.cu). Rebuild with `cmake --build build-bootstrap --target bootstrap -j 4` after editing.
- Python: `main()` in [ckks_bootstrapping.py](python/examples/ckks_bootstrapping.py).

Ring dimension, modulus chain, slots, level budget, and the number of level-consuming operations are related and should be reviewed together.

## 5. Runtime troubleshooting

- **`ModuleNotFoundError: pyPhantom`:** Check that the extension was built in `build-python/lib`, that `PYTHONPATH` includes this directory, and that you are using the Python environment selected at build time.
- **`libPhantom.so` not found:** Prepend the appropriate build directory's `lib` path to `LD_LIBRARY_PATH`.
- **CUDA out of memory:** Check GPU memory usage with `nvidia-smi` and select a GPU with enough available memory.
- **`invalid device ordinal`:** Check that the selected GPU exists and verify `CUDA_VISIBLE_DEVICES`.
- **`no kernel image is available`:** Rebuild in a new build directory with `CMAKE_CUDA_ARCHITECTURES` set for the target GPU.
