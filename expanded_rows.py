import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd

# Sample data for the main DataTable
clients_data = pd.DataFrame({
    "Client ID": [101, 102, 103],
    "Name": ["Alice Smith", "Bob Johnson", "Charlie Davis"],
    "Email": ["alice@example.com", "bob@example.com", "charlie@example.com"]
})

# Sample data for additional contact details
contacts_data = {
    101: pd.DataFrame({"Contact Name": ["John Doe", "Emily White"], "Phone": ["123-456-7890", "987-654-3210"]}),
    102: pd.DataFrame({"Contact Name": ["Sarah Brown"], "Phone": ["555-666-7777"]}),
    103: pd.DataFrame({"Contact Name": ["Michael Green", "Olivia Black"], "Phone": ["222-333-4444", "888-999-0000"]}),
}

# Initialize the Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H3("Client Data"),
    dash_table.DataTable(
        id='clients-table',
        columns=[{"name": col, "id": col} for col in clients_data.columns],
        data=clients_data.to_dict('records'),
        style_table={'overflowX': 'auto'},
        row_selectable='single',
    ),
    html.Div(id='expanded-row-container')
])


@app.callback(
    Output('expanded-row-container', 'children'),
    Input('clients-table', 'selected_rows'),
)
def display_expanded_row(selected_rows):
    if not selected_rows:
        return html.Div("Select a row to see additional contacts.")

    client_id = clients_data.iloc[selected_rows[0]]['Client ID']
    additional_contacts = contacts_data.get(client_id)

    if additional_contacts is not None:
        return dash_table.DataTable(
            columns=[{"name": col, "id": col} for col in additional_contacts.columns],
            data=additional_contacts.to_dict('records'),
            style_table={'margin-top': '20px'}
        )
    return html.Div("No additional contacts available.")


if __name__ == '__main__':
    app.run_server(debug=True)