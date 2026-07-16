import sys
from pathlib import Path

import numpy as np
from runner import AutoSwitch, gplot

dt = 1e-2

model = r"""
node 1 0 0
node 2 1 0

material ExpMises1D 1 {mat_line}

element T2D2 1 1 2 1 1

plainrecorder 1 Element HIST 1
plainrecorder 2 Element S 1
plainrecorder 3 Element E 1

fix2 1 1 1
fix2 2 2 1 2

expression SimpleScalar 1 t t<1?30t:t<20?25sin(2pi*t)+30:t<21?30t-570:25sin(2pi*t)+60

amplitude Custom 3 1

disp 1 3 1e-4 1 2

step static 1 30
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

    size = (3.1, 2)

    def plot(mat_line, title, anno):
        with AutoSwitch(model=model.format(mat_line=mat_line, dt=dt)):
            strain = np.loadtxt("R3-E1.txt")
            stress = np.loadtxt("R2-S1.txt")

            fig, ax = gplot(
                strain[:, 1] * 1000, stress[:, 1] * 1000, cmap="rainbow", size=size
            )
            ax.set_xlabel("strain ($10^{-3}$)")
            ax.set_ylabel("stress (MPa)")
            ax.annotate(
                anno,
                xy=(6.8, 100),
                xytext=(5.5, -350),
                arrowprops=dict(arrowstyle="-|>", lw=1, color="#4daf4a"),
            )
            fig.savefig(prefix / f"../{title}.pdf")

    plot(
        "200 .4 .05 1e3 .0",
        "af.no.iso",
        "stabilizes with\nno/saturated\nisotropic hardening",
    )
    plot(
        "200 .4 0 0 .05",
        "af.iso",
        "reduces to elastic\ndue to unbounded\nisotropic hardening",
    )
