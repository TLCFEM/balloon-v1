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


def K_m(z, z_r, k_r, k_b):
    denom = 1 - k_b * np.log(1 - z_r)
    epsilon = 1e-8
    z_diff = np.where(np.abs(z - z_r) < epsilon, epsilon, z - z_r)
    exponent = z / (k_r * z_diff)
    return (1 - np.exp(exponent)) / denom


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)

    z_r = 0.85
    k_b = 0.3

    ls_gen = line_style_generator()
    plt.figure(figsize=(5, 2))
    for k_r in [0.2, 0.5, 1.0, 2.0, 5]:
        z = np.linspace(0, z_r - 1e-4, 200)
        plt.plot(z, K_m(z, z_r, k_r, k_b), linestyle=next(ls_gen))

    ax = plt.gca()
    ax.annotate(
        "",
        xy=(0.9, 0.4),
        xytext=(0.9, 0.8),
        arrowprops=dict(arrowstyle="<|-|>", lw=1.5, color="red"),
    )
    ax.annotate(r"$k_b$", xy=(0.92, 0.65))
    ax.annotate(
        "",
        xy=(0.75, 0.85),
        xytext=(0.95, 0.85),
        arrowprops=dict(arrowstyle="<|-|>", lw=1.5, color="red"),
    )
    ax.annotate(r"$z_r$", xy=(0.85, 0.89))
    ax.annotate(
        r"$k_r$",
        xy=(0.65, 0.2),
        xytext=(0.25, 0.7),
        arrowprops=dict(arrowstyle="<|-|>", lw=1.5, color="red"),
    )

    plt.xlabel(r"$z$")
    plt.ylabel(r"$K_m(z)$")
    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("illustration_km.pdf")
