#!/usr/bin/env python
# coding: utf-8

# ### Import Dataset

# In[1]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import datetime as dt
import itertools

get_ipython().run_line_magic('matplotlib', 'inline')


# In[2]:


folder = 'Datasets\\'
rawData1 = pd.read_csv(folder + '2000-01.csv')
rawData2= pd.read_csv(folder + '2001-02.csv')
rawData3= pd.read_csv(folder + '2002-03.csv')
rawData4= pd.read_csv(folder + '2003-04.csv')
rawData5= pd.read_csv(folder + '2004-05.csv')
rawData6 = pd.read_csv(folder + '2005-06.csv')
rawData7 = pd.read_csv(folder + '2006-07.csv')
rawData8 = pd.read_csv(folder + '2007-08.csv')
rawData9 = pd.read_csv(folder + '2008-09.csv')
rawData10 = pd.read_csv(folder + '2009-10.csv')
rawData11 = pd.read_csv(folder + '2010-11.csv')
rawData12 = pd.read_csv(folder + '2011-12.csv')
rawData13 = pd.read_csv(folder + '2012-13.csv')
rawData14 = pd.read_csv(folder + '2013-14.csv')
rawData15 = pd.read_csv(folder + '2014-15.csv')
rawData16 = pd.read_csv(folder + '2015-16.csv')
rawData17 = pd.read_csv(folder + '2016-17.csv')
rawData18 = pd.read_csv(folder + '2017-18.csv')
rawData19 = pd.read_csv(folder + '2018-19.csv')
rawData20 = pd.read_csv(folder + '2019-20.csv')


# In[3]:


columns_req = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR']
playingStats1 = rawData1[columns_req]
playingStats2 = rawData2[columns_req]
playingStats3 = rawData3[columns_req]
playingStats4 = rawData4[columns_req]
playingStats5 = rawData5[columns_req]
playingStats6 = rawData6[columns_req]
playingStats7 = rawData7[columns_req]
playingStats8 = rawData8[columns_req]
playingStats9 = rawData9[columns_req]
playingStats10 = rawData10[columns_req]
playingStats11 = rawData11[columns_req]
playingStats12 = rawData12[columns_req]
playingStats13 = rawData13[columns_req]
playingStats14 = rawData14[columns_req]
playingStats15 = rawData15[columns_req]
playingStats16 = rawData16[columns_req]
playingStats17 = rawData17[columns_req]
playingStats18 = rawData18[columns_req]
playingStats19 = rawData19[columns_req]
playingStats20 = rawData20[columns_req]


# ### Goals Scored/Conceded at end of matchweek

# In[4]:


def get_goals_scored(playingStats):
    #create dictionary with keys being team names
    teams = {}
    for i in playingStats.groupby('HomeTeam').mean().T.columns:
        teams[i] = []
        
    # list containing match locations
    for i in range(len(playingStats)):
        HTGS = playingStats.iloc[i]['FTHG']
        ATGS = playingStats.iloc[i]['FTAG']
        teams[playingStats.iloc[i].HomeTeam].append(HTGS)
        teams[playingStats.iloc[i].AwayTeam].append(ATGS)
    
    # create dataframe for goals scored where rows are teams and cols are a matchweek
    goalsScored = pd.DataFrame(data=teams, index = [i for i in range(1,39)]).T
    goalsScored[0] = 0
    for i in range(2,39):
        goalsScored[i] = goalsScored[i] + goalsScored[i-1]
    return goalsScored


# In[5]:


def get_goals_conceded(playingStats):
    #create dictionary with keys being team names
    teams = {}
    for i in playingStats.groupby('HomeTeam').mean().T.columns:
        teams[i] = []
        
    # value corresponding to keys is list containing match location
    for i in range(len(playingStats)):
        ATGC = playingStats.iloc[i]['FTHG']
        HTGC = playingStats.iloc[i]['FTAG']
        teams[playingStats.iloc[i].HomeTeam].append(HTGC)
        teams[playingStats.iloc[i].AwayTeam].append(ATGC)
        
    # create dataframe for goals scored, rows = teams columns = matchweeks
    goalsConceded = pd.DataFrame(data=teams, index = [i for i in range(1,39)]).T
    goalsConceded[0] = 0
    for i in range(2,39):
        goalsConceded[i] = goalsConceded[i] + goalsConceded[i-1]
    return goalsConceded


# In[6]:


def get_gss(playingStats):
    GC = get_goals_conceded(playingStats)
    GS = get_goals_scored(playingStats)
    
    j = 0
    HTGS = []
    ATGS = []
    HTGC = []
    ATGC = []
    
    for i in range(380):
        ht = playingStats.iloc[i].HomeTeam
        at = playingStats.iloc[i].AwayTeam
        HTGS.append(GS.loc[ht][j])
        ATGS.append(GS.loc[at][j])
        HTGC.append(GS.loc[ht][j])
        ATGC.append(GS.loc[at][j])
        
        if ((i+1)%10) == 0:
            j += 1
    
    playingStats['HTGS'] = HTGS
    playingStats['ATGS'] = ATGS
    playingStats['HTGC'] = HTGC
    playingStats['ATGC'] = ATGC
    
    return playingStats


# In[7]:


playingStats1 = get_gss(playingStats1)
playingStats2 = get_gss(playingStats2)
playingStats3 = get_gss(playingStats3)
playingStats4 = get_gss(playingStats4)
playingStats5 = get_gss(playingStats5)
playingStats6 = get_gss(playingStats6)
playingStats7 = get_gss(playingStats7)
playingStats8 = get_gss(playingStats8)
playingStats9 = get_gss(playingStats9)
playingStats10 = get_gss(playingStats10)
playingStats11 = get_gss(playingStats11)
playingStats12 = get_gss(playingStats12)
playingStats13 = get_gss(playingStats13)
playingStats14 = get_gss(playingStats14)
playingStats15 = get_gss(playingStats15)
playingStats16 = get_gss(playingStats16)
playingStats17 = get_gss(playingStats17)
playingStats18 = get_gss(playingStats18)
playingStats19 = get_gss(playingStats19)
playingStats20 = get_gss(playingStats20)


# ### Get total points

# In[ ]:


def get_points(result):
    if result == 'W':
        return 3
    elif result == 'D':
        return 1
    else:
        return 0


# In[ ]:


def get_cuml_points(matchres):
    matchres_points = matchres.applymap(get_points)
    for i in range(2,39):
        matchres_points[i] = matchres_points[i] + matchres_points[i-1]
    
    matchres_points.insert(column = 0, loc = 0, value = [0*i for i in range(20)])
    return matchres_points


# In[ ]:


def get_matchres(playingStats):
    #create dictionary with keys being team names
    teams = {}
    for i in playingStats.groupby('HomeTeam').mean().T.columns:
        teams[i] = []
        
    # values contain match result
    for i in range(len(playingStats)):
        if playingStats.iloc[i].FTR == 'H':
            teams[playingStats.iloc[i].HomeTeam].append('W')
            teams[playingStats.iloc[i].AwayTeam].append('L')
        elif playingStats.iloc[i].FTR == 'A':
            teams[playingStats.iloc[i].AwayTeam].append('W')
            teams[playingStats.iloc[i].HomeTeam].append('L')
        else:
            teams[playingStats.iloc[i].HomeTeam].append('D')
            teams[playingStats.iloc[i].AwayTeam].append('D')
    return pd.DataFrame(data = teams, index = [i for i in range(1,39)]).T


# In[ ]:


def get_agg_points(playingStats):
    matchres = get_matchres(playingStats)
    cum_pts = get_cuml_points(matchres)
    HTP = []
    ATP = []
    j = 0
    for i in range(380):
        ht = playingStats.iloc[i].HomeTeam
        at = playingStats.iloc[i].AwayTeam
        HTP.append(cum_pts.loc[ht][j])
        ATP.append(cum_pts.loc[at][j])
        
        if ((i+1)%10) == 0:
            j += 1
    playingStats['HTP'] = HTP
    playingStats['ATP'] = ATP
    return playingStats


# In[ ]:


playingStats1 = get_agg_points(playingStats1)
playingStats2 = get_agg_points(playingStats2)
playingStats3 = get_agg_points(playingStats3)
playingStats4 = get_agg_points(playingStats4)
playingStats5 = get_agg_points(playingStats5)
playingStats6 = get_agg_points(playingStats6)
playingStats7 = get_agg_points(playingStats7)
playingStats8 = get_agg_points(playingStats8)
playingStats9 = get_agg_points(playingStats9)
playingStats10 = get_agg_points(playingStats10)
playingStats11 = get_agg_points(playingStats11)
playingStats12 = get_agg_points(playingStats12)
playingStats13 = get_agg_points(playingStats13)
playingStats14 = get_agg_points(playingStats14)
playingStats15 = get_agg_points(playingStats15)
playingStats16 = get_agg_points(playingStats16)
playingStats17 = get_agg_points(playingStats17)
playingStats18 = get_agg_points(playingStats18)
playingStats19 = get_agg_points(playingStats19)
playingStats20 = get_agg_points(playingStats20)


# ### Get team form

# In[ ]:


def get_form(playingStats, num):
    form = get_matchres(playingStats)
    form_final = form.copy()
    for i in range(num,39):
        form_final[i] = ''
        j = 0
        while j < num:
            form_final[i] += form[i-j]
            j+= 1
    return form_final


# In[ ]:


def add_form(playingStats, num):
    form = get_form(playingStats, num)
    h = ['M' for i in range(num*10)]
    a = ['M' for i in range(num*10)]
    
    j = num
    for i in range((num*10),380):
        ht = playingStats.iloc[i].HomeTeam
        at = playingStats.iloc[i].AwayTeam
        
        past = form.loc[ht][j]
        h.append(past[num-1])
        
        past = form.loc[at][j]
        a.append(past[num-1])
        
        if ((i+1)%10) == 0:
            j = j+1
    
    playingStats['HM' + str(num)] = h
    playingStats['AM' + str(num)] = a
    
    return playingStats


# In[ ]:


def add_form_df(playingStats):
    playingStats = add_form(playingStats,1)
    playingStats = add_form(playingStats,2)
    playingStats = add_form(playingStats,3)
    playingStats = add_form(playingStats,4)
    playingStats = add_form(playingStats,5)
    return playingStats


# In[ ]:


playingStats1 = add_form_df(playingStats1)
playingStats2 = add_form_df(playingStats2)
playingStats3 = add_form_df(playingStats3)
playingStats4 = add_form_df(playingStats4)
playingStats5 = add_form_df(playingStats5)
playingStats6 = add_form_df(playingStats6)
playingStats7 = add_form_df(playingStats7)
playingStats8 = add_form_df(playingStats8)
playingStats9 = add_form_df(playingStats9)
playingStats10 = add_form_df(playingStats10)
playingStats11 = add_form_df(playingStats11)
playingStats12 = add_form_df(playingStats12)
playingStats13 = add_form_df(playingStats13)
playingStats14 = add_form_df(playingStats14)
playingStats15 = add_form_df(playingStats15)
playingStats16 = add_form_df(playingStats16)
playingStats17 = add_form_df(playingStats17)
playingStats18 = add_form_df(playingStats18)
playingStats19 = add_form_df(playingStats19)
playingStats20 = add_form_df(playingStats20)


# In[ ]:


cols = ['Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 'HM1', 'HM2', 'HM3', 'HM4', 'HM5', 'AM1', 'AM2', 'AM3', 'AM4', 'AM5']

playingStats1 = playingStats1[cols]
playingStats2 = playingStats2[cols]
playingStats3 = playingStats3[cols]
playingStats4 = playingStats4[cols]
playingStats5 = playingStats5[cols]
playingStats6 = playingStats6[cols]
playingStats7 = playingStats7[cols]
playingStats8 = playingStats8[cols]
playingStats9 = playingStats9[cols]
playingStats10 = playingStats10[cols]
playingStats11 = playingStats11[cols]
playingStats12 = playingStats12[cols]
playingStats13 = playingStats13[cols]
playingStats14 = playingStats14[cols]
playingStats15 = playingStats15[cols]
playingStats16 = playingStats16[cols]
playingStats17 = playingStats17[cols]
playingStats18 = playingStats18[cols]
playingStats19 = playingStats19[cols]
playingStats20 = playingStats20[cols]


# ### Matchweek

# In[11]:


def mw(playingStats):
    j=1
    matchWk = []
    for i in range(380):
        matchWk.append(j)
        if ((i + 1)%10)==0:
            j += 1
    playingStats['MW'] = matchWk
    return playingStats


# In[12]:


playingStats1 = mw(playingStats1)
playingStats2 = mw(playingStats2)
playingStats3 = mw(playingStats3)
playingStats4 = mw(playingStats4)
playingStats5 = mw(playingStats5)
playingStats6 = mw(playingStats6)
playingStats7 = mw(playingStats7)
playingStats8 = mw(playingStats8)
playingStats9 = mw(playingStats9)
playingStats10 = mw(playingStats10)
playingStats11 = mw(playingStats11)
playingStats12 = mw(playingStats12)
playingStats13 = mw(playingStats13)
playingStats14 = mw(playingStats14)
playingStats15 = mw(playingStats15)
playingStats16 = mw(playingStats16)
playingStats17 = mw(playingStats17)
playingStats18 = mw(playingStats18)
playingStats19 = mw(playingStats19)
playingStats20 = mw(playingStats20)


# ### Transfer to one file

# In[ ]:


def getFormPoints(string):
    sum = 0
    for letter in string:
        sum += getPoints(letter)
    return sum

