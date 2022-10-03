# -*- coding: utf-8 -*-
"""
Created on Wed May  4 19:26:49 2022

@author: Lisa
"""

import pandas as pd
import numpy as np


df_5w  = pd.read_excel('C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo6/5W_Colombia_-_RMRP_2022_Consolidado SEIS_18082022.xlsx')

#agrego una nueva columna concatenando departamento y municipio
df_5w["Full Name"] = df_5w["Admin Departamento"] + df_5w["Admin Municipio"]

df_5w['Mes de atención'].unique()

df_5w['_ Sector'].unique()

mes = ['04_Abril','05_Mayo','06_Junio']
sector = ['Agua_Saneamiento_e_Higiene']

df_5w.columns 
#con la que trabajaré apartir de ahora 
df_5w_sector_mes = df_5w[(df_5w['_ Sector'].isin(sector))&(df_5w['Mes de atención'].isin(mes))]

#Otro Formato
#df_5w_sector_mes2 = df_5w[(df_5w['Sector']=='Educación')&(df_5w['Mes de atención'] == '03_Marzo')]

#Cargo api

df_api_ind_mpio = pd.read_excel('C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo6/API_Consolidado_ciclo_seis_GENERAL_ 18082022.xlsx', sheet_name = 'Indicador y Municipio')

df_api_ind_mpio.columns

df_api_ind_mpio["Full Name"] = df_api_ind_mpio["Departamento"] + df_api_ind_mpio["Municipio"]
df_api_sector_mes = df_api_ind_mpio[(df_api_ind_mpio['Sector'].isin(sector))&(df_api_ind_mpio['Mesdeatención'].isin(mes))]
#df_api_sector_mes2 = df_api_ind_mpio[(df_api_ind_mpio['Sector']=='Educación')&(df_api_ind_mpio['Mesdeatención'] == '03_Marzo')]

#Divipola 

divipola = pd.read_excel("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/divipolita.xlsx")

#agrego una nueva columna concatenando departamento y municipio
divipola["Full Name"] = divipola["Departamento"] + divipola["Municipio"]
divipola["Full Name"] = divipola["Full Name"].drop_duplicates()


def standardize_territories(column):
    column = column.str.replace("_"," ", regex=True)
    column = column.map(lambda x: x.lower())
    column = column.map(lambda x: x.strip())
    column = column.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    column = column.str.replace(r'[^\w\s]+', '', regex=True)
    column = column.str.replace("narinotumaco","narinosan andres de tumaco", regex=True)
    return column


# Estandarizando nombres de departamentos ...
df_5w_sector_mes['Full Name'] = standardize_territories(df_5w_sector_mes['Full Name'])
df_api_sector_mes['Full Name'] = standardize_territories(df_api_sector_mes['Full Name'])
divipola['Full Name'] = standardize_territories(divipola['Full Name'])


#prueba = df_5w_sector_mes['Full Name'].sort_values()

#prueba1 = divipola['Full Name'].sort_values()

# Adicionar el divipola más adecuado
df_5w_sector_mes = pd.merge(df_5w_sector_mes, divipola, how= 'left', left_on = 'Full Name',
                 right_on = 'Full Name')

if df_5w_sector_mes['Full Name'].isna().sum() > 1:
    print('Ajustar full name')
    
if df_5w_sector_mes['dpto'].isna().sum() > 1:
    print('Ajustar Divipola dpto')
    
if df_5w_sector_mes['mpio'].isna().sum() > 1:
    print('Ajustar Divipola mpio')


# Adicionar el divipola más adecuado
df_api_sector_mes = pd.merge(df_api_sector_mes, divipola, how= 'left', left_on = 'Full Name',
                 right_on = 'Full Name')


if df_api_sector_mes['Full Name'].isna().sum() > 1:
    print('Ajustar full name')
    
if df_api_sector_mes['dpto'].isna().sum() > 1:
    print('Ajustar Divipola dpto')
    
if df_api_sector_mes['mpio'].isna().sum() > 1:
    print('Ajustar Divipola mpio')
    


## Pivot table 
mapa = df_5w_sector_mes[["mpio","Admin Municipio"]]
mapa.dtypes
mapa["mpio"] = mapa["mpio"].astype('Int64')
mapa = mapa.pivot_table(index=["mpio","Admin Municipio"]) 


Tablero = df_5w_sector_mes[["Admin Municipio","Socio Principal Nombre"]]
Tablero = Tablero.pivot_table(index=["Admin Municipio","Socio Principal Nombre"]) 


df_5w_sector_mes.columns

#Group by
Act_dpt_total = df_5w_sector_mes.groupby("Admin Departamento")["_ Actividad Asociada"].count()

Act_mes_total = df_5w_sector_mes.groupby("Mes de atención")["_ Actividad Asociada"].count()

Act_ind_total = df_5w_sector_mes.groupby("_ Actividad Asociada")["Nombre de la actividad"].count()

# Api 
df_api_sector_mes.columns

Act_dpt_total_api = df_api_sector_mes.groupby("Indicador")["bene_nuevos"].sum()

poblacion_atendida = round(df_api_sector_mes["bene_nuevos"].sum())


## ver

Act_mes_total_api = df_api_sector_mes.groupby("Mesdeatención")["bene_nuevos"].sum()
Act_mes_total_api = Act_mes_total_api.to_frame()#.resetindexindex()
Act_mes_total_api.columns
Act_mes_total_api['Beneficiarios Nuevos %'] = (Act_mes_total_api['bene_nuevos'] /Act_mes_total_api['bene_nuevos'].sum())*100


Writer= pd.ExcelWriter("C:/Users/Lisa/Documents/Bases de Python/Bases Actualizables/Ciclo6/tablero_wash_trimeste2_2022.xlsx")
mapa.to_excel(Writer, sheet_name='mapa5w.xlsx')
Tablero.to_excel(Writer, sheet_name='tablero5w.xlsx')
Act_dpt_total.to_excel(Writer, sheet_name='Act_dpt_total5w.xlsx')
Act_mes_total.to_excel(Writer, sheet_name='Act_mes_total5w.xlsx')
Act_ind_total.to_excel(Writer, sheet_name='Act_ind_total5w.xlsx')
Act_dpt_total_api.to_excel(Writer, sheet_name='Act_dpt_total_api.xlsx')
Act_mes_total_api.to_excel(Writer, sheet_name='Act_mes_total_api.xlsx')

Writer.save()