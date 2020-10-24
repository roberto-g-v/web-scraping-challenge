# MongoDB and Flask Application

# Dependencies and Setup
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scrape_mars
import pymongo

# Flask Setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# PyMongo Connection Setup
client = pymongo.MongoClient()
db = client.mars_db
collection = db.mars_facts

# Root Route to Query MongoDB & Pass Mars Data Into HTML Template: index.html to Display Data
@app.route("/")
def index():
    Mars = mongo.db.Mars.find_one()
    return render_template("index.html", mars=Mars)


# Scrape Route to Import `scrape_mars.py` Script & Call `scrape` Function
@app.route("/scrape")
def scrapper():
    mars = mongo.db.Mars
    mars_app = scrape_mars.get_everything()
    mars.update({}, mars_app, upsert=True)
    return redirect("/", code=302)


# Define Main Behavior
if __name__ == "__main__":
    app.run(debug=True)