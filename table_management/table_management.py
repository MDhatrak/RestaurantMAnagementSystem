from flask import jsonify

class TableManagement:
    def __init__(self, db):
        self.db = db

    def get_tables(self):
        try:
            tables = []
            tables_detail = self.db.tables_info.find({})
            for item in tables_detail:
                updated_item = self.update_id(item)
                tables.append(updated_item)
            return jsonify({'data': tables})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not found.'})

    def update_id(self, record):
        record['_id'] = str(record['_id'])
        return record

    def add_table(self, request):
        try:
            table_number = request.json['tableNumber']
            table = self.db.tables_info.find_one({'tableNumber': table_number})
            if table is not None:
                return 'Table already exist!'
            response = self.db.tables_info.insert_one({'tableNumber': table_number})
            if response is not None:
                return jsonify({'data': 'Successful.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not inserted.'})

    def del_table(self, table_number):
        try:
            item = self.db.tables_info.find_one({'tableNumber': int(table_number)})
            if item is not None:
                self.db.tables_info.delete_one({'tableNumber': int(table_number)})
                return jsonify({'data': 'Successful.'})
            return jsonify({'error': 'Table not exist.'})
        except Exception as e:
            print(e)
        return jsonify({'error': 'data not deleted.'})
