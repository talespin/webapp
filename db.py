import os
import xml.etree.ElementTree as ET
from typing import Dict
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from typing import AsyncGenerator
from sqlalchemy.orm import declarative_base, sessionmaker


DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("POSTGRESQL_USER")}:{os.environ.get("POSTGRESQL_PASSWORD")}@{os.environ.get("POSTGRESQL_SERVER")}:{os.environ.get("POSTGRESQL_PORT")}/{os.environ.get("POSTGRESQL_DB")}'
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
Base = declarative_base()


async def get_db_conn() -> AsyncGenerator[AsyncConnection, None]:
    async with engine.connect() as conn:
        yield conn

class XMLSqlLoader:
    def __init__(self):
        self.queries: Dict[str, str] = {}

    def load_mappers(self, mapper_dir: str):
        """mapper 폴더 내의 모든 xml 파일을 읽어 캐싱"""
        if not os.path.exists(mapper_dir):
            return
        for filename in os.listdir(mapper_dir):
            if filename.endswith(".xml"):
                filepath = os.path.join(mapper_dir, filename)
                tree = ET.parse(filepath)
                root = tree.getroot()
                namespace = root.attrib.get("namespace", "")
                for statement in root:
                    query_id = statement.attrib.get("id")
                    if query_id:
                        key = f"{namespace}.{query_id}" if namespace else query_id
                        self.queries[key] = statement.text.strip()

    def get_sql(self, query_key: str) -> str:
        """캐싱된 SQL 문자열을 반환."""
        sql = self.queries.get(query_key)
        if not sql:
            raise KeyError(f"XML 매퍼에서 쿼리를 찾을 수 없슴: {query_key}")
        return sql

sql_loader = XMLSqlLoader()