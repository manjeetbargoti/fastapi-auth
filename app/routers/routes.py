from fastapi import APIRouter, Depends
from app.routers.auth import authRouter
from app.routers.admin.users import userRouter
from app.routers.admin.admin_rbac import rbacRouter

routes = APIRouter()
routes.include_router(router=authRouter)
routes.include_router(router=userRouter)
routes.include_router(router=rbacRouter)
