import os
import shutil
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep

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


def run_model(model: str, print_result: bool = False):
    with open("balloon.sp", "w") as file:
        file.write(model)
    result = subprocess.run(
        [SUANPAN_EXE, "-f", "balloon.sp"], capture_output=True, text=True
    )
    if print_result or "[ERROR]" in result.stdout:
        print(result.stdout)


COUNTER = 1


def gplot(x, y, *, cmap=None, color=None, linewidth=1, size=(6, 5), scatter=False):
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

    global COUNTER
    COUNTER += 1
    fig = plt.figure(COUNTER, size, layout="tight")
    ax = fig.gca()
    ax.grid(True, linestyle="--", linewidth=0.5)
    if scatter:
        ax.scatter(x, y, 2, color)
    else:
        ax.add_collection(lc)
    ax.autoscale()

    return fig, ax


class AutoSwitch(TemporaryDirectory):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop("model")
        self.print_result = kwargs.pop("print_result", False)
        super().__init__(*args, **kwargs)
        self._old_cwd = None

    def __enter__(self):
        self._old_cwd = os.getcwd()
        target = super().__enter__()
        os.chdir(target)
        run_model(self.model, self.print_result)
        return target

    def __exit__(self, exc_type, exc_value, traceback):
        if self._old_cwd is not None:
            sleep(1)
            os.chdir(self._old_cwd)
        return super().__exit__(exc_type, exc_value, traceback)
