from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from services.recommender import get_recommendation

app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    job_role: str = Form(...),
    competencies: str = Form(...)
):
    query = f"{job_role} with competencies in {competencies}"
    recommendations = await get_recommendation(query)
    return templates.TemplateResponse("index.html", {
        "request": request,
        "recommendations": recommendations,
        "job_role": job_role,
        "competencies": competencies
    })
