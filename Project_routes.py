import Project_define as pk_db
import json
from Project_forms import Delete_Customer

from sqlalchemy.orm import sessionmaker

from Project_forms import Sold_To
from flask import Flask, render_template, url_for, request, redirect

Session = sessionmaker(bind = pk_db.engine)
session = Session()

query = session.query(pk_db.Company)
results = query.all()
result_dict = [u.__dict__ for u in results]

query2 = session.query(pk_db.Product)
results2 = query2.all()
result_dict2 = [u.__dict__ for u in results2]

query3 = session.query(pk_db.Customer)
results3 = query3.all()
result_dict3 = [u.__dict__ for u in results3]
   
app = Flask(__name__)

app.config["SECRET_KEY"] = 'Car'

@app.route("/")
def myredirect():
   return redirect(url_for('company_datatable'))

@app.route('/company_datatable')
def company_datatable():
    return render_template('company_datatable.html', title = "Company", header = "Company", companies = result_dict)

@app.route('/product_table')
def product_table():
    return render_template('product_table.html', title = "Company", header = "Company", products = result_dict2)

@app.route('/customer_datatable')
def customer_datatable():
    return render_template('customer_datatable.html', title = "Customer", header = "Customer", customers = result_dict3)

@app.route('/customer_delete', methods = ['GET', 'POST'])
def customer_delete():
   form = Delete_Customer()

   if form.validate_on_submit():
      result = request.form
      
      customer_to_delete = session.query(pk_db.Customer).get(int(result["customer_id"]))
      print("Going to delete")
      print(customer_to_delete.name)
      session.delete(customer_to_delete)
      session.commit()

      query3 = session.query(pk_db.Customer)
      results3 = query3.all()
      result_dict3 = [u.__dict__ for u in results3]
      
      return render_template('customer_datatable.html', title = "After Deletion", header = "After Deletion", customers = result_dict3)

   return render_template('customer_delete.html', title = "Delete Customer Form", header="Delete Customer Form", form = form)

@app.route('/sold_to', methods=['GET', 'POST'])
def sold_to():
   form = Sold_To()

   if form.validate_on_submit():
      result = request.form

      for customer_id in result.getlist("customer_id"):
         for product_id in result.getlist("product_id"):
            session.execute(pk_db.customers_and_products.insert().values([(customer_id, product_id)]))
      session.commit()

      return render_template('sold_to_after.html', title = "Sold", header = "Sold", result = result)

   return render_template('sold_to.html', title = "Sell to", header = "Sell to", form = form)

@app.route('/company_api')
def company_api():
   for item in result_dict:
      item.pop("_sa_instance_state", None)
   return json.dumps(result_dict)

@app.route('/product_api')
def product_api():
   for item in result_dict2:
      item.pop("_sa_instance_state", None)
   return json.dumps(result_dict2)

@app.route('/customer_api')
def customer_api():
   for item in result_dict3:
      item.pop("_sa_instance_state", None)
   return json.dumps(result_dict3)

if __name__ == "__main__":
   app.run(debug=True)  
