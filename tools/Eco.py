class Eco:
    def __init__(self, coll, id_):
        self.coll = coll
        self.id = id_
        self.find = {"_id": str(self.id)}

    def init(self):
        data = {"_id": str(self.id), "money": 0}
        self.coll.insert_one(data)

    def delete(self):
        self.coll.delete_one(self.find)