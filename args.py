import argparse

file_name = './asset/Raw_AgroEdi___Export_EDI_prepared.csv'
phyto_data = './asset/produits_condition_emploi_utf8.csv'



parser = argparse.ArgumentParser(description='Description de votre programme.')

parser.add_argument('--product', type=int, default=-1, help='Description de l\'argument --product')
parser.add_argument('--verbose', '-v', action='store_true', help='Description de l\'argument --verbose')
parser.add_argument('--show', type=str, default='no', help='Description de l\'argument --show')
parser.add_argument('--plant', type=str, default='no', help='Description de l\'argument --plant')

args = parser.parse_args()

amm_id = args.product
verbose = args.verbose
plant = args.plant
show = args.show

