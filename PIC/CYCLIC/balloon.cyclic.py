import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 6})


model = r"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
1 5E2 10 \
1E0 0 -0.9 1E-1 \ ! u
1 1E-2 0 0 \ ! hfm
0 0 3E-1 2E-2 \ ! hfc
1E-1 0 0 0 \ ! ha
9E-1 1E-2 0 0 \ ! hd
1E-2 1. \ ! fc
2E-2 1. \ ! alpha
1E-2 1. ! d

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

# expression SimpleScalar 1 t t<20?1-cos(2pi*t):t<40?2-2cos(2pi*t):t<60?3-3cos(2pi*t):t<80?4-4cos(2pi*t):5-5cos(2pi*t)
expression SimpleScalar 1 t t<20?sin(2pi*t):t<40?2sin(2pi*t):t<60?3sin(2pi*t):t<80?4sin(2pi*t):5sin(2pi*t)

amplitude Custom 3 1

# cload 1 3 200 1 2
disp 1 3 10 1 2

step static 1 100
set fixed_step_size 1
set ini_step_size 1E-2
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 1

analyze

save recorder 1 2 3

exit
"""


def new_fig():
    fig = plt.figure(figsize=(6, 5), tight_layout=True)
    ax1 = fig.add_subplot(111)
    ax1.grid(True)
    return fig, ax1


def plot_gradient_line(
    x,
    y,
    cmap="viridis",
    linewidth=2,
    marker: str | None = "x",
    markevery=149,
):
    x = np.asarray(x)
    y = np.asarray(y)
    z = np.arange(len(x))

    points = np.array([x, y]).T.reshape(-1, 1, 2)

    lc = LineCollection(
        np.concatenate([points[:-1], points[1:]], axis=1),
        cmap=cmap,
        norm=Normalize(z.min(), z.max()),
    )
    lc.set_array(z)
    lc.set_linewidth(linewidth)

    # Plot
    fig, ax = new_fig()
    ax.add_collection(lc)
    ax.set_xlim(x.min(), x.max())
    ax.set_ylim(y.min(), y.max())

    # Add optional markers
    if marker:
        ax.plot(
            x[::markevery],
            y[::markevery],
            linestyle="None",
            marker=marker,
            color="black",
        )

    return fig, ax


SUANPAN_EXE = (
    ("C:\\Users\\Theodore\\Documents\\Repos\\suanPan\\MSVC\\Release\\suanPan.exe")
    if os.name == "nt"
    else "suanpan"
)


def plot():
    global SUANPAN_EXE
    if not SUANPAN_EXE:
        if subprocess.run(["which", "suanpan"]).returncode != 0:
            print("suanPan not found, please install it first.")
            return
        SUANPAN_EXE = "suanpan"

    prefix = Path(__file__).parent

    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with open("balloon.sp", "w") as file:
            file.write(model)
        subprocess.run(
            [SUANPAN_EXE, "-f", "balloon.sp"], capture_output=True, text=True
        )

        strain = np.loadtxt("R3-E1.txt")
        stress = np.loadtxt("R2-S1.txt")
        hist = np.loadtxt("R1-HIST1.txt")

        fig, ax = plot_gradient_line(
            strain[:, 1], stress[:, 1], marker=None, cmap="rainbow"
        )
        ax.set_xlabel("normalised strain (1)")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "_balloon.stress.pdf")

        items = [
            (4, "$q_m$", "qm"),
            (5, "$z$", "z"),
            (6, "$f_c$", "fc"),
            (7, r"$\alpha$", "alpha"),
        ]

        for idx, label, filename in items:
            fig, ax = plot_gradient_line(
                strain[:, 1], hist[:, idx], marker=None, cmap="rainbow"
            )
            ax.set_xlabel("normalised strain (1)")
            ax.set_ylabel(label)
            ax.set_xbound(min(strain[:, 1]), max(strain[:, 1]))

            print(f"{max(hist[:, idx]):.16e}")

            fig.savefig(prefix / f"_balloon.{filename}.pdf")

        turning_points = []
        for i in range(1, len(stress[:, 1]) - 1):
            if (stress[i - 1, 1] < stress[i, 1] > stress[i + 1, 1]) or (
                stress[i - 1, 1] > stress[i, 1] < stress[i + 1, 1]
            ):
                turning_points.append(stress[i, 1])

        fig, ax = new_fig()
        ax.plot(
            range(len(turning_points)),
            turning_points,
            color="#d73027",
            marker=".",
            linestyle="None",
        )
        fig.savefig(prefix / "_balloon.cyclic.pdf")


if __name__ == "__main__":
    plot()
