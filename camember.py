from classes import DataPhyto, FindPhyto, Intrant, Phyto
from typing import List
import matplotlib.pyplot as plt
import pandas as pd

threshold_percentage = 2

def makeCamembert(result:dict, text:str):
    sorted_result = dict(sorted(result.items(), key=lambda item: item[1], reverse=False))
    plt.figure(figsize=(8, 8))
    plt.pie(sorted_result.values(), labels=sorted_result.keys(), autopct='%1.1f%%', startangle=90)
    plt.title(text)
    plt.show()

def speciesCount(data: List[Intrant], plante:dict):
    species_counts = {}

    for entry in data:
        species = entry.plante
        if species in species_counts:
            species_counts[species] += 1
        else:
            species_counts[species] = 1
    total_entries = len(data)
    filtered_species = {plante[species]: count for species, count in species_counts.items() if (count/total_entries) >= (threshold_percentage/100)}
    filtered_species['Autre'] = sum(count for count in species_counts.values() if (count/total_entries) < (threshold_percentage/100))
    makeCamembert(filtered_species, "Répartition des espèces touchées (en nombre d'utilisations)'")
    

def productCount(data: List[Phyto], amm:List[DataPhyto]):
    product_counts = {}

    some = 0
    some_different_product = 0
    for entry in data:
        species = entry.amm_id
        value = FindPhyto(amm, species)
        name = value.name if value != False else "Inconnu"
        if species in product_counts:
            product_counts[name] += entry.quantite
        else:
            product_counts[name] = entry.quantite
            some_different_product += 1
        some += entry.quantite
    print(product_counts.items())
    filtered_species = {species: count for species, count in product_counts.items() if (count/some) >= (threshold_percentage/100)}
    filtered_species['Autre'] = sum(count for count in product_counts.values() if (count/some) < (threshold_percentage/100))
    makeCamembert(filtered_species, "Produits les plus utilisés (en quantité), " + str(some_different_product) + " produits différents")

def doseOnSurface(data: List[Intrant]):
    parsedList = [intrant for intrant in data if intrant.surface <= 20]

    df = pd.DataFrame({'Surface': [phyto.surface for phyto in parsedList],
                   'Dose': [phyto.dose for phyto in parsedList]})

    df_mean = df.groupby('Surface').mean().reset_index()

    plt.figure(figsize=(10, 6))
    plt.bar(df_mean['Surface'], df_mean['Dose'], color='b', alpha=0.7)
    plt.title('Moyenne de la dose en fonction de la surface')
    plt.xlabel('Surface (ha)')
    plt.ylabel('Moyenne de la dose utilisée')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()
