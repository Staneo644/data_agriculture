import matplotlib.pyplot as plt
import pandas as pd
from src.classes import Intrant
from decimal import ROUND_HALF_UP, Decimal
from typing import List

def makeBar(firstTab:[], secondTab:[], text:str, text_x:str, text_y:str):
    print(str(len(firstTab))  + " " + str(len(secondTab)))
    print(firstTab)
    print(secondTab)
    plt.figure(figsize=(10, 6))
    plt.bar(firstTab, secondTab, color='b', alpha=0.7)
    plt.title(text)
    plt.xlabel(text_x)
    plt.ylabel(text_y)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()


def doseOnSurface(data: List[Intrant]):
    parsedList = [intrant for intrant in data if intrant.surface <= 50]

    df = pd.DataFrame({'Surface': [phyto.surface.quantize(Decimal('1'), rounding=ROUND_HALF_UP) for phyto in parsedList],
                   'Dose': [phyto.dose for phyto in parsedList]})
    print(df['Surface'].value_counts())

    df_mean = df.groupby('Surface', as_index=False)['Dose'].mean()

    makeBar(df_mean['Surface'], df_mean['Dose'], 'Moyenne de la dose en fonction de la surface', 'Surface (ha)', 'Moyenne de la dose utilisée')

def quantiteOnTime(data:List[Intrant]):
    result_dict = {}
    some = 0
    for intrant in data:

        if (intrant.quantite > 10000000):
            print(intrant.quantite)
            continue

        if intrant.date.year in result_dict:
            result_dict[intrant.date.year] += int(intrant.quantite)
        else:
            result_dict[intrant.date.year] = int(intrant.quantite)
    makeBar(list(result_dict.keys()), list(result_dict.values()), 'Quantité utilisée en fonction de l\'année', 'Temps', 'Moyenne de la quantité utilisée')