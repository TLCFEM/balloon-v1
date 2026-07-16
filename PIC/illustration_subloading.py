import os
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({"font.size": 6})

isotropic_stress = 3e2
hardening = 0
kinematic_stress = 2e2

z_rate = 4e2
a_rate = 1e3
d_rate = 2e3

model = rf"""
node 1 0 0
node 2 1 0

material Subloading1D 1 2E5 \
{isotropic_stress} {hardening} 0 0 \
0 0 0 0 \
{z_rate} {a_rate} {d_rate} 0

material Subloading1D 2 2E5 \
{isotropic_stress} {hardening} 0 0 \
{kinematic_stress} 0 0 0 \
{z_rate} {a_rate} {d_rate} 0

material Subloading1D 3 2E5 \
{isotropic_stress} {hardening} 0 0 \
0 0 0 0 \
{z_rate} {a_rate} {d_rate} 0.9

material Subloading1D 4 2E5 \
{isotropic_stress} {hardening} 0 0 \
{kinematic_stress} 0 0 0 \
{z_rate} {a_rate} {d_rate} 0.9

element T2D2 1 1 2 1 1
element T2D2 2 1 2 2 1
element T2D2 3 1 2 3 1
element T2D2 4 1 2 4 1

plainrecorder 1 Element S 1 2 3 4
plainrecorder 2 Element E 1 2 3 4

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t 0.5-0.5*cos(2pi*t)

amplitude Custom 3 1

disp 1 3 1e-2 1 2

step static 1 1
set fixed_step_size 1
set ini_step_size 1E-3
set symm_mat 0

converger RelIncreDisp 1 1E-10 10 0

analyze

save recorder 1 2

exit
"""


def new_fig():
    fig = plt.figure(figsize=(5, 2), tight_layout=True)
    ax1 = fig.add_subplot(111)
    ax1.grid(True)
    return fig, ax1


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

    with TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        with open("subloading.sp", "w") as file:
            file.write(model)
        subprocess.run(
            [SUANPAN_EXE, "-f", "subloading.sp"], capture_output=True, text=True
        )

        fig, ax = new_fig()
        for number, label in zip(
            (1, 2, 3, 4),
            (
                "no hardening",
                r"with $\mathbf{\alpha}$",
                r"with $\mathbf{d}$",
                r"with $\mathbf{\alpha}$ and $\mathbf{d}$",
            ),
        ):
            stress = np.loadtxt(f"R1-S{number}.txt")
            strain = np.loadtxt(f"R2-E{number}.txt")

            ax.plot(strain[:, 1] * 1e3, stress[:, 1], label=label)

        ax.legend()
        ax.set_xlabel("strain ($1/1000$)")
        ax.set_ylabel("stress (MPa)")

        fig.savefig(Path(__file__).parent / "illustration_subloading.pdf")


if __name__ == "__main__":
    plot()
