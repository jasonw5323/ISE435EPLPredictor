# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 21:09:46 2020

@author: jhwhe
"""
import pandas as pd
import numpy as np
from numpy import random
import matplotlib.pyplot as plt

# Sort data by year
def seasonDataSort(histData,year):
	seasonData = histData[histData['Season']==year]
	return seasonData

# using poisson distribution, predict the outcome of each fixture
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

'''
Import 2020-21 fixture info from csv file
File from https://fixturedownload.com/results/epl-2020
'''

colFixHeads = ['Round Number', 'Home Team', 'Away Team','AResult','AFTHG','AFTAG']

fixReader = pd.read_csv('EPL_Fixtures.csv',usecols = colFixHeads)

# Get played current season games
matchWk = int(input("Which week of games do you want predicted?\n"))

currentSeas = fixReader.loc[fixReader['Round Number'] < matchWk]
currentSeas['Season'] = '2020-21'

fixReader['FTHG'] = np.nan
fixReader['FTAG'] = np.nan
fixReader['FTR'] = np.nan
fixReader['Perc'] = np.nan

# Get all team names in the EPL this year
teamNames = sorted(fixReader['Home Team'].unique())

# Import historical data from 1993-2018
# File from https://www.kaggle.com/thefc17/epl-results-19932018
colHistHeads = ['Date','HomeTeam','AwayTeam','FTHG','FTAG','FTR','Season']
histReader = pd.read_csv('EPL_Data.csv',usecols = colHistHeads)

# Replace relevant team names to be consistent between files
histReader = histReader.replace('Sheffield United','Sheffield Utd')
histReader = histReader.replace('Tottenham','Spurs')
histReader = histReader.replace('Man United','Man Utd')

# Pull 2010-18 seasons to be used from historical data file
season1 = seasonDataSort(histReader,'2010-11')
season2 = seasonDataSort(histReader,'2011-12')
season3 = seasonDataSort(histReader,'2012-13')
season4 = seasonDataSort(histReader,'2013-14')
season5 = seasonDataSort(histReader,'2014-15')
season6 = seasonDataSort(histReader,'2015-16')
season7 = seasonDataSort(histReader,'2016-17')
season8 = seasonDataSort(histReader,'2017-18')
season9 = seasonDataSort(histReader,'2018-19')
season10 = seasonDataSort(histReader,'2019-20')

# Concatenate 2010-18 seasons into one dataset
seas = [season1,season2,season3,season4,season5,season6,season7,season8,season9,season10,currentSeas]
moreSeas = pd.concat(seas)

# Get average goals scored and conceded per team based on home or away and
# input into Dataframe
aveHomeGoals = moreSeas.groupby('HomeTeam')['FTHG'].mean()
aveHomeConc = moreSeas.groupby('HomeTeam')['FTAG'].mean()
aveAwayGoals = moreSeas.groupby('AwayTeam')['FTAG'].mean()
aveAwayConc = moreSeas.groupby('AwayTeam')['FTHG'].mean()

aveGoals = pd.DataFrame({'HomeScored':aveHomeGoals,'HomeConc':aveHomeConc,'AwayScored':aveAwayGoals,'AwayConc':aveAwayConc})
aveFixtGoals = moreSeas.groupby(['HomeTeam','AwayTeam'])[['FTHG','FTAG']].mean()

'''
Function for Specific Match
'''

# Run through each match, getting specific from function getMatchScore
# then inputting the match result, (home/away win or draw)

def matchOutcome(homeScore,awayScore):
	outcome = []
	for i in range(len(homeScore)):
		if homeScore[i] > awayScore[i]:
			outcome.append('H')
		elif homeScore[i] < awayScore[i]:
			outcome.append('A')
		else:
			outcome.append('A')
	return outcome
	
def overallWins(outcome):
	homeWins = outcome.count('H')
	awayWins = outcome.count('A')
	draws = outcome.count('D')
	if homeWins > awayWins and homeWins > draws:
		bestPick = 'H'
		perc = homeWins / len(outcome)
	elif awayWins > homeWins and awayWins > draws:
		bestPick = 'A'
		perc = awayWins / len(outcome)
	elif draws > homeWins and draws > awayWins:
		bestPick = 'D'
		perc = draws / len(outcome)
	elif homeWins == awayWins and homeWins > draws:
			bestPick = 'H A'
			perc = (homeWins + awayWins) / len(outcome)
	elif homeWins == draws and homeWins > awayWins:
			bestPick = 'H D'
			perc = (homeWins + draws) / len(outcome)
	elif awayWins == draws and awayWins > homeWins:
			bestPick = 'A D'
			perc = (awayWins + draws) / len(outcome)
	return bestPick, perc

cnt = 0
for index, row in fixReader.iterrows():
	homeScores = []
	awayScores = []
	homeTeam = fixReader['Home Team'][index]
	awayTeam = fixReader['Away Team'][index]
	for i in range(50):
		home,away = getMatchScore(homeTeam,awayTeam,aveFixtGoals,aveHomeGoals,aveHomeConc,aveAwayGoals,aveAwayConc, moreSeas)
		homeScores.append(home)
		awayScores.append(away)
	outcome = matchOutcome(homeScores,awayScores)
	result,bestPerc = overallWins(outcome)
	fixReader['FTHG'][index] = sum(homeScores)/len(homeScores)
	fixReader['FTAG'][index] = sum(awayScores)/len(awayScores)
	fixReader['FTR'][index] = result
	fixReader['Perc'][index] = bestPerc
	cnt = cnt + 1

wkOutcome = fixReader.loc[fixReader['Round Number'] == matchWk]
print(wkOutcome)

'''
Create league table
'''

leagueTable = pd.DataFrame(teamNames, columns=['Team'])
leagueTable['Points'] = np.nan

# Get total number of points each team earned then input it into the league table
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

# Sort by most points then input each team's place into the table
leagueTable = leagueTable.sort_values('Points',ascending=False).reindex()
place = list(range(1,21))
leagueTable.insert(0,'Place',place)

# Create new league table, inputting correct order with index being their place
finalTable = pd.DataFrame(index = range(20), columns = ['Team', 'Points'])
i = 0
for index, row in leagueTable.iterrows():
	finalTable['Team'][i] = leagueTable['Team'][index]
	finalTable['Points'][i] = leagueTable['Points'][index]
	i  += 1
finalTable.index = np.arange(1,len(finalTable)+1)

'''
Print top 3 finishers and the number of points they earned
'''
print('The top 3 finishers are: \n', finalTable.head(3))

'''
Create graph showing number of points the champion of the EPL had at the
end of each matchweek
'''

champName = finalTable['Team'][1]
champPoints = pd.DataFrame(index = range(38),columns = ['Points'])

# Get number of points the team had at the end of each matchweek and input
# it into a dataframe
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

# Increase all indexes by one to show specific matchweek
champPoints.index = np.arange(1,len(champPoints)+1)

# Create plot
fig = plt.figure()
plt.plot(champPoints.index,champPoints['Points'])

plt.xlabel('Match Week')
plt.ylabel('Number of Points')
plt.title(f'Total Points of {champName}')
plt.show()

'''
Create 2 outputs to CSV
- EPLFixturePred.csv shows the score of each fixture of the 2020-21 season
- EPLTablePred.csv shows the final league table based on the predictions
'''

fixReader.to_csv('EPLFixturePred.csv', index=False)
finalTable.to_csv('EPLTablePred.csv')