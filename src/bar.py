import matplotlib.pyplot as plt
import pandas as pd
from src.classes import Intrant
from decimal import ROUND_HALF_UP, Decimal
from typing import List

def makeBar(firstTab:[], secondTab:[], text:str, text_x:str, text_y:str):
    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.attributes('-zoomed', True)
    plt.bar(firstTab, secondTab, color='b', alpha=0.7)
    plt.title(text)
    plt.xlabel(text_x)
    plt.ylabel(text_y)
    plt.grid(axis='y', linestyle='--', alpha=0.7)

def makeOneBar(firstTab:[], secondTab:[], text:str, text_x:str, text_y:str) -> bool:
    if (len(firstTab) == 1):
        return False
    makeBar(firstTab, secondTab, text, text_x, text_y)
    plt.show()
    return True

def makeTwoBar(firstTab:[], secondTab:[], firstTab2:[], secondTab2:[] , text:str, text2:str, text_x:str, text_y:str, text_y2:str) -> bool:
    if (len(firstTab) == 1 or len(firstTab2) == 1):
        return False
    plt.subplot(1, 2, 1)
    makeBar(firstTab, secondTab, text, text_x, text_y)
    plt.subplot(1, 2, 2)
    makeBar(firstTab2, secondTab2, text2, text_x, text_y2)
    plt.show()
    return True

def doseOnSurface(data: List[Intrant]) -> bool:
    parsedList = [intrant for intrant in data if intrant.surface <= 50]

    df = pd.DataFrame({'Surface': [phyto.surface.quantize(Decimal('1'), rounding=ROUND_HALF_UP) for phyto in parsedList],
                   'Dose': [phyto.dose for phyto in parsedList]})

    df_mean = df.groupby('Surface', as_index=False)['Dose'].mean()

    return makeOneBar(df_mean['Surface'], df_mean['Dose'], 'Moyenne de la dose en fonction de la surface', 'Surface (ha)', 'Moyenne de la dose utilisée')

def quantiteOnTime(data:List[Intrant]) -> bool:
    result_dict = {}
    count_dict = {}
    for intrant in data:

        if intrant.date.year in result_dict:
            count_dict[intrant.date.year] += 1
            result_dict[intrant.date.year] += int(intrant.quantite)
        else:
            count_dict[intrant.date.year] = 1
            result_dict[intrant.date.year] = int(intrant.quantite)
    return makeTwoBar(list(result_dict.keys()), list(result_dict.values()), list(count_dict.keys()), list(count_dict.values()), 'Quantité utilisée en fonction de l\'année', 'Nombre d\'utilisations en fonction de l\'année', 'Temps', 'Somme de la quantité utilisée', 'Nombre d\'utilisations')