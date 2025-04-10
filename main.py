from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.recommender import get_recommendation

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/recommend", response_class=HTMLResponse)
async def recommend(
    request: Request,
    job_role: str = Form(...),
    competencies: str = Form(...)
):
    try:
        query = f"{job_role} with competencies in {competencies}"
        recommendations = await get_recommendation(query)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "recommendations": recommendations,
            "status_code": 200
        })
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "recommendations": [{"error": str(e)}],
            "status_code": 500
        })

@app.get("/health")
async def health():
    return {"status": "healthy"}
