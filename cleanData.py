# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:09:46 2020

@author: jhwhe
"""
import csv
import pandas as pd


colFixHeads = ['Round Number', 'Home Team', 'Away Team']

fixReader = pd.read_csv('EPL_Fixtures.csv',usecols = colFixHeads)
print(fixReader)
teamNames = fixReader['Home Team'].unique()
print(sorted(teamNames))


colHistHeads = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','Season']
histReader = pd.read_csv('EPL_Data.csv',usecols = colHistHeads)

def seasonDataSort(histData,year):
	seasonData = histData[histData['Season']==year]
	return seasonData

histReader = histReader.replace('Sheffield United','Sheffield Utd')
histReader = histReader.replace('Tottenham','Spurs')

season1 = seasonDataSort(histReader,'2010-11')
season2 = seasonDataSort(histReader,'2011-12')
season3 = seasonDataSort(histReader,'2012-13')
season4 = seasonDataSort(histReader,'2013-14')
season5 = seasonDataSort(histReader,'2014-15')
season6 = seasonDataSort(histReader,'2015-16')
season7 = seasonDataSort(histReader,'2016-17')
season8 = seasonDataSort(histReader,'2017-18')

seas = [season1,season2,season3,season4,season5,season6,season7,season8]

moreSeas = pd.concat(seas)
print(moreSeas)




