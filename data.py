import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from src.parsing import get_plante_dict, get_code_dict, checkData, load_data, get_data_phyto
from src.classes import Intrant
from typing import List
from src.camember import speciesCount, productCount, typeProduct
from src.bar import doseOnSurface, quantiteOnTime
from args import file_name, phyto_data





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

type_amm_column = data['amm_id']
print(type_amm_column.value_counts())
print(type_amm_column.__len__())

plant_dict = get_plante_dict(data)
code_dict = get_code_dict(data)
phytoDoc = get_data_phyto(data_phyto)
intrantList, phytoList = load_data(data, phytoDoc, plant_dict, code_dict)
if (plant_dict == {} or code_dict == {} or phytoDoc == [] or not checkData(data) or intrantList == []):
    print("Erreur dans les données")
    exit()
print("Données chargées avec succès")

# fig, axs = plt.subplots(3, 3, figsize=(10, 5))
# doseOnSurface(phytoList)
# quantiteOnTime(intrantList)
typeProduct(phytoList, phytoDoc)
# speciesCount(intrantList, plant_dict)
# productCount(phytoList, phytoDoc)

# doses = [phyto.dose for phyto in intrantList]

# productCount(phytoList, phytoDoc)

# plt.hist(doses, bins=20, color='blue', alpha=0.7)
# plt.title('Distribution des doses de produits phytosanitaires')
# plt.xlabel('Dose')
# plt.ylabel('Fréquence')
# plt.show()

# plt.figure(0)
# date = np.arange(0,2*np.pi,0.1)   # start,stop,step
# y = np.sin(x)
# z = np.cos(x)
# plt.plot(x,y,x,z)
# plt.legend(['sin(x)', 'cos(x)'])     
# plt.show()

# types_de_travail = [intrant.travail for intrant in intrantList]

# sns.countplot(x=types_de_travail)
# plt.title('Répartition des types de travaux')
# plt.xlabel('Type de travail')
# plt.ylabel('Nombre d\'occurrences')
# plt.show()
#print(str(intrantList))
#data = load_data()