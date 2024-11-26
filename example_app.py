import dash
from dash import dcc, html, Input, Output
from dash import dash_table
import pandas as pd
import json

# Sample JSON data
json_data = '''
[
    {"Name": "Alice", "Age": 24, "City": "New York"},
    {"Name": "Bob", "Age": 35, "City": "Los Angeles"},
    {"Name": "Charlie", "Age": 45, "City": "Chicago"},
    {"Name": "David", "Age": 20, "City": "Houston"},
    {"Name": "Eva", "Age": 29, "City": "Phoenix"}
]
'''

# Load JSON data into a DataFrame
data = json.loads(json_data)
df = pd.DataFrame(data)

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Data Table with Age Filter"),

    # Age filter input
    html.Div([
        html.Label("Minimum Age:"),
        dcc.Input(id='min-age', type='text', value=0, min=0, max=100, step=1),
    ], style={'padding': '10px'}),

    html.Div([
        html.Label("Maximum Age:"),
        dcc.Input(id='max-age', type='text', value=100, min=0, max=100, step=1),
    ], style={'padding': '10px'}),

    # Data table
    dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records')
    )
])

print("hi")
print(df["Age"])

@app.callback(
    Output('table', 'data'),
    [Input('min-age', 'value'), Input('max-age', 'value')]
)

def update_table(min_age, max_age):
    # Filter the DataFrame based on age range
    if min_age == '':
        min_age = 0
    if max_age == '':
        max_age = 120
    filtered_df = df[(df["Age"] >= int(min_age)) & (df["Age"] <= int(max_age))]
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)