#! /usr/bin/env python3
# coding: utf-8

import operator as op
import numpy as np
import pandas as pd

from .read_data import xlsx as xl
from . import plotdef as pl


class DataManager:
    """Container class for data and filter
    
    Class designed to simplify interfaces between the
    core logic and dash gui.

    Attributes
    ----------
 
    """
    
    def __init__(self, **kwargs):
        self._dataframe = None
        self._subsets = {}
        self._df_vars = []
        self._df_ops = [{'disp':'==', 'op':op.eq},
                        {'disp':'!=', 'op':op.ne},
                        {'disp':'>',  'op':op.gt},
                        {'disp':'<',  'op':op.lt},
                        {'disp':'>=', 'op':op.ge},
                        {'disp':'<=', 'op':op.le}]

    @property
    def dataframe(self):
        """Pandas dataframe (data container). """
        return self._dataframe

    @property
    def subsets(self):
        """Dict of tupples (str var, operator, value) identified by an
        integer ID.
        used for data slicing :
            - str var : dataframe column ID tupple (var, unit) expected.
            - fct operator : to apply (using operator basic package)
            - float value : criterion for the filter.
        """
        return self._subsets
    
    @property
    def df_vars(self):
        """List of dicts :
            - key = description str with df variable (column header) & unit.
            - value = tupple (var, unit). """
        return self._df_vars
    
    @property
    def df_ops(self):
        """List of dicts :
            - description string of the operator.
            - operator. """
        return self._df_ops

    def add_subset(self, subset_id, subset):
        """Add a subset to the list. """
        self._subsets[subset_id] = subset
        
    def remove_subset(self, subset_id):
        """Remove a subset from the list. """
        del self._subsets[subset_id]
        
    def readxlsx(self, container):
        """Concert an Excel workbook to a Dataframe. """
        self._dataframe = xl.workbook_to_dataframe(container)
        self._df_vars = {var[0] + ' (' + var [1] + ")": var
                         for var in self._dataframe.columns}
        
    def check_subset(self, var, oper, crit):
        """Chech if an operation is applicable to the dataframe. """
        # Check if not already existing
        if (var, oper, crit) in [(ss['var'],
                                  ss['oper'],
                                  ss['crit'])for ss in self._subsets.values()]:
            return False
        # Check if criterion valid
        try:
            if crit.isnumeric() :
                converted_crit = float(crit)
            else:
                converted_crit = crit
            oper(self._dataframe[var], converted_crit)
            return True
        except Exception as e: 
            print(e)
            return False
        
    def plot_par_coor(self, subsets, varlist):
        plotter = pl.ParCoorPlot(dataframe = self._dataframe,
                                 subsets = subsets,
                                 varlist = varlist)
        return plotter.figure
    
    def plot_scatter(self, subsets, x_var, y_var, z_var):
        plotter = pl.ScatterPlot(dataframe = self._dataframe,
                                 subsets = subsets,
                                 x_var = x_var,
                                 y_var = y_var,
                                 z_var = z_var)
        return plotter.figure


def main():
    pass
    

if __name__ == "__main__":
    main()
