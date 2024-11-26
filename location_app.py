import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
from geopy.distance import geodesic
import googlemaps

# Initialize Dash app
app = dash.Dash(__name__)
server = app.server

# Google Maps API key
API_KEY = "AIzaSyCQ8O5kjzZ2IjBxM6lO94QqklKZX52utz0"
gmaps = googlemaps.Client(key=API_KEY)

# Sample data with addresses
data = {
    "Address": [
        "1600 Amphitheatre Parkway, Mountain View, CA",
        "1 Infinite Loop, Cupertino, CA",
        "500 S Buena Vista St, Burbank, CA",
        "1111 S Figueroa St, Los Angeles, CA",
    ],
    "Name": ["Google HQ", "Apple HQ", "Disney Studios", "Crypto.com Arena"],
}
df = pd.DataFrame(data)

# Cache for coordinates
address_coords_cache = {}

def get_coordinates(address):
    """
    Fetch coordinates for a given address using Google Maps API.
    """
    if address in address_coords_cache:
        return address_coords_cache[address]

    try:
        result = gmaps.geocode(address)
        if result:
            coords = (result[0]["geometry"]["location"]["lat"], result[0]["geometry"]["location"]["lng"])
            address_coords_cache[address] = coords
            return coords
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None


# Los Angeles coordinates
LA_COORDS = (34.238412561733554, -118.44726802035643)

# App layout
app.layout = html.Div([
    html.H1("Filter Addresses by Distance from Los Angeles"),
    dcc.Input(id="distance-input", type="number", placeholder="Distance in miles", debounce=True),
    html.Button("Apply Filter", id="apply-button", n_clicks=0),
    dash_table.DataTable(
        id="data-table",
        columns=[{"name": col, "id": col} for col in df.columns],
        data=df.to_dict("records"),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'},
    ),
])


# Callback to filter the table based on distance
@app.callback(
    Output("data-table", "data"),
    Input("apply-button", "n_clicks"),
    State("distance-input", "value"),
)
def filter_by_distance(n_clicks, max_distance):
    if not max_distance:
        return df.to_dict("records")

    filtered_data = []

    for _, row in df.iterrows():
        coords = get_coordinates(row["Address"])
        if coords:
            distance = geodesic(LA_COORDS, coords).miles
            if distance <= max_distance:
                filtered_data.append(row)

    return pd.DataFrame(filtered_data).to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)