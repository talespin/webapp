import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from db import engine, sql_loader
from router.item_router import router as item_router
from router.roadmap_router import router as roadmap_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # [서버 시작 시] mappers 디렉토리 내의 XML 파일 전체 로드
    sql_loader.load_mappers(mapper_dir="./mapper")
    yield
    # [서버 종료 시]
    await engine.dispose()

app = FastAPI(lifespan=lifespan, title='수플레')
app.include_router(item_router)
app.include_router(roadmap_router)
app.mount('/', StaticFiles(directory='web', html=True), name='root')



if __name__=='__main__':
    uvicorn.run(app='main:app', port=80, reload=True)
