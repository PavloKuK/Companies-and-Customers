from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///products.db?check_same_thread=False')
Base = declarative_base()

customers_and_products = Table('customers_and_products', Base.metadata,
    Column('customer_id', Integer, ForeignKey('customer.id')),
    Column('product_id', Integer, ForeignKey('product.id'))
)

companies_and_products = Table('companies_and_products', Base.metadata,
    Column('company_id', Integer, ForeignKey('company.id')),
    Column('product_id', Integer, ForeignKey('product.id'))
)

class Company(Base):
   __tablename__ = 'company'
   
   id = Column(Integer, primary_key=True)
   name = Column(String)
   headquarters = Column(String)
   CEO = Column(String)
   revenue = Column(Float)
   num_of_employees = Column(Float)
   sells = relationship("Product", secondary = companies_and_products, viewonly=True)

class Product(Base):
   __tablename__ = 'product'
   
   id = Column(Integer, primary_key=True)
   name = Column(String)
   release_date = Column(String)
   price = Column(Float)
   company_id = Column(Integer, ForeignKey('company.id'))
   bought_by = relationship("Customer", secondary = customers_and_products, viewonly=True)
   sells_at = relationship("Company", secondary = companies_and_products, viewonly=True)

class Customer(Base):
   __tablename__ = 'customer'

   id = Column(Integer, primary_key=True)
   name = Column(String)
   cardNumber = Column(Integer)
   city = Column(String)
   date = Column(String)
   bought = relationship("Product", secondary = customers_and_products, viewonly=True)

Base.metadata.create_all(engine)