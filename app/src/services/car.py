
from ..connections.mongo import car_collection
from bson.objectid import ObjectId
from datetime import datetime

def car_helper(car):
    return {
        "id": str(car["_id"]),
        "name": car["name"],
        "branch_id": car["branch_id"],
        "description": car["description"],
        "thumbnail": car["thumbnail"],
        "images": car["images"],
        "created_at": car["created_at"],
        "updated_at": car["updated_at"],
        "deleted_at": car["deleted_at"],
    }

# Retrieve all cars present in the database
async def retrieve_cars(brand_id: str, search: str = None, limit: int = None, offset: int = None):
    cars = []
    query = {"deleted_at": None}
    if brand_id is not None:
        query["branch_id"] = brand_id
    if search is not None:
        await car_collection.create_index([("name", "text")])
        query["$text"] = {"$search": search}

    async for car in car_collection.find(query):
        cars.append(car_helper(car))
    return cars


# Add a new car into to the database
async def add_car(car_data: dict) -> dict:
    car = await car_collection.insert_one(car_data)
    new_car = await car_collection.find_one({"_id": car.inserted_id})
    return car_helper(new_car)


# Retrieve a car with a matching ID
async def retrieve_car(id: str) -> dict:
    car = await car_collection.find_one({"_id": ObjectId(id), "deleted_at": None})
    if car:
        return car_helper(car)


# Update a car with a matching ID
async def update_car(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        updated_car = await car_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_car:
            return True
        return False


# Delete a car from the database / soft delete
async def delete_car(id: str):
    car = await car_collection.find_one({"_id": ObjectId(id)})
    if car:
        await car_collection.update_one({"_id": ObjectId(id)}, {"$set": {"deleted_at": datetime.now()}})
        return True