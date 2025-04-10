from dash import Dash, html, dcc, Input, Output, no_update
import mysql.connector
from datetime import datetime
import csv
from io import StringIO

app = Dash(__name__)

# RDS MySQL credentials and connection setup
DB_HOST = 'database-1.c12wu4gkibta.us-east-2.rds.amazonaws.com'
DB_USER = 'admin'
DB_PASSWORD = 'pass_mysql'
DB_NAME = 'prueba_sql'

# Create the connection
def get_db_connection():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    return conn

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
    html.Button('Submit', id='submit-button', n_clicks=0, disabled=False),
    html.Div(id='output-div', style={'marginTop': '20px'}),
])

@app.callback(
    [Output('output-div', 'children'), Output('submit-button', 'disabled')],
    [Input('submit-button', 'n_clicks'),
     Input('name-input', 'value'),
     Input('color-dropdown', 'value'),
     Input('comments-textarea', 'value')]
)
def update_output(n_clicks, name, color, comments):
    if n_clicks > 0:
        now = datetime.now().strftime('%Y%m%d_%H%M%S')
        # Connect to the RDS MySQL database
        conn = get_db_connection()
        cursor = conn.cursor()

        # Insert data into the database
        cursor.execute("""
            INSERT INTO responses (name, favorite_color, comments, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (name, color, comments, now))

        # Fetch all table names in the database
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        # Commit changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()

        # Format the table names for display
        table_list = html.Ul([html.Li(table[0]) for table in tables])

        return html.Div([
            html.H2(f"Respuesta Guardada a la hora {now} "),
            html.P(f"Name: {name}"),
            html.P(f"Favorite Color: {color}"),
            html.P(f"Comments: {comments}"),
            html.H3("Tables in the Database:"),
            table_list
        ]), True
    return "", no_update


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8050)
