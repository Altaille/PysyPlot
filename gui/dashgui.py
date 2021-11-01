#! /usr/bin/env python3
# coding: utf-8

import io
import base64
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, MATCH, ALL



#####################################
############ Main layout ############
#####################################

def set_app_layout(dm):   
    
    app = dash.Dash(__name__)
    
    app.layout = html.Div(
        # Titles
        id='wrapper',
        children=[
        html.H1(
            children='Interactive plotter',
        ),
        
        # Upload anf filters definition
        def_upload(),
        def_div_subsets(dm),
        def_div_graphs()
    ])    
    
    return app


####################################
############ Components ############
####################################


def def_upload():
    upload = dcc.Upload(
        className='upload',
        id='upload',
        children=[
            html.Div(id = 'ul_txt_1', children =
                ['Drag and drop or click to select a single file to upload.']
            ),
            html.Div(id = 'ul_txt_2', children =
                ['--- No file selected. ---']
            )
        ],
        multiple=False,
    )
    return upload


def def_div_subsets(dm):
       
    div = html.Div(
        id='subsets',
        className='subwrapper',
        children=[
            html.H2(
                children='Subsets definition'
            ),
            html.Div(
                className='flex',
                children = [
                    html.Div(children=dcc.Dropdown(
                        id='var_dropdown',
                        options=[],
                        placeholder="Select variable"
                    ), className='flex-item'),
                    html.Div(children=dcc.Dropdown(
                        id='op_dropdown',
                        className='flex-item',
                        options=[],
                        placeholder="Select sign"
                    ), className='flex-item'),
                    dcc.Input(
                        id='crit_input',
                        className='flex-item',
                        placeholder="Enter criterion"
                    ),
                    html.Button(
                        id='add_subset_button',
                        className='flex-item',
                        children='Add subset'
                    ),
                ]
            ),
            html.Div(
                id='subsets_container',
                children=[]
            )
        ],
        style={'display': 'none'}
    )
    return div


def def_div_subset(id_index, text):
    
    div = html.Div(
        className='container',
        id={'type': 'subset_div',
            'index': id_index},
        children=[
            html.Div(
                className='one-half column',
                children=text
            ),
            html.Button(
                id={'type': 'subset_del_button',
                    'index': id_index},
                className='one-half column',
                children='del subset'
            )
        ]
    )
    return div


def def_div_graphs():
    
    div = html.Div(
        id='graphs',
        className='subwrapper',
        children=[
            html.H2(
                children='Graphs def',
            ),
            html.Button(
                id='add_scatterPlot_button',
                className='one-half column',
                children='Add scatter plot'
            ),
            html.Button(
                id='add_parCoorPlot_button',
                className='one-half column',
                children='Add parallel coordinates plot'
            ),
            html.Div(
                id='graphs_container',
                children=[]
            )
        ],
        style={'display': 'none'}
    )
    return div


def def_div_scatter_plot(id_index, dm):

    var_options = [{'value' : var_disp, 'label' : var_disp}
                   for var_disp in dm.df_vars.keys()]
    div = html.Div(
        className='container-flex',
        id={'type': 'graph_div',
            'index': id_index},
        children=[
            html.Div(
                id={'type': 'graph_scatter_div_left',
                    'index': id_index},
                className='flex-item-50pct',
                children=[
                    html.H3(
                        children='Plot {0} : scatter'.format(id_index),
                        className='one-half column',
                    ),
                    dcc.Dropdown(
                        id={'type': 'subsets_dropdown',
                            'index': id_index},
                        options=[],
                        multi=True,
                        placeholder="Select subsets to apply"
                    ),
                    dcc.Dropdown(
                        id={'type': 'var_x_dropdown',
                            'index': id_index},
                        options=var_options,
                        placeholder="X-axis variable"
                    ),
                    dcc.Dropdown(
                        id={'type': 'var_y_dropdown',
                            'index': id_index},
                        options=var_options,
                        placeholder="Y-axis variable"
                    ),
                    dcc.Dropdown(
                        id={'type': 'var_z_dropdown',
                            'index': id_index},
                        options=var_options,
                        placeholder="Z-axis variable (optionnal)"
                    ),
                    html.Button(
                        id={'type': 'graph_plot_scatter_button',
                            'index': id_index},
                        children='Plot'
                    ),
                    html.Button(
                        id={'type': 'graph_del_button',
                            'index': id_index},
                        children='Delete'
                    )
                ]
            ),
            html.Div(
                id={'type': 'graph_scatter_div_right',
                    'index': id_index},
                className='flex-item-50pct'
            )
        ]
    )
    return div


def def_div_par_coor_plot(id_index, dm):

    var_options = [{'value' : var_disp, 'label' : var_disp}
                   for var_disp in dm.df_vars.keys()]    

    div = html.Div(
        className='container-flex',
        id={'type': 'graph_div',
            'index': id_index},
        children=[
            html.Div(
                id={'type': 'graph_parcoor_scatter_div_left',
                    'index': id_index},
                className='flex-item-50pct',
                children=[
                    html.H3(
                        children='Plot {0} : parallel coordinates'
                        .format(id_index),
                        className='one-half column',
                    ),
                    dcc.Dropdown(
                        id={'type': 'subsets_dropdown',
                            'index': id_index},
                        options=[],
                        multi=True,
                        placeholder="Select subsets to apply"
                    ),
                    dcc.Dropdown(
                        id={'type': 'vars_dropdown',
                            'index': id_index},
                        options=var_options,
                        multi=True,
                        placeholder="Select variables to plot"
                    ),
                    html.Button(
                        id={'type': 'graph_plot_parcoor_button',
                            'index': id_index},
                        children='Plot'
                    ),
                    html.Button(
                        id={'type': 'graph_del_button',
                            'index': id_index},
                        children='Delete'
                    )
                ]
            ),
            html.Div(
                id={'type': 'graph_parcoor_scatter_div_right',
                    'index': id_index},
                className='flex-item-50pct'
            )
        ]
    )
    return div

####################################
############ Callbacks ############
####################################

def callbacks(app, dm):

    # Load a file
    @app.callback(
        [
        Output('ul_txt_2', 'children'),
        Output('subsets', 'style'),
        Output('graphs', 'style'),
        Output('var_dropdown', 'options'),
        Output('op_dropdown', 'options'),
        Output({'type': 'var_x_dropdown', 'index': ALL}, 'options'),
        Output({'type': 'var_y_dropdown', 'index': ALL}, 'options'),
        Output({'type': 'var_z_dropdown', 'index': ALL}, 'options'),
        Output({'type': 'vars_dropdown', 'index': ALL}, 'options')        
        ],
        [
        Input('upload', 'contents')
        ],
        [
        State('upload', 'filename'),
        State('upload', 'last_modified'),
        State('graphs_container', 'children')
        ]
    )
    def update_div_excel_disp(contents,
                              name,
                              last_modified,
                              graphs):
        # No action on initialization
        if contents is None:
            raise dash.exceptions.PreventUpdate
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            file = io.BytesIO(decoded)
            dm.readxlsx(file)
            var_options = [{'value' : var_disp, 'label' : var_disp}
                           for var_disp in dm.df_vars.keys()]
            op_options = [{'value' : op['disp'], 'label' : op['disp']} 
                          for op in dm.df_ops]
            file_desc = '--- File : ' + \
                        name + \
                        ' -- ' + \
                        str(dt.datetime.fromtimestamp(last_modified)) + \
                        ' ---'
            display_state = {'display': 'block'}
            n_scatters = len(dash.callback_context.outputs_list[5])
            n_parcoors = len(dash.callback_context.outputs_list[8])
            var_options_scatters = [var_options for i in range(n_scatters)]
            var_options_parcoors = [var_options for i in range(n_parcoors)]
            return (file_desc,
                    display_state,
                    display_state,
                    var_options,
                    op_options,
                    var_options_scatters,
                    var_options_scatters,
                    var_options_scatters,
                    var_options_parcoors)
        
        except Exception as e: 
            print(e)
            file_desc = '--- Invalid file ! ---'
            display_state = {'display': 'none'}
            return (file_desc,
                    display_state,
                    display_state,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update)
            
            
    # Add or remove subsets
    @app.callback(
        Output('subsets_container', 'children'),
        [
        Input('add_subset_button', 'n_clicks'),
        Input({'type': 'subset_del_button', 'index': ALL}, 'n_clicks')
        ],
        [
        State('var_dropdown', 'value'),
        State('op_dropdown', 'value'),
        State('crit_input', 'value'),
        State('subsets_container', 'children')
        ]
    )
    def manage_subsets(n_clicks_add, n_clicks_rm,
                       var_disp, op_disp, crit, current_subsets):
        
        # Context and init handling (no action)
        ctx = dash.callback_context
        if (not ctx.triggered) | any((var_disp is None, 
                                      op_disp is None,
                                      crit is None)):
            raise dash.exceptions.PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        # Creation of a new subset
        if button_id == 'add_subset_button':
            var = dm.df_vars[var_disp]
            oper = {o['disp'] : o['op'] for o in dm.df_ops}[op_disp]
            if not dm.check_subset(var, oper, crit):
                raise dash.exceptions.PreventUpdate
            text = var_disp + " " + op_disp + " " + crit,
            subset = {'disp': text,
                      'var': var,
                      'oper': oper,
                      'crit': crit}
            dm.add_subset(n_clicks_add, subset)
            subset_div = def_div_subset(n_clicks_add, text)
            return current_subsets + [subset_div]
        
        # Removal of an existing subset
        else:
            subset_id_to_remove = eval(button_id)['index']
            dm.remove_subset(subset_id_to_remove)
            return [ss for ss in current_subsets
                    if ss['props']['id']['index'] != subset_id_to_remove]


    # Add or remove graphs
    @app.callback(
        Output('graphs_container', 'children'),
        [
        Input('add_scatterPlot_button', 'n_clicks'),
        Input('add_parCoorPlot_button', 'n_clicks'),
        Input({'type': 'graph_del_button', 'index': ALL}, 'n_clicks')
        ],
        [
        State('graphs_container', 'children')
        ]
    )
    def manage_graphs(n_clicks_scatter, n_clicks_par_coor, n_clicks_rm,
                      current_graphs):
        
        # Context and init handling (no action)
        ctx = dash.callback_context
        if not ctx.triggered :
            raise dash.exceptions.PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
                 
        # Creation of a new graph
        if button_id in ('add_scatterPlot_button',
                         'add_parCoorPlot_button'):
            # ID index definition
            if n_clicks_scatter is None :
                n_scatter = 0
            else:
                n_scatter = n_clicks_scatter
            if n_clicks_par_coor is None :
                n_par_coor = 0
            else:
                n_par_coor = n_clicks_par_coor
            id_index = n_scatter + n_par_coor
             # new graph creation
            if button_id == 'add_scatterPlot_button':
                subset_graph = def_div_scatter_plot(id_index, dm)
                return current_graphs + [subset_graph]
            elif button_id == 'add_parCoorPlot_button':
                subset_graph = def_div_par_coor_plot(id_index, dm)
                return current_graphs + [subset_graph]
            
            # Removal of an existing graph
        else:
            graph_id_to_remove = eval(button_id)['index']
            return [gr for gr in current_graphs
                    if gr['props']['id']['index'] != graph_id_to_remove]


    # Update subset dropdowns
    @app.callback(
        Output({'type': 'subsets_dropdown', 'index': ALL}, 'options'),
        [Input('subsets_container', 'children')],
        [State('graphs_container', 'children')]
    )
    def update_subsets_dropdown(subsets, graphs):
        graph_ss_options = []
        for subset_id, subset in dm.subsets.items():
            dropdown_item = {'value' : subset_id, 'label' : subset['disp']}
            graph_ss_options.append(dropdown_item)
        if not subsets:
            graphs_ss_options = [[] for i in range(len(graphs))]
        else:
            graphs_ss_options = [graph_ss_options for i in range(len(graphs))]
        return graphs_ss_options


    # Plot scatter
    @app.callback(
        Output({'type': 'graph_scatter_div_right', 'index': MATCH},
               'children'),
        [
        Input({'type': 'graph_plot_scatter_button', 'index': MATCH},
              'n_clicks')
        ],
        [
        State({'type': 'subsets_dropdown', 'index': MATCH}, 'value'),
        State({'type': 'var_x_dropdown', 'index': MATCH}, 'value'),
        State({'type': 'var_y_dropdown', 'index': MATCH}, 'value'),
        State({'type': 'var_z_dropdown', 'index': MATCH}, 'value')
        ]
    )  
    def plot_scatter(n_clicks, subset_ids, var_x_disp, var_y_disp, var_z_disp):
        ctx = dash.callback_context
        if not ctx.triggered :
            raise dash.exceptions.PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "":
            raise dash.exceptions.PreventUpdate
        if subset_ids is None :
            subsets = []
        else:
            subsets = [dm.subsets[ss_id] for ss_id in subset_ids]
        subsets_tups = [(ss['var'], ss['oper'], ss['crit']) for ss in subsets]
        var_x = dm.df_vars[var_x_disp]
        var_y = dm.df_vars[var_y_disp]
        if var_z_disp is None:
            var_z = None
        else:
            var_z = dm.df_vars[var_z_disp]
        return dcc.Graph(figure = dm.plot_scatter(subsets_tups,
                                                  var_x,
                                                  var_y,
                                                  var_z))


    # Plot parcoor
    @app.callback(
        Output({'type': 'graph_parcoor_scatter_div_right', 'index': MATCH},
               'children'),
        [
        Input({'type': 'graph_plot_parcoor_button', 'index': MATCH},
              'n_clicks')
        ],
        [
        State({'type': 'subsets_dropdown', 'index': MATCH}, 'value'),
        State({'type': 'vars_dropdown', 'index': MATCH}, 'value')
        ]
    )  
    def plot_parcoor(n_clicks, subset_ids, plot_vars_disp):
        ctx = dash.callback_context
        if not ctx.triggered :
            raise dash.exceptions.PreventUpdate
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        if button_id == "":
            raise dash.exceptions.PreventUpdate
        if subset_ids is None :
            subsets = []
        else:
            subsets = [dm.subsets[ss_id] for ss_id in subset_ids]
        subsets_tups = [(ss['var'], ss['oper'], ss['crit']) for ss in subsets]
        if plot_vars_disp is None:
            plot_vars = None
        else:
            plot_vars = [dm.df_vars[v] for v in plot_vars_disp]
        return dcc.Graph(figure = dm.plot_par_coor(subsets_tups, plot_vars))


def main():
    pass


if __name__ == '__main__':
    main()
