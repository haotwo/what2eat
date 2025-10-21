from typing import Literal

from fastapi import APIRouter, Depends, Query, status,Path
from loguru import logger

from src.dishes.service import DishService
from src.core.database import get_db
from src.dishes.repository import DishRepository
from src.dishes.schema import DishCreate, DishResponse, DishUpdate

# 创建路由器
router = APIRouter(prefix="/dishes", tags=["Dishes"])


# 依赖注入
async def get_dish_service(session=Depends(get_db)) -> DishService:
    repository = DishRepository(session)
    return DishService(repository)

@router.post("/",response_model=DishResponse,status_code=status.HTTP_201_CREATED,summary="创建菜品")
async def create_dish(
    dish_data:DishCreate,
    service:DishService = Depends(get_dish_service)
):
    """创建菜品"""
    new_dish =  await service.create_dish(dish_data)
    return new_dish

@router.get("/{dish_id}",response_model=DishResponse,summary="获取单个菜品")
async def get_dish(
    dish_id:int = Path(...,description="菜品ID"),
    service:DishService = Depends(get_dish_service)
):
    """获取单个菜品"""
    logger.debug(f"正在获取菜品ID:{dish_id}")
    try:
        dish = await service.get_dish_by_id(dish_id)
        logger.info(f"获取到菜品，ID:{dish_id}")
        return dish
    except Exception as e:
        logger.error(f"获取ID为{dish_id}的菜品出错:{str(e)}")
        raise

@router.get("/",response_model=list[DishResponse],summary="查询所有菜品")
async def list_dishes(
    search:str | None = Query(None,description="搜索关键词"),
    order_by:Literal["id","name","created_at"] = Query("id",description="排序字段"),
    direction:Literal["asc","desc"] = Query("asc",description="排序方向"),
    limit:int = Query(10,ge=1,le=500),
    offset:int = Query(0,ge=0),
    service:DishService = Depends(get_dish_service)
):
    """查询所有菜品"""
    return await service.list_dishes(
        search=search,
        order_by=order_by,
        direction=direction,
        limit=limit,
        offset=offset
    )

@router.put("/{dish_id}",response_model=DishResponse,summary="更新菜品")
async def update_dish(
    dish_data:DishUpdate,
    dish_id:int = Path(...,description="菜品ID"),
    service: DishService = Depends(get_dish_service)
):
    """更新菜品"""
    return await service.update_dish(dish_id,dish_data)


@router.delete("/{dish_id}",status_code=status.HTTP_204_NO_CONTENT,summary="删除菜品")
async def delete_dish(
    dish_id:int = Path(...,description="菜品ID"),
    service: DishService = Depends(get_dish_service)
):
    """删除菜品"""
    await service.delete_dish(dish_id)
    return