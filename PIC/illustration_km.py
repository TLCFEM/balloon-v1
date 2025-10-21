import os
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

import matplotlib

matplotlib.rcParams.update({"font.size": 6})


def line_style_generator():
    """
    Generator that yields different matplotlib line styles dynamically.
    """
    styles = ["-", "--", "-.", ":"]
    dash_styles = [
        (0, (3, 1, 1, 1)),
        (0, (5, 5)),
        (0, (1, 1)),
        (0, (5, 2, 1, 2)),
        (0, (2, 2, 8, 2)),
    ]
    i = 0
    while True:
        if i < len(styles):
            yield styles[i]
        else:
            yield dash_styles[(i - len(styles)) % len(dash_styles)]
        i += 1


def K_m(z, z_r, k_r):
    return 1 - np.exp((z - z_r) / k_r / (z - 1.0))


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)

    z_r = 0.35

    ls_gen = line_style_generator()
    plt.figure(figsize=(5, 2))
    for k_r in [1e-1, 0.2, 0.5, 1.0, 2.0, 5, 1e1]:
        z = np.linspace(z_r, 1.0, 80, endpoint=False)
        plt.plot(z, K_m(z, z_r, k_r), linestyle=next(ls_gen))

    ax = plt.gca()
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["0.0", "1.0"])
    ax.text(0.35, -0.05, r"$z_r$", ha="center", va="top", transform=ax.transAxes)
    ax.annotate(
        r"$k_r$",
        xy=(0.9, 0.2),
        xytext=(0.3, 0.7),
        arrowprops=dict(arrowstyle="<|-|>", lw=1.5, color="red"),
    )

    plt.xlabel(r"$z$")
    plt.ylabel(r"$K_m(z)$")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig("illustration_km.pdf")
