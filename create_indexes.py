from pymongo import MongoClient

# Step 1: Connect to MongoDB
client = MongoClient("mongodb+srv://kanurisathvika310_db_user:tender_db@prompts.nhy93fe.mongodb.net/")
# For Atlas use: MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")

# Step 2: Create (or switch to) a database
db = client["PromptsDB_org"]

# Step 3: Create (or switch to) a collection
collection = db["Keyword"]

# Step 4: Create indexes
# Single-field indexes
collection.create_index("api")
collection.create_index("purpose")

# Compound index (optional, for queries using both api + purpose together)
collection.create_index([("api", 1), ("purpose", 1)])

# Step 5: Insert a sample document
sample_prompt = {
    "api": "key",
    "purpose": "Generate tender summary",
    "main_prompt": "Summarize the tender document in 200 words and give me keywords.",
    "do": "Highlight key dates,\nInclude eligibility criteria",
    "donts": "Don’t add personal opinions,\n Don’t change legal terms",
    "examples": "Example tender summary text here..."
}

collection.insert_one(sample_prompt)

print("✅ Database, collection, and indexes created successfully!")
