# phantom-fhe-bootstrapping

A CUDA-accelerated CKKS bootstrapping implementation based on PhantomFHE, with C++ examples and Python bindings.

This document covers installation and building. See the [execution guide](RUNNING.md) for commands to run the examples and explanations of their output.

## 1. Prerequisites

- Linux and an NVIDIA GPU
- NVIDIA GPU driver and CUDA Toolkit, including `nvcc`
- A C++17 compiler compatible with your CUDA Toolkit
- CMake: the project requires at least 3.20. Use 3.24 or later for the `native` GPU architecture detection used below.
- Git and Make or Ninja
- Python 3.9 or later and Python development headers for the Python examples

The default bootstrapping examples use a ring dimension of `2^16` and `2^15` slots. Keys and precomputed data require substantial GPU memory; memory usage depends on the parameters.

On Ubuntu/Debian, install the basic build tools:

```bash
sudo apt-get update
sudo apt-get install -y build-essential git cmake python3-dev python3-venv
```

Install the CUDA Toolkit and GPU driver separately, then check your environment:

```bash
nvidia-smi
nvcc --version
cmake --version
```

The CUDA version shown by `nvidia-smi` may differ from the installed Toolkit version, so check `nvcc` as well.

## 2. Get the source

```bash
git clone --recursive https://github.com/sssongsihyeok11/phantomfhe_revised.git phantom-fhe-bootstrapping
cd phantom-fhe-bootstrapping
```

Run all subsequent commands from the repository root. If you already have the source, change to that directory.

## 3. Build C++ and Python together

Use one `build` directory for the shared library, C++ bootstrapping executable,
and Python extension. Activate your Python environment before configuring.
The bindings use `python/pybind11`; if it is missing, run
`git submodule update --init --recursive`. The coefficient example requires NumPy:

```bash
python -m pip install numpy

cmake -S . -B build \
  -DCMAKE_BUILD_TYPE=Release \
  -DCMAKE_CUDA_ARCHITECTURES=native \
  -DPHANTOM_ENABLE_BOOTSTRAP=ON \
  -DPHANTOM_ENABLE_EXAMPLE=OFF \
  -DPHANTOM_ENABLE_BENCH=OFF \
  -DPHANTOM_ENABLE_TEST=OFF \
  -DPHANTOM_ENABLE_PYTHON_BINDING=ON \
  -DPYTHON_EXECUTABLE="$(command -v python)"

cmake --build build -j 4
```

Build outputs:

- `build/lib/libPhantom.so`: shared library
- `build/bin/bootstrap`: C++ bootstrapping executable
- `build/lib/pyPhantom*.so`: Python extension

You can run the example directly from the build directory without installing it system-wide. See [Running the C++ example](RUNNING.md#cpp).

## 4. Use the Python bindings

Set the module and library paths, then verify the import. Activate the environment and set these paths again when opening a new terminal.

```bash
export PYTHONPATH="$PWD/build/lib${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$PWD/build/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
python -c "import pyPhantom; print(pyPhantom.__file__)"
python python/examples/ckks_coefficient_Test.py
```

See [Running the Python example](RUNNING.md#python) to execute bootstrapping.

## 5. Build troubleshooting

- **`nvcc` not found:** Add the CUDA Toolkit's `bin` directory to `PATH`, or pass `-DCMAKE_CUDA_COMPILER=/path/to/cuda/bin/nvcc` to CMake.
- **GPU architecture detection fails:** Configure on a machine where the GPU is visible, or replace `-DCMAKE_CUDA_ARCHITECTURES=native` with the target GPU's architecture number. The installed Toolkit must support that architecture.
- **Out of memory during compilation:** Reduce build parallelism to `-j 2` or `-j 1`.
- **Missing Python headers or pybind11:** Check that Python development headers and `python/pybind11/CMakeLists.txt` are present.
- **Changed compiler, source location, or Python environment:** Reconfigure the same directory with `cmake --fresh -S . -B build` and the options above (requires CMake 3.24 or later).
- **CUDA 12.0 reports `__builtin_dynamic_object_size` errors:** Add `-DCMAKE_CUDA_FLAGS="-U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2"` to the configure command.

## License

This project (PhantomFHE) is released under GPLv3 license. See [LICENSE](LICENSE) for more information.

Some files contain the modified code from [Microsoft SEAL](https://github.com/microsoft/SEAL). These codes are released
under MIT License. See [MIT License](https://github.com/microsoft/SEAL/blob/main/LICENSE) for more information.

Some files contain the modified code from [OpenFHE](https://github.com/openfheorg/openfhe-development). These codes are
released under BSD 2-Clause License.
See [BSD 2-Clause License](https://github.com/openfheorg/openfhe-development/blob/main/LICENSE) for more information.

## Citation

If you use Phantom in your research, please cite the following paper:

```
@article{DBLP:journals/tdsc/YangSDZLZ24,
  author       = {Hao Yang and
                  Shiyu Shen and
                  Wangchen Dai and
                  Lu Zhou and
                  Zhe Liu and
                  Yunlei Zhao},
  title        = {Phantom: {A} CUDA-Accelerated Word-Wise Homomorphic Encryption Library},
  journal      = {{IEEE} Trans. Dependable Secur. Comput.},
  volume       = {21},
  number       = {5},
  pages        = {4895--4906},
  year         = {2024},
  url          = {https://doi.org/10.1109/TDSC.2024.3363900},
  doi          = {10.1109/TDSC.2024.3363900},
  timestamp    = {Fri, 20 Sep 2024 14:01:59 +0200},
  biburl       = {https://dblp.org/rec/journals/tdsc/YangSDZLZ24.bib},
  bibsource    = {dblp computer science bibliography, https://dblp.org}
}
```

If you are exploring BFV optimizations, please also cite the following paper:

```
@article{PhantomFHE_BFV,
    author={Shen, Shiyu and Yang, Hao and Dai, Wangchen and Zhou, Lu and Liu, Zhe and Zhao, Yunlei},
    journal={IEEE Transactions on Computers},
    title={Leveraging GPU in Homomorphic Encryption: Framework Design and Analysis of BFV Variants},
    year={2024},
    volume={73},
    number={12},
    pages={2817-2829},
    doi={10.1109/TC.2024.3457733},
}
```
