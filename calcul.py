#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 29 12:26:24 2020

@author: ian
"""

import pandas as pd
import numpy as np
import requests

# un premier test à partir des données importés dans excel du HTML corrigé avec une connection direct
# on peut se raccorder directement au donnée avec pandas
stats_detail = pd.read_html("https://www.hockey-reference.com/playoffs/NHL_2020_skaters.html", header=1)[0]
detail = pd.DataFrame(stats_detail)

path1= "choix.xlsx"

les_choix = pd.read_excel(path1, header=0)
les_choix.fillna(0, inplace=True)

stats = detail[['Player', 'G', 'A', 'PTS']]
stats.fillna(0, inplace=True)

#fonction qui fait une iteration de tous les joueurs choisi et va chercher les stats à jour
#complète ensuite le fichier de choix
def calcul_point():
    for i in range(len(les_choix)):
      if les_choix.iloc[i,1]:
        joueur = stats[stats.Player == les_choix.iloc[i,1]]
        try :
          nb_but = int(joueur.G)
          nb_pass = int(joueur.A)
          nb_pts = int(joueur.PTS)
          les_choix.iloc[i,2] = nb_but
          les_choix.iloc[i,3] = nb_pass
          les_choix.iloc[i,4] = nb_pts
        except:
            continue

calcul_point()

#fait un sommaire par pooler
les_choix.sort_values('total', ascending=False, inplace=True)
sommaire = les_choix.groupby(['pooler']).sum()
sommaire.sort_values('total',ascending=False,inplace=True)
sommaire_joueur = les_choix.groupby(['pooler', 'nom']).sum()
sommaire_joueur.sort_values(['pooler','total'], ascending=False, inplace=True)

#une routine pour combiner les résultats du pool dans un seul fichier excel
with pd.ExcelWriter('classement.xlsx') as writer:  
    sommaire.to_excel(writer, sheet_name='classement')
    les_choix.to_excel(writer, sheet_name='pointage')
    stats.to_excel(writer, sheet_name='stat_detail')
sommaire_joueur.to_html('./templates/pointage.html')
#sommaire.to_html('./templates/classement.html')

print(sommaire)
