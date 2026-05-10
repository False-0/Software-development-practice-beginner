#整合 根据TOKEN查询用户，返回用户
from fastapi import Header, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from config.db_conf import get_db
from crud import users
from starlette import status

async def get_current_token(
        authorization: str = Header(...,alias="Authorization"),
        db:AsyncSession = Depends(get_db)
):
    #前端请求体的TOKEN格式：Bearer *****
    #第一种方法： token=authorization.split("")[1]
    #第二种方法：
    token = authorization.replace("Bearer ","")
    user = await users.get_user_by_token(db,token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="无效的令牌或已经过期的令牌")
    return user