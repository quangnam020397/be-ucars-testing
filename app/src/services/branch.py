
from ..connections.mongo import branch_collection
from bson.objectid import ObjectId
from datetime import datetime

def branch_helper(branch):
    return {
        "id": str(branch["_id"]),
        "name": branch["name"],
        "description": branch["description"],
        "logo": branch["logo"],
        "created_at": branch["created_at"],
        "updated_at": branch["updated_at"],
        "deleted_at": branch["deleted_at"],
    }

# Retrieve all branchs present in the database
async def retrieve_branchs():
    branchs = []
    async for branch in branch_collection.find({"deleted_at": None}):
        branchs.append(branch_helper(branch))
    print(branchs)
    return branchs


# Add a new branch into to the database
async def add_branch(branch_data: dict) -> dict:
    branch = await branch_collection.insert_one(branch_data)
    new_branch = await branch_collection.find_one({"_id": branch.inserted_id})
    return branch_helper(new_branch)


# Retrieve a branch with a matching ID
async def retrieve_branch(id: str) -> dict:
    branch = await branch_collection.find_one({"_id": ObjectId(id), "deleted_at": None})
    if branch:
        return branch_helper(branch)


# Update a branch with a matching ID
async def update_branch(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    branch = await branch_collection.find_one({"_id": ObjectId(id)})
    if branch:
        updated_branch = await branch_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_branch:
            return True
        return False


# Delete a branch from the database / soft delete
async def delete_branch(id: str):
    branch = await branch_collection.find_one({"_id": ObjectId(id)})
    if branch:
        await branch_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}})
        return True
    
# check is exist branch with a matching ID
async def check_branch_existed(id: str) -> dict:
    branch = await branch_collection.find_one({"_id": ObjectId(id), "deleted_at": None})
    if branch:
        return True
    return False
