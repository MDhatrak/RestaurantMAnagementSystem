from flask import jsonify

class CustomerInformation:
    def __init__(self, db):
        self.db = db

    def get_customers(self):
        try:
            customers = []
            cust_details = self.db.customer_info.find({})
            for customer in cust_details:
                updated_item = self.update_id(customer)
                customers.append(updated_item)
            return jsonify({'data': customers})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not found.'})

    def update_id(self, record):
        record['_id'] = str(record['_id'])
        return record
