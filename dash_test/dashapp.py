import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import plotly.express as px
import base64
import io

# Initialize the app
app = dash.Dash(__name__)

# Store uploaded data in memory
uploaded_data = {}

app.layout = html.Div([
    html.H1("CSV Loader and Plotter", style={"textAlign": "center"}),
    dcc.Upload(
        id="upload-data",
        children=html.Div(["Drag and Drop or ", html.A("Select CSV File")]),
        style={
            "width": "10%",
            "height": "60px",
            "lineHeight": "60px",
            "borderWidth": "1px",
            "borderStyle": "dashed",
            "borderRadius": "5px",
            "textAlign": "center",
            "margin": "10px",
        },
        multiple=False,
    ),
    html.Div(
        id="output-data-upload",
        style={
            "marginTop": "20px",  # Add space above
            "marginBottom": "20px",  # Add space below
            "marginLeft": "10px",  # Add space to the left
            "marginRight": "10px",  # Add space to the right
            "textAlign": "center"  # Optional: Center the text
        }
    ),
    html.Div([
        html.Label("Select X-axis:"),
        dcc.Dropdown(id="x-axis-dropdown", placeholder="Select a column", style={"width": "200px"}),
        html.Label("Select Y-axis:"),
        dcc.Dropdown(id="y-axis-dropdown", placeholder="Select a column", style={"width": "200px"}),
    ]),
    dcc.Graph(
        id="plot-area",
        style={"width": "70%", "margin": "0 auto"}
    ),
])

@app.callback(
    [Output("output-data-upload", "children"),
     Output("x-axis-dropdown", "options"),
     Output("y-axis-dropdown", "options")],
    [Input("upload-data", "contents")],
    [State("upload-data", "filename")]
)
def load_csv(contents, filename):
    if contents is not None:
        try:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            df = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

            # Store the data for later use
            global uploaded_data
            uploaded_data = df

            # Create dropdown options based on columns
            options = [{"label": col, "value": col} for col in df.columns]
            return f"Loaded file: {filename}", options, options
        except Exception as e:
            return f"Error loading file: {e}", [], []
    return "No file loaded yet.", [], []

@app.callback(
    Output("plot-area", "figure"),
    [Input("x-axis-dropdown", "value"),
     Input("y-axis-dropdown", "value")]
)
def update_plot(x_col, y_col):
    if x_col is None or y_col is None or uploaded_data.empty:
        return dash.no_update
    try:
        fig = px.scatter(
            uploaded_data,
            x=x_col,
            y=y_col,
            labels={'x': x_col, 'y': y_col},
            title=f"Scatter Plot of {x_col} vs {y_col}"
        )
        fig.update_layout(width=800)
        return fig
    except Exception as e:
        return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)
