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

# %% jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
import warnings
import matplotlib.pyplot as plt
with warnings.catch_warnings():
    from egmn.ConsPensionModel import PensionConsumerType, init_pension_contrib
    from HARK.interpolation._sklearn import GeneralizedRegressionUnstructuredInterp
    from egmn.utilities import plot_3d_func, plot_scatter_hist

figures_path = "../../content/figures/"

# %%
baseline_params = init_pension_contrib.copy()
baseline_params["mCount"] = 50
baseline_params["mMax"] = 10
baseline_params["mNestFac"] = -1

baseline_params["nCount"] = 50
baseline_params["nMax"] = 12
baseline_params["nNestFac"] = -1

baseline_params["lCount"] = 50
baseline_params["lMax"] = 9
baseline_params["lNestFac"] = -1

baseline_params["blCount"] = 50
baseline_params["blMax"] = 13
baseline_params["blNestFac"] = -1

baseline_params["aCount"] = 50
baseline_params["aMax"] = 8
baseline_params["aNestFac"] = -1

baseline_params["bCount"] = 50
baseline_params["bMax"] = 14
baseline_params["bNestFac"] = -1

max_cycles = 5
baseline_params["cycles"] = max_cycles

# %% jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
agent = PensionConsumerType(**baseline_params)

# %% jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
with warnings.catch_warnings():
    agent.solve()

T = 0

# %%
#| label: conspension
import ipywidgets as w
from ipywidgets import VBox, HBox
import numpy as np

debug = w.Output()

state = dict(cycles=-1)

# plt.ioff()
# fig = plt.figure()
# ax=fig.add_subplot(1,1,1, projection="3d")

lookup = {
    'Consumption Value Function (VF)': lambda a, t: a.solution[t].consumption_stage.v_func.vFuncNvrs,
    'Consumption VF Derivative L':  lambda a, t: a.solution[t].consumption_stage.dvdl_func.cFunc,
    'Consumption VF Derivative B':  lambda a, t: a.solution[t].consumption_stage.dvdb_func.cFunc,
    'Deposit Amount': lambda a, t: a.solution[t].deposit_stage.d_func,
    'Deposit Stage Consumption': lambda a, t : a.solution[t].deposit_stage.c_func,
    'Deposit Stage Value Function (VF)': lambda a, t : a.solution[t].deposit_stage.v_func.vFuncNvrs,
    'Deposit Stage VF Derivative M': lambda a,t: a.solution[t].deposit_stage.dvdm_func.cFunc,
    'Deposit Stage VF Derivative N': lambda a,t: a.solution[t].deposit_stage.dvdn_func.cFunc
}

options = list(lookup.keys())

w_count = w.IntSlider(50, min=10, max=100, description="Count:")
w_nestfac = w.IntSlider(-1, min=-5, max=5, description="NestFac:")
w_cycles = w.IntSlider(max_cycles, min=1, max=20, description="Cycles:")
w_mMax = w.IntSlider(10, min=1, max=30, description="mMax:")
w_nMax = w.IntSlider(12, min=1, max=30, description="nMax:")
w_lMax = w.IntSlider(9, min=1, max=30, description="lMax:")
w_blMax = w.IntSlider(13, min=1, max=30, description="blMax:")
w_aMax = w.IntSlider(8, min=1, max=30, description="aMax:")
w_bMax = w.IntSlider(14, min=1, max=30, description="bMax:")
out_readout = w.Output()

w_t = w.IntSlider(0, min=0, max=max_cycles-1, description="Cycle (t):")
w_plottype = w.Dropdown(options=options, value=options[0], description="Plot Type:")
w_plottype.layout.width = '400px'
w_solve = w.Button(description='Solve')
w_elev = w.IntSlider(20, min=0, max=85, description="Elevation:")
w_azim = w.IntSlider(245, min=0, max=360, description="Azimuth:")

def plot(cycles, t, plottype, elev, azim):
    global agent
    with debug:
        params = dict(**baseline_params)
        fig = plt.figure(figsize=(6,6))
        ax = plt.axes(projection="3d")
        ax.view_init(elev=elev, azim=azim)
        ax.tick_params(axis='both', labelsize=8) 
        plot_3d_func(lookup[plottype](agent, t), [0, 5], [0, 5], 
                     meta={
                         "title": "Cons Pension Model", 
                         "xlabel": "Retirement balance $n$", 
                         "ylabel":"Market Resources $m$", 
                         "zlabel": "Pension Deposits $d$"},
                     ax=ax, show=False)
        
        
    with out_readout:
        out_readout.clear_output(wait=True)

baseline_ctrl = VBox([
    w.Label("Baseline Settings (press 'solve' to apply)"),
    HBox([
    VBox([w_count, w_mMax, w_lMax, w_aMax, w_cycles]),
    VBox([w_nestfac, w_nMax, w_blMax, w_bMax,HBox([w_solve, out_readout])]),
])])


def do_solve(_):
    global baseline_params
    global max_cycles
    global agent
    with out_readout:
        out_readout.clear_output(wait=True)
        print('solving...')

    with debug:
        baseline_params["mCount"] = w_count.value
        baseline_params["mMax"] = 10
        baseline_params["mNestFac"] = -1
        
        baseline_params["nCount"] = w_count.value
        baseline_params["nMax"] = 12
        baseline_params["nNestFac"] = -1
        
        baseline_params["lCount"] = w_count.value
        baseline_params["lMax"] = 9
        baseline_params["lNestFac"] = -1
        
        baseline_params["blCount"] = w_count.value
        baseline_params["blMax"] = 13
        baseline_params["blNestFac"] = -1
        
        baseline_params["aCount"] = w_count.value
        baseline_params["aMax"] = 8
        baseline_params["aNestFac"] = -1
        
        baseline_params["bCount"] = w_count.value
        baseline_params["bMax"] = 14
        baseline_params["bNestFac"] = -1
    
        max_cycles = w_cycles.value
        baseline_params["cycles"] = max_cycles
    
        agent = PensionConsumerType(**baseline_params)
        agent.solve()

        plot(cycles=w_cycles.value, t=w_t.value, plottype=w_plottype.value)
        
    with out_readout:
        out_readout.clear_output(wait=True)

w_solve.on_click(do_solve)

interactive_ctrl = VBox([w.Label("Interactive Controls"),w_t, w_plottype, HBox([w_elev, w_azim])])

e_out = w.interactive_output(plot, dict(cycles=w_cycles, t=w_t, plottype=w_plottype, elev=w_elev, azim=w_azim))
plots = HBox([e_out])

# TODO get baseline controls working
# ui = VBox([baseline_ctrl, interactive_ctrl, plots])
ui = VBox([interactive_ctrl, plots])
display(ui)
display(debug)

# %%

# %%
