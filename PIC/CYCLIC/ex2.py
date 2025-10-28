import sys
from pathlib import Path

import numpy as np
from runner import AutoSwitch, gplot

model = r"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
1 1E2 10 \
1E1 0 0 0 \ ! u
1 5e-2 0 0 \ ! hfm
0 0 0 0 \ ! hfc
.5 0 0 0 \ ! ha
0 0 0 0 \ ! hd
1E-2 1. \ ! fc
1E0 1. \ ! alpha
1E-2 1. ! d

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t t<5?1-cos(2pi*t):t<10?1.5-1.5*cos(2pi*t):t<15?2-2cos(2pi*t):t<20?2.5-2.5cos(2pi*t):3-3cos(2pi*t)
# expression SimpleScalar 1 t t<10?sin(2pi*t):t<20?1.5sin(2pi*t):t<30?2sin(2pi*t):t<40?2.5sin(2pi*t):3sin(2pi*t)

amplitude Custom 3 1

disp 1 3 2 1 2

step static 1 20
set fixed_step_size 1
set ini_step_size 2E-3
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
        fig.savefig(prefix / "../ex2.stagnation.pdf")

        turning_points = []
        for i in range(1, len(stress[:, 1]) - 1):
            if (stress[i - 1, 1] < stress[i, 1] > stress[i + 1, 1]) or (
                stress[i - 1, 1] > stress[i, 1] < stress[i + 1, 1]
            ):
                turning_points.append(stress[i, 1])
        turning_points = turning_points[::2]
        fig, ax = gplot(
            range(len(turning_points)),
            turning_points,
            color="#ca0020",
            size=(4, 2.5),
            scatter=True,
        )
        ax.set_xlabel("cycles")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "../ex2.stagnation.cycle.pdf")
