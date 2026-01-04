from fastapi import APIRouter, Depends
from app.routers.auth import authRouter
from app.routers.admin.users import userRouter

routes = APIRouter()
routes.include_router(router=authRouter)
routes.include_router(router=userRouter)
