import asyncio
import aiohttp
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from core.config import URL_MAIN_HTML
from db.base import database
from endpoints import transaction
from services import push_transactions

app = FastAPI()

app.include_router(transaction.router, prefix="/transaction", tags=["transactions"])


@app.on_event("startup")
async def startup():
    await database.connect()
    asyncio.create_task(push_transactions())


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(URL_MAIN_HTML) as response:
                if response.status == 200:
                    r = await response.text()
                    return r
                return "Ваш запрос в очереди"
        except BaseException:
            return "Ваш запрос в очереди"


if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, host="0.0.0.0")
