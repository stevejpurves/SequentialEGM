# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.16.1
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %%
import pickle
import matplotlib.pyplot as plt
import numpy as np

# %%
with open('./baseline.pkl', 'rb') as f:
    data = pickle.load(f)

# %%
#| label: conspension-precanned
import ipywidgets as w
from ipywidgets import VBox, HBox
import numpy as np

debug = w.Output()

state = dict(cycles=-1)

options = list(data.keys())
max_cycles = len(data[options[0]])

w_t = w.IntSlider(0, min=0, max=max_cycles-1, description="Cycle (t):")
w_plottype = w.Dropdown(options=options, value=options[0], description="Plot Type:")
w_plottype.layout.width = '400px'
w_solve = w.Button(description='Solve')
w_elev = w.IntSlider(20, min=0, max=85, description="Elevation:")
w_azim = w.IntSlider(245, min=0, max=360, description="Azimuth:")

def plot(t, plottype, elev, azim):
    global agent
    with debug:
        fig = plt.figure(figsize=(6,6))
        ax = plt.axes(projection="3d")
        ax.view_init(elev=elev, azim=azim)
        ax.tick_params(axis='both', labelsize=8)
        xMat, yMat, zMat = data[plottype][t]
        ax.plot_surface(xMat, yMat, zMat, cmap="viridis")
        ax.set_title("Cons Pension Model")
        ax.set_xlabel("Retirement balance $n$")
        ax.set_ylabel("Market Resources $m$")
        ax.set_zlabel("Pension Deposits $d$")

interactive_ctrl = VBox([w.Label("Interactive Controls"),w_t, w_plottype, HBox([w_elev, w_azim])])

e_out = w.interactive_output(plot, dict(t=w_t, plottype=w_plottype, elev=w_elev, azim=w_azim))
plots = HBox([e_out])

# TODO get baseline controls working
# ui = VBox([baseline_ctrl, interactive_ctrl, plots])
ui = VBox([interactive_ctrl, plots])
display(ui)
display(debug)

# %%

# %%
