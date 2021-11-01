#! /usr/bin/env python3
# coding: utf-8

import operator as op
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

class _Plotter:
    """Abstract class used as a base for graph plotters.
    
    Store a dataframe as data source, and allow filtering on it,
    tanks to a subset list. 

    Attributes
    ----------
    dataframe : pandas dataframe
        Data source.
    subsets : list of tupples (str var, operator, float value)
        Filters to apply on data.
    masked_dataframe : pandas dataframe
        Dataframe sliced thanks to the subsets.  
    """
    
    def __init__(self, *, dataframe, subsets = [], **kwargs):
        """Creation of a Plotter object.
        
        Every plotter need data, given by the dataframe.
        Optionnal subsets allow data slicing before plotting
        operations (plotting described in children classes).

        Parameters
        ----------
        * : force naming of the arguments.
        dataframe : pandas dataframe
            Data container.
        subsets : list of tupples (str var, operator, float value)
            Filters to apply on data. The default is [] (no filters).
        """
        self._dataframe = dataframe
        self._subsets = subsets
        self._mask = self._mask_from_subsets()
        self._masked_dataframe = self._build_masked_dataframe()
        
    def _update(self):
        """Update the object attributes.
        
        if the data or the subset are changed, this method is
        called to update the slicing. This method should be
        extended in children classes in order to update figures. 
        """
        self._mask = self._mask_from_subsets()
        self._masked_dataframe = self._build_masked_dataframe()

    @property
    def subsets(self):
        """List of tupples (str var, operator, float value)
        used for data slicing :
            - str var : dataframe column ID tupple (var, unit) expected.
            - fct operator : to apply (using operator basic package)
            - float value : criterion for the filter.
        """
        return self._subsets

    @subsets.setter
    def subsets(self, subsets):
        """Call to the update method after parameter change. """
        self._subsets = subsets
        self._update()

    @property
    def dataframe(self):
        """Pandas dataframe (data container). """
        return self._dataframe

    @dataframe.setter
    def dataframe(self, dataframe):
        """Call to the update method after parameter change."""
        self._dataframe = dataframe
        self._update()
        
    @property
    def masked_dataframe(self):
        """Pandas dataframe corresponding to a slice of the input
        dataframe respecting the filters defined in "subsets". 
        """
        return self.masked_dataframe
        
    def _mask_from_subsets(self):
        """Build a mask (boolean serie) by applying filters
        (contained in "subsets") to the data ("dataframe").
        """
        if len(self._subsets) == 0:
            return []
        else:
            masks = []
            for (var, oper, crit) in self._subsets:
                masks.append(oper(self._dataframe[var], crit))
            return np.logical_and.reduce([m.squeeze() for m in masks])
                                     
    def _build_masked_dataframe(self):
        """Apply a mask (boolean serie) to a dataframe in order
        to slice it to keep usefull data only.
        """
        if len(self._mask) == 0:
            masked_df = self._dataframe
        else:
            masked_df = self._dataframe.loc[self._mask,:]
        return masked_df
    

class ParCoorPlot(_Plotter):
    """Class designed to build a parallel coordinates plot.
    
    Parallel plot based on a list of variable "varlist", each of one
    representing an axis. 

    Attributes
    ----------
    All the attributes from parent class _Plotter, plus :
    varlist : list
        List of variables to plot.
    figure : plotly figure object
        Parallel coordinates plot. 
    """
    
    def __init__(self, *, varlist = None, **kwargs):
        """Creation of a ParCoorPlot object.
        
        Inherited from _Plotter.

        Parameters
        ----------
        All the inputs from parent class _Plotter, plus :
        varlist : list
            List of variables to plot (each variable is an axis).
            Variables are defined by tupples (var name, var unit).
        """
        super(ParCoorPlot, self).__init__(**kwargs)
        self._varlist = varlist
        self._figure_dict = {}
        self._update_figure_data()
        self._figure = go.Figure(data=go.Parcoords(self._figure_dict))
        
    def _update(self):  
        """ Extended update method to add figure update. """
        super()._update()
        self._update_figure_data()
        
    @property
    def varlist(self):
        """List of variables to plot (one axis per variable).
        if "None" is given, all the variables will be plotted.
        """
        return self._varlist

    @varlist.setter
    def varlist(self, varlist):
        """Call to the update method after parameter change. """
        self._varlist = varlist
        self._update()
            
    @property
    def figure(self):
        """ Plotly figure for display. """
        return self._figure
    
    def _update_figure_data(self):
        """ Definition of the figure parameters. """
        if self._varlist == None:
            vars_to_plot = self._dataframe.columns.values
        else:
            vars_to_plot = self._varlist
        
        labels = {v : v[0] + " (" + v[1] + ")" for v in vars_to_plot}
        dims = []
        for v in vars_to_plot:
            dim = {}
            dim["label"] = labels[v]
            if pd.api.types.is_numeric_dtype(self._masked_dataframe[v]):
                dim["values"] = self._masked_dataframe[v]
            else:
                tickvals = self._masked_dataframe[v].values
                tickset = []
                for tv in tickvals:
                    if tv not in tickset:
                        tickset.append(tv)
                tickdic = {tv: i for (i, tv) in enumerate(tickset)} 
                dim["ticktext"] = tickset
                dim["tickvals"] = [tickdic[tv] for tv in tickset]
                dim["values"] = [tickdic[tv] for tv in tickvals]
            dims.append(dim)
        self._figure_dict["dimensions"] = dims


class ScatterPlot(_Plotter):
    """Class designed to build a scatter plot.
    
    2D scatter plot with the option of plotting multiple series
    with different colors to take into account a 3rd dimension.

    Attributes
    ----------
    All the attributes from parent class _Plotter, plus :
    x_var : tupple
        ID of the variable for the plot X-axis
        (tupple (var name, unit name)).
    y_var : tupple
        ID of the variable for the plot Y-axis
        (tupple (var name, unit name)).
    z_var : tupple
        ID of the variable for the coloring
        (tupple (var name, unit name)).
    figure : plotly figure object
        Parallel coordinates plot. 
    """
    
    def __init__(self, *, x_var, y_var, z_var = None, **kwargs):
        """Creation of a scatter plot object.
        
        Inherited from _Plotter.

        Parameters
        ----------
        All the inputs from parent class _Plotter, plus :
        x_var : tupple
            ID of the variable for the plot X-axis
            (tupple (var name, unit name)).
        y_var : tupple
            ID of the variable for the plot Y-axis
            (tupple (var name, unit name)).
        z_var : tupple
            ID of the variable for the coloring
            (tupple (var name, unit name)).
        """
        super(ScatterPlot, self).__init__(**kwargs)
        self._x_var = x_var
        self._y_var = y_var
        self._z_var = z_var
        self._figure_list = []
        self._update_figure_data()
        self._figure = go.Figure(data=self._figure_list)
        
    def _update(self): 
        """ Extended update method to add figure update. """
        super()._update()
        self._update_figure_data()
        
    @property
    def x_var(self):
        """ tupple (var name, unit name) for the plot X-axis. """
        return self._x_var

    @x_var.setter
    def x_var(self, x_var):
        """ Extended update method to add figure update. """
        self._x_var = x_var
        self._update()

    @property
    def y_var(self):
        """ tupple (var name, unit name) for the plot Y-axis. """
        return self._y_var

    @y_var.setter
    def y_var(self, y_var):
        """ Extended update method to add figure update. """
        self._y_var = y_var
        self._update()

    @property
    def z_var(self):
        """ tupple (var name, unit name) for the plot Z-axis (coulour). """
        return self._z_var

    @z_var.setter
    def z_var(self, z_var):
        """ Extended update method to add figure update. """
        self._z_var = z_var
        self._update()
            
    @property
    def figure(self):
        """ Plotly figure for display. """
        return self._figure
        
    def _update_figure_data(self): 
        """ Definition of the figure parameters. """
        (x_label, y_label) = [v[0] + " (" + v[1] + ")" for v in (self.x_var,
                                                                 self.y_var)]
        if self.z_var == None:
            z_label = None
            z_values = [None]
            z_legends = [None]
        else:
            z_label = self.z_var[0] + " (" + self._z_var[1] + ")"
            z_values = set(self._masked_dataframe[self._z_var])
            z_legends = [z_label + " = " + str(v) for v in z_values]
        
        for (z_leg, z_val) in zip(z_legends, z_values):
            serie = {}
            serie["type"] = "scatter"
            if z_val == None:
                sliced_df = self._masked_dataframe
            else:
                mask = op.eq(self._masked_dataframe[self._z_var], z_val)
                sliced_df = self._masked_dataframe.loc[mask.squeeze(), :]
                serie["name"] = z_leg

            serie["x"] = sliced_df[self._x_var].squeeze()
            serie["y"] = sliced_df[self._y_var].squeeze()
            self._figure_list.append(serie)
        pass


def main():
    
    pio.renderers.default='browser'
    
    df = pd.DataFrame(data={('col1',"m"): [1, 2, 3, 1, 2, 3],
                            ('col2',"-"): [4.1, 5.2, 6.1, 6.1, 5.1, 6.1],
                            ('col3',"-"): ["bla1", "bla1", "bla1", "bla2", "bla2", "bla2"]})
    subsets = []
    plot1 = ParCoorPlot(dataframe=df,
                        subsets=subsets)
    plot1.figure.show()
    
    plot2 = ScatterPlot(dataframe=df,
                        subsets=subsets,
                        x_var=('col1',"m"),
                        y_var=('col2',"-"),
                        z_var=('col3',"-"))
    plot2.figure.show()
    
    subsets = [('col1', op.le, 3),
               ('col2', op.eq, 6.1)]
    

if __name__ == "__main__":
    main()
