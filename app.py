from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import HTMLResponse
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from sql_app import crud, models, schemas
from main import InMemoryRepository, SQLRepository, URLShortener, URL
from sql_app.database import SessionLocal, engine


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_shortener():
    db = SessionLocal()
    shortener = URLShortener(repo=SQLRepository(db=db))
    try:
        yield shortener
    finally:
        db.close()


class LongUrl(BaseModel):
    url: str


class ShortUrl(BaseModel):
    url: str

templates = Jinja2Templates(directory="ui")


@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/shorten')
def shorten(item: LongUrl, shortener=Depends(get_shortener)) -> ShortUrl:
    short_url = shortener.zip(url=URL(urlstr=item.url))
    short = ShortUrl(url='tiny/' + short_url)
    return short


@app.get('/tiny/{short_url}')
def short_redirect(short_url, shortener=Depends(get_shortener)) -> RedirectResponse:
    long_url = shortener.unzip(short_key=short_url)
    return RedirectResponse(long_url)


# Debug runner
if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
