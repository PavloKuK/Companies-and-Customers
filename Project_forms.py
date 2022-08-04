from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, FloatField, SelectMultipleField, SelectField
from wtforms.validators import InputRequired, Length

import Project_define as pk_db

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind = pk_db.engine)
session = Session()

company_list = session.query(pk_db.Company).all()
company_choices = []
for item in company_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}".format(item.name))
   my_tuple = tuple(mylist)
   company_choices.append(my_tuple)

product_list = session.query(pk_db.Product).all()
product_choices = []
for item in product_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}".format(item.name))
   my_tuple = tuple(mylist)
   product_choices.append(my_tuple)

customer_list = session.query(pk_db.Customer).all()
customer_choices = []
for item in customer_list:
   mylist=[]
   mylist.append(str(item.id))
   mylist.append("{}".format(item.name))
   my_tuple = tuple(mylist)
   customer_choices.append(my_tuple)

class Sold_To(FlaskForm):
   customer_id = SelectField("Customer", choices = customer_choices)
   product_id = SelectMultipleField("Product", choices = product_choices)
   submit = SubmitField("Add sell")

class Delete_Customer(FlaskForm):
   customer_id = SelectField("Customer ", choices = customer_choices)   
   submit = SubmitField("Delete Customer")
