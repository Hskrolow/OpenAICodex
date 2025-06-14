# coding: utf-8
"""Visualize a Tonnetz on a torus.

Usage:
    python torus_tonnetz.py [x]

Where x is the number of points per pitch class.
"""
import matplotlib; matplotlib.use("Agg")
import math
import sys
from dataclasses import dataclass

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import for mpl
import numpy as np

PITCH_CLASSES = [
    "C", "C#", "D", "D#", "E", "F",
    "F#", "G", "G#", "A", "A#", "B"
]

@dataclass
class Point:
    pc_index: int
    replicate: int
    x: float
    y: float
    z: float


def torus_point(theta: float, phi: float, R: float = 3.0, r: float = 1.0) -> tuple[float, float, float]:
    """Return 3D coordinates for angles on a torus."""
    x = (R + r * math.cos(phi)) * math.cos(theta)
    y = (R + r * math.cos(phi)) * math.sin(theta)
    z = r * math.sin(phi)
    return x, y, z


def build_points(x: int) -> list[Point]:
    points = []
    for replicate in range(x):
        for pc_index in range(12):
            theta = 2 * math.pi * (pc_index + replicate / x) / 12
            phi = 2 * math.pi * replicate / x
            coord = torus_point(theta, phi)
            points.append(Point(pc_index, replicate, *coord))
    return points


def connect_indices(pc_index: int, interval: int) -> int:
    return (pc_index + interval) % 12


COLOR_MAP = {
    7: "blue",   # perfect fifth
    4: "red",    # major third
    3: "green",  # minor third
}


def plot_torus(points: list[Point], x: int) -> None:
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection="3d")

    # Plot points
    for p in points:
        ax.scatter(p.x, p.y, p.z, color="black")
        ax.text(p.x, p.y, p.z, PITCH_CLASSES[p.pc_index], fontsize=8)

    # Draw connections for each replicate
    for replicate in range(x):
        replicate_points = [p for p in points if p.replicate == replicate]
        by_index = {p.pc_index: p for p in replicate_points}
        for pc in range(12):
            start = by_index[pc]
            for interval, color in COLOR_MAP.items():
                end = by_index[connect_indices(pc, interval)]
                ax.plot(
                    [start.x, end.x],
                    [start.y, end.y],
                    [start.z, end.z],
                    color=color,
                )

    ax.set_axis_off()
    plt.savefig("torus_tonnetz.png")


def main() -> None:
    if len(sys.argv) > 1:
        try:
            x = int(sys.argv[1])
        except ValueError:
            print("x must be an integer")
            sys.exit(1)
    else:
        x = 1

    points = build_points(x)
    plot_torus(points, x)


if __name__ == "__main__":
    main()
