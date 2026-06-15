from fastapi import APIRouter, Depends, HTTPException, status
from service.item_service import ItemService

router = APIRouter(
    prefix='/api/item',
)

@router.get("/items")
async def read_items(item_service: ItemService = Depends(ItemService)):
    return await item_service.get_all_items()
    
@router.get("/item/{user_id}")
async def read_item_by_node_id(node_id: int, item_service: ItemService = Depends(ItemService)):
    return await item_service.get_itemr_by_node_id(node_id)
