"""
Matplotlib module for equation graphing
"""

import matplotlib.pyplot as plt
import numpy as np


class CurvePlotter:
    """
    Class for plotting curves
    """

    def __init__(self):
        self.default_title = "Graphique"


    def plot_function(self, f, x_min, x_max, title=None, xlabel="x", ylabel="y"):
        x = np.linspace(x_min, x_max, 1000)
        y = f(x)

        if title is None:
            title = self.default_title

        plt.plot(x, y, label=title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()
        plt.show()

    def plot_data_points(self, x, y, title=None, xlabel="x", ylabel="y"):
        if title is None:
            title = self.default_title

        plt.scatter(x, y, label=title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid()
        plt.show()
