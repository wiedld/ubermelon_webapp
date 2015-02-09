from flask import Flask, request, session, render_template, g, redirect, url_for, flash, escape
import model
import jinja2
import os

app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'
app.jinja_env.undefined = jinja2.StrictUndefined

@app.route("/")
def index():
    """This is the 'cover' page of the ubermelon site"""
    return render_template("index.html")

@app.route("/melons")
def list_melons():
    """This is the big page showing all the melons ubermelon has to offer"""
    melons = model.get_melons()
    return render_template("all_melons.html",
                           melon_list = melons)

@app.route("/melon/<int:id>")
def show_melon(id):
    """This page shows the details of a given melon, as well as giving an
    option to buy the melon."""
    melon = model.get_melon_by_id(id)
    print melon
    # in session dict, have dict 'cart'  
    # values in dict cart are {id: [name,price]} 
    if 'cart' not in session:
        session['cart'] = {}
    session['cart'][melon.id]= list()
    session['cart'][melon.id].append(melon.common_name)
    session['cart'][melon.id].append(melon.price)
    return render_template("melon_details.html",
                  display_melon = melon)

@app.route("/cart")
def shopping_cart():
    """Display the contents of the shopping cart."""
    if 'cart' not in session:
        session['cart'] = {}
    list_of_subtotals = [session['cart'][melon][3] for melon in session['cart'] if len(session['cart'][melon])>2]
    order_total = sum(list_of_subtotals)
    order_total = "$%.2f" % order_total
    return render_template("cart.html", total=order_total)

@app.route("/add_to_cart/<int:id>")
def add_to_cart(id):
    """when a melon is added to a cart, redirect them to the
    shopping cart page, while displaying the message
    "Successfully added to cart" """
    ## in session dict, have dict 'cart'  
    # vvalues in dict cart are  {id: [name,price] } 
    # the code below adds tp the dict cart. {id(key): [common_name,price,qty,subtotal]}
    key = str(id)
    price_index = 1
    qty_index = 2
    subtotal_index = 3
    price = session['cart'][key][price_index]
    # see if there is any quantities add (a.k.a. is the list of values 2 or 4?)
    if len(session['cart'][key]) == 2:   
        session['cart'][key].append(1)     # add a qty of 1
        session['cart'][key].append(price*1)    # make the subtotal index exist
    else:
        session['cart'][key][qty_index] += 1
        qty = session['cart'][key][qty_index]
        session['cart'][key][subtotal_index] = qty * price 
    flash("Successfully added to cart.")
    return redirect("/cart")


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def process_login():
    """TODO: Receive the user's login credentials located in the 'request.form'
    dictionary, look up the user, and store them in the session."""
    #  test with emails in database:  amy@jaxworks.info, norma@realmix.com
    if 'login' not in session:
        session['login']={}
    user_email = request.form.get("email")
    pwd = request.form.get("password")
    customer = model.get_customer_by_email(user_email)
    email, f_name, l_name = customer[0],customer[1],customer[2]
    flash("Welcome " +f_name+ " " +l_name+ ".")
    return redirect("/melons")


@app.route("/checkout")
def checkout():
    """TODO: Implement a payment system. For now, just return them to the main
    melon listing page."""
    flash("Sorry! Checkout will be implemented in a future version of ubermelon.")
    return redirect("/melons")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
