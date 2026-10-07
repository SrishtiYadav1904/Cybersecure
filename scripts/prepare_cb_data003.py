from pathlib import Path
import pandas as pd

root = Path(__file__).resolve().parents[1]
source_dir = root / "data" / "unified" / "cyberbullying"
output_dir = root / "data" / "unified" / "cyberbullying_cb003"
splits = {}

for name in ("train", "validation", "test"):
    data = pd.read_parquet(source_dir / f"{name}.parquet")

    noisy = (
        (data["source_dataset"] == "Kaggle-CB-Tweets-v1")
        & (data["source_label"].astype(str) == "other_cyberbullying")
    )
    print(f"{name}: excluding {int(noisy.sum())} uncertain Kaggle rows")
    splits[name] = data.loc[~noisy].copy()

output_dir.mkdir(parents=True, exist_ok=True)

for name, data in splits.items():
    data.to_parquet(output_dir / f"{name}.parquet", index=False)
    print(f"{name}: kept {len(data)} rows; labels:")
    print(data["label"].value_counts().sort_index().to_string())

hashes = {
    name: set(data["text_hash"].dropna())
    for name, data in splits.items()
}

for left, right in (("train", "validation"), ("train", "test"), ("validation", "test")):
    overlap = hashes[left] & hashes[right]
    if overlap:
        raise RuntimeError(f"{left}/{right} overlap: {len(overlap)} hashes")
print("Saved CB-DATA-003 splits; hashes are disjoint.")