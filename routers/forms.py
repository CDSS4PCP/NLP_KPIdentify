from fastapi import FastAPI, Request, Form, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from mainV2 import predict_kp
import json

router = APIRouter()
templates = Jinja2Templates(directory="templates/")


@router.get("/forms", response_class=HTMLResponse)
def form_get(request: Request):
    # result = "Type a number"
    return templates.TemplateResponse('forms.html', context={'request': request})


@router.post("/getPredictions", response_class=HTMLResponse)
def form_post1(request: Request, title: str = Form(...), abstract: str = Form(...)):
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
    # print(result)
    return templates.TemplateResponse('forms.html', context={'request': request, 'result': result})


# @router.post("/form2", response_class=HTMLResponse)
# def form_post2(request: Request, number: int = Form(...)):
#     result = number + 100
#     return templates.TemplateResponse('forms.html', context={'request': request, 'result': result, 'yournum': number})
