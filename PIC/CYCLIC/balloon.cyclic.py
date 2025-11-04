import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from runner import AutoSwitch, gplot

model = r"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
1 5E2 10 \
1E0 0 -0.9 1E-1 \ ! u
1 1E-2 0 0 \ ! hfm
0 0 3E-1 2E-2 \ ! hfc
1E-1 0 0 0 \ ! ham
0 0 0 0 \ ! hac
1E-2 1. \ ! fc
1E-2 1. \ ! ac
2E-2 1. \ ! alpha
1E-2 .9 ! d

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


if __name__ == "__main__":
    prefix = Path(__file__).parent
    sys.path.insert(0, str(prefix.resolve()))

    with AutoSwitch(model=model):
        strain = np.loadtxt("R3-E1.txt")
        stress = np.loadtxt("R2-S1.txt")
        hist = np.loadtxt("R1-HIST1.txt")

        fig, ax = gplot(strain[:, 1], stress[:, 1], cmap="rainbow")
        ax.set_xlabel("normalised strain (1)")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "_balloon.stress.pdf")

        items = [
            (4, "$q_m$", "qm"),
            (5, "$z$", "z"),
            (6, "$f_c$", "fc"),
            (8, r"$a$", "a"),
        ]

        for idx, label, filename in items:
            fig, ax = gplot(strain[:, 1], hist[:, idx], cmap="rainbow")
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

        fig = plt.figure(figsize=(6, 5), tight_layout=True)
        ax = fig.add_subplot(111)
        ax.grid(True)
        ax.plot(
            range(len(turning_points)),
            turning_points,
            color="#d73027",
            marker=".",
            linestyle="None",
        )
        fig.savefig(prefix / "_balloon.cyclic.pdf")
