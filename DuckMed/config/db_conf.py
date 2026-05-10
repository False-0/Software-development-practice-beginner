from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker,create_async_engine

#数据库URL
ASYNC_DATABASE_URL = "mysql+aiomysql://root:wojiaoQTC1314@localhost:3306/duckmed?charset=utf8mb4"

#创建异步引擎
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=True,  #可选，输出SQL日志
    pool_size=10,  #设置连接池活跃的连接数
    max_overflow=10 #允许额外的连接数
)

#创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)

#依赖项，用于获取数据库会话
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session #返回数据库会话给路由处理函数
            await session.commit() #提交事务
        except Exception :
            await session.rollback()  #有异常，回滚
            raise
        finally:
            await session.close()  #关闭会话