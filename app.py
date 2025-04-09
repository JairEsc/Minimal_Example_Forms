from dash import Dash, html, dcc, Input, Output

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Google Forms Replica", style={'textAlign': 'center'}),
    html.Div([
        html.Label("What is your name?"),
        dcc.Input(id='name-input', type='text', placeholder='Enter your name'),
    ], style={'marginBottom': '20px'}),
    html.Div([
        html.Label("What is your favorite color?"),
        dcc.Dropdown(
            id='color-dropdown',
            options=[
                {'label': 'Red', 'value': 'Red'},
                {'label': 'Blue', 'value': 'Blue'},
                {'label': 'Green', 'value': 'Green'},
                {'label': 'Other', 'value': 'Other'}
            ],
            placeholder='Select a color'
        ),
    ], style={'marginBottom': '20px'}),
    html.Div([
        html.Label("Any additional comments?"),
        dcc.Textarea(
            id='comments-textarea',
            placeholder='Enter your comments here',
            style={'width': '100%', 'height': '100px'}
        ),
    ], style={'marginBottom': '20px'}),
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-div', style={'marginTop': '20px'})
])

@app.callback(
    Output('output-div', 'children'),
    Input('submit-button', 'n_clicks'),
    [Input('name-input', 'value'),
     Input('color-dropdown', 'value'),
     Input('comments-textarea', 'value')]
)
def update_output(n_clicks, name, color, comments):
    if n_clicks > 0:
        return html.Div([
            html.P(f"Name: {name}"),
            html.P(f"Favorite Color: {color}"),
            html.P(f"Comments: {comments}")
        ])
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)