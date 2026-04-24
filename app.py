# Flask + all routes

import json
from flask import Flask, render_template, request, jsonify
from models import Property

app = Flask(__name__)

DATA_FILE = "C:\\Users\\DELL\\Desktop\\Evista\\data\\properties.json"

# Reads all properties from the JSON file and returns a list of objects
def load_properties():
    with open(DATA_FILE, "r") as f:
        raw_list = json.load(f)

    properties = []
    for item in raw_list:
        prop = Property(
            prop_id=item["prop_id"],
            title=item["title"],
            price=item["price"],
            area=item["area"],
            prop_type=item["prop_type"],
            bedrooms=item["bedrooms"],
            bathrooms=item["bathrooms"],
            image_url=item["image_url"]
        )
        prop.listed_at = item["listed_at"]  # Restore the original listing date
        properties.append(prop)

    return properties

# Move property objects to the JSON file
def save_properties(properties):
    with open(DATA_FILE, "w") as f:
        # Convert each Property object to a dict before saving
        json.dump([p.to_dict() for p in properties], f, indent=4)


# Routes
# homepage 
@app.route("/")
def home():
    properties = load_properties()
    # Show only the first 4 as featured (slicing a list)
    featured = properties[:4]
    return render_template("index.html", properties=featured)

# filter page
@app.route("/search")
def search():
    area = request.args.get("area", "").strip()
    prop_type = request.args.get("type", "").strip()
    max_price_str = request.args.get("max_price", "").strip()

    # Validate max_price input
    max_price = None
    if max_price_str:
        try:
            max_price = int(max_price_str)
        except ValueError:
            max_price = None  # ignore bad input

    all_properties = load_properties()
    results = []

    # Filter loop
    for prop in all_properties:
        if prop.matches_filter(area=area, prop_type=prop_type, max_price=max_price):
            results.append(prop)

    return render_template(
        "search.html",
        properties=results,
        selected_area=area,
        selected_type=prop_type,
        selected_price=max_price_str
    )

# full details for each property
@app.route("/property/<int:prop_id>")
def property_detail(prop_id):
    """Property detail page — shows full info for one property."""
    all_properties = load_properties()
    found = None

    for prop in all_properties:
        if prop.prop_id == prop_id:
            found = prop
            break

    # If property doesn't exist, 404 page --> will be resolved later
    if not found:
        return render_template("404.html"), 404

    return render_template("property.html", property=found)

# add new property page with form
@app.route("/add-property", methods=["GET", "POST"])
def add_property():
    if request.method == "POST":
        # Read text inputs from the form
        title = request.form.get("title", "").strip()
        area = request.form.get("area", "").strip()
        prop_type = request.form.get("prop_type", "").strip()

        # Validate and convert numeric inputs
        try:
            price = int(request.form.get("price", 0))
            bedrooms = int(request.form.get("bedrooms", 1))
            bathrooms = int(request.form.get("bathrooms", 1))
        except ValueError:
            return render_template("add_property.html", error="Please enter valid numbers for price, bedrooms, and bathrooms.")

        if not title or not area or not prop_type:
            return render_template("add_property.html", error="All fields are required.")

        # Load current list
        all_properties = load_properties()
        new_id = max([p.prop_id for p in all_properties], default=0) + 1

        # Instantiate the Property class 
        new_prop = Property(
            prop_id=new_id,
            title=title,
            price=price,
            area=area,
            prop_type=prop_type,
            bedrooms=bedrooms,
            bathrooms=bathrooms,
            image_url="https://images.unsplash.com/photo-1560448204-e02f11c3d0e2?w=400"
        )

        # Use a method on the object
        summary = new_prop.get_summary()

        # Save to file
        all_properties.append(new_prop)
        save_properties(all_properties)

        return render_template("add_property.html", success=f"Property added! {summary}")

    return render_template("add_property.html")


if __name__ == "__main__":
    app.run(debug=True)