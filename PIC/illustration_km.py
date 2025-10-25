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
    return 1 - np.exp((1 - z_r) / k_r * z / (z - 1))


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)

    ls_gen = line_style_generator()
    plt.figure(figsize=(5, 2))
    ax = plt.gca()

    for k_r in [0.5, 1, 2, 5, 1e1]:
        z = np.linspace(0, 1.0, 80, endpoint=False)
        plt.plot(z, K_m(z, 0.5, k_r), linestyle=next(ls_gen), color="#ca0020")

    ax.annotate(
        r"$k_r\uparrow~z_r\uparrow$",
        xy=(0.9, 0.2),
        xytext=(0.3, 0.7),
        arrowprops=dict(arrowstyle="-|>", lw=1.5, color="#0571b0"),
    )

    plt.xlabel(r"$z$")
    plt.ylabel(r"$K_m$")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True, linestyle="--", linewidth=0.5)
    plt.tight_layout()
    plt.savefig("illustration_km.pdf")
