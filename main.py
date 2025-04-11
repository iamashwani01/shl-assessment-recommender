from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.recommender import get_recommendation

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>SHL Assessment Recommendation Engine</title>
        </head>
        <body style="font-family: Arial; text-align: center; padding: 50px;">
            <h1>👋 Welcome to the SHL Assessment Recommender</h1>
            <p>This API recommends SHL assessments based on job role and competencies.</p>
            <p>➡️ <a href="/docs">Click here to open the Swagger UI</a></p>
        </body>
    </html>
    """


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
