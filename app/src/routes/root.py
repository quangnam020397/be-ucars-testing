from fastapi import (
    APIRouter,
)

from .branch import branchRouter

from .car import carRouter

router = APIRouter()

router.include_router(branchRouter, tags=["Branchs"], prefix='/branch')

router.include_router(carRouter, tags=["Cars"], prefix='/car')


