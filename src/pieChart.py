from src.classes import DataPhyto, FindPhyto, Intrant, Phyto
from typing import List
import matplotlib.pyplot as plt

# Modifier la variable ci-dessous si vous souhaitez voir plus ou moins de données dans les diagrammes en camembert, suivant le poucentage "limite"
threshold_percentage = 2

def showPieChart(result:dict, text:str, some:int):
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.attributes('-zoomed', True)
    filtered_species = {species: count for species, count in result.items() if (count/some) >= (threshold_percentage/100)}
    other = sum(count for count in result.values() if (count/some) < (threshold_percentage/100))
    if (other > 0):
        filtered_species['Autre'] = other
    sorted_result = dict(sorted(filtered_species.items(), key=lambda item: item[1], reverse=False))
    plt.pie(sorted_result.values(), labels=sorted_result.keys(), autopct='%1.1f%%', startangle=90)
    plt.title(text)

def onePieChart(result:dict, text:str, some) -> bool:
    if (len(result) == 1):
        return False
    plt.figure(figsize=(8, 8))
    showPieChart(result, text, some)
    plt.show()
    return True

def twoPieChart(result:dict, result2:dict, text:str, text2:str, some:int, some2:int) -> bool:
    if (len(result) == 1 or len(result2) == 1):
        return (False)
    plt.subplot(1, 2, 1)
    showPieChart(result, text, some)
    plt.subplot(1, 2, 2)
    showPieChart(result2, text2, some2)
    plt.show()
    return True

def plantPieChart(data: List[Intrant], plante:dict) -> bool:
    species_counts = {}
    species_quantity = {}

    some = 0
    for entry in data:
        species = entry.plante
        if plante[species] in species_counts:
            species_counts[plante[species]] += 1
            species_quantity[plante[species]] += entry.quantity
        else:
            species_counts[plante[species]] = 1
            species_quantity[plante[species]] = entry.quantity
        some += entry.quantity

    return twoPieChart(species_counts, species_quantity, "Répartition des espèces touchées (en nombre d'utilisations)", "Répartition des espèces touchées (en quantité)", len(data), some)


def productPieChart(data: List[Phyto], amm:List[DataPhyto]) -> bool:
    product_counts = {}
    product_quantity = {}

    some = 0
    for entry in data:
        product = (FindPhyto(amm,entry.amm_id)).name
        if product in product_counts:
            product_quantity[product] += entry.quantity
            product_counts[product] += 1
        else:
            product_quantity[product] = entry.quantity
            product_counts[product] = 1
        some += entry.quantity
    
    return twoPieChart(product_counts, product_quantity, "Produits les plus utilisés (en nombre d'utilisations)", "Produits les plus utilisés (en quantité)", len(data), some)

def typeOfProductPieChart(data: List[Phyto], amm:List[DataPhyto]) -> bool:
    product_counts = {}
    product_quantity = {}

    some = 0
    for entry in data:
        species = (FindPhyto(amm, entry.amm_id)).type
        if species in product_counts:
            product_counts[species] += 1
            product_quantity[species] += entry.quantity
        else:
            product_counts[species] = 1
            product_quantity[species] = entry.quantity
        some += entry.quantity
    
    return twoPieChart(product_counts, product_quantity, "Type de produit utilisé (en nombre d'utilisations)", "Type de produit utilisé (en quantité)", len(data), some)

def workTypePieChart(data: List[Intrant], work_dict:dict) -> bool:
    species_counts = {}
    species_quantity = {}

    some = 0
    for entry in data:
        work = entry.travail
        if work_dict[work] in species_counts:
            species_counts[work_dict[work]] += 1
            species_quantity[work_dict[work]] += entry.surface
        else:
            species_counts[work_dict[work]] = 1
            species_quantity[work_dict[work]] = entry.surface
        some += entry.surface
    return twoPieChart(species_counts, species_quantity, "Répartition des travaux effectués (en nombre d'utilisations)", "Répartition des travaux effectués (en surface totale travaillée)", len(data), some)
