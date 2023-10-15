from typing import Union
from fastapi import Request, FastAPI 
from fastapi.middleware.cors import CORSMiddleware
from model import ActivityRecomendation as Model
import requests
import json
import random

app = FastAPI()

# GPT 3.5 api config
GPTurl = "https://api.openai.com/v1/chat/completions"
GPTkey = "Bearer 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"
headers = {"Authorization": GPTkey}

model = Model()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Extraccion de caracteristicas
async def gpt2JSON(inputMsg):
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
        {
            "role": "system",
            "content": "eres un modelo que busca sacar las caracteristicas de un texto que te enviaré, tu respuesta debe estar unicamente en Json, las llaves son, budget (es numero cualquiera, por defecto 50000), activityType (es que tipo de actividad es, las posibles opciones son 'Competencia', 'Educación', 'Deportes' y 'Recreación', por defecto 'Deportes'), people (cantidad de participantes, por defecto 1), activityCategory (es la categoria de la actividad, las posibles opciones son 'Curso', 'Festivales', 'Plan Afiliación' o 'Practica Libre', por defecto 'Practica Libre'), n es el numero de recomendaciones (por defecto 1), y category, puede ser 'Clase A', 'Clase B', 'Clase C' o 'Clase D' por defecto 'Clase D', el valor por defecto solo debe ser usado en caso de que no se encuentre en el texto."},
        {
            "role": "user",
            "content": inputMsg
        }
        ]
    }
    response = requests.post(GPTurl, headers=headers, json=body)
    json_response = response.json()
    return json_response["choices"][0]["message"]["content"]

# Respuesta a la sugerencia
def JSON2gpt(suggestion):
    body = {
        "model": "gpt-3.5-turbo",
        "messages": [
        {
            "role": "system",
            "content": "Eres Vivian, eres un miembro de la familia, debes resaltar eso, eres amigable como una madre. Vas a tomar el json y vas a escribir un texto diciendo el 'displayName', di el precio 'Price', no uses el signo $, por el contrario escribe 'pesos', la capacidad 'Capacity', y en que lugar esta disponible la actividad, adicionalmente pregunta si quiere agendar para mañana a una hora aleatoria entre las 7am y las 8pm, limita tus respuestas a 20 palabras"},
        {
            "role": "user",
            "content": json.dumps(suggestion)
        }
        ]
    }
    response = requests.post(GPTurl, headers=headers, json=body)
    json_response = response.json()
    text_response = json_response["choices"][0]["message"]["content"]
    return text_response


# Prediccion
@app.post("/predict")
async def predict_activity(request: Request):
    inputMsg = await request.json()
    inputMsg = inputMsg["text"]
    processed_text = json.loads(await gpt2JSON(inputMsg))
    parsed_json = textInput(processed_text)
    results = pipeline(
        parsed_json["location"] ,
        parsed_json["category"] ,
        parsed_json["budget"] ,
        parsed_json["people"] ,
        parsed_json["activityType"] ,
        parsed_json["activityCategory"],
        parsed_json["n"]
    )
    final_response = {
        "activity": JSON2gpt(results)
    }
    return final_response

# Valores por defecto en caso de fallo
def textInput(processed_text):    
    real_keys = ["location", "category", "budget", "people", "activityType", "activityCategory", "n"]
    processed_text["location"] = [random.uniform(4.486987081428798,4.955016037947576), random.uniform(-74.23392383743702,-73.98626912611371)]
    for key in real_keys:
        if key not in list(processed_text.keys()):
            if key == "category":
                processed_text["category"] = "Clase D"
            if key == "budget":
                processed_text["budget"] = 50000
            if key == "people":
                processed_text["people"] = 1
            if key == "activityType":
                processed_text["activityType"] = "Deportes"
            if key == "activityCategory":
                processed_text["activityCategory"] = "Practica Libre"
            if key == "n":
                processed_text["n"] = 1

    for key in list(processed_text.keys()):
        if key not in real_keys:
            del processed_text[key]

    print(processed_text)
    return processed_text


# Pipeline de ejecución para la prediccion
def pipeline(location, userClass, budget, people, activityType, activityCategory, n):
    user_vector, targetVector = model.processInput(location, 
                                                   userClass, 
                                                   int(budget), 
                                                   int(people), 
                                                   activityType, 
                                                   activityCategory)
    predictions = model.predict(user_vector, targetVector, n)
    results = model.getResults(predictions)
    return results

@app.get("/")
def read_root():
    return {"propouse": "Hola, soy Vivian, ve a /predict"}
