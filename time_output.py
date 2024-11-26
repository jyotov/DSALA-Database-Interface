from dash import Dash, html, Output, Input
from datetime import datetime

# Initialize the Dash app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Button("Click Me", id="button", n_clicks=0),
    html.Div(id="output-div")
])

# Callback to update the output with the timestamp
@app.callback(
    Output("output-div", "children"),
    Input("button", "n_clicks")
)
def update_output(n_clicks):
    if n_clicks > 0:
        # Get current date and time
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Button clicked at: {current_time}"
    return "Click the button to see the timestamp."

# Run the server
if __name__ == "__main__":
    app.run_server(debug=True)