import dash
from dash import dcc, html, dash_table, Input, Output
import pandas as pd
import sqlite3

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Simulate a database
DATABASE = "accounts.db"


# Create a sample SQLite database
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS accounts (
            id INTEGER PRIMARY KEY,
            name TEXT,
            email TEXT,
            created_date TEXT
        )
    ''')
    conn.commit()

    # Insert sample data
    cursor.execute('DELETE FROM accounts')  # Clear existing data
    sample_data = [
        ("Alice", "alice@example.com", "2023-01-15"),
        ("Bob", "bob@example.com", "2022-12-10"),
        ("Charlie", "charlie@example.com", "2023-03-20"),
        ("Diana", "diana@example.com", "2023-02-05"),
    ]
    cursor.executemany('''
        INSERT INTO accounts (name, email, created_date)
        VALUES (?, ?, ?)
    ''', sample_data)
    conn.commit()
    conn.close()


# Initialize the database
init_db()


# Fetch data from the database and sort by created_date
def fetch_sorted_data():
    conn = sqlite3.connect(DATABASE)
    query = "SELECT * FROM accounts ORDER BY created_date ASC"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


# App layout
app.layout = html.Div([
    html.H1("Accounts Ordered by Creation Date"),
    dash_table.DataTable(
        id="data-table",
        columns=[
            {"name": "ID", "id": "id"},
            {"name": "Name", "id": "name"},
            {"name": "Email", "id": "email"},
            {"name": "Created Date", "id": "created_date"},
        ],
        data=fetch_sorted_data().to_dict("records"),
        sort_action="native",
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'padding': '10px'},
        style_header={'fontWeight': 'bold'},
    ),
])

if __name__ == "__main__":
    app.run_server(debug=True)