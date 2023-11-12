from decimal import ROUND_HALF_UP, Decimal
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import seaborn as sns
from src.parsing import get_plante_dict, get_code_dict, checkData, load_data, get_data_phyto
from src.classes import FindPhyto, Intrant
from typing import List
from src.camember import speciesCount, productCount, typeProduct, workCount
from src.bar import doseOnSurface, quantiteOnTime
from args import file_name, phyto_data
from args import amm_id, show, plant, verbose




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

plant_dict = get_plante_dict(data)
code_dict = get_code_dict(data)
phytoDoc = get_data_phyto(data_phyto)
intrantList, phytoList = load_data(data, phytoDoc, plant_dict, code_dict)
if (plant_dict == {} or code_dict == {} or phytoDoc == [] or not checkData(data) or intrantList == []):
    print("Erreur dans les données")
    exit()
print("Données chargées avec succès")

if (amm_id >= 0):
    doc = FindPhyto(phytoDoc, amm_id)
    if (doc == False):
        print("Aucun produit phytosanitaire trouvé avec cet amm_id")
        exit()
    print("\nNom du produit : " + doc.name)
    print("\nType du produit : " + doc.type)
    print("\n\nConditions d'utilisation : ")
    for condition in doc.conditions:
        label, text = condition
        if (label.startswith('Condition: ')):
            label = label[11:]
        print(f'{text} : {label}\n')
    phytoList = [phyto for phyto in phytoList if phyto.amm_id == amm_id]
    if (phytoList == []):
        print("Ce produit n'a pas été utilisé")
        exit()
    print("Produit phytosanitaire trouvé avec succès")
    if (len(phytoList) == 1):
        print("Ce produit n'a été utilisé qu'une seule fois")
        print("Date : " + str(phytoList[0].date))
        print("Plante : " + str(phytoList[0].plante))
        print("Travail : " + str(phytoList[0].travail))
        print("Numéro de parcelle : " + str(phytoList[0].numero_parcelle))
        print("Dose : " + str(phytoList[0].dose))
        print("Surface : " + str(phytoList[0].surface))
        print("Quantité : " + str(phytoList[0].quantite))
        print("Unité : " + str(phytoList[0].unite))
        exit()
    print("Ce produit a été utilisé " + str(len(phytoList)) + " fois")
    print("Unité : " + str(phytoList[0].unite))
    print("Surface moyenne : " + str((sum([phyto.surface for phyto in phytoList]) / len(phytoList)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))
    print("Dose moyenne : " + str((sum([phyto.dose for phyto in phytoList]) / len(phytoList)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))
    print("Dose maximale : " + str(max([phyto.dose for phyto in phytoList])))
    print("Dose minimale : " + str(min([phyto.dose for phyto in phytoList])))
    if (speciesCount(phytoList, plant_dict) == False):
        print("La seule utilisation du produit est sur des " + plant_dict[phytoList[0].plante])
    if (quantiteOnTime(phytoList) == False):
        print("La seule utilisation du produit est en " + str(phytoList[0].date.year))

if (show == 'intrant'):
    intrantList = intrantList + phytoList
    print("Nombre d'intrants : " + str(len(intrantList)))
    quantiteOnTime(intrantList)
    speciesCount(intrantList, plant_dict)
    workCount(intrantList, code_dict)
    doseOnSurface(intrantList)  

if (show == 'phyto'):
    print("Nombre de produits phytosanitaires : " + str(len(phytoList)))
    typeProduct(phytoList, phytoDoc)
    productCount(phytoList, phytoDoc)
    speciesCount(phytoList, plant_dict)
    doseOnSurface(phytoList)

if (plant in plant_dict):
    print("\nRecherche pour " + plant_dict[plant])
    plantList = [element for element in phytoList if element.plante == plant]
    print("Nombre de " + plant_dict[plant] +  " prises : " + str(len(plantList)))
    if (productCount(plantList, phytoDoc) == False):
        print("\nCette plante est traitée uniquement avec du " + FindPhyto(phytoDoc, plantList[0].amm_id).name)
    if (typeProduct(plantList, phytoDoc) == False):
        print ("\nCette plante est traitée uniquement avec des produits " + FindPhyto(phytoDoc, plantList[0].amm_id).type)
    quantiteOnTime(plantList)
    doseOnSurface(plantList)




# fig, axs = plt.subplots(3, 3, figsize=(10, 5))
# doseOnSurface(phytoList)
# quantiteOnTime(intrantList)
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