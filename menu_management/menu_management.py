from flask import jsonify
from bson import ObjectId

class MenuManagement:
    def __init__(self, db):
        self.db = db

    def get_menu(self):
        try:
            menu = []
            menu_details = self.db.menu_options.find({})
            for item in menu_details:
                updated_item = self.update_id(item)
                menu.append(updated_item)
            return jsonify({'data': menu})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not found.'})

    def update_id(self, record):
        record['_id'] = str(record['_id'])
        return record

    def create_menu(self, request):
        try:
            category = request.json['category']
            type = request.json['type']
            name = request.json['name']
            price = request.json['price']
            response = self.db.menu_options.insert_one({'category': category, 'type': type, 'name': name, 'price': price})
            if response is not None:
                return jsonify({'data': 'Successful.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not inserted.'})

    def update_item_price(self, request, id):
        try:
            price = request.json['price']
            item = self.db.menu_options.find_one({'_id': ObjectId(id)})
            if item is not None:
                self.db.menu_options.update_one({'_id': ObjectId(id)},
                                           {'$set': {'price': price}})
                return jsonify({'data': 'Successful.'})
            return jsonify({'error': 'Invalid Object Id.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not modified.'})

    def del_menu(self, id):
        try:
            item = self.db.menu_options.find_one({'_id': ObjectId(id)})
            if item is not None:
                self.db.menu_options.delete_one({'_id': ObjectId(id)})
                return jsonify({'data': 'Successful.'})
            return jsonify({'error': 'Invalid Object Id.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not deleted.'})


