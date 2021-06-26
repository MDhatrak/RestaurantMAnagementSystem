from flask import Flask
from pymongo import MongoClient
from flask import request
from menu_management.menu_management import MenuManagement
from table_management.table_management import TableManagement
from order_management.order_management import OrderManagement
from customer_details.cust_info import CustomerInformation

app = Flask(__name__)
mongo_client = MongoClient(host='localhost', port=27017)
db = mongo_client.restaurant_management

#API to get list of menu items
@app.route('/get-menu', methods=['GET'])
def get_menu():
    menu_management_obj = MenuManagement(db)
    response = menu_management_obj.get_menu()
    return response

#API to add item to menu
@app.route('/create-menu', methods = ['POST'])
def create_menu():
    menu_management_obj = MenuManagement(db)
    response = menu_management_obj.create_menu(request)
    return response

#API to update menu item price
@app.route('/update-menu/<id>', methods=['PUT'])
def update_menu(id):
    menu_management_obj = MenuManagement(db)
    response = menu_management_obj.update_item_price(request, id)
    return response

#API to delete menu item
@app.route('/del-menu/<id>', methods=['DELETE'])
def del_menu(id):
    menu_management_obj = MenuManagement(db)
    response = menu_management_obj.del_menu(id)
    return response

#API to get tables list
@app.route('/get-tables', methods=['GET'])
def get_tables():
    table_management_obj = TableManagement(db)
    response = table_management_obj.get_tables()
    return response

#API to add table
@app.route('/add-table', methods = ['POST'])
def add_table():
    table_management_obj = TableManagement(db)
    response = table_management_obj.add_table(request)
    return response

#API to delete table by table number
@app.route('/del-table/<table_number>', methods=['DELETE'])
def del_table(table_number):
    table_management_obj = TableManagement(db)
    response = table_management_obj.del_table(table_number)
    return response

#API to get list of orders by diff status placed order/ongoing order/completed order
@app.route('/get-orders/<status>', methods=['GET'])
def get_orders_by_status(status):
    order_management_obj = OrderManagement(db)
    response = order_management_obj.get_orders_by_status(status)
    return response

#API to get list of orders
@app.route('/get-orders', methods=['GET'])
def get_orders():
    order_management_obj = OrderManagement(db)
    response = order_management_obj.get_orders()
    return response

#API to place new order
@app.route('/place-order', methods = ['POST'])
def place_order():
    order_management_obj = OrderManagement(db)
    response = order_management_obj.place_order(request)
    return response

#API to update status of the order
@app.route('/update-order-status/<id>', methods=['PUT'])
def update_order_status(id):
    order_management_obj = OrderManagement(db)
    response = order_management_obj.update_order_status(request, id)
    return response

#API to update table/transfer table
@app.route('/update-order-table/<id>', methods=['PUT'])
def update_order_table(id):
    order_management_obj = OrderManagement(db)
    response = order_management_obj.update_order_table(request, id)
    return response

#API to get list of customers
@app.route('/get-customers', methods=['GET'])
def get_customers():
    cust_info_obj = CustomerInformation(db)
    response = cust_info_obj.get_customers()
    return response

if __name__ == "__main__":
    app.run(port= 80, debug = True)
