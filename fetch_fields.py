from pymongo import MongoClient

# 1. Connect
client = MongoClient("mongodb+srv://kanurisathvika310_db_user:tender_db@prompts.nhy93fe.mongodb.net/")
db = client["PromptsDB_org"]
collection = db["Keyword"]

# 2. Query using indexes (api + purpose)
query = {"api": "key", "purpose": "Generate tender summary"}

# 3. Projection → specify which fields to fetch (1 = include, 0 = exclude)
projection = {
    "_id": 0,          # Exclude _id field
    "main_prompt": 1,
    "do": 1,
    "donts": 1,
    "examples": 1
}

# 4. Fetch multiple documents
# results = collection.find(query, projection)
# print("printing results:")
# print(results)
# print(collection.count_documents({}))

# # 5. Print results
# for doc in results:
#     print(doc)


def fetch_details(api,purpose,fields):
    query = {"api": api, "purpose": purpose}
    projection = {field: 1 for field in fields}
    results = collection.find(query, projection)
    return list(results)
