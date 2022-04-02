from datetime import datetime
from fastapi import APIRouter, Body, File, UploadFile
from fastapi.encoders import jsonable_encoder

from ..services.upload import uploadFile

from ..services.branch import (
    add_branch,
    delete_branch,
    retrieve_branch,
    retrieve_branchs,
    update_branch,
)
from ..models.branch import (
    BranchSchema,
    UpdateBranchSchema,
)
from ..models.BaseModel import (
    ErrorResponseModel,
    ResponseModel,
)


branchRouter = APIRouter()


@branchRouter.post("/", response_description="Branch data added into the database")
async def add_branch_data(branch: BranchSchema = Body(...)):
    branch = jsonable_encoder(branch)
    new_branch = await add_branch(branch)
    return ResponseModel(new_branch, "branch added successfully.")


@branchRouter.get("/", response_description="branchs retrieved")
async def get_branchs():
    branchs = await retrieve_branchs()
    if branchs:
        return ResponseModel(branchs, "branchs data retrieved successfully")
    return ResponseModel(branchs, "Empty list returned")


@branchRouter.get("/{id}", response_description="branch data retrieved")
async def get_branch_data(id):
    branch = await retrieve_branch(id)
    if branch:
        return ResponseModel(branch, "branch data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "branch doesn't exist.")


@branchRouter.put("/{id}")
async def update_branch_data(id: str, req: UpdateBranchSchema = Body(...)):
    req.updated_at = datetime.now()
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_branch = await update_branch(id, req)
    if updated_branch:
        return ResponseModel(
            "branch with ID: {} name update is successful".format(id),
            "branch name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the branch data.",
    )


@branchRouter.delete("/{id}", response_description="branch data deleted from the database")
async def delete_branch_data(id: str):
    deleted_branch = await delete_branch(id)
    if deleted_branch:
        return ResponseModel(
            "branch with ID: {} removed".format(
                id), "branch deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "branch with id {0} doesn't exist".format(id)
    )


@branchRouter.post("/{id}/logo", response_description="logo uploaded")
async def upload_file_to_minio(id: str, file: UploadFile = File(...)):
    try:
        branch = await retrieve_branch(id)
        if not branch:
            return ErrorResponseModel("An error occurred.", 404, "branch doesn't exist.")

        data_file = await uploadFile(file)
        if(data_file != None):
            await update_branch(id, {"logo": data_file.get("url")})
            data = await retrieve_branch(id)
            return ResponseModel(data, "file uploaded successfully")
        return ErrorResponseModel("An error occurred", 404, "file not found")
    except Exception as e:
        return ErrorResponseModel("An error occurred", 404, str(e))
