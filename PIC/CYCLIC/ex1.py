import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

import numpy as np
from runner import AutoSwitch, gplot, run_model


model = r"""
node 1 0 0
node 2 1 0

material Balloon1D 1 \
1 1E0 4 \
1E2 0 -1E2 15E-1 \ ! u
1 1e-8 0 0 \ ! hfm
0 0 0 2E-2 \ ! hfc
0 0 0 0 \ ! ha
0 0 0 0 \ ! hd
1E-2 1. \ ! fc
2E-2 1. \ ! alpha
1E-2 1. ! d

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t t<1?1-cos(2pi*t):t<2?1.5-1.5*cos(2pi*t):t<3?2-2cos(2pi*t):t<4?2.5-2.5cos(2pi*t):3-3cos(2pi*t)

amplitude Custom 3 1

disp 1 3 2 1 2

step static 1 5
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

        fig, ax = gplot(strain[:, 1], stress[:, 1], cmap="rainbow")
        ax.set_xlabel("normalised strain (1)")
        ax.set_ylabel("normalised stress (1)")
        fig.savefig(prefix / "_balloon.stress.pdf")
