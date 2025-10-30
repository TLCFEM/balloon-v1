import sys
from pathlib import Path

import numpy as np
from runner import AutoSwitch, gplot

dt = 2e-3
interval = int(0.25 / dt)

model = rf"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
1 1E1 10 \
1E1 0 0 0 \ ! u
1 1e-2 0 0 \ ! hfm
0 0 1 2e-1 \ ! hfc
0 0 0 0 \ ! ha
0 0 0 0 \ ! hd
2E-1 1. \ ! fc
1E0 1. \ ! alpha
1E0 1. ! d

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

# expression SimpleScalar 1 t t<10?1-cos(2pi*t):t<20?1.5-1.5*cos(2pi*t):t<30?2-2cos(2pi*t):t<40?2.5-2.5cos(2pi*t):3-3cos(2pi*t)
expression SimpleScalar 1 t t<10?sin(2pi*t):t<20?1.5sin(2pi*t):t<30?2sin(2pi*t):t<40?2.5sin(2pi*t):3sin(2pi*t)

amplitude Custom 3 1

disp 1 3 2 1 2

step static 1 50
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

        fig, ax = gplot(strain[:, 1], stress[:, 1], cmap="rainbow", size=(4, 2.5))
        ax.set_xlabel("normalised strain (1)")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "../ex3.hardening.pdf")

        turning_points = stress[interval :: 2 * interval, 1]
        fig, ax = gplot(
            np.array(range(len(turning_points))) / 2,
            turning_points,
            color="#ca0020",
            size=(4, 2.5),
            scatter=True,
        )
        ax.set_xlabel("cycles")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "../ex3.hardening.cycle.pdf")
