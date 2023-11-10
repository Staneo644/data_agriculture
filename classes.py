from decimal import Decimal
import datetime 

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