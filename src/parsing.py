import pandas as pd
from datetime import datetime
from typing import List, Tuple
from decimal import ROUND_DOWN, ROUND_UP, Decimal, InvalidOperation
from args import verbose
from src.classes import Intrant, DataPhyto, Phyto

def get_phyto_by_amm_id(amm_id:int, data_phyto:List[DataPhyto]) -> DataPhyto:
    for phyto in data_phyto:
        if (phyto.amm_id == amm_id):
            return phyto
    return False

def get_data_phyto(data:pd.DataFrame) -> List[DataPhyto]:

    ret = []
    for i in range(0, len(data)):
        amm_id = (data.iloc[i])[1]
        if (not ('-' in str(amm_id) or '+' in str(amm_id) or '/' in str(amm_id))) :#and not math.isnan(amm_id)):
            amm_id = int(amm_id)
            name = data['nom produit'][i]
            type = data['type produit'][i]
            condition_categorie = data.iloc[i][3]
            condition_libelle = data.iloc[i][4]
            find_phyto = get_phyto_by_amm_id(amm_id, ret)
            if (not find_phyto):
                p = DataPhyto(int(amm_id), name, type)
                p.addCondition([condition_libelle, condition_categorie])
                ret.append(p)
            else:
                if (not find_phyto.checkValue(name, type)):
                    if (verbose):
                        print("\n\nPhyto invalide : amm_id identique mais nom ou type different")
                    return []
                find_phyto.addCondition([condition_libelle, condition_categorie])
    if (verbose):
        print("\n\nPhyto :" + str(len(ret)))
    sorted_ret = sorted(ret, key=lambda x: x.amm_id)
    return sorted_ret

def checkData(data:pd.DataFrame) -> bool:

    parcelles_dif = data[data['id_parcelle_pv'] != data['id_parcelle_vi']]
    if (parcelles_dif.__len__() > 0):
        if (verbose):
            print("\n\nParcelles differentes : " + str(parcelles_dif))
        return False
    return True

def get_date(data:pd.DataFrame, index:int) -> datetime or bool:
    date_format = "%Y%m%d"
    type_date_column = data['debut_traitement'][index]
    precedent_date = datetime(2017, 1, 1)

    text = str(type_date_column)
    date = datetime.strptime(text + "0101" if len(text) < 8 else text[:8], date_format)
    if (date < precedent_date or date > datetime.now()):
        if (verbose):
            print("date invalide pour l'élément : " + str(index))
        return False
    return date
        
def get_dose(data:pd.DataFrame, index:int) -> Tuple[Decimal, Decimal, Decimal] :
    dose_column = data['dose'][index]
    surface_column = data['surface_evt'][index]
    quantity_column = data['quantite_intrant'][index]
    result = 0
    try:
        dose_decimal = Decimal(dose_column.replace(',', '.'))
        surface_decimal = Decimal(surface_column.replace(',', '.'))
        quantity_decimal = Decimal(quantity_column.replace(',', '.'))
        if (quantity_decimal > 10000000):
            return [0, 0, 0]
        result = ((dose_decimal * surface_decimal).quantize(Decimal('0.1'), rounding=ROUND_UP), (dose_decimal * surface_decimal).quantize(Decimal('0.1'), rounding=ROUND_DOWN))
        if (quantity_decimal.quantize(Decimal('0.1'), rounding=ROUND_UP) not in result and quantity_decimal.quantize(Decimal('0.1'), rounding=ROUND_DOWN) not in result):
            return [0, 0, 0]
        return [dose_decimal, surface_decimal, quantity_decimal]
    except InvalidOperation:
        return [0, 0, 0]

def get_amm_id(data: pd.DataFrame, index:int, data_phyto:List[DataPhyto]) -> int:

    amm_id = data['amm_id'][index]
    
    for phyto in data_phyto:
        if (phyto.amm_id == amm_id):
            return amm_id
    return False

def get_plante_dict(data: pd.DataFrame) -> dict:
    ret = {}
    for i in range(0, len(data)):
        title = data['espece_botanique_title'][i]
        if (title.__class__ != 0.1.__class__):
            code = data['espece_botanique_code'][i]
            if code in ret:
                if ret[code] != title:
                    if (verbose):
                        print("\n\nplante invalide : lignes de codes identique")
                    return {}
            elif title in ret.values():
                if (verbose):
                    print("\n\nplante invalide : valeurs identiques")
                return {}
            else:
                ret[code] = title
    if (verbose):
        print('\n\n Plantes :' + str(ret))
    return ret


def get_code_dict(data: pd.DataFrame) -> dict:
    ret = {}

    for i in range(0, len(data)):
        title = data['type_travail_title'][i]
        if (title.__class__ != 0.1.__class__):
            code = data['type_travail_code'][i]
            if code in ret:
                if ret[code] != title:
                    if (verbose):
                        print("\n\ntravail invalide : lignes de codes identique")
                    return {}
            elif title in ret.values():
                if (verbose):
                    print("\n\ntravail invalide : valeurs identiques")
                return {}
            else:
                ret[code] = title
    if (verbose):
        print('\n\n Travail :' + str(ret))
    return ret


def load_data(data: pd.DataFrame, phyto: List[Phyto], plante_dict:dict, code_dict:dict) -> tuple[List[Intrant], List[Phyto]]:
    retIntrant = []
    retPhyto = []
    surface_max = 0
    surface_min = 100000
    rejected_data = 0

    for index, row in data.iterrows():
        dose, surface, quantity = get_dose(data, index)
        if (dose == 0 or surface == 0 or quantity == 0):
            if (verbose):
                print("\n\nDose invalide, numéro : " + str(index))
            rejected_data += 1
            continue

        date = get_date(data, index)
        if (date == False):
            if (verbose):
                print("\n\nDate invalide, numéro : " + str(index))
            rejected_data += 1
            continue

        plante = row['espece_botanique_code']
        if (not plante in plante_dict):
            if (verbose):
                print("\n\nPlante invalide, numéro : " + str(plante))
            rejected_data += 1
            continue
        travail = row['type_travail_code']
        if (not travail in code_dict):
            if (verbose):
                print("\n\nTravail invalide, numéro : " + str(travail))
            rejected_data += 1
            continue
        numero_parcelle = row['id_parcelle_pv']
        unite = row['unite_intrant']
        if (surface > surface_max):
            surface_max = surface
        if (surface < surface_min):
            surface_min = surface
        if (travail == 'SEX'):
            amm_id = get_amm_id(data, index, phyto)
            if (amm_id > 0):
                retPhyto.append(Phyto(date, plante, travail, numero_parcelle, dose, surface, quantity, unite, amm_id))
            else:
                rejected_data += 1
        else:
            retIntrant.append(Intrant(date, plante, travail, numero_parcelle, dose, surface, quantity,  unite))
    if (verbose):
        print("\n\nSurface max : " + str(surface_max) + " Surface min : " + str(surface_min))
        print("\n\n" + str(rejected_data) + " valeurs ont été rejeté car elles ne possédaient pas les bons critères")
    return retIntrant, retPhyto

