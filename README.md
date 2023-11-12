# data_agriculture
reading a CSV file and get informations with python


Lancez "python data.py" dans un terminal pour executer le script. Vous pouvez ajouter l'argument "--product={numéro AMM du produit}", pour avoir les informations sur le produit, l'argument --show={phyto / intrant} pour avoir une vue d'ensemble des bases de données, et l'argument "--plant={nom de code plante}" pour avoir toutes les informations sur le traitement de la plante. Les noms de codes des plantes correspondent à ce qu'il y a dans la base donnée "Raw_AgroEdi", les codes sont retranscrits en bas du README.

Les informations vont se retrouver sur le terminal ainsi que par des fenêtres qui s'ouvriront. Fermez chaque fenêtre pour avoir accès à la fenêtre qui suit.

Si vous souhaitez voir les erreurs et les logs, vous pouvez ajouter l'argument "--verbose" ou "-v"




# Exemples d'utilisation

python data.py --product=8700462

python data.py --product=2110102

python data.py --plant=ZDH

python data.py --show=intrant

python data.py --show=phyto




# Cas d'erreurs

Le code ne s'executera pas si dans la bases de données "Raw_AgroEdi", la valeur "id_parcelle_pv" n'est pas égal à "id_parcelle_vi", si à un moment, pour les espèces botaniques ou la forme de travail, un clé n'a pas la même valeur qu'avant et une valeur n'a pas la même clé qu'avant

Un élément ne sera pas incorporé si la date de début de traitement précède le premier janvier 2017 ou succède à aujourd'hui Les dates ne contenant que l'année sont définit comme du premier janvier. Il ne sera pas non plus incorporé si la dose de traitement multiplié par la surface ne vaut pas la quantité (tronqué au dixième, ou mis à la valeur supérieur au dixième) ou si la quantité a une valeur qui semble exagérée (supérieure à 10 000 000). 
Si l'élément n'a pas de d' "espece_botanique_title" ou de "type_travail_title", il ne sera pas non plus incorporé. Enfin, si l'AMM n'est pas retrouvé dans la base de donnée "produits_condition_emploie", il ne sera pas non plus incorporé.

Le code ne s'execute pas dans la base de donnée "produits_condition_emploie", si un nom de produit apparaît sur deux AMM, si un AMM a deux noms différent ou si un AMM a deux type de produits différents.



# Noms de codes

ZAG: Ail

ZOH: Autres ornementales

ZAM: Avoine

E31: Avoine nue

ZAP: Betterave

ZAQ: Blé dur

ZAR: Blé tendre

ZAV: Carotte

ZAX: Céleri

ZAZ: Chanvre

ZBA: Chicorée

ZBB: Chou


ZBE: Colza

E90: Courge

ZBI: Courgette

ZBJ: Dactyle

ZBK: Echalote

ZBM: Epeautre

ZBN: Epinard

ZOJ: Espèces diverses

ZBQ: Fétuque élevée

F15: Fétuque rouge

ZBS: Fève

ZBT: Fèverole

ZCA: Haricot

ZCL: Lin

ZCN: Lupin blanc

ZCQ: Luzerne

ZCS: Maïs

H69: Mélange

ZDA: Moutarde blanche

ZDF: Oeillette (pavot)

ZDG: Oignon

ZDH: Orge

ZDL: Phacélie

ZDN: Poireau

ZDO: Pois

ZOD: Pois chiche

ZDS: Pomme de terre

ZDU: Prairie

ZDX: Ray-grass anglais

ZDZ: Ray-grass d'Italie

ZEJ: Seigle

G55: Seigle forestier

ZEL: Soja

ZMB: Tournesol

ZMC: Trèfle violet

ZMI: Triticale

ZMK: Vesce commun
