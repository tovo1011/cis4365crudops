import mysql.connector
import credentials
import flask
from flask import jsonify
from flask import request
from mysql.connector import Error
from sqlstuffs import create_connection
from sqlstuffs import execute_query 
from sqlstuffs import execute_read_query

#creating connection to mysql db
myCreds = credentials.Credentials()
conn = create_connection(myCreds.constring, myCreds.username,myCreds.password, myCreds.dbname)

app = flask.Flask(__name__)#sets up app
app.config["debug"] = True 

@app.route("/api/Customer", methods = ["GET"])
def getAllCustomers():
    query = "SELECT * FROM Customer"
    result = execute_read_query(conn, query)
    return jsonify(result)

@app.route("/api/Customer/add", methods = ["POST"])
def addOneCustomer():
    requestdata = request.get_json()
    name = requestdata["name"]
    email = requestdata["email"]
    
    
    query2 = "INSERT INTO Customer (name, email) VALUES ('%s', '%s')" % (name, email)
    execute_query(conn, query2)
    return jsonify({"message": "added a customer!"}), 201

@app.route("/api/Customer/updateEmail", methods = ["PUT"])
def updateCustomer():
    requestdata = request.get_json()
    custid = requestdata["customer_id"]

    newEmail = requestdata["email"]
    
   
    if not custid: #check if valid id
        return jsonify({"error": "Invalid email"})
    else:
        query3 = "UPDATE Customer SET email = '%s' WHERE customer_id = %s" % (newEmail, custid)
        execute_query(conn, query3)
    
    return "delete request successful"
    
    
    
    return jsonify({"message": "customer email updated successfully"})

@app.route('/api/Customer/delete', methods=['DELETE'])
def customer_delete():
    request_data = request.get_json()
    delete_id = request_data['customer_id']

    if not delete_id:  # check if valid id
        return jsonify({"error": "Invalid ID"})
    else:
        # Delete related rows in the Order table
        delete_orders_query = f"DELETE FROM `Order` WHERE customer_id = {delete_id}"
        execute_query(conn, delete_orders_query)

        # Delete the customer
        delete_query = f"DELETE FROM Customer WHERE customer_id = {delete_id}"
        execute_query(conn, delete_query)

    return jsonify({"message": "Customer and related orders deleted successfully"})











app.run()