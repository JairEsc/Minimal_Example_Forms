from dash import Dash, html, dcc, Input, Output, State
import base64

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Minimal Google Forms Example"),
    html.Label("What is your favorite color?"),
    dcc.Input(id="color-input", type="text", placeholder="Enter a color"),
    html.Br(),
    html.Label("Rate your experience (1-5):"),
    dcc.Slider(id="rating-slider", min=1, max=5, step=1, value=3,
               marks={i: str(i) for i in range(1, 6)}),
    html.Br(),
    html.Label("Upload an image file:"),
    dcc.Upload(
        id="file-upload",
        children=html.Button("Upload File"),
        accept=".jpeg,.jpg,.png",
    ),
    html.Div(id="file-upload-output"),
    html.Br(),
    html.Button("Submit", id="submit-button", n_clicks=0),
    html.Div(id="output-div"),
    dcc.Store(id="geo-location-store"),  # Store for geographical location
    html.Div(id="geo-location-output"),
    html.Script("""
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const lat = position.coords.latitude;
                const lon = position.coords.longitude;
                const locationData = JSON.stringify({latitude: lat, longitude: lon});
                const event = new CustomEvent("geoLocationUpdate", {detail: locationData});
                window.dispatchEvent(event);
            }
        );
    """, type="text/javascript")
])

@app.callback(
    Output("geo-location-store", "data"),
    Input("submit-button", "n_clicks"),
    prevent_initial_call=True
)
def get_geo_location(n_clicks):
    # This callback is triggered by the JavaScript event
    return None  # Placeholder for location data

@app.callback(
    Output("file-upload-output", "children"),
    Input("file-upload", "contents"),
    State("file-upload", "filename"),
    prevent_initial_call=True
)
def handle_file_upload(contents, filename):
    if contents:
        content_type, content_string = contents.split(',')
        if "jpg" in content_type:
            decoded = base64.b64decode(content_string)
            return f"File {filename} uploaded successfully."
    return "Invalid file type. Please upload a .jpg file."

@app.callback(
    Output("output-div", "children"),
    Input("submit-button", "n_clicks"),
    State("color-input", "value"),
    State("rating-slider", "value"),
    State("geo-location-store", "data"),
    prevent_initial_call=True
)
def update_output(n_clicks, color, rating, geo_data):
    if n_clicks > 0:
        location = geo_data if geo_data else "Location not available"
        return f"Your favorite color is {color}, you rated your experience as {rating}, and your location is {location}."
    return ""

if __name__ == "__main__":
    app.run_server(debug=True)