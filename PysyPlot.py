#! /usr/bin/env python3
# coding: utf-8

import operator as op
import numpy as np
import pandas as pd

import plotly as pl
import gui.dashgui as gui
import plotly.express as px
import plotly.io as pio

import dash
import dash_core_components as dcc
import dash_html_components as html

import core.datamanagement as dm
import core.plotdef as plotdef
import gui.dashgui as gui

from dash.dependencies import Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate

#def main():

#if __name__ == "__main__":
#    main()

datam = dm.DataManager()

#datam.readxlsx("data/test3.xlsx")

pio.renderers.default='browser'
# plot1 = plotdef.ParCoorPlot(dataframe=datam.dataframe,
#                             subsets=datam.subsets)

# plot2 = plotdef.ScatterPlot(dataframe=datam.dataframe,
#                             subsets=datam.subsets,
#                             x_var=('regime',"rpm"),
#                             y_var=('poussee',"N"),
#                             z_var=None)

app = gui.set_app_layout(datam)
gui.callbacks(app, datam)
# app.layout.children.append(dcc.Graph(id='plot1', figure=plot1.figure))
# app.layout.children.append(dcc.Graph(id='plot2', figure=plot2.figure))
app.run_server(debug=False, port=8080, host='0.0.0.0')

