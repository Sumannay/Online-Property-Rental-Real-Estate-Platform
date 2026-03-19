from flask import Flask, render_template, request, redirect, session, flash
from model import db, User, Property, Favorite, Booking
import os
import re

app = Flask(__name__)
app.secret_key = "secret123"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

db.init_app(app)

with app.app_context():
    db.create_all()


# ---------------- HOME PAGE ----------------
@app.route("/", methods=["GET", "POST"])
def index():

    search = request.form.get("search")
    type_filter = request.form.get("type")

    query = Property.query

    if search:
        query = query.filter(Property.location.contains(search))

    if type_filter:
        query = query.filter_by(property_type=type_filter)

    properties = query.all()

    return render_template("index.html", properties=properties)


# ---------------- PROPERTY DETAIL ----------------
@app.route("/property/<int:id>")
def property_detail(id):
    property = Property.query.get(id)
    return render_template("property_detail.html", property=property)


# ---------------- REGISTER ----------------
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        user = User(
            name=request.form["name"],
            email=request.form["email"],
            password=request.form["password"]
        )

        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please Login", "success")
        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = User.query.filter_by(
            email=request.form["email"],
            password=request.form["password"]
        ).first()

        if user:
            session["user"] = user.id
            flash("Login Successful", "success")
            return redirect("/dashboard")
        else:
            flash("Invalid Email or Password", "danger")

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/login")

    properties = Property.query.all()
    return render_template("dashboard.html", properties=properties)


# ---------------- ADD PROPERTY ----------------
@app.route("/add", methods=["GET", "POST"])
def add_property():

    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":

        title = request.form["title"]
        location = request.form["location"]
        price = request.form["price"]
        description = request.form["description"]
        contact = request.form["contact_number"]
        property_type = request.form.get("property_type")

        # ✅ VALIDATION
        if not price.isdigit():
            flash("❌ Price must be numbers only", "danger")
            return redirect("/add")

        if not re.fullmatch(r"\d{10}", contact):
            flash("❌ Contact must be 10 digits", "danger")
            return redirect("/add")

        if not re.fullmatch(r"[A-Za-z ]+", location):
            flash("❌ Location must contain only letters", "danger")
            return redirect("/add")

        if property_type not in ["sell", "rent"]:
            flash("❌ Please select property type", "danger")
            return redirect("/add")

        image = request.files["image"]
        image2 = request.files.get("image2")
        image3 = request.files.get("image3")

        filename = ""
        filename2 = ""
        filename3 = ""

        if image and image.filename:
            filename = image.filename
            image.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if image2 and image2.filename:
            filename2 = image2.filename
            image2.save(os.path.join(app.config['UPLOAD_FOLDER'], filename2))

        if image3 and image3.filename:
            filename3 = image3.filename
            image3.save(os.path.join(app.config['UPLOAD_FOLDER'], filename3))

        new_property = Property(
            title=title,
            location=location,
            price=price,
            description=description,
            contact_number=contact,
            property_type=property_type,   # ✅ NEW FEATURE
            image=filename,
            image2=filename2,
            image3=filename3
        )

        db.session.add(new_property)
        db.session.commit()

        flash("Property Added Successfully!", "success")
        return redirect("/dashboard")

    return render_template("add_property.html")


# ---------------- EDIT PROPERTY ----------------
@app.route("/edit_property/<int:id>", methods=["GET", "POST"])
def edit_property(id):

    if "user" not in session:
        return redirect("/login")

    property = Property.query.get(id)

    if not property:
        flash("Property not found", "danger")
        return redirect("/dashboard")

    if request.method == "POST":

        location = request.form["location"]
        price = request.form["price"]
        contact = request.form["contact_number"]
        property_type = request.form.get("property_type")

        # ✅ VALIDATION
        if not price.isdigit():
            flash("❌ Price must be numbers only", "danger")
            return redirect(f"/edit_property/{id}")

        if not re.fullmatch(r"\d{10}", contact):
            flash("❌ Contact must be 10 digits", "danger")
            return redirect(f"/edit_property/{id}")

        if not re.fullmatch(r"[A-Za-z ]+", location):
            flash("❌ Location must contain only letters", "danger")
            return redirect(f"/edit_property/{id}")

        if property_type not in ["sell", "rent"]:
            flash("❌ Please select property type", "danger")
            return redirect(f"/edit_property/{id}")

        property.title = request.form["title"]
        property.location = location
        property.price = price
        property.description = request.form["description"]
        property.contact_number = contact
        property.property_type = property_type   # ✅ NEW

        db.session.commit()

        flash("Property Updated Successfully!", "success")
        return redirect("/dashboard")

    return render_template("edit_property.html", property=property)


# ---------------- DELETE PROPERTY ----------------
@app.route("/delete_property/<int:id>")
def delete_property(id):

    if "user" not in session:
        return redirect("/login")

    property = Property.query.get(id)

    if not property:
        flash("Property not found", "danger")
        return redirect("/dashboard")

    db.session.delete(property)
    db.session.commit()

    flash("Property Deleted Successfully!", "info")
    return redirect("/dashboard")


# ---------------- FAVORITE ----------------
@app.route("/favorite/<int:id>")
def favorite(id):

    if "user" not in session:
        return redirect("/login")

    fav = Favorite(
        user_id=session["user"],
        property_id=id
    )

    db.session.add(fav)
    db.session.commit()

    return redirect("/favorites")


# ---------------- FAVORITES ----------------
@app.route("/favorites")
def favorites():

    if "user" not in session:
        return redirect("/login")

    favs = Favorite.query.filter_by(user_id=session["user"]).all()
    properties = [Property.query.get(f.property_id) for f in favs]

    return render_template("favorites.html", properties=properties)


# ---------------- BOOK ----------------
@app.route("/book/<int:id>")
def book(id):

    if "user" not in session:
        return redirect("/login")

    property = Property.query.get(id)

    booking = Booking(
        user_id=session["user"],
        property_id=id
    )

    property.status = "sold"

    db.session.add(booking)
    db.session.commit()

    return redirect("/bookings")


# ---------------- BOOKINGS ----------------
@app.route("/bookings")
def bookings():

    if "user" not in session:
        return redirect("/login")

    bookings = Booking.query.filter_by(user_id=session["user"]).all()
    properties = [Property.query.get(b.property_id) for b in bookings]

    return render_template("bookings.html", properties=properties)


# ---------------- ADMIN ----------------
@app.route("/admin")
def admin():

    users = User.query.all()
    properties = Property.query.all()

    return render_template("admin.html", users=users, properties=properties)


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)
    flash("Logged out successfully", "info")

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)