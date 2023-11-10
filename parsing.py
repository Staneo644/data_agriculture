#Check if the dates are in the good order (after 2017) 
#Check if the parcelle_pv and parcelle_vi are the same
#Check if the amm_id is valid
#Check if the dose is valid (dose * surface = quantite_intrant)

import pandas as pd
from classes import Intrant, DataPhyto, Phyto
from datetime import datetime
from typing import List
import math
from typing import Tuple
from decimal import ROUND_DOWN, ROUND_UP, Decimal, InvalidOperation
from args import verbose

def get_phyto_by_amm_id(amm_id:int, data_phyto:List[DataPhyto]) -> DataPhyto:
    for phyto in data_phyto:
        if (phyto.amm_id == amm_id):
            return phyto
    return False
    


def get_data_phyto(data:pd.DataFrame) -> List[DataPhyto]:

    ret = []
    for i in range(0, len(data)):
        # print(data.iloc[0][1])
        amm_id = (data.iloc[i])[1]
        # print(amm_id)
        # print(amm_id)
        # return []
        # print(math.isnan(amm_id))
        if (not ('-' in str(amm_id) or '+' in str(amm_id) or '/' in str(amm_id))) :#and not math.isnan(amm_id)):
            amm_id = int(amm_id)
            name = data['nom produit'][i]
            type = data['type produit'][i]
            condition_categorie = data.iloc[i][3]
            condition_libelle = data.iloc[i][4]
            find_phyto = get_phyto_by_amm_id(amm_id, ret)
            # print(find_phyto)
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
    return ret

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
        print("date invalide")
        return False
    return date
        
def get_dose(data:pd.DataFrame, index:int) -> Tuple[Decimal, Decimal, Decimal] :
    type_dose_column = data['dose'][index]
    type_surface_column = data['surface_evt'][index]
    type_quantite_intrant_column = data['quantite_intrant'][index]
    # print(type_dose_column)
    # print(type_surface_column)
    # print(type_quantite_intrant_column)
    # print(str(type(type_dose_column)) + " " + str(type(type_surface_column)) + " " + str(type(type_quantite_intrant_column)))
    # if (type_dose_column.__len__() != type_surface_column.__len__() or type_dose_column.__len__() != type_quantite_intrant_column.__len__()):
    #     print("dose invalide")
    #     return False
    # num = 0
    # for i in range(0, type_dose_column.__len__()):
    result = 0
    try:
        dose_decimal = Decimal(type_dose_column.replace(',', '.'))
        surface_decimal = Decimal(type_surface_column.replace(',', '.'))
        quantite_intrant_decimal = Decimal(type_quantite_intrant_column.replace(',', '.'))
        result = [(dose_decimal * surface_decimal).quantize(Decimal('0.1'), rounding=ROUND_UP), (dose_decimal * surface_decimal).quantize(Decimal('0.1'), rounding=ROUND_DOWN) ]
        if (quantite_intrant_decimal.quantize(Decimal('0.1'), rounding=ROUND_UP) not in result and quantite_intrant_decimal.quantize(Decimal('0.1'), rounding=ROUND_DOWN) not in result):
            return [0, 0, 0]
        return [dose_decimal, result, quantite_intrant_decimal]
    except InvalidOperation:
        return [0, 0, 0]

def get_amm_id(data: pd.DataFrame, index:int, data_phyto:List[DataPhyto]) -> int:

    amm_id = data['amm_id'][index]
    
    for phyto in data_phyto:
        if (phyto.amm_id == amm_id):
            return amm_id
    return False

#     type_amm_id_column = data['amm_id']
#     type_culture_phyto_column = data_phyto['numero AMM']
#     amm_id_dict = {}
#     for phyto in data_phyto:
#         if (not ('+' or '/' in str(phyto['numero AMM'])) and  not int(str(phyto['numero AMM'])) in amm_id_dict):
#             amm_id_dict[phyto] = phyto['nom produit']
#     print(amm_id_dict)
#     for phyto in type_culture_phyto_column:
#         if (not ('+' or '/' in str(culture)) ):
#             phyto = int(phyto)
#     print(type_culture_phyto_column)
#     type_culture_phyto_column.sort_values(ascending=True)
#     print(type_amm_id_column.value_counts())
#     print(type_culture_phyto_column.value_counts())
#     for culture in type_amm_id_column:
#         if (not ('+' or '/' in str(culture)) and not math.isnan( culture)):
#             print("//////////////" + str(int(culture)))
        

#         if ((not math.isnan( culture)) and (int(culture)) not in type_culture_phyto_column):

#             print(type_culture_phyto_column.__len__())
#             print("amm id invalide")
#             print(int(culture))
#             return False

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


def load_data(data: pd.DataFrame, phyto: List[Phyto]) -> List[Intrant]:
    ret = []

    for index, row in data.iterrows():
        surface, dose, quantite = get_dose(data, index)
        if (dose == 0 or surface == 0):
            break

        date = get_date(data, index)
        if (date == False):
            break

        plante = row['espece_botanique_code']
        travail = row['type_travail_code']
        numero_parcelle = row['id_parcelle_pv']
        dose = row['dose']

        surface = row['surface_evt']
        unite = row['unite_intrant']
        if (travail == 'SEX'):
            amm_id = get_amm_id(data, index, phyto)
            if (amm_id > 0):
                ret.append(Phyto(date, plante, travail, numero_parcelle, dose, surface, quantite, unite, amm_id))
        else:
            ret.append(Intrant(date, plante, travail, numero_parcelle, dose, surface, quantite,  unite))
    return ret

