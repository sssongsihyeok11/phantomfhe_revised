# phantom-fhe_revised

GPU-accelerated CKKS implementation with bootstrapping support, targeting machine learning workloads.

## Current Features

* CKKS bootstrapping (implemented using codex (reference : openfhe-development, NEXUS)
* GPU-accelerated homomorphic operations

## Current Limitations
* Encryption currently requires an auxiliary modulus (special prime) used for key switching.

## Planned Features

* Support encryption without an auxiliary modulus
* Simple machine learning inference
* Coefficient encoding
* Noise flooding
* Key switching optimization
