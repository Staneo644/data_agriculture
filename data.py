import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from parsing import get_plante_dict, get_code_dict, checkData, load_data, get_data_phyto
from classes import Intrant
from typing import List



file_name = 'Raw_AgroEdi___Export_EDI_prepared.csv'
phyto_data = 'produits_condition_emploi_utf8.csv'


data = pd.read_csv(file_name)
data_phyto = pd.read_csv(phyto_data, sep=';')

def load_datas() -> List[Intrant]:
    ret = []

    for index, row in data.iterrows():
        
        date = datetime.strptime(str(row['debut_traitement']), "%Y%m%d")
        plante = row['espece_botanique_title']
        travail = row['type_travail_title']
        numero_parcelle = row['id_parcelle_pv']
        dose = row['dose']

        surface = row['surface_evt']
        unite = row['unite_intrant']
        ret.append(Intrant(date, plante, travail, numero_parcelle, dose, surface, unite))


    type_travail_column = data['type_travail_title']
    print(type_travail_column.value_counts())
    type_plante_column = data['espece_botanique_title']
    print(type_plante_column.value_counts())
    type_uc_column = data['uc_name']
    print(type_uc_column.value_counts())
    print(type_uc_column.__len__())

    type_travail_code_column = data['type_travail_code']
    print(type_travail_code_column.value_counts())
    type_unite_intrant_column = data['unite_intrant']
    print(type_unite_intrant_column.value_counts())


    return data

plant_dict = get_plante_dict(data)
code_dict = get_code_dict(data)
phytoList = get_data_phyto(data_phyto)
intrantList = load_data(data, phytoList)
if (plant_dict == {} or code_dict == {} or phytoList == [] or not checkData(data) or intrantList == []):
    print("Erreur dans les données")
    exit()
print("Données chargées avec succès")
#print(str(intrantList))
#data = load_data()