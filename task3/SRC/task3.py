#-*-coding: utf-8 =*-
import os.path
import sys
import csv
import datetime
import  random

SIZE_OF_LOG_FILE = 2**20
COMMAND_SCOOP_BARREL = 'scoop'
COMMAND_TOPUP_BARREL = 'top up'

def makeLogFile(path): #делаем если нужно новый лог файл
    output = open(path, 'w')
    barrelSize = random.randint(100, 1000)
    barrelCurrentVolume = random.randint(10, barrelSize)
    output.write("META DATA:\n" + str(barrelSize) + " (объём бочки)\n" + str(barrelCurrentVolume) + " (текущий объём воды в бочке)\n")
    lastLog = '2020-01-01T12:51:32.12Z – [username1] - wanna scoop 1l (успех)\n'
    barrelCurrentVolume -= 1
    output.write(lastLog)
    while os.path.getsize(path) <= SIZE_OF_LOG_FILE :
        newLog, barrelCurrentVolume = makeLog(lastLog, barrelSize, barrelCurrentVolume)
        output.write(newLog)
        lastLog = newLog

def getDateTimeFromLog(log):
    date = log[:log.find('T')]
    date = list(map(int, date.split('-')))
    time = log[log.find('T') + 1: log.find('Z')]
    time = list(map(int, time.replace('.', ':').split(':')))
    if len(time) < 4:
        time.append(0)
    dateTime = datetime.datetime(date[0], date[1], date[2], time[0], time[1], time[2],
                                     time[3])
    return dateTime

def getComandResult(comand, litrs, barrelSize, currentVolume):
    if comand == COMMAND_TOPUP_BARREL:
        if currentVolume + litrs <= barrelSize:
            result = 'успех'
            currentVolume += litrs
        else:
            result = 'фейл'
    else:
        if currentVolume - litrs >= 0:
            result = 'успех'
            currentVolume -= litrs
        else:
            result = 'фейл'

    return result, currentVolume

def makeLog(lastLog, barrelSize, currentVolume):
    dateTimeLast = getDateTimeFromLog(lastLog)
    changerDate = datetime.timedelta(random.choice([0, 1]), hours=random.randint(0, 23), minutes = random.randint(0, 59), seconds = random.randint(0, 59), microseconds=random.randint(0, 1000000))
    user = 'temich' + str(random.randint(0, 40))
    comand = random.choice([COMMAND_SCOOP_BARREL, COMMAND_TOPUP_BARREL])
    litrs = random.randint(0, 1000)

    result, currentVolume = getComandResult(comand, litrs, barrelSize, currentVolume)

    outLogDateTime = dateTimeLast + changerDate
    outLog = str(outLogDateTime.date()) + "T" + str(outLogDateTime.time()) + "Z" + '– [{0}] - wanna {1} {2}l ({3})\n'.format(user, comand, str(litrs), result)
    return outLog, currentVolume

def checkDate(dateOnCheck, dateMin, dateMax):
    if dateMin <= dateOnCheck <= dateMax:
        return True
    return False

def countCounters(command, litrs, result, dictCounters):

    if command == COMMAND_SCOOP_BARREL:
        if result == 'успех':
            dictCounters['counterScoopSuccessfull'] += 1
            dictCounters['waterScoopSuccessfull'] += litrs
        else:
            dictCounters['counterScoopFailed'] += 1
            dictCounters['waterScoopFailed'] += litrs
    else:
        if result == 'успех':
            dictCounters['counterTopUpSuccessfull'] += 1
            dictCounters['waterTopUpSuccessfull'] += litrs
        else:
            dictCounters['counterTopUpFailed'] += 1
            dictCounters['waterTopUpFailed'] += litrs

def setProcentFailedInDict(dict) :
    if dict['counterTopUpFailed'] == 0 and dict['counterTopUpSuccessfull'] == 0:
        dict['counterTopUpProcentFailed'] = 0
    else:
        dict['counterTopUpProcentFailed'] = float(dict['counterTopUpFailed']) / float(
            dict['counterTopUpFailed'] + dict['counterTopUpSuccessfull'])

    if dict['counterScoopFailed'] == 0 and dict['counterScoopSuccessfull'] == 0:
        dict['counterScoopProcentFailed'] = 0
    else:
        dict['counterScoopProcentFailed'] = float(dict['counterScoopFailed']) / float(
            dict['counterScoopFailed'] + dict['counterScoopSuccessfull'])

def parseLogFile(path, minData, maxData):
    output = open(path, 'r')
    dictCounters = dict()
    dictCounters['counterTopUpSuccessfull'] = 0
    dictCounters['counterTopUpFailed'] = 0
    dictCounters['counterScoopSuccessfull'] = 0
    dictCounters['counterScoopFailed'] = 0
    dictCounters['waterTopUpSuccessfull'] = 0
    dictCounters['waterTopUpFailed'] = 0
    dictCounters['waterScoopSuccessfull'] = 0
    dictCounters['waterScoopFailed'] = 0
    flag = True
    for line in output:
        if line.find('META') >= 0:
            continue
        elif not line.find('(объём бочки)') == -1:
            barrelSize = int(line[:line.find('(объём бочки)')])
        elif not line.find('(текущий объём воды в бочке)') == -1:
            currentVolume = int(line[:line.find('(текущий объём воды в бочке)')])
        else:
            command = COMMAND_TOPUP_BARREL if line[line.find('wanna') + len('wanna '):line.find(' ', line.find(
                'wanna') + len('wanna '))] == 'top' else COMMAND_SCOOP_BARREL
            litrs = int(line[line.find(' ', line.find(command) + len(command)) + 1: line.find('l')])
            result, currentVolume = getComandResult(command, litrs, barrelSize, currentVolume)
            # Просто считаем все счётчики
            if checkDate(getDateTimeFromLog(line), minData, maxData):
                if flag:#check startVolume
                    dictCounters['volumeStart'] = currentVolume
                    flag = False
                countCounters(command, litrs, result, dictCounters)

    setProcentFailedInDict(dictCounters)
    if flag:
        dictCounters['volumeStart'] = 'Не определено'
        dictCounters['volumeEnd'] = 'Не определено'
        return dictCounters
    dictCounters['volumeEnd'] = dictCounters['volumeStart'] - dictCounters['waterScoopSuccessfull'] + dictCounters['waterTopUpSuccessfull']
    return dictCounters

def writeDictInCsvFile(dict):
    with open('results', 'w') as csvFile:
        writer = csv.writer(csvFile, delimiter=',')
        writer.writerow(['какое количество попыток налить воду в бочку было за указанный период?',
                        'какой процент ошибок в наливании воды был допущен за указанный период',
                        'какой объем воды был налит в бочку за указанный период?',
                        'какой объем воды был не налит в бочку за указанный период?',

                        'какое количество попыток слить воду из бочки было за указанный период?',
                        'какой процент ошибок сливания воды был допущен за указанный период',
                        'какой объем воды был слит из бочки за указанный период?',
                        'какой объем воды был не слит из бочки за указанный период?',

                        'какой объем воды был в бочке в начале указанного периода',
                        'Какой в конце указанного периода?'])

        writer.writerow([dict['counterTopUpSuccessfull'] + dict['counterTopUpFailed'],
                        dict['counterTopUpProcentFailed'],
                        dict['waterTopUpSuccessfull'],
                        dict['waterTopUpFailed'],

                        dict['counterScoopSuccessfull'] + dict['counterScoopFailed'],
                        dict['counterScoopProcentFailed'],
                        dict['waterScoopSuccessfull'],
                        dict['waterScoopFailed'],

                        dict['volumeStart'],
                        dict['volumeEnd']])

if __name__ == "__main__":
    sys.argv = sys.argv[1:]
    if len (sys.argv) == 3:
        path = sys.argv[0]
        minData = sys.argv[1] + "Z" #for parsing
        maxData = sys.argv[2] + "Z"#...
        minData = getDateTimeFromLog(minData)
        maxData = getDateTimeFromLog(maxData)
        resultsInDict = parseLogFile(path, minData, maxData)
        writeDictInCsvFile(resultsInDict)
    else:
        print("usage")
        sys.exit (1)

