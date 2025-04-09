from dash import Dash, html, dcc, Input, Output
import boto3
from datetime import datetime
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
    html.Button('Submit', id='submit-button', n_clicks=0),
    html.Div(id='output-div', style={'marginTop': '20px'}),
    html.Div([
    html.Script("""
        document.addEventListener("DOMContentLoaded", function() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    const coords = {
                        lat: position.coords.latitude,
                        lon: position.coords.longitude
                    };
                    const store = document.querySelector('[data-dash-is-loading="false"] [id="geo-coordinates"]');
                    if (store) {
                        store.setAttribute("data-data", JSON.stringify(coords));
                        store.dispatchEvent(new Event("change"));
                    }
                });
            }
        });
    """)
])
])

@app.callback(
    Output('output-div', 'children'),
    Input('submit-button', 'n_clicks'),
    [Input('name-input', 'value'),
     Input('color-dropdown', 'value'),
     Input('comments-textarea', 'value'),
     Input('geo-coordinates', 'data')]
)
def update_output(n_clicks, name, color, comments, geo_data):
    if n_clicks > 0:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        nombre_archivo = f'respuesta_{now}.txt'

        lat, lon = None, None
        if geo_data:
            lat = geo_data.get("lat")
            lon = geo_data.get("lon")
        # with open(nombre_archivo, 'w', encoding='utf-8') as file:
        #     file.write(f"Nombre: {name} \n Color: {color} \n Comentario: {comments}")
        contenido = f"Nombre: {name} \nColor: {color} \nComentario: {comments} \nLatitud: {lat} \nLongitud: {lon}"
        s3.put_object(Bucket=BUCKET_NAME, Key=nombre_archivo, Body=contenido.encode('utf-8'))

        return html.Div([
            html.P(f"Name: {name}"),
            html.P(f"Favorite Color: {color}"),
            html.P(f"Comments: {comments}"),
            html.P(f"Lat: {lat}, Lon: {lon}")
        ])
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)