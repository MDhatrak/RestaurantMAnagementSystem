from flask import jsonify
from bson import ObjectId
import time

class OrderManagement:
    def __init__(self, db):
        self.db = db

    def get_orders(self):
        try:
            orders = []
            order_details = self.db.order_details.find({})
            for order in order_details:
                updated_item = self.update_id(order)
                orders.append(updated_item)
            return jsonify({'data': orders})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not found.'})

    def get_orders_by_status(self, status):
        try:
            orders = []
            order_details = self.db.order_details.find({'status': status})
            for order in order_details:
                updated_item = self.update_id(order)
                orders.append(updated_item)
            return jsonify({'data': orders})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not found.'})

    def update_id(self, record):
        record['_id'] = str(record['_id'])
        return record

    def place_order(self, request):
        try:
            total = 0
            cust_name = request.json['name']
            contact_number = request.json['contactNumber']
            email = request.json['emailAddress']
            cust_obj = self.db.customer_info.insert_one({'name': cust_name, 'contactNumber': contact_number,
                                                    'emailAddress': email})

            cust_id = str(cust_obj.inserted_id)
            table_num = request.json['tableNumber']
            order_details = request.json['orderDetails']
            discount_percentage = request.json['discountPercentage']
            status = request.json['status']
            date_time = time.asctime(time.localtime(time.time()))

            for item in order_details:
                item_id = item['itemId']
                quantity = item['quantity']
                item_info = self.db.menu_options.find_one({'_id': ObjectId(item_id)})
                item_price = item_info['price']
                total_item_amt = item_price * quantity
                total += total_item_amt

            if discount_percentage == 0 or discount_percentage == 1:
                billing_amt = total
            else:
                discount_amt = (total * discount_percentage) / 100
                billing_amt = total - discount_amt
            response = self.db.order_details.insert_one({'customerId': cust_id, 'tableNumber': table_num,
                                                    'orderDetails': order_details, 'totalPrice': total,
                                                    'discountPercentage': discount_percentage, 'status': status,
                                                    'billingAmount': billing_amt, 'orderDateAndTime': str(date_time)})
            if response is not None:
                return jsonify({'data': 'Successful.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not inserted.'})

    def update_order_status(self, request, id):
        try:
            status = request.json['status']
            item = self.db.order_details.find_one({'_id': ObjectId(id)})
            if item is not None:
                self.db.order_details.update_one({'_id': ObjectId(id)},
                                            {'$set': {'status': status}})
                return jsonify({'data': 'Successful.'})
            return jsonify({'error': 'Invalid Object Id.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not modified.'})

    def update_order_table(self, request, id):
        try:
            table_number = request.json['tableNumber']
            item = self.db.order_details.find_one({'_id': ObjectId(id)})
            if item is not None:
                self.db.order_details.update_one({'_id': ObjectId(id)},
                                            {'$set': {'tableNumber': int(table_number)}})
                return jsonify({'data': 'Successful.'})
            return jsonify({'error': 'Invalid Object Id.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not modified.'})
