import pymongo

class Database:
    def __init__(self, db_name, col):
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        self.col = db[col]

    def print_db(self):
        for x in self.col.find({}, {"_id": 0}):
            print(x)

    def clear_db(self):
        self.col.delete_many({})
        self.col.drop()

    def add_field(self, obj):
        self.col.insert_one(obj);

    def get_field(self):
        return self.col.find_one({},{ "_id": 0})


class MongoDriver:
    def __init__(self,player_id):
        self.database = Database("user_data",player_id)

    def encode(self , positions, score, lives, level):
        obj = { "positions" : [],
                "score" : score,
                "lives" : lives,
                "level" : level}
        for i in positions:
            obj['positions'].append(self.encode_tuple(i))
        return obj

    def encode_tuple(self, tuple):
        obj = {"x": tuple[0],"y": tuple[1],"name" : tuple[2]}
        return obj

    def decode_tuple(self, obj):
        return (obj['x'],obj['y'],obj['name'])

    def decode_position(self, obj):
        responce = []
        for a in obj['positions']:
            responce.append(self.decode_tuple(a))
        return responce

    def save(self, positions, score,lives,level):
        self.database.add_field(self.encode(positions, score,lives,level))

    def pri(self):
        self.database.print_db()

    def get_score(self):
        return self.database.get_field()['score']

    def get_level(self):
        return self.database.get_field()['level']

    def get_lives(self):
        return self.database.get_field()['lives']

    def get_pellets(self):
        return self.decode_position(self.database.get_field())

    def clean(self):
        self.database.clear_db()
