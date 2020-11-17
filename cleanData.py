# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:09:46 2020

@author: jhwhe
"""
import pandas as pd
import numpy as np
from numpy import random
from scipy.stats import poisson
import seaborn as sb
import matplotlib.pyplot as plt

def seasonDataSort(histData,year):
	seasonData = histData[histData['Season']==year]
	return seasonData


colFixHeads = ['Round Number', 'Home Team', 'Away Team']

fixReader = pd.read_csv('EPL_Fixtures.csv',usecols = colFixHeads)
fixReader['FTHG'] = np.nan
fixReader['FTAG'] = np.nan
fixReader['FTR'] = np.nan

teamNames = sorted(fixReader['Home Team'].unique())
print(sorted(teamNames))


colHistHeads = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','Season']
histReader = pd.read_csv('EPL_Data.csv',usecols = colHistHeads)

histReader = histReader.replace('Sheffield United','Sheffield Utd')
histReader = histReader.replace('Tottenham','Spurs')
histReader = histReader.replace('Man United','Man Utd')
#teamnames2 = sorted(histReader['HomeTeam'].unique())

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

aveHomeGoals = moreSeas.groupby('HomeTeam')['FTHG'].mean()
aveHomeConc = moreSeas.groupby('HomeTeam')['FTAG'].mean()
aveAwayGoals = moreSeas.groupby('AwayTeam')['FTAG'].mean()
aveAwayConc = moreSeas.groupby('AwayTeam')['FTHG'].mean()

aveGoals = pd.DataFrame({'HomeScored':aveHomeGoals,'HomeConc':aveHomeConc,'AwayScored':aveAwayGoals,'AwayConc':aveAwayConc})

aveFixtGoals = moreSeas.groupby(['HomeTeam','AwayTeam'])[['FTHG','FTAG']].mean()
print(aveFixtGoals.at[('Wigan','Swansea'),'FTHG'])

### 
# Function for Specific Match
### 

def getMatchScore(home,away,aveFixt,aveHomeGoals,aveHomeConc,aveAwayGoals,aveAwayConc,allSeasons):
	if (home,away) in aveFixt:
		homeForm = aveFixt.at[(home,away),'FTHG']
		awayForm = aveFixt.at[(home,away),'FTAG']
	elif (home in aveHomeGoals) and (away in aveHomeGoals):
		homeForm = 0.5 * (aveHomeGoals[home]+aveAwayConc[away])
		awayForm = 0.5 * (aveAwayGoals[away]+aveHomeConc[home])
	elif (home in aveHomeGoals) and (away not in aveHomeGoals):
		homeForm = 0.5 * (aveHomeGoals[home]+allSeasons['FTHG'].mean())
		awayForm = 0.5 * (allSeasons['FTAG'].mean()+aveHomeConc[home])
	elif (home not in aveHomeGoals) and (away in aveHomeGoals):
		homeForm = 0.5 * (allSeasons['FTHG'].mean()+aveAwayConc[away])
		awayForm = 0.5 * (aveAwayGoals[away]+allSeasons['FTAG'].mean())
	elif (home not in aveHomeGoals) and (away not in aveAwayGoals):
		homeForm = allSeasons['FTHG'].mean()
		awayForm = allSeasons['FTAG'].mean()
	h_scored = random.poisson(lam=homeForm,size=1)
	a_scored = random.poisson(lam=awayForm,size=1)
	return h_scored, a_scored

cnt = 0
for index, row in fixReader.iterrows():
	homeScores = []
	awayScores = []
	homeTeam = fixReader['Home Team'][index]
	awayTeam = fixReader['Away Team'][index]
	#for i in range(50):
	home,away = getMatchScore(homeTeam,awayTeam,aveFixtGoals,aveHomeGoals,aveHomeConc,aveAwayGoals,aveAwayConc, moreSeas)
	homeScores.append(home)
	awayScores.append(away)
	
	fixReader['FTHG'][index] = sum(homeScores)/len(homeScores)
	fixReader['FTAG'][index] = sum(awayScores)/len(awayScores)
	if fixReader['FTHG'][index] > fixReader['FTAG'][index]:
		result = 'H'
	elif fixReader['FTHG'][index] < fixReader['FTAG'][index]:
		result = 'A'
	else:
		result = 'D'
	fixReader['FTR'][index] = result
	cnt = cnt + 1

print("count is: ",cnt)

leagueTable = pd.DataFrame(teamNames, columns=['Team'])
leagueTable['Points'] = np.nan

for index, row in leagueTable.iterrows():
	totPts = 0
	homeGames = fixReader.loc[fixReader['Home Team'] == leagueTable['Team'][index]]
	homeW = len(homeGames[homeGames['FTR'].str.contains('H')])
	homeD = len(homeGames[homeGames['FTR'].str.contains('D')])
	awayGames = fixReader.loc[fixReader['Away Team'] == leagueTable['Team'][index]]
	awayW = len(awayGames[awayGames['FTR'].str.contains('A')])
	awayD = len(awayGames[awayGames['FTR'].str.contains('D')])
	
	totPts = ((homeW + awayW) * 3) + (homeD + awayD)
	leagueTable['Points'][index] = totPts

leagueTable = leagueTable.sort_values('Points',ascending=False).reindex()

place = list(range(1,21))
leagueTable.insert(0,'Place',place)

finalTable = pd.DataFrame(index = range(20), columns = ['Team', 'Points'])
i = 0

for index, row in leagueTable.iterrows():
	finalTable['Team'][i] = leagueTable['Team'][index]
	finalTable['Points'][i] = leagueTable['Points'][index]
	i  += 1
	
finalTable.index = np.arange(1,len(finalTable)+1)
	
print('The top 3 finishers are: \n', finalTable.head(3))

champName = finalTable['Team'][1]

champPoints = pd.DataFrame(index = range(38),columns = ['Points'])

i = 0
totpts = 0
for index,row in fixReader.iterrows():
	include = False
	if fixReader['Home Team'][index] == champName:
		include = True
		if fixReader['FTR'][index] == 'H':
			totpts = totpts + 3
		elif fixReader['FTR'][index] == 'D':
			totpts = totpts + 1
	elif fixReader['Away Team'][index] == champName:
		include = True
		if fixReader['FTR'][index] == 'A':
			totpts = totpts + 3
		elif fixReader['FTR'][index] == 'D':
			totpts = totpts + 1
	if include == True:
		champPoints['Points'][i] = totpts
		i += 1
champPoints.index = np.arange(1,len(champPoints)+1)

fig = plt.figure()
plt.plot(champPoints.index,champPoints['Points'])

plt.xlabel('Match Week')
plt.ylabel('Number of Points')
plt.title('Total Points of Winning Team')
plt.show()


fixReader.to_csv('EPLFixturePred.csv', index=False)
finalTable.to_csv('EPLTablePred.csv')


