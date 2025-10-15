from fastapi import FastAPI,Response,Depends
from src.core.config import Settings

app = FastAPI(description="FastAPI项目实战")

# 路由引入
@app.get("/")
def read_root(
  settings: Settings = Depends(Settings)
):
  return {
    "message":f"Hello from the {settings.app_name}!",
    "database_url":settings.database_url,
    "jwt_secret":settings.jwt_secret

  }

@app.get("/health")
async def health_check(response:Response):
  response.status_code = 200
  return {"status":"ok 👌"}