from pymongo import MongoClient

# Step 1: Connect to MongoDB (local server or Atlas connection string)
client = MongoClient("mongodb+srv://kanurisathvika310_db_user:tender_db@prompts.nhy93fe.mongodb.net/")  
# For Atlas use: MongoClient("mongodb+srv://<username>:<password>@cluster.mongodb.net/")

# Step 2: Create (or switch to) a database
db = client["PromptsDB"]

# Step 3: Create (or switch to) a collection
collection = db["Chat"]

# Step 4: Insert a sample document
sample_prompt = {
    "api": "query",
    "purpose": "Generate tender summary",
    "main_prompt": "Summarize the tender document in 200 words.",
    "do": ["Highlight key dates", "Include eligibility criteria"],
    "donts": ["Don’t add personal opinions", "Don’t change legal terms"],
    "examples": ["Example tender summary text here..."]
}

collection.insert_one(sample_prompt)

print("✅ Database and collection created, sample document inserted!")
