from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import text
from typing import Optional, List, Dict, Any

from db import get_db_conn, sql_loader

class ItemService:
    def __init__(self, conn: AsyncConnection = Depends(get_db_conn)):
        self.conn = conn

    async def get_all_items(self) -> List[Dict[str, Any]]:
        raw_sql = sql_loader.get_sql("ItemMapper.getAllItems")        
        result = await self.conn.execute(text(raw_sql))
        rows = result.fetchall()
        return [row._asdict() for row in rows]

    async def get_itemr_by_node_id(self, node_id: str) -> Optional[Dict[str, Any]]:
        raw_sql = sql_loader.get_sql("ItemMapper.getItemByNodeId")
        result = await self.conn.execute(text(raw_sql), {"node_id": node_id})
        rows = result.fetchall()
        return [row._asdict() for row in rows]

