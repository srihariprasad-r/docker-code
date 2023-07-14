import csv

# data rows as dictionary objects
mydict = [{'Sno': '1', 'birth_date': '2023-03-10', 'first_name': 'Ash Ketchum', 'last_name': 'Jr.', 'created_date': '2020-01-01T14:49:12.301977',
           'ssn': '360-56-6750', 'credit_card_number': '3600-5600-6750-0000', 'address': 'NY, NY', 'salary': '352200'}]

# field names
fields = ['Sno', 'birth_date', 'first_name', 'last_name',
          'created_date', 'ssn', 'credit_card_number', 'address', 'salary']

with open('customers.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fields)
    writer.writeheader()
    writer.writerows(mydict)
