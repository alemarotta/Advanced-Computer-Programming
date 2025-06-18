from flask import Flask,request
from pymongo import MongoClient

app=Flask(__name__)
def get_database():
    uri="mongodb://localhost:27017/"
    client=MongoClient(uri)
    return client["db"]

@app.post("/update_booking")
def update_booking():
    db = get_database()
    collection = db["booking_collection"]

    request_message = request.get_json()

    operator = request_message["operator"]


    list_of_bookings = list(collection.find({
        "operator":operator, 
        "nights": {"$gte": request_message["nights"]}
        }))
    for booking in list_of_bookings:
        current_price = booking["cost"]
        new_price = current_price-request_message["discount"]
        if new_price < 0:
            new_price = 0
        try:
            collection.update_one(
                booking,
                {"$set":{"cost":new_price}}
            )
        except Exception as e:
            print("[DBSERVER] Something went wrong while updating")
            return "Fail", 500
    return "ACK", 200

@app.put("/create_booking")
def create_booking():
    db = get_database()
    collection = db["booking_collection"]

    request_message = request.get_json()
    try:
        collection.insert_one(request_message)
        print("[DBSERVER] Added")
    except Exception as e:
        print("[DBSERVER] Operation failed")
        return "Fail-"+str(e), 500
    else:
        print("[DBSERVER] Booking insert correctly")
        return "ACK", 200
        
    
    
if __name__=="__main__":
   app.run(port=5001,debug=True)