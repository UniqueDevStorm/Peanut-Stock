class Eco:
    def __init__(self, coll, id_):
        self.coll = coll
        self.id = id_
        self.find = {"_id": str(self.id)}

    def init(self):
        data = {
            "_id": str(self.id),
            "money": 0,
            "뇌제트": 0,
            "앗뜨거빙수": 0,
            "땅콩와플": 0,
            "백병원": 0,
            "스톰전자": 0,
            "인절미": 0,
            "존맛토스트": 0,
            "호두과자": 0,
        }
        self.coll.insert_one(data)

    def delete(self):
        self.coll.delete_one(self.find)