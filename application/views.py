from pyexpat.errors import messages
from django.shortcuts import redirect, render
from django.http import JsonResponse
import numpy as np
import matplotlib.pyplot as plt 
import pandas as pd 
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics
# Create your views here.

def prediction(request):
    return render(request, 'main/predictionPage.html')

def result(request):
    
    df2 = pd.read_csv('static/file/mubawab_listings_eda.csv')
    df2.dropna(inplace=True)  
    df3 = df2.drop(['Other_tags'], axis=1)
    df5=df3
                        # Extrait la colonne 'Type' de df5
    t = df2['Type']

    # Crée le mapping de types vers des valeurs numériques
    type_mapping = {
        'Riad': 0,
        'Maisons': 1,
        'Appartements': 2,
        'Villas': 3
    }

    # Applique le mapping à la colonne 'Type' dans df5 pour créer 'Type_Numeric'
    df5['Type_Numeric'] = df5['Type'].map(type_mapping)

    c = df2['Current_state']

    # Crée le mapping de types vers des valeurs numériques
    type_mappingg = {
        'Bon état': 0,
        'Nouveau': 1,
        'À rénover':2,
        
        
    }
    # Applique le mapping à la colonne 'Type' dans df5 pour créer 'Type_Numeric'
    df5['Current_state_Numeric'] = df5['Current_state'].map(type_mappingg)

    j = df2['Localisation']

    type_mappinggg = {
        'Anfa':0,
        'La Gironde':1,
        'Bourgogne Ouest':2,
        'Les princesses':3,
        "Triangle d'Or":4,
        'Californie':5,
        'Maârif':6,
        'Racine':7,
        'Gauthier':8,
        'Val Fleury':9,
        'Sidi Maarouf':10,
        'Ain Diab':11,
        'Casablanca Finance City':12,
        'Palmier':13,
        'Oasis':14,
        'CIL (Hay Salam)':15,
        'Maârif Extension':16,
        'Ain Diab Extension':17,
        'Mers Sultan':18,
        'Longchamps (Hay Al Hanâa)':19,
        'Oulfa':20,
        'Les Hôpitaux':21,
        'Aïn Sebaâ':22,
        'Polo':23,
        'Anfa Supérieur':24,
        'Hermitage':25,
        'Belvédère':26,
        
        
    }

    df5['Localisation_Numeric'] = df5['Localisation'].map(type_mappinggg)
    df6 = df5
    df6.dropna()
    df7 = df6.drop(['Localisation','Current_state','Type','Age','Price_m2'], axis=1)  
    df7.head()
    x=df7.drop('Price', axis=1)
    y=df7['Price']
    x_train, x_test, y_train, y_test = train_test_split(x,y,test_size=.30)
        #TAINING +PREDICTION
    model=LinearRegression()
    model.fit(x_train,y_train)

    
    var1 = float(request.GET.get('aria'))
    var2 = float(request.GET.get('room'))
    var3 = float(request.GET.get('bedroom'))
    var4 = float(request.GET.get('bathromm'))
    var5 = float(request.GET.get('floor'))
    var6 = float(request.GET.get('type'))
    var7 = float(request.GET.get('condition'))
    var8 = float(request.GET.get('location'))

    pred=model.predict(np.array([var1,var2,var3,var4,var5,var6,var7,var8]).reshape(1,-1))
    pred=round(pred[0])
    price = str(pred)
    return render(request,"main/predictionPage.html",{"result":price})

