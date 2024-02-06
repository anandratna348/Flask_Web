import os
from flask import Flask, flash
from flask import request
from flask import redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydata.sqlite3"
db = SQLAlchemy(app)



class User(db.Model):
    id = db.Column(db.Integer, nullable=False, primary_key = True, autoincrement=True)
    username = db.Column(db.String, nullable = False)
    email = db.Column(db.String,nullable = False,unique = True)
    password = db.Column(db.String,nullable = False)

class Admin(db.Model):
    username = db.Column(db.String,primary_key = True, nullable = False)
    email = db.Column(db.String, nullable = False,  unique = True)
    password = db.Column(db.String, nullable = False)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    product_relation=db.relationship("Product",backref="category_relation", secondary="assosciation") 
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable = False)
    price_rate = db.Column(db.Float, nullable = False)
    manufacturer = db.Column(db.String(150), nullable=False)
    stock = db.Column(db.Integer,nullable = False)
    category_id=db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)

class Buy(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    product_id=db.Column(db.Integer, nullable=False)
    product_name=db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.Integer, nullable=False) 
    email = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    quantity = db.Column(db.Integer, nullable = False)
    total_amount=db.Column(db.Integer, nullable=False)

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    product_id=db.Column(db.Integer, db.ForeignKey("product.id"), nullable = False)
    product_name=db.Column(db.String, nullable=False)
    quantity=db.Column(db.Integer, nullable=False, default=1)
    price=db.Column(db.Integer, nullable=False,  default=0)

class Assosciation(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),primary_key = True, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"),primary_key = True,nullable = False)
class Ratings(db.Model):
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"),primary_key = True, nullable=False)
    ratings = db.Column(db.Integer,nullable = False)
    feedback = db.Column(db.String,nullable = False)

@app.route('/',methods = ["GET"])
def home():
    return render_template("home.html")

@app.route('/summary',methods = ["GET"])
def summary():
    return render_template("summary.html")

@app.route('/success',methods = ["GET"])
def success():
    if request.method == "GET":
        return render_template("success.html")

@app.route('/rate',methods = ["GET"])
def rate():
    if request.method == "GET":
        P = Product.query.all()
        return render_template("rating.html",getrating = P)

@app.route('/p/<id>',methods = ["GET"])
def sr(id):
    if request.method == "GET":
        return render_template("confirmation_product.html",k_id = id)

@app.route('/c/<id>',methods = ["GET"])
def category_x(id):
    if request.method == "GET":
        return render_template("confirmation_category.html",category_id = id)

@app.route('/rater/<p_id>',methods = ["GET"])
def rater(p_id):
    if request.method == "GET":
        P = Ratings.query.filter_by(product_id=p_id).all()
        list=[]
        for i in P:
            list.append(i.ratings)
        if len(list)==0:
            rate = None
        else:
            rate = sum(list)/len(list)

        return render_template("check_ratings.html",rate = rate)

@app.route('/ratings/<p_id>',methods = ["GET","POST"])
def ratings(p_id):
    if request.method == "GET":
        return render_template("ratings.html")
    elif request.method=="POST":
        a = p_id
        b = request.form["rating"]
        c = request.form["feedback"]
        v = Ratings(product_id = a,ratings = b,feedback =c)
        db.session.add(v)
        db.session.commit()
        return redirect("/rate")
@app.route('/out_of_stock',methods = ["GET"])
def out_of_stock():
    if request.method == "GET":
        return render_template("out_of_stock.html")


@app.route('/unsuccessful',methods = ["GET"])
def unsuccess():
    if request.method == "GET":
        return render_template("unsuccessful.html")

@app.route('/user_dashboard',methods = ["GET"])
def user_dashboard():
    if request.method == "GET":
        return render_template("user_dashboard.html")

@app.route('/admin_dashboard',methods = ["GET"])
def admin_dashboard():
    if request.method == "GET":
        y = Category.query.all()
        v = Product.query.all()
        return render_template("admin_dashboard.html",  category_list = y, product_list = v)
@app.route('/category_list',methods = ['GET'])
def category_list():
    if request.method == "GET":
        y = Category.query.all()
        return render_template("category.html",getcategory = y)
    
@app.route('/category_admin_list',methods = ['GET'])
def category_list_good():
    if request.method == "GET":
        y = Category.query.all()
        return render_template("category_admin.html", getcategory = y)
    
@app.route('/category_details/<c_id>/goods',methods = ['GET'])
def category_list_1(c_id):
    if request.method == "GET":
        y = Category.query.filter_by(id=c_id).all()
        return render_template("category_details.html",getg = y)

@app.route('/category_product_list',methods = ['GET'])
def category_product_list():
    if request.method == "GET":
        y = Category.query.all()
        v = Product.query.all()
        return render_template("category_product_list.html",getcategory = y,getproduct = v)
    
@app.route('/cr',methods = ['GET'])
def cr():
    if request.method == "GET":
        y = Category.query.all()
        v = Product.query.all()
        return render_template("c_r.html",getcategory = y,getproduct = v)

@app.route('/buying/<product_id>/', methods=["GET","POST"])
def buying(product_id):
    if request.method == "POST":
        x = Cart.query.filter_by(product_id=product_id).first()
        a = request.form["name"]
        b = request.form["email"]
        c = request.form["mobile"]
        d = request.form["address"]
        e =  product_id
        f= x.product_name
        g = x.price
        h = x.quantity
        data = Buy(product_id = e , product_name=f, name = a, mobile = c, email = b, address = d, quantity=h,total_amount=g)
        db.session.add(data)
        db.session.commit()
        Cart.query.filter_by(product_id=e).delete()
        db.session.commit()
        return redirect('/buy')
    elif request.method == "GET":
        return render_template("buy.html")
    
@app.route('/signup',methods = ["GET","POST"])
def signup():
    if request.method == "POST":
        a = request.form['username']
        b = request.form['password']
        c = request.form['email']
        user_record = User(username=a, email=c, password=b)
        y = User.query.all()
        l = []
        for i in y:
            l.append(i.username)
        if a in l:
            return ('/')
        else:
            db.session.add(user_record)
            db.session.commit()
            return redirect('/success')
    elif request.method == "GET":
        return render_template("signup.html")
    else:
        return redirect('/')
@app.route('/admin_register', methods = ['GET', 'POST'])
def admin_register():
    if request.method == "POST":
        a = request.form['username']
        b = request.form['email']
        c = request.form['password']
        admin_record = Admin(username=a, email=b, password=c)
        y = Admin.query.all()
        l = []
        for i in y:
            l.append(i.username)
        if a in l:
            return('/')
        else:
            db.session.add(admin_record)
            db.session.commit()
            return redirect('/success')
    elif request.method == "GET":
        return render_template("admin_register.html")
    else:
        return redirect('/')

@app.route('/buy',methods=["GET"])
def buyer():
    y = Buy.query.all()
    return render_template("purchased.html", get_purchased_product = y)
 
@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    elif request.method == "POST":
        a = request.form['username']
        b = request.form['password']
        user = User.query.filter_by(username=a).first()
        if b == user.password:
            return redirect('/user_dashboard')
        else:
            return redirect('/')
    

@app.route('/admin_login', methods = ["GET","POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin_login.html")
    elif request.method == "POST":
        a = request.form['username']
        b = request.form['password']
      #  y = Admin.query.all()
        admin_user = Admin.query.filter_by(username=a).first()
        if b==admin_user.password:
            return redirect('/admin_dashboard')
        else:
            return redirect('/')
        

@app.route('/add_category', methods=['GET', 'POST'])
def add_category():
    if request.method == 'POST':
        name = request.form['name']
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        return redirect('/add_category')
    elif request.method == "GET":
        return render_template("add_category.html")
    

@app.route('/add_to_cart/<id>/', methods=["GET","POST"])
def add_to_cart(id):
    if request.method == "POST":
        b = request.form["quantity"]
        x = Product.query.filter_by(id=id).first()
        if int(x.stock)>int(b):
            y=int(x.price_rate)*int(b)
            z=x.name
            data = Cart(user_id=id, product_id = id, product_name=z, quantity=b, price=y)
            db.session.add(data)
            db.session.commit()
            d = int(x.stock) - int(b)
            Product.query.filter_by(id=id).update({'stock':d})
            db.session.commit()
            return redirect('/category_product_list') 
        else:
            return redirect('/out_of_stock')
    elif request.method == "GET":
        return render_template("add_to_cart.html")
    
@app.route('/remove/<product_id>/', methods=["GET"])
def remove(product_id):
    Cart.query.filter_by(product_id=product_id).delete()
    db.session.commit()
    return redirect('/cart')
    #elif request.method == ["GET"]:
     #   return render_template("remove_product_in_cart.html")
         
    
@app.route('/cart', methods=["GET"])
def my_cart():
    y = Cart.query.all()
    return render_template("my_cart.html", cart_added_product = y)
 

@app.route('/category/<cat_id>/delete', methods = ['GET', 'POST'])
def delete(cat_id):
    Category.query.filter_by(category_id = cat_id).delete()
    db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/category/<c_id>/edit',methods = ["GET","POST"])
def edit_catgeory(c_id):
    if request.method =='GET':
        return render_template('edit_category.html')
    elif request.method == 'POST':
        name = request.form['name']
        id = c_id
        Category.query.filter(Category.id==c_id).update({'id':id,'name':name})
        db.session.commit()
        return redirect('/admin_dashboard')
    
@app.route('/add_product/', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price_rate = request.form['price_rate']
        manufacturer = request.form['manufacturer']
        stock = request.form['stock']
        category_id = request.form['category_id']
        v =Category.query.filter_by(id = category_id).first()
        product = Product(name = name, description = description, price_rate = price_rate, manufacturer = manufacturer, stock=stock, category_id = category_id)
        db.session.add(product)
        db.session.commit()
        p = Product.query.filter_by(name = name, description = description, price_rate = price_rate, category_id = category_id).first()
        cr = Assosciation.query.filter_by(category_id = category_id, product_id=p.id).first()
        if cr is  None:
             assos = Assosciation( category_id = category_id)
             db.session.add(assos)
             db.session.commit()
        return redirect('/admin_dashboard')
    elif request.method == "GET":
        return render_template("add_product.html")

@app.route('/product/<p_id>/edit',methods = ["GET","POST"])
def edit_product(p_id):
    if request.method =='GET':
        return render_template('edit_product.html')
    elif request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price_rate = request.form['price_rate']
        manufacturer = request.form['manufacturer']
        stock = request.form['stock']
        category_id = request.form['category_id']
        Product.query.filter(Product.id==p_id).update({'id':p_id,'name':name, 'description':description, 'manufacturer':manufacturer, 'price_rate':price_rate, 'stock':stock, 'category_id':category_id})
        db.session.commit()
        return redirect('/admin_dashboard')

@app.route('/product/<k_id>/delete', methods = ['GET', 'POST'])
def deleting(k_id):
    Product.query.filter_by(id = k_id).delete()
    db.session.commit()
    Assosciation.query.filter_by(product_id = k_id).delete()
    db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/visit_product/<c_id>', methods = ['GET', 'POST'])
def products(c_id):
    if request.method=="GET":
        a = Product.query.filter_by(category_id = c_id).all()
        return render_template('category_product_list.html', getproduct = a)
    
@app.route("/search_op",methods=["GET","POST"])
def search_op():
    if request.method == "GET":
        return render_template("search_op.html")
    elif request.method=="POST":
        a = request.form["search"]
        a1 = Category.query.filter(Category.name.ilike("%"+a+"%")).all()
        return render_template("search_results.html",result = a1)

@app.route("/search_cp",methods=["GET","POST"])
def search_cp():
    if request.method == "GET":
        return render_template("search_op.html")
    elif request.method=="POST":
        a = request.form["search"]
        a1 = Product.query.filter(Product.name.ilike("%"+a+"%")).all()
        return render_template("search_results.html",result = a1)
@app.route("/search_manufacturer",methods=["GET","POST"])
def manufacturer():
    if request.method == "GET":
        return render_template("manufacturer.html")
    elif request.method=="POST":
        a = request.form["search"]
        a1 = Product.query.filter(Product.manufacturer.ilike("%"+a+"%")).all()
        return render_template("search_results.html",result = a1)
if __name__=="__main__":
    app.run(debug = True)