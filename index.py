import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd


vg = pd.read_csv('vgsales.csv')


app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

app.layout = html.Div([

    html.Div([
        html.Div([
            html.Div([
                html.H3('Video Game Sales', style = {'margin-bottom': '0px', 'color': 'white'}),
            ])
        ], className = "create_container1 four columns", id = "title"),

    ], id = "header", className = "row flex-display", style = {"margin-bottom": "25px"}),


    html.Div([
        html.Div([


            html.P('Select Genre', className = 'fix_label', style = {'color': 'white', 'margin-top': '2px'}),
            dcc.Dropdown(id = 'select_genre',
                         multi = False,
                         clearable = True,
                         disabled = False,
                         style = {'display': True},
                         value = 'Action',
                         placeholder = 'Select Countries',
                         options = [{'label': c, 'value': c}
                                    for c in (vg['Genre'].unique())], className = 'dcc_compon'),




        ], className = "create_container2 four columns", style = {'margin-bottom': '20px'}),
    ], className = "row flex-display"),



    html.Div([
        html.Div([
            html.P('Select Platform', className = 'fix_label', style = {'color': 'white'}),
            dcc.RadioItems(id = 'radio_items',
                           labelStyle = {"display": "inline-block"},
                           options = [],
                           style = {'text-align': 'center', 'color': 'white'}, className = 'dcc_compon'),

            dcc.Graph(id = 'scatter_chart',
                      config = {'displayModeBar': 'hover'}),

        ], className = "create_container2 eight columns"),

    ], className = "row flex-display"),

], id= "mainContainer", style={"display": "flex", "flex-direction": "column"})

@app.callback(
    Output('radio_items', 'options'),
    [Input('select_genre', 'value')])
def get_platform_options(select_genre):
    vg1 = vg[vg['Genre'] == select_genre]
    return [{'label': k, 'value': k} for k in vg1['Platform'].unique()]

@app.callback(
    Output('radio_items', 'value'),
    [Input('radio_items', 'options')])
def get_platform_value(radio_items):
    return [k['value'] for k in radio_items][0]


@app.callback(Output('scatter_chart', 'figure'),
              [Input('select_genre', 'value')],
              [Input('radio_items', 'value')])
def update_graph(select_genre, radio_items):
    vg2 = vg.groupby(['Platform', 'Genre', 'Publisher'])['NA_Sales'].sum().reset_index()
    vg3 = vg2[(vg2['Genre'] == select_genre) & (vg2['Platform'] == radio_items)]



    return {
        'data':[go.Scatter(
                    x=vg3['Publisher'],
                    y=vg3['NA_Sales'],
                    mode = 'markers',
                    marker = dict(
                        size = 20,
                        color = vg3['NA_Sales'],
                        colorscale = 'HSV',
                        showscale = False,
                        line = dict(
                            color = 'MediumPurple',
                            width = 2
                        )),
                    hoverinfo='text',
                    hovertext=
                    '<b>Genre</b>: ' + vg3['Genre'].astype(str) + '<br>' +
                    '<b>Platform</b>: ' + vg3['Platform'] + '<br>' +
                    '<b>Publisher</b>: ' + vg3['Publisher'].astype(str) + '<br>' +
                    '<b>Sales in NA</b>: $' + [f'{x:,.2f}' for x in vg3['NA_Sales']] + '<br>'


              )],


        'layout': go.Layout(
             plot_bgcolor='#010915',
             paper_bgcolor='#010915',
             title={
                'text': '',

                'y': 0.96,
                'x': 0.5,
                'xanchor': 'center',
                'yanchor': 'top'},
             titlefont={
                        'color': 'rgb(50, 50, 50)',
                        'size': 15},

             hovermode='x',
             margin = dict(b = 160),
             xaxis=dict(title='<b></b>',
                        color='white',
                        showline=True,
                        showgrid=False,
                        linecolor='white',
                        linewidth=1,


                ),

             yaxis=dict(title='<b>Sales in NA(Region)</b>',
                        color='white',
                        showline=False,
                        showgrid=True,
                        linecolor='white',

                ),

            legend = {
                'orientation': 'h',
                'bgcolor': '#010915',
                'x': 0.5,
                'y': 1.25,
                'xanchor': 'center',
                'yanchor': 'top'},
            font = dict(
                family = "sans-serif",
                size = 12,
                color = 'white',


                 )
        )

    }


if __name__ == '__main__':
    app.run_server(debug=True)