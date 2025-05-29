from pathlib import Path
import zipfile
zipped_dir = Path(__file__).parent / 'twic-pgns-zipped'
extracted_dir = Path(__file__).parent / 'twic-pgns'
total = 0
for filepath in zipped_dir.iterdir():
    if filepath.suffix == ".zip":
        with zipfile.ZipFile(filepath, 'r') as zip_ref:
            zip_ref.extractall(extracted_dir)
            total += 1
print(total)