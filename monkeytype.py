import string
import math
import datetime
from time import time
import requests

def getMonkeyTypeRequest(sublink: string, headers: dict, params: dict):
    response = requests.get("http://api.monkeytype.com/" + sublink, headers=headers, params=params)
    if response.json()['message'].endswith("retrieved"):
        return response.json()
    else:
        return None

def generatePersonalBestString(data: dict, mode: string):
    response = ""
    if not (mode in data):
        response += "No data found.\n"
    else:
        response += "**WPM:** " + str(data[mode][0]['wpm']) + "\n"
        response += "**Raw WPM:** " + str(data[mode][0]['raw']) + "\n"
        response += "**Accuracy:** " + str(data[mode][0]['acc']) + "\n"
        response += "**Consistency:** " + str(data[mode][0]['consistency']) + "\n"
        response += "**Difficulty:** " + data[mode][0]['difficulty'] + "\n"
        response += "**Language:** " + data[mode][0]['language'] + "\n"
        response += "**Punctuation:** " + str(data[mode][0]['punctuation']) + "\n"
        response += "**Lazy Mode:** " + str(data[mode][0]['lazyMode']) + "\n"
        response += "**Date:** " + str(datetime.datetime.utcfromtimestamp(data[mode][0]['timestamp'] / 1e3)) + "\n"
    return response

def generateLastResultString(data: dict):
    response = ""
    if not ("wpm" in data):
        response += "No data found.\n"
    else:
        response += "**Mode:** " + str(data['mode']) + "\n"
        response += "**SubMode:** " + str(data['mode2']) + "\n"
        response += "**WPM:** " + str(data['wpm']) + "\n"
        response += "**Raw WPM:** " + str(data['rawWpm']) + "\n"
        response += "**Accuracy:** " + str(data['acc']) + "\n"
        response += "**Consistency:** " + str(data['consistency']) + "\n"
        response += "**# of Restarts Prior:** " + str(data['restartCount']) + "\n"
        response += "**Date:** " + str(datetime.datetime.utcfromtimestamp(data['timestamp'] / 1e3)) + "\n"
    return response

def generatePersonalStatsString(apekey: string, userID: string):
    # Create Personal General Stats Section #
    data = getMonkeyTypeRequest("users/stats", {"Authorization" : "ApeKey " + apekey}, {})
    responseAccum = ""
    if data == None:
        return None
    data = data['data']
    responseAccum += "__**<@" + userID + ">'s MonkeyType Stats**__\n\n"
    responseAccum += "__**General**__\n"
    responseAccum += "**Tests Started:** " + str(data['startedTests']) + "\n"
    responseAccum += "**Completed Tests:** " + str(data['completedTests']) + "\n"
    responseAccum += "**Completed to Started Ratio:** " + str(round(data['completedTests']/data['startedTests'], 2)) + "\n"
    responseAccum += "**Time Typing:** " + str(math.floor(data['timeTyping']/60/60)) + " hours, " + str(math.floor(data['timeTyping']/60)) + " minutes, " + str(math.floor(data['timeTyping']%60)) + "\n\n"
    return responseAccum

def generateTimeBestsString(apekey: string):
    # Creating Timed Personal Bests Section #
    data = getMonkeyTypeRequest("users/personalBests", {"Authorization" : "ApeKey " + apekey}, {"mode": "time"})
    responseAccum = ""
    if data == None:
        return None
    responseAccum += "__**Timed Personal Bests**__\n"
    data = data['data']
    for i in ['15', '30', '60', '120']:
        responseAccum += "__**" + i + " Seconds**__\n"
        responseAccum += generatePersonalBestString(data, i)
        responseAccum += '\n'
    return responseAccum

def generateWordBestsString(apekey: string):
    # Creating Word Personal Bests Section #
    data = getMonkeyTypeRequest("users/personalBests", {"Authorization" : "ApeKey " + apekey}, {"mode": "words"})
    responseAccum = ""
    if data == None:
        return None
    responseAccum += "__**Words Personal Bests**__\n"
    data = data['data']
    for i in ['10', '25', '50', '100']:
        responseAccum += "__**" + i + " Words**__\n"
        responseAccum += generatePersonalBestString(data, i)
        responseAccum += '\n'
    return responseAccum

def generateLastResult(apekey: string, userID: string):
    # Creating Last Result Section #
    data = getMonkeyTypeRequest("results/last", {"Authorization" : "ApeKey " + apekey}, {})
    responseAccum = ""
    if data == None:
        return None
    responseAccum += "__**<@" + userID + "> Last Result**__\n"
    data = data['data']
    responseAccum += generateLastResultString(data)
    responseAccum += '\n'
    return responseAccum

def createStatsEmbedDescription(apekey: string, userID: string, mode: string):
    embedString = generatePersonalStatsString(apekey, userID)
    if embedString == None:
        return None
    if mode == 'time':
        embedString += generateTimeBestsString(apekey)
    elif mode == 'words':
        embedString += generateWordBestsString(apekey)
    return embedString

def createLastEmbedDescription(apekey: string, userID: string):
    embedString = generateLastResult(apekey, userID)
    if embedString == None:
        return None
    else:
        return embedString