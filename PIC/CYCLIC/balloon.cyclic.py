import os
import subprocess
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 6})


def new_fig():
    fig = plt.figure(figsize=(6, 2.5), tight_layout=True)
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

    subprocess.run([SUANPAN_EXE, "-f", "balloon.cyclic.sp"], stdout=subprocess.DEVNULL)

    strain = np.loadtxt("R3-E1.txt")
    stress = np.loadtxt("R2-S1.txt")
    hist = np.loadtxt("R1-HIST1.txt")

    fig, ax = new_fig()

    ax.plot(
        strain[:, 1] * 1e3, stress[:, 1], color="#d73027", marker="x", markevery=149
    )
    ax.legend(["$\\sigma$"], loc="upper left")
    ax.set_xlabel("strain ($1/1000$)")
    ax.set_ylabel("stress (MPa)")
    ax.set_xbound(min(strain[:, 1] * 1e3), max(strain[:, 1] * 1e3))
    ax.set_ybound(1.1 * min(stress[:, 1]), 1.1 * max(stress[:, 1]))

    fig.savefig("cyclic.total.pdf")

    fig, ax = plot_gradient_line(
        strain[:, 1] * 1e3, stress[:, 1], marker=None, cmap="rainbow"
    )
    ax.set_xlabel("strain ($1/1000$)")
    ax.set_ylabel("stress (MPa)")
    fig.savefig("cyclic.gradient.pdf")

    fig, ax = new_fig()

    ax.plot(strain[:, 1] * 1e3, hist[:, 5], color="#d73027", marker="x", markevery=149)
    ax.legend(["$z$"], loc="upper left")
    ax.set_xlabel("strain ($1/1000$)")
    ax.set_ylabel("normal yield ratio $z$")
    ax.set_xbound(min(strain[:, 1] * 1e3), max(strain[:, 1] * 1e3))
    ax.set_ybound(0, 1.1)

    print(max(hist[:, 5]))

    fig.savefig("cyclic.ratio.total.pdf")

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
    fig.savefig("cyclic.stress.total.pdf")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    plot()
