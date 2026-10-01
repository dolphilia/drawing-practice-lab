"""Copy PNGs under shuffled IDs. Does not alter originals or image pixels."""
import csv, random, shutil, sys
from pathlib import Path
if len(sys.argv) != 3:
    raise SystemExit("Usage: python3 blind.py INPUT_DIRECTORY NEW_OUTPUT_DIRECTORY")
source, output = map(Path, sys.argv[1:])
files = sorted(source.glob("*.png"))
if not files:
    raise SystemExit("No PNG files")
key = output.parent / (output.name + "-key.csv")
if output.exists() or key.exists():
    raise SystemExit("Output or key exists; choose a new name")
random.SystemRandom().shuffle(files)
output.mkdir(parents=True)
with key.open("x", newline="") as handle:
    writer = csv.writer(handle)
    writer.writerow(["image_id", "original_file"])
    for i, path in enumerate(files, 1):
        ident = f"image-{i:03d}.png"
        shutil.copyfile(path, output / ident)
        writer.writerow([ident, path.name])
print(f"Copied {len(files)} PNGs. Key: {key}")
