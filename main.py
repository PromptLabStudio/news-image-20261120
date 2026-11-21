from pathlib import Path
import shutil


source = Path(__file__).with_name("image.png")
destination_dir = Path("/output")
destination_dir.mkdir(parents=True, exist_ok=True)
shutil.copyfile(source, destination_dir / "entry.png")
