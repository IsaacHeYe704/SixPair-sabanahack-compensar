import numpy as np
import pandas as pd
import re
import matplotlib.pyplot as plt
import json
import string
import unidecode
import random
from sklearn.preprocessing import StandardScaler
import math
import os

class ActivityRecomendation:
    # inicializacion y carga de datos
    def __init__(self):
        # Reproducibilidad
        random.seed(824)
        # Data loading
        dfs = []
        for file in os.listdir("./data"):
            f = open("./data/"+file)
            data = json.load(f)
            data = list(map(lambda x:{
                "x_typePyS":x["x_typePyS"],
                'salePrice': x["salePrice"],
                'listPrice': x["listPrice"],
                'displayName': x["displayName"],
            },data["items"]))
            dfs.append(pd.DataFrame.from_records(data))
            f.close()

        # Coordenadas de las sedes
        self.locations = {    
            "Autopista Sur": [4.5955987784088945, -74.17316263319985],
            "Avenida 68": [4.661312982014069, -74.10096479074343],
            "Cajica": [4.9557094907674895, -74.00709977539742],
            "Calle 220": [4.79912962151117, -74.03149096375901],
            "Calle 94": [4.681425114476471, -74.05747134656302],
            "CBI Americas": [4.62802761547265, -74.134944106088],
            "CBI Cedritos": [4.728979684495284, -74.0504959576009],
            "CBI Centro Mayor": [4.591267305931821, -74.12350111958004],
            "CBI Soacha": [4.588764984327801, -74.22588957910462],
            "Chia": [4.863262546063276, -74.05364440268606],
        }
        # multiplicador de precio por clase
        self.categoryScaler = {"Clase D":1, 
                  "Clase C":0.9, 
                  "Clase B":0.7, 
                  "Clase A":0.5}
        # Generacion del dataset
        self.services = pd.concat(dfs)
        self.scaler_prices, self.scaler_location = self.dataProcessing()
        
    # Formato de los resultados como respuesta json
    def getResults(self, closest):
        results = self.services.iloc[closest.index]
        results = results[["displayName", "Price", "Capacity", self.closest]].transpose().to_dict()
        if len(results.keys()) != 0:
            if list(results.keys())[0] == "Price":
                results = {
                    "0": results
                }
        else:
            return "No hay opciones para estas caracteristicas"
        return results


    # Predicción 
    def predict(self, userVector, targetValues, n):
        closest = targetValues.copy()
        closest = closest.astype(int)
        closest["price_i"] = userVector[0]
        closest["cap_i"] = userVector[1]
        closest["distances"] = np.sqrt((closest["Scaled_prices"]-closest["price_i"])**2+(closest["Capacity"]-closest["cap_i"])**2)
        return closest["distances"].nsmallest(n)
    
    # Filtrado a partir de las necesidades
    def filterOptions(self, categoryScaler, activityType, activityCategory, closest, budget, people):
        vectors_processed = self.services.copy()
        vectors_processed["Price"] = vectors_processed["Price"]*categoryScaler
        vectors_processed["Scaled_prices"] = vectors_processed["Scaled_prices"]*categoryScaler
        vectors_processed = vectors_processed[(vectors_processed["Type_"+activityType]==1) 
                                            #& (vectors_processed["Category_"+activityCategory]==1) 
                                            & (vectors_processed[closest]==1) 
                                            & (vectors_processed["Scaled_prices"]<=budget) 
                                            & (vectors_processed["Capacity"].astype(int) >= people)]
        vectors_processed = vectors_processed[["Scaled_prices", "Capacity"]].astype(int)
        return vectors_processed

    # Procesamiento del vector de entrada
    def processInput(self, location, userClass, budget, people, activityType, activityCategory):
        pos_i = self.scaler_location.transform([location])
        scaler = self.categoryScaler[userClass]
        budget = self.scaler_prices.transform([[budget]])[0][0]
        user_vector = [budget, people]
        self.closest = self.nearestLocation(pos_i[0], self.locations)
        targetVectors = self.filterOptions(scaler, activityType, activityCategory, self.closest , budget, people)
        return user_vector, targetVectors

    # Calculo de la ubicacion más cercana 
    def nearestLocation(self, origin, locations):
        distance = []
        for location in locations.keys():
            distance.append(math.dist(origin, locations[location]))
        distance = np.array(distance)
        return list(locations.keys())[distance.argmin()]

    # Procesamiento de los datos
    def dataProcessing(self):
        self.services = self.services[self.services["x_typePyS"]!="Cita Médica"]
        self.services = self.services[self.services["x_typePyS"]!="Material-artículo"]
        self.services["x_typePyS"] = self.services["x_typePyS"].apply(lambda x: x.replace("Prácticas Libres", "Practica Libre"))
        self.services = self.services.reset_index(drop=True)
        self.services["Type"] = self.services["displayName"].apply(lambda x: self.setActivityType(x))
        self.services["Capacity"] = self.services["displayName"].apply(lambda x: self.setActivityCapacity(x))
        for location in self.locations.keys():
            self.services[location] = 0
            self.services[location] = self.services[location].apply(lambda x: random.randint(0,1))
        self.services.rename(columns={"x_typePyS": "Category", "salePrice":"Price"}, inplace=True)
        self.services = pd.get_dummies(self.services, columns=['Type', "Category"])
        self.services = self.services.drop(columns=["listPrice"], axis=0)
        #scalers
        scaler_prices = StandardScaler()
        scaled_price = scaler_prices.fit_transform(self.services[["Price"]]).flatten()
        self.services["Scaled_prices"] = scaled_price
        coords = [ubi for ubi in self.locations.values()]

        # Inicializa el StandardScaler
        scaler_location = StandardScaler()
        scaled_coords = scaler_location.fit_transform(coords)
        for i, ubicacion in enumerate(self.locations.keys()):
            self.locations[ubicacion] = scaled_coords[i].tolist()

        return scaler_prices, scaler_location

    # Generacion del dataset
    def setActivityType(self, name):
        punctuation = string.punctuation
        name = name.lower()
        name = unidecode.unidecode(name)
        name = name.replace(punctuation, " ")
        recreation = ["pasadia", 'campamento', "parque", "travesia", "laberinto", "dia", "caminata"]
        competence = ["campeonato", 'copa']
        education = ["academia", 'curso', "clase", "taller"]
        if any(ext in name for ext in recreation):
            activityType = "Recreación"
        elif any(ext in name for ext in education):
            activityType = "Educación"
        elif any(ext in name for ext in competence):
            activityType = "Competencia"
        else:
            activityType = "Deportes"
        return activityType
    
    # Generacion del dataset
    def setActivityCapacity(self, name):
        punctuation = string.punctuation
        name = name.lower()
        name = unidecode.unidecode(name)    
        name = name.replace(punctuation, " ")
        capacity = re.findall(r'\d+', name)
        if len(capacity) == 0:
            capacity = random.randint(1, 10)
        else:
            capacity = capacity[0]
        return capacity
