from fastapi import FastAPI
from routers import questions,users,user_errors,user_correct,user_favorites,forum,user_statistics
from fastapi.middleware.cors import CORSMiddleware
from utils.exception_handles import register_exception_handlers
app = FastAPI()

#注册异常处理器
register_exception_handlers(app)

#origins=[
     #"http:......
#]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], #允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,   #允许携带COOKIE
    allow_methods=["*"],      #允许的请求方法
    allow_headers=["*"],      #允许的请求头
)

@app.get("/")
async def root():
    return {"message": "Hello World"}

#挂载路由/注册路由
app.include_router(questions.router)
app.include_router(users.router)
app.include_router(user_correct.router)
app.include_router(user_errors.router)
app.include_router(user_favorites.router)
app.include_router(forum.router)
app.include_router(user_statistics.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

