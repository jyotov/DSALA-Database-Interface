from gsheet import GSheet
from database import Database, Client, Contact

gs = GSheet()
db = Database()

# Modify populate to check the database if a record of a client exists
#   If it does, then update it
#   If it doesn't, then create it
def populate() -> None:
    for client in gs.get_clients():
        print(client)
        db.session.add(
            Client(id=client["ID"],
                   date_created=client["Date Created"],
                   first_name=client["First Name"],
                   last_name=client["Last Name"],
                   suffix=client["Suffix"],
                   preferred_name=client["Preferred Name"],
                   email=client["Email"],
                   phone=client["Phone Number"],
                   dob=client["Date of Birth"],
                   ethnicity=client["Ethnicity"],
                   gender=client["Gender"],
                   language=client["Preferred Language"],
                   address1=client["Address Line 1"],
                   address2=client["Address Line 2"],
                   city=client["City"],
                   state=client["State"],
                   zip=client["Zip"],
                   birth_hospital=client["Birth Hospital"],
                   birth_city=client["Birth City"],
                   birth_state=client["Birth State"],
                   notes=client["Notes"])
        )
        db.session.commit()

    for contact in gs.get_contacts():
        print(contact)
        db.session.add(
            Contact(client_id=contact["DS Client's ID"],
                    index=contact["Index"],
                    first_name=contact["First Name"],
                    last_name=contact["Last Name"],
                    email=contact["Email"],
                    phone=contact["Phone Number"],
                    relationship=contact["Relationship"],
                    address1=contact["Address Line 1"],
                    address2=contact["Address Line 2"],
                    city=contact["City"],
                    state=contact["State"],
                    zip=contact["Zip"],
                    receive_emails=contact["Do you want to receive emails?"],
                    notes=contact["Notes"])
        )
        db.session.commit()

    # db.session.commit()

# print(os.getcwd())
populate()
# TODO:
#       pull all records from the database and show them in dash in a datatable
#       have 2 data tables -- when you select a client, it can refresh the contract table

for c in db.session.query(Contact).all():
    print(c.first_name, c.last_name, c.email, c)
