import os
import shutil
import subprocess
from pathlib import Path

if os.name == "nt":
    SUANPAN_EXE = (
        "C:\\Users\\Theodore\\Documents\\Repos\\suanPan\\MSVC\\Release\\suanPan.exe"
    )
    target = Path(SUANPAN_EXE)
    if not target.exists():
        raise RuntimeError(f"suanPan.exe not found at {SUANPAN_EXE}.")
else:
    SUANPAN_EXE = "suanpan"
    if shutil.which(SUANPAN_EXE) is None:
        raise RuntimeError("suanPan not found.")


def run_model(model: str):
    with open("balloon.sp", "w") as file:
        file.write(model)
    subprocess.run([SUANPAN_EXE, "-f", "balloon.sp"], capture_output=True, text=True)
