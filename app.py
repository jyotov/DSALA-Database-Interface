import json
from datetime import datetime

import dash
import googlemaps
from dash import dcc, html, dash_table, callback
from dash.dependencies import Input, Output, State
from geopy.distance import geodesic
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import test
from database import Client, Contact

# database connection
DATABASE_URL = 'sqlite:///dsala.db'  # Replace with your actual database URL
engine = create_engine('sqlite:///dsala.db')
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Google Maps API key
API_KEY = "AIzaSyCQ8O5kjzZ2IjBxM6lO94QqklKZX52utz0"
gmaps = googlemaps.Client(key=API_KEY)

# Cache for coordinates
address_coords_cache = {}

# model
# class YourModel(Base):
#     __tablename__ = 'clients'
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String, index=True)
#     value = Column(String)

# query and return data as JSON for clients
def get_data_as_json():
    session = SessionLocal()
    try:
        # Query the database
        results = session.query(Client).all()

        # Convert results to JSON-compatible format
        json_list = [result.__dict__ for result in results]
        for item in json_list:
            item.pop('_sa_instance_state', None)  # Remove SQLAlchemy instance state

        return json.dumps(json_list)  # Convert list to JSON string
    finally:
        session.close()

json_data = get_data_as_json()

# Load JSON data into Python objects
data = json.loads(json_data)
# df = pd.DataFrame(data)

# for contacts
def get_data_contacts_as_json(client_id):
    session = SessionLocal()
    try:
        # Query the database
        results = session.query(Contact).where(Contact.client_id == client_id).all()

        # Convert results to JSON-compatible format
        json_list = [result.__dict__ for result in results]
        for item in json_list:
            item.pop('_sa_instance_state', None)  # Remove SQLAlchemy instance state

        return json.dumps(json_list)  # Convert list to JSON string
    finally:
        session.close()

# Gets coordinates for address using Google Maps API
def get_coordinates(address):
    if address in address_coords_cache:
        print(f"Cache hit for: {address}")
        return address_coords_cache[address]

    try:
        print(f"Querying coordinates for: {address}")
        result = gmaps.geocode(address)  # Works for ZIP codes or addresses
        if result:
            coords = (
                result[0]["geometry"]["location"]["lat"],
                result[0]["geometry"]["location"]["lng"],
            )
            address_coords_cache[address] = coords
            print(f"Resolved {address} to coordinates: {coords}")
            return coords
        else:
            print(f"No results found for: {address}")
    except Exception as e:
        print(f"Error geocoding {address}: {e}")
    return None

# # DSALA coordinates
# DSALA_COORDS = (34.238412561733554, -118.44726802035643)

# column names for the DataTable
#columns = [{"name": i, "id": i} for i in data[0].keys()]
columns = [{'name': 'ID', 'id': 'id'},
           {"name": 'Date Created', "id": 'date_created'},
           {"name": 'First Name', "id": 'first_name'},
           {"name": 'Last Name', "id": 'last_name'},
           {"name": 'Suffix', "id": 'suffix'},
           {"name": 'Preferred Name', "id": 'preferred_name'},
           {"name": 'Email', "id": 'email'},
           {"name": 'Phone Number', "id": 'phone'},
           {"name": 'Date of Birth', "id": 'dob'},
           {"name": 'Ethnicity', "id": 'ethnicity'},
           {"name": 'Gender', "id": 'gender'},
           {"name": 'Preferred Language', "id": 'language'},
           {"name": 'Address Line 1', "id": 'address1'},
           {"name": 'Address Line 2', "id": 'address2'},
           {"name": 'City', "id": 'city'},
           {"name": 'State', "id": 'state'},
           {"name": 'Zipcode', "id": 'zip'},
           {"name": 'Birth Hospital', "id": 'birth_hospital'},
           {"name": 'Birth City', "id": 'birth_city'},
           {"name": 'Birth State', "id": 'birth_state'},
           {"name": 'Do You Have an Interest in Sports?', "id": 'sports'},
           {"name": 'Do You Have an Interest in Dancing?', "id": 'dancing'},
           {"name": 'Do You Have an Interest in Art?', "id": 'art'},
           {"name": 'Do You Have an Interest in Acting?', "id": 'acting'},
           {"name": 'Notes', "id": 'notes'}]

columns_contacts = [{'name': "DS Client's ID", 'id': 'client_id'},
            {'name': "Index", 'id': 'index'},
           {"name": 'First Name', "id": 'first_name'},
           {"name": 'Last Name', "id": 'last_name'},
           {"name": 'Email', "id": 'email'},
           {"name": 'Phone Number', "id": 'phone'},
           {"name": 'Your Relationship to the Client', "id": 'relationship'},
           {"name": 'Address Line 1', "id": 'address1'},
           {"name": 'Address Line 2', "id": 'address2'},
           {"name": 'City', "id": 'city'},
           {"name": 'State', "id": 'state'},
           {"name": 'Zipcode', "id": 'zip'},
           {"name": 'Do you want to receive emails?', "id": 'receive_emails'},
           {"name": 'Notes', "id": 'notes'},
            ]

# Dash app initialization
app = dash.Dash(__name__)

print(str(datetime.today().date()))

num_clients = len(data)

# app layout for data table
app.layout = (html.Div([
    html.H1(children='DSALA Client Database', style={'textAlign': 'center'}),

    html.Div('Search for clients in the database. Be sure to click the "Refresh Data" button below to generate the most '
             'updated version of the client database. '
             'Clients can be filtered based on their age and their location of residence. '
             'After applying the desired filters, click the "Download Emails" button to generate a text (.txt) '
             'file of all clients and their associated contacts. These emails can then be copied directly as email recipients.'),

    html.B(html.Div(f'There are currently {num_clients} total clients in the database (this will not vary based on filters). Click the "Refresh Data" '
           'button below to ensure that this is the most updated number.')),
    html.Button('Refresh Data', id='refresh',style={'margin-top':'10px'}),
    html.Div(id="output", style={"margin-top": "10px", "color": "red"}),

    html.H4(children='Age Filter'),
    html.Div('To filter by age, enter a minimum age and maximum age (inclusive). Only clients whose ages are equal to '
             'or between these two values will be displayed in the table.'),
    # Age filter input
    html.Div([
        html.Label("Minimum Age: "),
        dcc.Input(id='min-age', type='number', value=0, min=0, max=120, step=1, style={'margin-right': '10px'}),
        html.Label("Maximum Age: "),
        dcc.Input(id='max-age', type='number', value=120, min=0, max=120, step=1),
    ], style={'padding': '5px'}),

    html.H4(children='Location Filter'),
    html.Div('To filter by location, enter a zipcode as the "center point" and the desired distance (in miles) from that center point. '
             'Only clients with addresses within that radius will be displayed in the table.'),
    dcc.Input(id="zipcode-input", type="number", placeholder="Enter ZIP code", debounce=True,
              style={'margin-right': '10px'}),
    dcc.Input(id="distance-input", type="number", placeholder="Distance in miles", debounce=True,style={'margin-top': '5px'}),

    html.H4(children='Interest Filter'),
    html.Div('To filter by client interests, check the interests (sports, dancing, art and/or acting to display in the table. '
             'Clients who have indicated any of the selected interests will be displayed in the table.'),
    dcc.Checklist(
        id="interest-filter",
        options=[
            {'label': 'Sports', 'value': 'sports'},
            {'label': 'Dancing', 'value': 'dancing'},
            {'label': 'Art', 'value': 'art'},
            {'label': 'Acting', 'value': 'acting'},
        ],
        value=[],
        style={'margin-top': '10px'}
    ),

    html.Div(
    html.Button("Apply Filters", id="apply-button", n_clicks=0,style={'margin-top': '30px'}),),

    html.Div([
        dash_table.DataTable(
            id='table',
            columns=columns,
            data=data,
            page_size=50,  # Number of rows per page
            style_table={'overflowY': 'auto', 'margin-top': '10px','margin-bottom': '10px'},  # Optional styling
            style_cell={'textAlign': 'left'},
            #filter_action="native",
            sort_action="native",
            sort_mode="multi",
            #column_selectable="single",
            row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
        ),
        html.Div(
            id='contacts_container'
        ),
        html.Div([
            html.Button("Download Emails", id="btn-download-txt",style={'margin-top': '10px'}),
            dcc.Download(id="download-text")
        ]),

    ])
]))

# def calculate_age(birth_date):
#     if isinstance(birth_date, str):
#         birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
#
#     today = datetime.today().date()
#     age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
#
#     return age
#
# birth_date = '1990-04-25'
# age = calculate_age(birth_date)
# print(f"Age: {age}")

def calculate_age(birthdate):
    today = datetime.today().date()
    year, month, day = map(int, birthdate.split("-"))
    age = today.year - year - ((today.month, today.day) < (month, day))
    return age

filtered = []

# Refreshing table
@callback(
    Output('table', 'data', allow_duplicate=True),
    Output('table', 'selected_rows', allow_duplicate=True),
    Output('output', 'children'),
    # Output('num_clients', 'children'),
    Input('refresh','n_clicks'),
    config_prevent_initial_callbacks=True
)
def update_table2(n_clicks):
    test.populate()
    json_data = get_data_as_json()
    # Load JSON data into Python objects
    data = json.loads(json_data)

    last_refreshed = f"Last refreshed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    # num_clients = (f'There are currently {len(data)} total clients in the database (this will not vary based on filters). '
    #                f'Click the "Refresh Data" button below to ensure that this is the most updated number.')

    return data, [], last_refreshed

# Filtering table based on age, location, and interest
@callback(
    Output('table', 'data'),
    Output('table','selected_rows'),
    State('min-age', 'value'),
    State('max-age', 'value'),
    State('zipcode-input', 'value'),
    State("distance-input", "value"),
    State('interest-filter', 'value'),
    Input("apply-button", "n_clicks"),
)

def update_table(min_age, max_age, zipcode, max_distance, interests, n_clicks):
    global filtered_data
    # print(f"Received ZIP code: {zipcode}, Max Distance: {max_distance}")

    # Filter the datatable based on age range
    if min_age is None:
        min_age = 0
    if max_age is None:
        max_age = 120
    data2 = [person for person in data if min_age <= calculate_age(person['dob']) <= max_age]

    # Filter the datatable based on location

    # if max_distance:
    #     filtered_data = []
    #     for row in data2:
    #         address = (row["address1"] + ", " + row["address2"] + ", " + row["city"] + " " +
    #                    row["state"] + " " + row["zip"])
    #         coords = get_coordinates(address)
    #         if coords:
    #             distance = geodesic(get_coordinates(zipcode), coords).miles
    #             if distance <= max_distance:
    #                 filtered_data.append(row)

    if max_distance:
        try:
            max_distance = float(max_distance)
        except ValueError:
            return data2, []  # unfiltered data

        filtered_data = []
        for row in data2:
            address = (row["address1"] + ", " + row["address2"] + ", " + row["city"] + " " +
                       row["state"] + " " + row["zip"])
            coords = get_coordinates(address)
            print("Coordinates: ", coords)
            print("Zipcode ", get_coordinates(zipcode))
            if coords:
                distance = geodesic(get_coordinates(zipcode), coords).miles
                if distance <= max_distance:
                    filtered_data.append(row)
    else:
        filtered_data = data2

    # Filter the datatable based on interests
    if interests:
        filtered_data = [
            person for person in filtered_data
            if any(person.get(interest, "No").lower() == "yes" for interest in interests)
        ]

    # for person in filtered_data:
    #     if person not in filtered:
    #         filtered.append(person)
    # for person in filtered:
    #     if person not in filtered_data:
    #         filtered.remove(person)

    return filtered_data, []

# Filtering table based on distance from DSALA
# def filter_by_distance(n_clicks, max_distance):
#     if not max_distance:
#         return df.to_dict("records")
#
#     filtered_data = []
#
#     for row in data:
#         address = (row["address1"] + ", " + row["address2"] + ", " + row["city"] + " " +
#                    row["state"] + " " + row["zip"])
#         coords = get_coordinates(address)
#         if coords:
#             distance = geodesic(DSALA_COORDS, coords).miles
#             if distance <= max_distance:
#                 filtered_data.append(row)
#
#     return filtered_data

# Displaying contacts of a client
@app.callback(
    Output('contacts_container', 'children'),
    Input('table', 'selected_rows'),
    State('table','data')
)
def display_expanded_row(selected_rows, data):
    if not selected_rows:
        return html.Div("Select a row to see that client's contacts.")

    client_id = data[selected_rows[0]]['id']
    # additional_contacts = data_contacts.get(client_id)

    json_data_contacts = get_data_contacts_as_json(client_id)

    # Load JSON data into Python objects
    data_contacts = json.loads(json_data_contacts)

    if True is not None:
        # return html.Div(f"Select a row to see additional contacts.{client_id}")
        return dash_table.DataTable(
            id='table_contacts',
            columns=columns_contacts,
            data=data_contacts,
            page_size=10,  # Number of rows per page
            style_table={'overflowY': 'auto'},  # Optional styling
            style_cell={'textAlign': 'left'},
            # filter_action="native",
            sort_action="native",
            sort_mode="multi",
            # column_selectable="single",
            #row_selectable="single",
            row_deletable=False,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
        ),
    return html.Div("No additional contacts available.")

# Downloading emails of filtered clients in a .txt file
@callback(
    Output("download-text", "data"),
    Input("btn-download-txt", "n_clicks"),
    prevent_initial_call=True,
)
def func(n_clicks):
    global filtered_data  # Access the filtered list

    emails = ""
    for person in filtered_data:
        # emails of clients
        emails += person.get("email", "") + "\n"
        # emails of contacts of clients
        client_contacts_json = get_data_contacts_as_json(person["id"])
        client_contacts = json.loads(client_contacts_json)
        for contact in client_contacts:
            emails += contact.get("email", "") + "\n"

    return dict(content=emails, filename="emails_" + datetime.today().strftime('%Y-%m-%d') + ".txt")


if __name__ == '__main__':
    app.run_server(debug=True)