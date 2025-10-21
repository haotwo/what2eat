from fastapi import FastAPI, Response, Depends

from src.core.config import settings
from src.lifespan import lifespan
from src.core.exception import register_exception_handlers
from src.dishes.router import router as dishes_router


app = FastAPI(
    app_name=settings.app_name,
    version="0.1.0",
    description="FastAPI 练习项目实战",
    lifespan=lifespan,
)

# 注册异常处理器
register_exception_handlers(app)

# 注册路由
app.include_router(dishes_router)

@app.get("/health")
async def health_check(response:Response):
  response.status_code = 200
  return {"status":"ok 👌"}