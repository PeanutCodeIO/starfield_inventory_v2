import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import io
import csv

# ____ Get all suppliers
@anvil.server.callable
def get_all_suppliers():
  return app_tables.suppliers.search()




#____ Create a new supplier
@anvil.server.callable
def save_new_supplier(all_data):
    id = auto_increment_supplier_id()
    app_tables.suppliers.add_row(supplier_id=id, **all_data)








#____ Export CSV File
@anvil.server.callable
def create_suppliers_import_template():
    # Define the headers for your CSV file
    headers = ["Business Name", "ABN", "Address", "Contact", "Phone", "Email", "Website","Customer Reference ID", "Payment Terms", "Bank Account Name", "BSB", "Account", "Fullfillment Time", "Notes" ]
  
    # Use StringIO to create a file-like object in memory
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(headers)

    # Convert the StringIO object to a Media object
    return anvil.BlobMedia('text/csv', output.getvalue().encode(), name='suppliers_template.csv')



#____ Import CSV File
def auto_increment_supplier_id():
    # Create a new supplier_id
    supplier_data = app_tables.suppliers.search()
    if supplier_data:
        last_supplier_id = max((d['supplier_id'] for d in supplier_data if d['supplier_id'] is not None), default=0)
        next_supplier_id = last_supplier_id + 1
    else:
        next_supplier_id = 1

    return next_supplier_id


@anvil.server.callable
def upload_csv_and_create_suppliers(file):
    # Read the uploaded CSV file
    file_content = file.get_bytes().decode('utf-8')
    file_io = io.StringIO(file_content)
    reader = csv.reader(file_io)
    
    # Get the headers from the first row of the CSV
    headers = next(reader)
    
    # Create a dictionary to map the CSV headers to the database column names
    header_map = {
        "Business Name": "business_name",
        "ABN": "abn",
        "Address": "address",
        "Contact": "contact",
        "Phone": "phone",
        "Email": "email",
        "Website": "website",
        "Customer Reference ID":"customer_ref",
        "Payment Terms": "payment_terms",
        "Bank Account Name": "bank_name",
        "BSB": "bsb",
        "Account": "account",
        "Fullfillment Time": "fullfillment",
        "Notes": "notes"
    }
    
    # Loop through each row in the CSV file
    for row in reader:
        supplier_data = {header_map[header]: value for header, value in zip(headers, row)}
        
        # Search for an existing supplier with the given business name
        existing_suppliers = app_tables.suppliers.search(business_name=supplier_data["business_name"])
        
        # Check if any suppliers were found
        existing_supplier = None
        for supplier in existing_suppliers:
            existing_supplier = supplier
            break
        
        if existing_supplier:
            # Update the existing supplier row
            for key, value in supplier_data.items():
                setattr(existing_supplier, key, value)
        else:
            # If no existing supplier, add a new row
            supplier_data["supplier_id"] = auto_increment_supplier_id()
            app_tables.suppliers.add_row(**supplier_data)

    return "Upload and supplier creation successful!"