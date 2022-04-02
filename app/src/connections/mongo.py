import motor.motor_asyncio

from ..configs.configs import (DB_URL)

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = client.uCars_testing
branch_collection = database.get_collection("branch_collection")
car_collection = database.get_collection("car_collection")