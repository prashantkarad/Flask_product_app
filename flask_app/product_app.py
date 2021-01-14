from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask import Flask,render_template,request

app=Flask(__name__)

import pymysql

#app.config['SQLALCHEMY_DATABASE_URI']="postgresql+psycopg2://postgres:prashant@localhost/product_db" #3306
app.config['SQLALCHEMY_DATABASE_URI']="mysql+pymysql://root:prashant@localhost/product_db"  #5432
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
#app.config['SQLALCHEMY_ECHO']=True
db=SQLAlchemy(app)


class products(db.Model):
    pid = db.Column('prod_Id', db.Integer(),primary_key=True)
    pname=db.Column('prod_Name',db.String(100))
    pqty = db.Column('prod_Qty', db.Integer())
    pprice=db.Column('prod_price',db.Integer())
    pcat=db.Column('Prod_cat',db.String(25))
    pvendor=db.Column('Prod_vendor',db.String(25))
    created = db.Column('created', db.DateTime,default=db.func.current_timestamp())  # date type --> when this record added into db
    updated = db.Column('updated', db.DateTime, default=db.func.current_timestamp(),onupdate=db.func.current_timestamp())  # date type --> when last time updated
    created_by = db.Column('created_by', db.Integer(), default=0)  # who created
    updated_by = db.Column('updated_by', db.Integer(), default=0)  # who last time updated


    def __str__(self):
        return f'''
            Product Id:{self.pid}
            Product Name: {self.pname}
            Product Quantity: {self.pqty}
            Product Price :{self.pprice}
            Product category :{self.pcat}
            Product Vendor: {self.pvendor}
            product Created :{self.created}
            product Updated :{self.updated} '''

    def __repr__(self):
        return str(self)




class dbormimplementation():

    def get_dummy_product(self):
        return products(pid=0,pname=0,pqty=0,pprice=0,pcat=0,pvendor=0)

    def Add_product(self,prod):
        if type(self.get_prod(prod.pid)) == products:
            return self.update_product(prod)
        else:
            db.session.add(prod)
            db.session.commit()
            return "Product added successfully"


    def delete_product(self,prid):
        prod=self.get_prod(prid)
        try:
            if type(prod)==products:
                db.session.delete(prod)
                db.session.commit()
                return "product deleted successfully"
        except:
            print("product cannot be deleted")

        return "product Not found"

    def update_product(self,user_given_prod):
        prod=self.get_prod(user_given_prod.pid)

        if type(prod)==products:
            prod.pname=user_given_prod.pname
            prod.pqty=user_given_prod.pqty
            prod.pprice=user_given_prod.pprice
            prod.pcat=user_given_prod.pcat
            prod.pvendor=user_given_prod.pvendor
            db.session.commit()
            print("Product Updated Successfully...")
        else:
            print("product not availabe,Cannot Update")

    def get_prod(self,prid):

            prod = products.query.filter_by(pid=prid).first()
            return prod


    def get_all_products(self):
        return products.query.all()



dbop = dbormimplementation()
msg=' '

@app.route("/",methods=['GET'])
def welcome():
    return render_template('product.html',prodlist=dbop.get_all_products(),resp=msg,prod='')


@app.route("/persist/",methods=['Post'])
def add_edit_product_info():
    formdata=request.form
    prod=products(pid=formdata.get('proid'),
                  pname=formdata.get('proname'),
                  pqty=formdata.get('proqty'),
                  pprice=formdata.get('proprice'),
                  pcat=formdata.get('procat'),
                  pvendor=formdata.get('provendor'))
    msg=dbop.Add_product(prod)
    return render_template('product.html',prodlist=dbop.get_all_products(),resp=msg,prod='')


@app.route("/edit/<int:pid>",methods=['GET'])       ##http://localhost:5000/edit/101 --GET -->pathvariable
def edit_product_info(pid):

    return render_template('product.html',prodlist = dbop.get_all_products(),prod = dbop.get_prod(pid),resp=msg)

@app.route("/delete/<int:pid>",methods=['GET']) #http://localhost:5000/delete/101 --GET
def delete_product_info(pid):
    msg = dbop.delete_product(pid)
    return render_template('product.html',prodlist = dbop.get_all_products(),prod=dbop.get_dummy_product(),resp=msg)

if __name__=='__main__':
    app.run(debug=True,port=5000)