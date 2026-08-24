"""Generate exact replayable evidence for (1,4,5,6,7,11,13,16) being a seedless band tuple."""
from fractions import Fraction
from itertools import combinations, product
from math import gcd
from search_prep import (
    is_band_tuple, merged_coverage, coverage_intervals,
    seed_certificates, has_coefficient_two_relation, band_radius, primitive
)

v = (1, 4, 5, 6, 7, 11, 13, 16)
n = len(v)

print("=== TUPLE ===")
print(f"v = {v}, n = {n}")
print(f"gcd = {gcd(*v)}")
print(f"primitive = {primitive(v)}")
print(f"band_radius(8) = 2/17 = {band_radius(n)}")
print()

print("=== BAND MEMBERSHIP ===")
merged = merged_coverage(v)
print(f"Merged intervals covering [0,1]:")
for i, (left, right) in enumerate(merged):
    print(f"  [{left}, {right}]")
band = is_band_tuple(v)
print(f"is_band_tuple: {band}")
# Verify it's a single interval covering [0,1]
print(f"  starts at 0: {merged[0][0] == 0}")
print(f"  ends at 1: {merged[-1][1] == 1}")
print()

print("=== SEED CERTIFICATE SEARCH ===")
certs = seed_certificates(v)
print(f"seed_certificates: {certs}")
print()

print("=== EXHAUSTIVE SEED SET FAILURE EVIDENCE ===")
indices = tuple(range(n))

for size in (1, 2):
    print(f"--- Size-{size} candidate sets ---")
    for support in combinations(indices, size):
        # Check condition 1: no coeff-2 relation in S
        has_internal_rel = has_coefficient_two_relation(v, support)
        if has_internal_rel:
            print(f"  S={support} (indices {[v[i] for i in support]}): FAILS condition 1 (has internal relation)")
            continue
        # Check condition 2: every outsider j has a coeff-2 relation in S ∪ {j} with c_j != 0
        outsiders = [j for j in indices if j not in support]
        missing = []
        for j in outsiders:
            ext_support = tuple(sorted((*support, j)))
            if not has_coefficient_two_relation(v, ext_support, required_index=j):
                missing.append(j)
        if missing:
            print(f"  S={support} (values {[v[i] for i in support]}): FAILS condition 2 for outsiders {missing} (values {[v[j] for j in missing]})")
        else:
            print(f"  S={support} (values {[v[i] for i in support]}): WOULD BE CERTIFICATE (but this should not happen)")

print()
print("=== CONCLUSION ===")
print(f"v = {v} is a band tuple: {band}")
print(f"v has a seed certificate: {bool(certs)}")
print(f"v is a SEEDLESS BAND TUPLE: {band and not certs}")
