import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def load_data():
    data = pd.read_csv('Raw_AgroEdi___Export_EDI_prepared.csv')
    type_travail_column = data['type_travail_title']
    print(type_travail_column.value_counts())
    type_plante_column = data['espece_botanique_title']
    print(type_plante_column.value_counts())
    type_uc_column = data['uc_name']
    print(type_uc_column.value_counts())
    print(type_uc_column.__len__())

    type_travail_code_column = data['type_travail_code']
    print(type_travail_code_column.value_counts())
    type_unite_intrant_column = data['unite_intrant']
    print(type_unite_intrant_column.value_counts())

    parcelles_dif = data[data['id_parcelle_pv'] != data['id_parcelle_vi']]
    print(parcelles_dif.__len__())

    return data


data = load_data()