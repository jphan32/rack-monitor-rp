from fastapi import FastAPI, Depends, HTTPException, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request

from models import RackStats

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


rack_stats = RackStats()


@app.get("/")
async def read_items(request: Request):
    items = rack_stats.readRecord()
    return templates.TemplateResponse("index.html", {"request": request, "items": items})


@app.post("/items/")
async def create_item(request: Request, name: str = Form(...)):
    item = rack_stats.addRecord(34.5, 67.4)
    return item

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
