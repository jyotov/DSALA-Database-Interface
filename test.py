from gsheet import GSheet
from database import Database, Client, Contact

gs = GSheet()
db = Database()

# Modify populate to check the database if a record of a client exists
#   If it does, then update it
#   If it doesn't, then create it
def populate() -> None:
    for client in gs.get_clients():
        if old_client := db.session.query(Client).where(Client.id == client["ID"]).first():
            # print(client, old_client)
            old_client.first_name = client["First Name"]
            old_client.last_name = client["Last Name"]
            old_client.suffix = client["Suffix"]
            old_client.preferred_name = client["Preferred Name"]
            old_client.email = client["Email"]
            old_client.phone = client["Phone Number"]
            old_client.dob = client["Date of Birth"]
            old_client.ethnicity = client["Ethnicity"]
            old_client.gender = client["Gender"]
            old_client.language = client["Preferred Language"]
            old_client.address1 = client["Address Line 1"]
            old_client.address2 = client["Address Line 2"]
            old_client.city = client["City"]
            old_client.state = client["State"]
            old_client.zip = client["Zipcode"]
            old_client.birth_hospital = client["Birth Hospital"]
            old_client.birth_city = client["Birth City"]
            old_client.birth_state = client["Birth State"]
            old_client.sports = client["Do You Have an Interest in Sports?"]
            old_client.dancing = client["Do You Have an Interest in Dancing?"]
            old_client.art = client["Do You Have an Interest in Art?"]
            old_client.acting = client["Do You Have an Interest in Acting?"]
            old_client.notes = client["Notes"]
        else:
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
                       zip=client["Zipcode"],
                       birth_hospital=client["Birth Hospital"],
                       birth_city=client["Birth City"],
                       birth_state=client["Birth State"],
                       sports=client["Do You Have an Interest in Sports?"],
                       dancing=client["Do You Have an Interest in Dancing?"],
                       art=client["Do You Have an Interest in Art?"],
                       acting=client["Do You Have an Interest in Acting?"],
                       notes=client["Notes"])
                )
        db.session.commit()

    for contact in gs.get_contacts():
        # print("---", contact)
        if old_contact := db.session.query(Contact).where((Contact.client_id == contact["DS Client's ID"]) &
                                                          (Contact.index == contact["Index"])).first():
            print(contact, old_contact)
            old_contact.first_name = contact["First Name"]
            old_contact.last_name = contact["Last Name"]
            old_contact.email = contact["Email"]
            old_contact.phone = contact["Phone Number"]
            old_contact.relationship = contact["Your Relationship to the Client"]
            old_contact.address1 = contact["Address Line 1"]
            old_contact.address2 = contact["Address Line 2"]
            old_contact.city = contact["City"]
            old_contact.state = contact["State"]
            old_contact.zip = contact["Zipcode"]
            old_contact.receive_emails = contact["Do you want to receive emails?"]
            old_contact.notes = contact["Notes"]
        else:
            print("new contact", contact)
            db.session.add(
                Contact(client_id=contact["DS Client's ID"],
                        index=contact["Index"],
                        first_name=contact["First Name"],
                        last_name=contact["Last Name"],
                        email=contact["Email"],
                        phone=contact["Phone Number"],
                        relationship=contact["Your Relationship to the Client"],
                        address1=contact["Address Line 1"],
                        address2=contact["Address Line 2"],
                        city=contact["City"],
                        state=contact["State"],
                        zip=contact["Zipcode"],
                        receive_emails=contact["Do you want to receive emails?"],
                        notes=contact["Notes"])
            )
        db.session.commit()

    # db.session.commit()

# print(os.getcwd())
# populate()
# TODO:
#       pull all records from the database and show them in dash in a datatable
#       have 2 data tables -- when you select a client, it can refresh the contract table

# print("-" * 100)
# for c in db.session.query(Contact).all():
#     print(c.first_name, c.last_name, c.email, c)
