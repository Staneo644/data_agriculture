from decimal import ROUND_HALF_UP, Decimal
import pandas as pd
from src.parsing import get_plante_dict, get_code_dict, checkData, load_data, get_data_phyto
from src.classes import FindPhyto
from src.pieChart import plantPieChart, productPieChart, typeOfProductPieChart, workTypePieChart
from src.barChart import doseToSurfaceBarChart, numberToTimeBarChart
from args import file_name, phyto_data
from args import amm_id, show, plant

data = pd.read_csv(file_name)
data_phyto = pd.read_csv(phyto_data, sep=';')

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
        print("Quantité : " + str(phytoList[0].quantity))
        print("Unité : " + str(phytoList[0].unite))
        exit()
    print("Ce produit a été utilisé " + str(len(phytoList)) + " fois")
    print("Unité : " + str(phytoList[0].unite))
    print("Surface moyenne : " + str((sum([phyto.surface for phyto in phytoList]) / len(phytoList)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))
    print("Dose moyenne : " + str((sum([phyto.dose for phyto in phytoList]) / len(phytoList)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)))
    print("Dose maximale utilisée : " + str(max([phyto.dose for phyto in phytoList])))
    print("Dose minimale utilisée : " + str(min([phyto.dose for phyto in phytoList])))
    if (plantPieChart(phytoList, plant_dict) == False):
        print("La seule utilisation du produit est sur des " + plant_dict[phytoList[0].plante])
    if (numberToTimeBarChart(phytoList) == False):
        print("La seule utilisation du produit est en " + str(phytoList[0].date.year))

if (show == 'intrant'):
    intrantList = intrantList + phytoList
    print("Nombre d'intrants : " + str(len(intrantList)))
    numberToTimeBarChart(intrantList)
    plantPieChart(intrantList, plant_dict)
    workTypePieChart(intrantList, code_dict)
    doseToSurfaceBarChart(intrantList)  

if (show == 'phyto'):
    print("Nombre de produits phytosanitaires : " + str(len(phytoList)))
    typeOfProductPieChart(phytoList, phytoDoc)
    productPieChart(phytoList, phytoDoc)
    plantPieChart(phytoList, plant_dict)
    doseToSurfaceBarChart(phytoList)

if (plant in plant_dict):
    print("\nRecherche pour " + plant_dict[plant])
    plantList = [element for element in phytoList if element.plante == plant]
    print("Nombre de " + plant_dict[plant] +  " prises : " + str(len(plantList)))
    if (productPieChart(plantList, phytoDoc) == False):
        print("\nCette plante est traitée uniquement avec du " + FindPhyto(phytoDoc, plantList[0].amm_id).name)
    if (typeOfProductPieChart(plantList, phytoDoc) == False):
        print ("\nCette plante est traitée uniquement avec des produits " + FindPhyto(phytoDoc, plantList[0].amm_id).type)
    numberToTimeBarChart(plantList)
    doseToSurfaceBarChart(plantList)