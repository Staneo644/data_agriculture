from decimal import ROUND_HALF_UP, Decimal
from src.classes import DataPhyto, FindPhyto, Intrant, Phyto
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

threshold_percentage = 2

def makeCamembert(result:dict, text:str, some:int):
    filtered_species = {species: count for species, count in result.items() if (count/some) >= (threshold_percentage/100)}
    other = sum(count for count in result.values() if (count/some) < (threshold_percentage/100))
    if (other > 0):
        filtered_species['Autre'] = other
    sorted_result = dict(sorted(filtered_species.items(), key=lambda item: item[1], reverse=False))
    plt.figure(figsize=(8, 8))
    plt.pie(sorted_result.values(), labels=sorted_result.keys(), autopct='%1.1f%%', startangle=90)
    plt.title(text)
    plt.show()

def speciesCount(data: List[Intrant], plante:dict):
    species_counts = {}

    for entry in data:
        species = entry.plante
        if plante[species] in species_counts:
            species_counts[plante[species]] += 1
        else:
            species_counts[plante[species]] = 1
    makeCamembert(species_counts, "Répartition des espèces touchées (en nombre d'utilisations)", len(data))

def productCount(data: List[Phyto], amm:List[DataPhyto]):
    product_counts = {}

    some = 0
    some_different_product = 0
    for entry in data:
        species = (FindPhyto(amm,entry.amm_id)).name
        if species in product_counts:
            product_counts[species] += entry.quantite
        else:
            product_counts[species] = entry.quantite
            some_different_product += 1
        some += entry.quantite
    
    makeCamembert(product_counts, "Produits les plus utilisés (en quantité), " + str(len(product_counts)) + " produits différents", some)

def typeProduct(data: List[Phyto], amm:List[DataPhyto]):
    product_counts = {}

    some = 0
    for entry in data:
        species = (FindPhyto(amm, entry.amm_id)).type
        if species in product_counts:
            product_counts[species] += entry.quantite
        else:
            product_counts[species] = entry.quantite
        some += entry.quantite
    
    makeCamembert(product_counts, "Type de produit utilisé (en quantité)", some)