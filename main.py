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
    customerID = requestdata["id"]
    newEmail = requestdata["email"]
    
    query3 = "UPDATE customer SET email = '%s' WHERE id = %s" % (newEmail, customerID)
    execute_query(conn, query3)
    
    return jsonify({"message": "customer email updated successfully"})

@app.route('/api/Customer/delete', methods=['DELETE']) #delete a book by id DELETE
def customer_delete():
    request_data = request.get_json()
    delete_id = request_data.get['id']
    query7 = "SELECT id FROM Customer WHERE id = %s" % (delete_id) 
    customer = execute_read_query(conn,query7)
    if not customer: #check if valid id
        return jsonify({"error": "Invalid ID"})
    else:
        delete_query = f"DELETE FROM Customer WHERE id = {delete_id}"
        execute_query(conn, delete_query)
    
    return "delete request successful"











app.run()