from decimal import ROUND_HALF_UP, Decimal
from src.classes import DataPhyto, FindPhyto, Intrant, Phyto
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

# Modifier la variable ci-dessous si vous souhaitez voir plus ou moins de données dans les diagrammes en camembert, suivant le poucentage "limite"
threshold_percentage = 2

def makeCamembert(result:dict, text:str, some:int):
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.attributes('-zoomed', True)
    filtered_species = {species: count for species, count in result.items() if (count/some) >= (threshold_percentage/100)}
    other = sum(count for count in result.values() if (count/some) < (threshold_percentage/100))
    if (other > 0):
        filtered_species['Autre'] = other
    sorted_result = dict(sorted(filtered_species.items(), key=lambda item: item[1], reverse=False))
    plt.pie(sorted_result.values(), labels=sorted_result.keys(), autopct='%1.1f%%', startangle=90)
    plt.title(text)

def makeOneCamembert(result:dict, text:str, some) -> bool:
    if (len(result) == 1):
        return False
    plt.figure(figsize=(8, 8))
    makeCamembert(result, text, some)
    plt.show()
    return True

def makeTwoCamembert(result:dict, result2:dict, text:str, text2:str, some:int, some2:int) -> bool:
    if (len(result) == 1 or len(result2) == 1):
        return (False)
    plt.subplot(1, 2, 1)
    makeCamembert(result, text, some)
    plt.subplot(1, 2, 2)
    makeCamembert(result2, text2, some2)
    plt.show()
    return True

def speciesCount(data: List[Intrant], plante:dict) -> bool:
    species_counts = {}
    species_quantite = {}

    some = 0
    for entry in data:
        species = entry.plante
        if plante[species] in species_counts:
            species_counts[plante[species]] += 1
            species_quantite[plante[species]] += entry.quantite
        else:
            species_counts[plante[species]] = 1
            species_quantite[plante[species]] = entry.quantite
        some += entry.quantite

    return makeTwoCamembert(species_counts, species_quantite, "Répartition des espèces touchées (en nombre d'utilisations)", "Répartition des espèces touchées (en quantité)", len(data), some)


def productCount(data: List[Phyto], amm:List[DataPhyto]) -> bool:
    product_counts = {}
    product_quantite = {}

    some = 0
    for entry in data:
        species = (FindPhyto(amm,entry.amm_id)).name
        if species in product_counts:
            product_quantite[species] += entry.quantite
            product_counts[species] += 1
        else:
            product_quantite[species] = entry.quantite
            product_counts[species] = 1
        some += entry.quantite
    
    return makeTwoCamembert(product_counts, product_quantite, "Produits les plus utilisés (en nombre d'utilisations)", "Produits les plus utilisés (en quantité)", len(data), some)

def typeProduct(data: List[Phyto], amm:List[DataPhyto]) -> bool:
    product_counts = {}
    product_quantite = {}

    some = 0
    for entry in data:
        species = (FindPhyto(amm, entry.amm_id)).type
        if species in product_counts:
            product_counts[species] += 1
            product_quantite[species] += entry.quantite
        else:
            product_counts[species] = 1
            product_quantite[species] = entry.quantite
        some += entry.quantite
    
    return makeTwoCamembert(product_counts, product_quantite, "Type de produit utilisé (en nombre d'utilisations)", "Type de produit utilisé (en quantité)", len(data), some)

def workCount(data: List[Intrant], work_dict:dict) -> bool:
    species_counts = {}
    species_quantite = {}

    some = 0
    for entry in data:
        work = entry.travail
        if work_dict[work] in species_counts:
            species_counts[work_dict[work]] += 1
            species_quantite[work_dict[work]] += entry.surface
        else:
            species_counts[work_dict[work]] = 1
            species_quantite[work_dict[work]] = entry.surface
        some += entry.surface
    return makeTwoCamembert(species_counts, species_quantite, "Répartition des travaux effectués (en nombre d'utilisations)", "Répartition des travaux effectués (en surface totale travaillée)", len(data), some)
