import sys
from pathlib import Path

import numpy as np
from runner import AutoSwitch, gplot

dt = 1e-2
interval = int(0.25 / dt)

model = rf"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
200 1e2 2 \
4E3 0 -3.6E3 1e3 \ ! u
.6 2 0 0 \ ! hfm
0 0 -.1 1e2 \ ! hfc
.1 0 0 0 \ ! ham
0 0 0 0 \ ! hac
5E1 1. \ ! fc
1E0 1. \ ! ac
1E2 1. \ ! na
1E2 .8 ! nd

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t t<40?3sin(2pi*t):t<80?5sin(2pi*t):t<120?7sin(2pi*t):10sin(2pi*t)

amplitude Custom 3 1

disp 1 3 1e-3 1 2

step static 1 130
set fixed_step_size 1
set ini_step_size {dt}
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

        fig, ax = gplot(
            strain[:, 1] * 1000, stress[:, 1] * 1000, cmap="rainbow", size=(4, 2.5)
        )
        ax.set_xlabel("strain ($10^{-3}$)")
        ax.set_ylabel("stress (MPa)")
        fig.savefig(prefix / "../cs1018.2.pdf")

        turning_points = stress[interval :: 2 * interval, 1]
        fig, ax = gplot(
            np.array(range(len(turning_points))) / 2,
            turning_points * 1000,
            color="#ca0020",
            size=(4, 2.5),
            scatter=True,
        )
        ax.set_xlabel("cycles")
        ax.set_ylabel("stress (MPa)")
        fig.savefig(prefix / "../cs1018.2.cycle.pdf")

        for idx, label, filename in [
            (4, "qm", "qm"),
            (6, "hfc", "hfc"),
            (8, "a", "a"),
            (9, "d", "d"),
        ]:
            fig, ax = gplot(
                strain[:, 1] * 1000, hist[:, idx], cmap="rainbow", size=(4, 2.5)
            )
            ax.set_xlabel("strain ($10^{-3}$)")
            ax.set_ylabel(label)
            fig.savefig(prefix / f"_{filename}.pdf")
