from math import sqrt
import os
import subprocess
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({"font.size": 6})


def F(q):
    return 232 + 70 * (1 - np.exp(-q * 30))

def H(q):
    return 209 + 63 * (1 - np.exp(-q * 30))

def new_fig():
    fig = plt.figure(figsize=(6, 2.5), tight_layout=True)
    ax1 = fig.add_subplot(111)
    ax1.grid(True)
    return fig, ax1


def plot():
    if os.name != "posix":
        print("This script only works on linux.")
        return

    if subprocess.run(["which", "suanpan"]).returncode != 0:
        print("suanPan not found, please install it first.")
        return

    subprocess.run(["suanpan", "-f", "cyclic.sp"], stdout=subprocess.DEVNULL)

    strain = np.loadtxt("R3-E1.txt")
    stress = np.loadtxt("R2-S1.txt")
    hist = np.loadtxt("R1-HIST1.txt")

    fig, ax = new_fig()

    ax.plot(
        strain[:, 1] * 1e3, stress[:, 1], color="#d73027", marker="x", markevery=149
    )
    ax.plot(
        strain[:, 1] * 1e3,
        hist[:, 6] * F(hist[:, 2]),
        color="#4575b4",
        marker="+",
        markevery=151,
    )
    ax.legend(["$\\sigma$", "$Fd$"], loc="upper left")
    ax.set_xlabel("strain ($1/1000$)")
    ax.set_ylabel("stress (MPa)")
    ax.set_xbound(0, max(strain[:, 1] * 1e3))
    ax.set_ybound(1.1 * min(stress[:, 1]), 1.1 * max(stress[:, 1]))

    fig.savefig("cyclic.total.pdf")

    fig, ax = new_fig()

    ax.plot(strain[:, 1] * 1e3, hist[:, 3], color="#d73027", marker="x", markevery=149)
    ax.legend(["$z$"], loc="upper left")
    ax.set_xlabel("strain ($1/1000$)")
    ax.set_ylabel("normal yield ratio $z$")
    ax.set_xbound(0, max(strain[:, 1] * 1e3))
    ax.set_ybound(0, 1.1)

    ax = ax.twinx()
    ax.plot(strain[:, 1] * 1e3, hist[:, 6], color="#4575b4", marker="+", markevery=151)
    ax.legend(["$d$"], loc="upper right")
    ax.set_ylabel("similarity vector $d$")
    ax.set_xbound(0, max(strain[:, 1] * 1e3))
    ax.set_ybound(0, 1.1)

    fig.savefig("cyclic.ratio.total.pdf")

    fig, ax = new_fig()

    ax.plot(hist[:, 2] * 1e3, hist[:, 3], color="#d73027", marker="x", markevery=149)
    ax.legend(["$z$"], loc="upper left")
    ax.set_xlabel("accumulated plastic strain $q$ ($1/1000$)")
    ax.set_ylabel("normal yield ratio $z$")
    ax.set_xbound(0, max(hist[:, 2] * 1e3))
    ax.set_ybound(0, 1.1)

    ax = ax.twinx()
    ax.plot(
        hist[:, 2] * 1e3,
        0.7 - 0.7 * np.exp(-143 * sqrt(1.5) * hist[:, 2]),
        color="#4575b4",
        marker="+",
        markevery=347,
        linestyle="dashed",
        linewidth=1,
    )
    ax.plot(hist[:, 2] * 1e3, hist[:, 6], color="#4575b4", marker="+", markevery=151)
    ax.legend(["monotonic bound $d$", "$d$"], loc="upper right")
    ax.set_ylabel("similarity vector $d$")
    ax.set_xbound(0, max(hist[:, 2] * 1e3))
    ax.set_ybound(0, 1.1)

    fig.savefig("cyclic.ratio.plastic.pdf")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    plot()
