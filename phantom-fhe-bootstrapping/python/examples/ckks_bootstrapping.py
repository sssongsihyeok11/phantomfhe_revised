"""CKKS bootstrapping example for both CtoS-first and StoC-first variants.

Build the extension from the repository root, then run for example:
    python python/examples/ckks_bootstrapping.py --order ctos
    python python/examples/ckks_bootstrapping.py --order stoc

The default parameters target an NVIDIA GPU with enough memory for N=2^16.
"""

import argparse
import math
import time

import pyPhantom as phantom


def make_message(slots: int) -> list[float]:
    """Return deterministic values in the recommended CKKS bootstrap range."""
    return [0.8 * math.sin(2.0 * math.pi * i / 257.0) for i in range(slots)]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--order",
        choices=("ctos", "stoc"),
        default="ctos",
        help="bootstrap stage ordering (default: ctos)",
    )
    args = parser.parse_args()

    ring_dimension = 1 << 16
    slots = ring_dimension // 2
    scale = 2.0**59
    level_budget = [2, 2]
    levels_after_bootstrap = 11
    special_moduli = 10

    bootstrap_depth = phantom.ckks_bootstrapper.depth(level_budget)
    multiplicative_depth = levels_after_bootstrap + bootstrap_depth
    modulus_bits = [60] + [59] * multiplicative_depth + [60] * special_moduli

    parameters = phantom.params(phantom.scheme_type.ckks)
    parameters.set_poly_modulus_degree(ring_dimension)
    parameters.set_special_modulus_size(special_moduli)
    parameters.set_coeff_modulus(
        phantom.create_coeff_modulus(ring_dimension, modulus_bits)
    )

    print(f"creating CKKS context (N={ring_dimension}, moduli={len(modulus_bits)})")
    context = phantom.context(parameters)
    secret_key = phantom.secret_key(context)
    public_key = secret_key.gen_publickey(context)
    encoder = phantom.ckks_encoder(context)

    message = make_message(slots)
    plaintext = encoder.encode_double_vector(context, message, scale)
    ciphertext = public_key.encrypt_asymmetric(context, plaintext)
    ciphertext.precompute_scale(context, scale)
    scaling_factors = ciphertext.scaling_factors()
    large_scaling_factors = ciphertext.large_scaling_factors()

    # Consume the application levels. StoC-first retains the levels required by
    # its initial low-modulus SlotsToCoeffs transform.
    for _ in range(25):
        phantom.eval_mult_const_inplace(context, ciphertext, 1.0, scaling_factors)

    order = (
        phantom.ckks_bootstrap_order.ctos_first
        if args.order == "ctos"
        else phantom.ckks_bootstrap_order.stoc_first
    )
    bootstrapper = phantom.ckks_bootstrapper(encoder)

    started = time.perf_counter()
    bootstrapper.setup(
        context,
        level_budget,
        scale,
        scaling_factors,
        large_scaling_factors,
        [0, 0],
        slots,
        0,
        True,
        order,
    )
    bootstrapper.generate_multiplication_key(secret_key, context)
    bootstrapper.generate_bootstrap_keys(secret_key, context, slots)
    setup_seconds = time.perf_counter() - started

    input_chain = ciphertext.chain_index()
    started = time.perf_counter()
    refreshed = bootstrapper.bootstrap(ciphertext, context, slots)
    bootstrap_seconds = time.perf_counter() - started

    decoded = encoder.decode_double_vector(
        context, secret_key.decrypt(context, refreshed)
    )[:slots]
    max_error = max(abs(expected - actual) for expected, actual in zip(message, decoded))
    mse = sum((expected - actual) ** 2 for expected, actual in zip(message, decoded)) / slots

    print(f"order: {args.order}-first")
    print(f"chain index: {input_chain} -> {refreshed.chain_index()}")
    print(f"setup/key generation: {setup_seconds:.3f} s")
    print(f"bootstrap: {bootstrap_seconds:.3f} s")
    print(f"MSE: {mse:.6e}; max error: {max_error:.6e}")
    print("first 8 values:")
    for expected, actual in zip(message[:8], decoded[:8]):
        print(f"  {expected:+.8f} -> {actual:+.8f}")


if __name__ == "__main__":
    main()
