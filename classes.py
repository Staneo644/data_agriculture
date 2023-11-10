from decimal import Decimal
import datetime
from typing import List 

class Intrant:
    def __init__(self, date:datetime, plante, travail, numero_parcelle:int, dose:Decimal, surface:Decimal, quantite:Decimal, unite:str):
        self.date = date
        self.plante = plante
        self.travail = travail
        self.numero_parcelle = numero_parcelle
        self.dose = dose
        self.quantite = quantite
        self.surface = surface
        self.unite = unite


class Phyto(Intrant):
    def __init__(self, date:datetime, plante, travail, numero_parcelle, dose:int, surface:Decimal, quantite:Decimal, unite:str, amm_id):
        super().__init__(date, plante, travail, numero_parcelle, dose, surface, quantite, unite)
        self.amm_id = amm_id


class DataPhyto():
    def __init__(self, amm_id, name, type):
        self.amm_id = amm_id
        self.name = name
        self.conditions = []
        self.type = type

    def addCondition(self, condition):
        self.conditions.append(condition)

    def checkValue(self, name, type):
        if (name != self.name or type != self.type):
            return False
        return True
    
# def FindPhyto(amm_id:int, list: List[DataPhyto]):

#     for i in range(0, len(list)):
#         if (list[i].amm_id == amm_id):
#             return list[i]
#     return False


def FindPhyto(data_list:List[DataPhyto], amm_id:int) -> DataPhyto:
    low = 0
    high = len(data_list) - 1

    while low <= high:
        mid = (low + high) // 2

        if data_list[mid].amm_id == amm_id:
            return data_list[mid]
        elif data_list[mid].amm_id < amm_id:
            low = mid + 1
        else:
            high = mid - 1

    return False