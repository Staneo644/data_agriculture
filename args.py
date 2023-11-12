import sys
import argparse

file_name = './asset/Raw_AgroEdi___Export_EDI_prepared.csv'
phyto_data = './asset/produits_condition_emploi_utf8.csv'

verbose = False

parser = argparse.ArgumentParser(description='Description de votre programme.')

parser.add_argument('--product', type=int, default=-1, help='Description de l\'argument --product')
args = parser.parse_args()
amm_id = args.product
print(amm_id)

if ("--verbose" in sys.argv or "-v" in sys.argv):
    verbose = True