from fastapi import FastAPI, Depends, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, Base, get_db
from crud import create_item, get_items, delete_item

app = FastAPI()

# HTML templates location
templates = Jinja2Templates(directory="templates")

# 🔹 Startup event
# WHY?
# - Runs once when app starts
# - Creates DB tables
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# READ page
@app.get("/")
async def index(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    # await because DB call
    items = await get_items(db)

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "items": items}
    )

# CREATE
@app.post("/add")
async def add_item(
    name: str = Form(...),
    # From HTML form
    db: AsyncSession = Depends(get_db)
):
    await create_item(db, name)

    # Redirect back to home
    return RedirectResponse("/", status_code=303)

# DELETE
@app.get("/delete/{item_id}")
async def remove_item(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    await delete_item(db, item_id)
    return RedirectResponse("/", status_code=303)
