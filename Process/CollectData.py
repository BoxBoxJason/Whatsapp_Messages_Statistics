# -*- coding: utf-8 -*-
'''
Created on 16 sept. 2023

@author: BoxBoxJason
'''
import re
import os
import logging
from datetime import date
from Process.Converter import convertTxtToJson
from Resources.enums import USERDICT

def collectData(sourceFolderPath,wordsToSearchFor):
    """
    Explores all files and collects valuable data from it
    """
    # List of files in source folder
    FILES = os.listdir(sourceFolderPath)
    # Number of files in source folder
    NUMBEROFFILES = len(FILES)
    # Users data dict
    usersDict = {}
    # Count of messages per day
    daysCount = {}
    # Count of messages per hour and day of week
    gridHourDay = [[0 for i in range(7)] for j in range(24)]

    #Beginning of files data collection
    for fileIndex,fileName in enumerate(FILES):
        FILEOK = True
        fileIndex += 1
        logging.debug(f"Collecting data from {fileName} (file {fileIndex}/{NUMBEROFFILES})")

        filePath = os.path.join(sourceFolderPath,fileName)
        if filePath.endswith(".txt") and os.path.exists(filePath) and os.access(filePath,os.R_OK):
            with open(filePath,'r',encoding="utf-8") as openedFile:
                fileContent = openedFile.readlines()
                messagesJson = convertTxtToJson(fileContent)
        else:
            logging.error(f"{filePath} could not be opened or read as a .txt file")
            FILEOK = False

        if FILEOK:
            #Creating users dictionary with all retrieved data
            participants = messagesJson["participants"]
            for participant in participants:
                if not participant in usersDict:
                    usersDict[participant] = USERDICT(participant)

            #Collecting messages data
            for message in messagesJson["messages"]:
                collectMessageData(usersDict, daysCount, gridHourDay, wordsToSearchFor, message)

    return usersDict,daysCount,gridHourDay


def collectMessageData(usersDict,daysCount,gridHourDay,wordsToSearchFor,message):
    """
    Collects message data and stores it into corresponding dict, list...
    """
    user = message["user"]
    mes = message["message"]
    msgdate = message["datetime"]
    #Determining type of message
    if re.match("<(.*)>",mes):
        usersDict[user]["photosAndVideos"] += 1
    else:
        usersDict[user]["messages"] += 1
    #Searching for particular words / phrases given in enums
    for wordToSearch in wordsToSearchFor:
        if wordToSearch in mes.lower():
            usersDict[user]["wordsToFind"] += 1
    #Vocabulary analysis
    mesSplit = re.sub(r' \W+', '', mes).lower().split(' ')
    for word in mesSplit:
        usersDict[user]["vocabulary"].add(word)
    usersDict[user]["messages"] += 1

    #Creating time statistics
    day = msgdate.date()
    if day in daysCount:
        daysCount[day] += 1
    else:
        daysCount[day] = 1
    dayOfWeek = msgdate.isoweekday() - 1
    hour = msgdate.hour
    gridHourDay[hour][dayOfWeek] += 1
