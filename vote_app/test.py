from pymongo.mongo_client import MongoClient
import subprocess

# MongoDB URI
uri = "mongodb+srv://VotantTEST:votant_test_parola@votecluster.bc2p3.mongodb.net/?retryWrites=true&w=majority&appName=VoteCluster"

# Create a new client and connect to the server
client = MongoClient(uri)

# Access the database and collection
db = client['ProiectVotare']
vot_col = db["Voturi"]
hwid_col = db["HWID"]

# Query for the Votes field and extract Calin Georgescu's votes
#result = col.find_one({}, {"Votes.Calin Georgescu"})  # Fetch only Calin Georgescu's votes
#calin_votes = result["Votes"].get("Calin Georgescu")
#print(calin_votes)
#def creste_voturi():
#    increase_vote = col.update_one(
#        {},  # You can specify a filter to select a specific document, here we update the first document
#        {"$inc": {f"Votes.Calin Georgescu": 1}}  # Use the $inc operator to increment the vote count
#    )
#result = col.find_one({}, {"Votes.Calin Georgescu"})  # Fetch only Calin Georgescu's votes
#calin_votes = result["Votes"].get("Calin Georgescu")
hwid_raw = subprocess.check_output(["wmic", "csproduct", "get", "uuid"], text=True).strip()
hwid_lines = hwid_raw.splitlines()
hwid_code = None
for line in hwid_lines:
    if "UUID" not in line and line.strip():  # Ignore the header and empty lines
        hwid_code = line.strip()
        break

def can_vote(hwid):
    # Query to check if the HWID is in the collection and if it has voted or not
    result = hwid_col.find_one({"HWID": hwid})
    
    if result:
        # If the HWID is found, check if the user has voted
        if result["Voted"]:
            return "a votat"  # Already voted
        else:
            return "nu a votat"  # Hasn't voted yet
    else:
        # If the HWID does not exist, allow voting
        return "nu e in baza de date"
print(can_vote(hwid_code))
def insert_hwid(hwid):
    # Insert a new document with HWID and voted status
    hwid_col.insert_one({"HWID": hwid, "Voted": False})
    print(f"HWID {hwid} added to the collection.")

