import Project_define as pk_db

from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind = pk_db.engine)
session = Session()

import json
import os
os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('static/data/company_data.json') as file:
   comp = json.load(file)

for i, companies in enumerate(comp["companies"]):
   company = pk_db.Company(name = companies["name"], headquarters = companies["headquarters"], 
   CEO = companies["CEO"], revenue = companies["revenue"], 
   num_of_employees = companies["num_of_employees"]) 
   session.add(company)
   session.flush()  
   
   for j, products in enumerate(comp["companies"][i]["products"]):
      product = pk_db.Product(name = products["name"], release_date = products["release_date"], 
      price = products["price"])
      product.company_id = company.id
      session.add(product)

session.commit()

customer1 = pk_db.Customer(name = "Dwayne Morton", cardNumber = 2100, city = "New York", date = "05/26/2021")
session.add(customer1)
customer2 = pk_db.Customer(name = "Johanna Carson", cardNumber = 1299, city = "Boston", date = "01/15/2019")
session.add(customer2)
customer3 = pk_db.Customer(name = "Brandy Martin", cardNumber = 6955, city = "Seattle", date = "09/13/2020")
session.add(customer3)
customer4 = pk_db.Customer(name = "Antonia Hill", cardNumber = 6999, city = "Denver", date = "12/08/2022")
session.add(customer4)
session.commit()
session.flush()

# Dwayne Morton
session.execute(pk_db.customers_and_products.insert().values([(1, 2), (1, 6), (1, 7)]))
session.commit()

# Johanna Carson
session.execute(pk_db.customers_and_products.insert().values([(2, 8), (2, 4)]))
session.commit()

# Brandy Martin
session.execute(pk_db.customers_and_products.insert().values([(3, 13)]))
session.commit()

# Antonia Hill
session.execute(pk_db.customers_and_products.insert().values([(4, 12), (4, 2)]))
session.commit()


# Best Buy
session.execute(pk_db.companies_and_products.insert().values([(1, 1), (1, 2), (1, 3), (1, 4), (1, 6), (1, 7), (1, 8), (1, 12)]))
session.commit()

# Target
session.execute(pk_db.companies_and_products.insert().values([(2, 2), (2, 2), (2, 3), (2, 5), (2, 9), (2, 10), (2, 11), (2, 13)]))
session.commit()

# Walmart
session.execute(pk_db.companies_and_products.insert().values([(3, 1), (3, 4), (3, 3), (3, 5), (3, 10), (3, 7), (3, 11), (1, 12)]))
session.commit()


companies = session.query(pk_db.Company).all()
for company in companies:
   print("Name = {}, headquarters = {}, CEO = {}, revenue = {}, number of employees = {}".format(company.name, company.headquarters, company.CEO, company.revenue, company.num_of_employees))

print("\n")

customer = session.query(pk_db.Customer).first()
print("{} bought the following items:".format(customer.name))
for product in customer.bought:
   print(product.name)
