from pathlib import Path
import zipfile
root_dir = Path(__file__).parent.parent
zipped_dir = root_dir / "input-files" / "twic-pgns-zipped"
extracted_dir = root_dir / "output-files" / "twic-pgns2"
total = 0
for filepath in zipped_dir.iterdir():
    if filepath.suffix == ".zip":
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
            total += 1
print(total)