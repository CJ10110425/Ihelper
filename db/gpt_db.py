import pymongo

client = pymongo.MongoClient("mongodb+srv://ze0966747312:a0966747312@cluster0.bf8bdil.mongodb.net/?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)
mydb = client["Angel"]
mycol = mydb["gpt"]

def insert(data):
    mycol.insert_one(data)

def update_msg(msg):
    mycol.update_one({}, {"$set": {"msg": msg}})

def get_msg():
    return mycol.find_one()
if __name__ == "__main__":
    pass