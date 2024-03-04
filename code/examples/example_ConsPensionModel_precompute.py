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

max_cycles = 20
baseline_params["cycles"] = max_cycles

# %% jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
agent = PensionConsumerType(**baseline_params)

# %% jupyter={"outputs_hidden": false} pycharm={"name": "#%%\n"}
with warnings.catch_warnings():
    agent.solve()

# %%
import numpy as np

def prep_3d_data(func, xlims, ylims, n=100):
    xgrid = np.linspace(xlims[0], xlims[1], n)
    ygrid = np.linspace(ylims[0], ylims[1], n)
    xMat, yMat = np.meshgrid(xgrid, ygrid, indexing="ij")
    zMat = func(xMat, yMat)
    return xMat, yMat, zMat


fn_lookup = {
    'Consumption Value Function (VF)': lambda a, t: a.solution[t].consumption_stage.v_func.vFuncNvrs,
    'Consumption VF Derivative L':  lambda a, t: a.solution[t].consumption_stage.dvdl_func.cFunc,
    'Consumption VF Derivative B':  lambda a, t: a.solution[t].consumption_stage.dvdb_func.cFunc,
    'Deposit Amount': lambda a, t: a.solution[t].deposit_stage.d_func,
    'Deposit Stage Consumption': lambda a, t : a.solution[t].deposit_stage.c_func,
    'Deposit Stage Value Function (VF)': lambda a, t : a.solution[t].deposit_stage.v_func.vFuncNvrs,
    'Deposit Stage VF Derivative M': lambda a,t: a.solution[t].deposit_stage.dvdm_func.cFunc,
    'Deposit Stage VF Derivative N': lambda a,t: a.solution[t].deposit_stage.dvdn_func.cFunc
}


data = dict()

for key in fn_lookup.keys():

    series = []
    for t in range(0, max_cycles):
        series.append(prep_3d_data(fn_lookup[key](agent,t),[0, 5], [0, 5]))

    data[key] = series
    
with open('./baseline.pkl', 'wb') as f:
    pickle.dump(data, f)

# %%
