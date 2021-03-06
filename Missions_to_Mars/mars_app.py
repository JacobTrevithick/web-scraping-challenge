from flask import Flask, render_template, redirect
from pymongo.mongo_client import MongoClient
# import pymongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")

mars_db = client['mars_db']

facts_collection = mars_db.facts

# Route to render index.html template using data from Mongo
@app.route("/")
def home():

    # Find one record of data from the mongo database
    
    # Attempt to find the latest record in the mongodb
    try:
        # Fails if first time through script since mars_db would be empty
        facts_data = facts_collection.find().sort('_id', -1).limit(1)[0]
    
    # Redirects to /scrape to populate the first document in database
    except:
        return redirect("/scrape")
    

    return render_template("index.html", facts=facts_data)
   

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    # Run the scrape function and save the results to a variable
    item = scrape_mars.scrape()

    # Update the Mongo database using update and upsert=True
    facts_collection.insert_one(item)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)