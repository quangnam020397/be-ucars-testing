from datetime import datetime
from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from ..services.car import (
    add_car,
    delete_car,
    retrieve_car,
    retrieve_cars,
    update_car,
)
from ..models.car import (
    CarSchema,
    UpdateCarSchema,
)
from ..models.BaseModel import (
    ErrorResponseModel,
    ResponseModel,
)

from ..services.branch import (check_branch_existed)
from bson.objectid import ObjectId



carRouter = APIRouter()

@carRouter.post("/", response_description="Branch data added into the database")
async def add_car_data(car: CarSchema = Body(...)):
    
    isExistBranch = await check_branch_existed(car.branch_id)
    if not isExistBranch:
        return ErrorResponseModel("An error occurred.", 400, "branch doesn't exist.")

    car = jsonable_encoder(car)
    
    new_car = await add_car(car)
    
    return ResponseModel(new_car, "car added successfully.")

@carRouter.get("/", response_description="cars retrieved")
async def get_cars(branch_id: str = None, searchValue: str = None):
    cars = await retrieve_cars(branch_id, searchValue)
    if cars:
        return ResponseModel(cars, "cars data retrieved successfully")
    return ResponseModel(cars, "Empty list returned")


@carRouter.get("/{id}/", response_description="car data retrieved")
async def get_car_data(id):
    car = await retrieve_car(id)
    if car:
        return ResponseModel(car, "car data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "car doesn't exist.")

@carRouter.put("/{id}")
async def update_car_data(id: str, req: UpdateCarSchema = Body(...)):
    req.updated_at = datetime.now()
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_car = await update_car(id, req)
    if updated_car:
        return ResponseModel(
            "car with ID: {} name update is successful".format(id),
            "car name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the car data.",
    )
    
@carRouter.delete("/{id}/", response_description="car data deleted from the database")
async def delete_car_data(id: str):
    deleted_car = await delete_car(id)
    if deleted_car:
        return ResponseModel(
            "car with ID: {} removed".format(id), "car deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "car with id {0} doesn't exist".format(id)
    )