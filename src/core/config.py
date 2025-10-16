from functools import lru_cache
from typing import Literal, Optional, Any, Dict
from pydantic import computed_field, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
  """应用配置（支持PostgreSQL和SQLite,含连接池设置）"""
  app_name: str = "What to Eat"
  debug: bool = False

  # 数据库类型
  db_type: Literal["postgres", "sqlite"] = "sqlite"

  # PostgreSQL 配置
  db_host: str = "localhost"
  db_port: int = 5432
  db_user: str = "postgres"
  db_password: str = "postgres"
  db_name: str = "what2eat"

  # 连接池配置（仅PostgreSQL有效）
  # 必选参数
  pool_size: int = 20  # 连接池基础大小
  max_overflow: int = 10  # 超过pool_size的最大连接数
  pool_timeout: int = 30  # 获取连接超时时间(秒)
  pool_pre_ping: bool = True  # 取连接前是否检查可用性

  # 可选调优参数
  pool_recycle: int = 3600  # 连接最大存活时间(秒)
  pool_use_lifo: bool = False  # 连接池取连接顺序
  echo: bool = False  # 是否打印SQL 开发可打开 生产关闭

  # SQLite配置
  sqlite_db_path: str = "./data/what2eat.sqlite3"

  @computed_field
  def database_url(self) -> str:
    if self.db_type == 'postgres':
      return (
        f"postgresql+asyncpg://{self.db_user}:{self.db_password}"
        f"@{self.db_host}:{self.db_port}/{self.db_name}"
      )
    elif self.db_type == 'sqlite':
      return f"sqlite+aiosqlite:///{self.sqlite_db_path}"
    else:
      raise ValueError(f"Unsupported DB_TYPE:{self.db_type}")
    
  @computed_field
  def engine_options(self) -> Dict[str, Any]:
    """统一封装engine options,供create_async_engine使用"""
    if self.db_type == 'postgres':
      return {
        "pool_size": self.pool_size,
        "max_overflow": self.max_overflow,
        "pool_timeout": self.pool_timeout,
        "pool_recycle": self.pool_recycle,
        "pool_use_lifo": self.pool_use_lifo,
        "echo": self.echo,
      }
    # SQLite 不支持pool设置，返回最小参数
    return {"echo": self.echo}

  # JWT配置
  jwt_secret: str = "G8V7aP2qX5sR9yL3nM6bK1tC4wF0zJ5dH8eQ2rT7yU3iP6oA9"

  model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore",  # 忽略未定义的配置项
  )




# @lru_cache
# def get_settings() -> Settings:
#     """获取缓存的设置实例"""
#     return Settings()

settings = Settings()