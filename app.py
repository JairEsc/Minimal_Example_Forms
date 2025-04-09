from dash import Dash, html, dcc, Input, Output, no_update
import boto3
from datetime import datetime
import csv
from io import StringIO
app = Dash(__name__)
s3 = boto3.client('s3')  # usa las credenciales configuradas con `aws configure`

BUCKET_NAME = 'aswbucketprueba'  # 
app.layout = html.Div([
    html.H1("Google Forms Replica", style={'textAlign': 'center'}),
    
    dcc.Store(id='geo-coordinates', storage_type='memory'),

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
    html.Button('Submit', id='submit-button', n_clicks=0,disabled=False),
    html.Div(id='output-div', style={'marginTop': '20px'}),

    # Geolocation script to fetch coordinates when the button is clicked
    html.Script("""
        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const coords = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    const geoStore = document.querySelector('#geo-coordinates');
                    geoStore.dataset.props = JSON.stringify({ data: coords });
                    geoStore.dispatchEvent(new Event('input'));
                }, function() {
                    alert("Sorry, no position available.");
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }

        // Trigger location fetch when the submit button is clicked
        document.getElementById("submit-button").addEventListener("click", getLocation);
    """)
])

@app.callback(
    [Output('output-div', 'children'),Output('submit-button', 'disabled')],
    [Input('submit-button', 'n_clicks'),
    Input('name-input', 'value'),
     Input('color-dropdown', 'value'),
     Input('comments-textarea', 'value'),]
)
def update_output(n_clicks, name, color, comments):
    if n_clicks > 0:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'respuesta_{now}.csv'
        # Create CSV content
        csv_buffer = StringIO()
        csv_writer = csv.writer(csv_buffer)
        csv_writer.writerow(["Name", "Favorite Color", "Comments" ])
        csv_writer.writerow([name, color, comments])

        # Upload CSV to S3
        s3.put_object(Bucket=BUCKET_NAME, Key=nombre_archivo, Body=csv_buffer.getvalue().encode('utf-8'))

        return html.Div([
            html.H2(f"Respuesta Guardada a la hora {now} "),
            html.P(f"Name: {name}"),
            html.P(f"Favorite Color: {color}"),
            html.P(f"Comments: {comments}")
        ]), True
    return "", no_update
#Falta ver la manera de ejecutar javascript cuando se da click en submit o al cargar a página.
#navigator.geolocation.getCurrentPosition(function(position) {
#    console.log(position.coords.latitude, position.coords.longitude);
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)