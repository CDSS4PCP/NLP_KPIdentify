from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.nlp.experiments.predictor import predict_kp
import json

router = APIRouter()
templates = Jinja2Templates(directory="web/templates")


@router.get("/getPredictions", response_class=HTMLResponse)
def form_get(request: Request):
    return templates.TemplateResponse('getPredictions.html', context={'request': request})


@router.post("/getPredictions", response_class=HTMLResponse)
def form_post(request: Request, title: str = Form(...), abstract: str = Form(...)):
    predict_data = [{
        "id": "",
        "title": "",
        "abstract": "",
        "methods": "",
        "results": "",
        "keywords": [],
        "actual_keywords": [],
        "fullText": "",
        "sentences": ""
        }]
    predict_data[0]['title'] = title
    predict_data[0]['abstract'] = abstract

    result = predict_kp(predict_data)
    return templates.TemplateResponse('getPredictions.html', context={'request': request, 'result': result})
