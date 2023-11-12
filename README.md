# data_agriculture
reading a CSV file and get informations with python


Lancez "python data.py" dans un terminal pour executer le script

Si vous souhaitez voire les erreurs et les logs, vous pouvez lancer "python data.py --verbose"

Le code ne s'executera pas si dans la bases de données "Raw_AgroEdi", la valeur "id_parcelle_pv" n'est pas égal à "id_parcelle_vi", si à un moment, pour les espèces botaniques ou la forme de travail, un clé n'a pas la même valeur qu'avant et une valeur n'a pas la même clé qu'avant

Un élément ne sera pas incorporé si la date de début de traitement précède le premier janvier 2017 ou succède à aujourd'hui Les dates ne contenant que l'année sont définit comme du premier janvier. Il ne sera pas non plus incorporé si la dose de traitement multiplié par la surface ne vaut pas la quantité (tronqué au dixième, ou mis à la valeur supérieur au dixième). 
Si l'élément n'a pas de d'espece_botanique_title ou de type_travail_title, il ne sera pas non plus incorporé. Enfin, si l'AMM n'est pas retrouvé dans la base de donnée "produits_condition_emploie", il ne sera pas non plus incorporé.

Le code ne s'execute pas si dans la base de donnée "produits_condition_emploie", un nom de produit apparaît sur deux AMM, un AMM a deux noms différent ou un AMM a deux type de produits différents.



