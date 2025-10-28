import os
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize

plt.rcParams.update({"font.size": 6})

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


def gplot(x, y, *, cmap=None, color=None, linewidth=2, size=(6, 5)):
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.arange(len(x))

    points = np.array([x, y]).T.reshape(-1, 1, 2)

    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    if cmap:
        lc = LineCollection(
            segments,  # type: ignore
            cmap=cmap,
            linewidth=linewidth,
            norm=Normalize(z.min(), z.max()),
        )
    else:
        lc = LineCollection(segments, colors=color, linewidth=linewidth)  # type: ignore
    lc.set_array(z)

    fig = plt.figure(figsize=size, tight_layout=True)
    ax = fig.add_subplot(111)
    ax.grid(True, linestyle="--", linewidth=0.5)
    ax.add_collection(lc)
    ax.autoscale()

    return fig, ax


class AutoSwitch(TemporaryDirectory):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        super().__init__(*args, **kwargs)

    def __enter__(self):
        target = super().__enter__()
        os.chdir(target)
        run_model(self.model)
        return target
