"""Run the n=8 exhaustive scan for seedless band tuples."""
import json
import sys
from itertools import combinations
from search_prep import primitive, is_band_tuple, seed_certificates

max_height = 20
n = 8
results = []
band_count = 0
checked = 0

for v in combinations(range(1, max_height + 1), n):
    if not primitive(v):
        continue
    checked += 1
    if checked % 10000 == 0:
        print(f"  checked {checked} primitive tuples, {band_count} band tuples so far", flush=True)
    if not is_band_tuple(v):
        continue
    band_count += 1
    certs = seed_certificates(v)
    if not certs:
        print(f"SEEDLESS BAND TUPLE: {v}", flush=True)
        results.append(list(v))

print(f"\nDone. Checked {checked} primitive 8-tuples, found {band_count} band tuples.")
print(f"Seedless band tuples: {len(results)}")
if results:
    print("Seedless tuples:", results)
else:
    print("No seedless band tuples found for n=8.")

# Save results
with open("n8_results.json", "w") as f:
    json.dump({"seedless_band_tuples": results, "band_count": band_count, "primitive_checked": checked}, f, indent=2)
