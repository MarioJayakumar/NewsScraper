
import os
import json
import argparse
import spacy
import time
import datetime
from spacy.matcher import PhraseMatcher
from geopy.geocoders import Nominatim

class JsonEnricher():
    def __init__(self):
        self.geolocator = Nominatim(user_agent="news_scraper")
        self.nlp = spacy.load("en_core_web_sm")

        self.matcher = PhraseMatcher(self.nlp.vocab, attr="LOWER")

        zeroTerms =[]
        oneTerms = []
        twoTerms = []
        threeTerms = []
        with open('misconduct_lexicon.txt', 'r') as misconductLexicon:
            lines = misconductLexicon.readlines()
            for line in lines:
                term, weight = line.strip().split('\t')
                if int(weight) == 0:
                    zeroTerms.append(term)
                elif int(weight) == 1:
                    oneTerms.append(term)
                elif int(weight) == 2:
                    twoTerms.append(term)
                elif int(weight) == 3:
                    threeTerms.append(term)

        zeroPatterns = [self.nlp.make_doc(text) for text in zeroTerms]
        self.matcher.add("ZeroPatterns", zeroPatterns)

        onePatterns = [self.nlp.make_doc(text) for text in oneTerms]
        self.matcher.add("OnePatterns", onePatterns)

        twoPatterns = [self.nlp.make_doc(text) for text in twoTerms]
        self.matcher.add("TwoPatterns", twoPatterns)

        threePatterns = [self.nlp.make_doc(text) for text in threeTerms]
        self.matcher.add("ThreePatterns", threePatterns)

        self.monthMap = {
            'jan': 1,
            'feb': 2,
            'mar': 3,
            'apr': 4,
            'may': 5,
            'jun': 6,
            'jul': 7,
            'aug': 8,
            'sep': 9,
            'oct': 10,
            'nov': 11,
            'dec': 12,
        }

        self.baltimoreLikeSources = ['BaltimoreFishbowl', 'BaltimoreJewishTimes', 'CNN', 'FoxBaltimore', 'NPR', 'WBLATV', 'WJLA', ]

    def get_unix_time(self, dateString, sourceName):
        if sourceName == 'ABC':
            if len(dateString.split(' ')) == 5:
                month, day, year, timeA, timeB = dateString.split(' ')
                monthNum = str(self.monthMap[month.lower()[:3]])
                day = day.replace(',', '')
                year = year.replace(',', '')
                slashDate = day + '/' + monthNum + '/' + year
                print(slashDate)
                unixTime = time.mktime(datetime.datetime.strptime(slashDate, "%d/%m/%Y").timetuple())

                hours = int(timeA.split(':')[0])
                if timeB.lower() == 'pm':
                    hours += 12
                minutes = int(timeA.split(':')[1])
                hours *= 3600
                minutes *= 60
                unixTime += (hours + minutes)

                return unixTime

        elif sourceName in self.baltimoreLikeSources:
            if len(dateString.split(' ')) == 2:
                datePortion, timePortion = dateString.split('T')
                unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

                hours, minutes, seconds = timePortion[:8].split(':')
                seconds = int(seconds)
                seconds += (int(hours) * 3600)
                seconds += (int(minutes) * 60)
                unixTime += seconds

                return unixTime

        elif sourceName == 'NJ':
            datePortion, timePortion = dateString[:10], dateString[-8:]
            unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

            hours, minutes, seconds = timePortion.split(':')
            seconds = int(seconds)
            seconds += (int(hours) * 3600)
            seconds += (int(minutes) * 60)
            unixTime += seconds

            return unixTime

        elif sourceName == 'PGPD':
            weekDay, month, day, year = dateString.split(' ')
            monthNum = str(self.monthMap[month.lower()[:3]])
            day = day.replace(',', '')
            datePortion = year + '-' + monthNum + '-' + day
            unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

            return unixTime

        elif sourceName == 'NBC_PG':
            return None

        elif sourceName == 'WJZ':
            if len(dateString.split(' ')) == 6:
                month, day, year, at, timeA, timeB = dateString.split(' ')
                monthNum = str(self.monthMap[month.lower()[:3]])
                day = day.replace(',', '')
                slashDate = day + '/' + monthNum + '/' + year
                print(slashDate)
                unixTime = time.mktime(datetime.datetime.strptime(slashDate, "%d/%m/%Y").timetuple())

                hours = int(timeA.split(':')[0])
                if timeB.lower() == 'pm':
                    hours += 12
                minutes = int(timeA.split(':')[1])
                hours *= 3600
                minutes *= 60
                unixTime += (hours + minutes)

                return unixTime

        elif sourceName == 'WKYT':
            if len(dateString.split(' ')) == 8:
                published, month, day, year, at, timeA, timeB, timezone = dateString.split(' ')
                monthNum = str(self.monthMap[month.lower()[:3]])
                day = day.replace(',', '')
                slashDate = day + '/' + monthNum + '/' + year
                print(slashDate)
                unixTime = time.mktime(datetime.datetime.strptime(slashDate, "%d/%m/%Y").timetuple())

                hours = int(timeA.split(':')[0])
                if timeB.lower() == 'pm':
                    hours += 12
                minutes = int(timeA.split(':')[1])
                hours *= 3600
                minutes *= 60
                unixTime += (hours + minutes)

                return unixTime

        elif sourceName == 'WMAR':
            if len(dateString.strip().split(' ')) == 5:
                timeA, timeB, month, day, year = dateString.strip().split(' ')
                monthNum = str(self.monthMap[month.lower()[:3]])
                timeB = timeB.replace(',', '')
                day = day.replace(',', '')
                slashDate = day + '/' + monthNum + '/' + year
                print(slashDate)
                unixTime = time.mktime(datetime.datetime.strptime(slashDate, "%d/%m/%Y").timetuple())

                hours = int(timeA.split(':')[0])
                if timeB.lower() == 'pm':
                    hours += 12
                minutes = int(timeA.split(':')[1])
                hours *= 3600
                minutes *= 60
                unixTime += (hours + minutes)

                return unixTime
        
        return None

    def enrich_json(self, artDict, sourceName):
        artText = artDict['body']
        artDict['source'] = sourceName
        doc = self.nlp(artText)
        matches = self.matcher(doc)
        sentStarts = []
        sentEnds = []
        misconductScore = 0
        if len(matches) > 0 and 'Terms of Use Agreement' not in artDict['title']:
            for matchId, _, _ in matches:
                matchType = nlp.vocab.strings[matchId]
                if matchType == 'OnePatterns':
                    misconductScore += 1
                elif matchType == 'TwoPatterns':
                    misconductScore += 2
                elif matchType == 'ThreePatterns':
                    misconductScore += 3

            persons = []
            orgs = []
            locations = []
            addresses = []
            coordTuples = []
            print(artDict['title'])
            for sent in doc.sents:
                sentStarts.append(sent.start)
                sentEnds.append(sent.end)
            knownPersons = []
            knownOrgs = []
            knownLocations = []
            knownLocTuples= []
            for i, sentence in enumerate(doc.ents):
                if sentence.label_ in ['PERSON']:
                    if str(sentence) not in knownPersons:
                        knownPersons.append(str(sentence))
                        persons.append(str(sentence))
                if sentence.label_ in ['ORG']:
                    if str(sentence) not in knownOrgs:
                        knownOrgs.append(str(sentence))
                        orgs.append(str(sentence))
                if sentence.label_ == 'GPE': 
                    if str(sentence).lower() not in knownLocations:
                        knownLocations.append(str(sentence).lower())
                        if 'D-' not in str(sentence) and 'R-' not in str(sentence):
                            knownLocTuples.append((i, str(sentence)))

            locBuffer = []
            for i, knownLocTuple in enumerate(knownLocTuples):
                idx, locStr = knownLocTuple
                print(locStr)
                if i < len(knownLocTuples) - 1 and idx == knownLocTuples[i + 1][0] - 1:
                    locBuffer.append(locStr)
                else:
                    try:
                        locBuffer.append(locStr)
                        print(locBuffer)
                        if len(locBuffer) > 1:
                            tempLocs = []
                            tempCoords = []
                            tempAddresses = []
                            areSame = True
                            for item in locBuffer:
                                tempLoc = self.geolocator.geocode(item)
                                tempX, tempY = tempLoc.longitude, tempLoc.latitude
                                tempCoords.append([tempX, tempY])
                                tempAddresses.append(tempLoc.address)
                                tempLocs.append(item)
                            prevCoords = tempCoords[0]
                            for coords in tempCoords[1:]:
                                if (coords[0] - prevCoords[0]) ** 2 > 400:
                                    areSame = False
                                    break
                                elif (coords[1] - prevCoords[1]) ** 2 > 400:
                                    areSame = False
                                    break
                                prevCoords = copy(coords)
                            if not areSame:
                                locations.extend(tempLocs)
                                addresses.extend(tempAddresses)
                                coordTuples.extend(tempCoords)
                        location = self.geolocator.geocode(' '.join(locBuffer))
                        if location is not None:
                            locations.append(' '.join(locBuffer))
                            addresses.append(location.address)
                            coordTuples.append([location.longitude, location.latitude])
                    except:
                        print('failed location retrieval')
                    locBuffer = []

            artDict['persons'] = persons
            artDict['orgs'] = orgs
            artDict['locations'] = locations
            artDict['addresses'] = addresses
            artDict['coords'] = coordTuples
            artDict['misconductScore'] = misconductScore

            artDict['date'] = self.get_unix_time(artDict['date'], sourceName)
            artDict['access_date']  = self.get_unix_time(artDict['access_date'], "BaltimoreFishbowl")

            if artDict['date'] is None:
                artDict['date'] = artDict['access_date']
        
            return artDict
        return None


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="WKYT", help="Which news source to use. Options are [ABC, BaltimoreFishbowl, CNN, NJ, NPR, WJLA, WKYT]")
    args = parser.parse_args()
    sourceName = args.source

    geolocator = Nominatim(user_agent="news_scraper")

    nlp = spacy.load("en_core_web_sm")
    matcher = PhraseMatcher(nlp.vocab, attr="LOWER")
    terms = ["police", "constable", "sheriff", "peace officer", "law enforcement"]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("PolicePersons", patterns)

    terms = ["detain", "arrest", "unarmed", "handcuff"]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("PoliceActions", patterns)

    terms = ["LPD"]
    patterns = [nlp.make_doc(text) for text in terms]
    matcher.add("PoliceOrganizations", patterns)

    monthMap = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april': 4,
        'may': 5,
        'june': 6,
        'july': 7,
        'august': 8,
        'september': 9,
        'october': 10,
        'november': 11,
        'december': 12,
    }

    for scrapedDir in os.listdir('newsscraper/Scraped/'):
        newsDir = 'newsscraper/Scraped/' + scrapedDir + '/'
        jsonFileNames = [fileName for fileName in os.listdir(newsDir) if '.json' in fileName]
        #personOrgTuples = []
        #locTuples = []
        #keywordTuples = []
        for jsonFileName in jsonFileNames:
            with open(newsDir + jsonFileName, 'r') as jsonFile:
                artDict = json.load(jsonFile)
                artText = artDict['body']
                artDict['source'] = sourceName
                doc = nlp(artText)
                matches = matcher(doc)
                sentStarts = []
                sentEnds = []
                if len(matches) > 0 and 'Terms of Use Agreement' not in artDict['title']:
                    persons = []
                    orgs = []
                    locations = []
                    addresses = []
                    coordTuples = []
                    print(artDict['title'])
                    for sent in doc.sents:
                        sentStarts.append(sent.start)
                        sentEnds.append(sent.end)
                    knownPersons = []
                    knownOrgs = []
                    knownLocations = []
                    knownLocTuples= []
                    for i, sentence in enumerate(doc.ents):
                        if sentence.label_ in ['PERSON']:
                            if str(sentence) not in knownPersons:
                                knownPersons.append(str(sentence))
                                persons.append(str(sentence))
                        if sentence.label_ in ['ORG']:
                            if str(sentence) not in knownOrgs:
                                knownOrgs.append(str(sentence))
                                orgs.append(str(sentence))
                        if sentence.label_ == 'GPE': 
                            if str(sentence).lower() not in knownLocations:
                                knownLocations.append(str(sentence).lower())
                                if 'D-' not in str(sentence) and 'R-' not in str(sentence):
                                    knownLocTuples.append((i, str(sentence)))

                    locBuffer = []
                    for i, knownLocTuple in enumerate(knownLocTuples):
                        idx, locStr = knownLocTuple
                        print(locStr)
                        if i < len(knownLocTuples) - 1 and idx == knownLocTuples[i + 1][0] - 1:
                            locBuffer.append(locStr)
                        else:
                            try:
                                locBuffer.append(locStr)
                                print(locBuffer)
                                if len(locBuffer) > 1:
                                    tempLocs = []
                                    tempCoords = []
                                    tempAddresses = []
                                    areSame = True
                                    for item in locBuffer:
                                        tempLoc = geolocator.geocode(item)
                                        tempX, tempY = tempLoc.longitude, tempLoc.latitude
                                        tempCoords.append([tempX, tempY])
                                        tempAddresses.append(tempLoc.address)
                                        tempLocs.append(item)
                                    prevCoords = tempCoords[0]
                                    for coords in tempCoords[1:]:
                                        if (coords[0] - prevCoords[0]) ** 2 > 400:
                                            areSame = False
                                            break
                                        elif (coords[1] - prevCoords[1]) ** 2 > 400:
                                            areSame = False
                                            break
                                        prevCoords = copy(coords)
                                    if not areSame:
                                        locations.extend(tempLocs)
                                        addresses.extend(tempAddresses)
                                        coordTuples.extend(tempCoords)
                                location = geolocator.geocode(' '.join(locBuffer))
                                if location is not None:
                                    locations.append(' '.join(locBuffer))
                                    addresses.append(location.address)
                                    coordTuples.append([location.longitude, location.latitude])
                            except:
                                print('failed location retrieval')
                            locBuffer = []

                    artDict['persons'] = persons
                    artDict['orgs'] = orgs
                    artDict['locations'] = locations
                    artDict['addresses'] = addresses
                    artDict['coords'] = coordTuples
                    artDict['misconductProb'] = 0.5

                    if scrapedDir == 'ABC':
                        dateString = artDict['date']
                        if len(dateString.split(' ')) != 5:
                            continue
                        month, day, year, timeA, timeB = dateString.split(' ')
                        monthNum = str(monthMap[month.lower()])
                        day = day.replace(',', '')
                        year = year.replace(',', '')
                        slashDate = day + '/' + monthNum + '/' + year
                        print(slashDate)
                        unixTime = time.mktime(datetime.datetime.strptime(slashDate, "%d/%m/%Y").timetuple())

                        hours = int(timeA.split(':')[0])
                        if timeB.lower() == 'pm':
                            hours += 12
                        minutes = int(timeA.split(':')[1])
                        hours *= 3600
                        minutes *= 60
                        unixTime += (hours + minutes)

                        artDict['date'] = unixTime

                    elif scrapedDir == 'BaltimoreFishbowl':
                        dateString = artDict['date']
                        datePortion, timePortion = dateString.split('T')
                        unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

                        hours, minutes, seconds = timePortion[:8].split(':')
                        seconds = int(seconds)
                        seconds += (int(hours) * 3600)
                        seconds += (int(minutes) * 60)
                        unixTime += seconds

                        artDict['date'] = unixTime

                    elif scrapedDir == 'NJ':
                        dateString = artDict['date']
                        datePortion, timePortion = dateString[:10], dateString[-8:]
                        unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

                        hours, minutes, seconds = timePortion.split(':')
                        seconds = int(seconds)
                        seconds += (int(hours) * 3600)
                        seconds += (int(minutes) * 60)
                        unixTime += seconds

                        artDict['date'] = unixTime

                    elif scrapedDir == 'NPR':
                        dateString = artDict['date']
                        if len(dateString.split(' ')) != 2:
                            continue
                        datePortion, timePortion = dateString.split('T')
                        unixTime = time.mktime(datetime.datetime.strptime(datePortion, "%Y-%m-%d").timetuple())

                        hours, minutes, seconds = timePortion[:8].split(':')
                        seconds = int(seconds)
                        seconds += (int(hours) * 3600)
                        seconds += (int(minutes) * 60)
                        unixTime += seconds

                        artDict['date'] = unixTime

                    else:
                        continue

                    artDict['access_date']  = artDict['date']
                    
                    if 'processed' not in os.listdir():
                        os.makedirs('processed')
                    with open('processed/' + jsonFileName, 'w+') as jsonFile:
                        print('writing json')
                        json.dump(artDict, jsonFile)
                                
                """
                for matchId, start, end in matches:
                    stringId = nlp.vocab.strings[matchId]  # Get string representation
                    keyword = doc[start:end].text
                    keywordIdx = start
                    for startIndex in reversed(sentStarts):
                        if startIndex <= start:
                            start = startIndex
                            break
                    for endIndex in sentEnds:
                        if endIndex >= end:
                            end = endIndex
                            break
                    #start = max(0, start-8)
                    #end = min(end+8, len(doc))
                    containingSentence = doc[start:end].text
                    sentStartIdx = start
                    sentEndIdx = end
                    #print(matchId, stringId, start, end, span.text)
                    keywordTuples.append([artDict['UUID'], keyword, str(keywordIdx), containingSentence, str(sentStartIdx), str(sentEndIdx)])
                if len(matches) > 0:
                    print('\n')
                """

        """
        with open('WKYT_entities.csv', 'w') as writeFile:
            for tup in entityTuples:
                writeFile.write('|'.join(tup) + '\n')

        with open('WKYT_keywords.csv', 'w') as writeFile:
            for tup in keywordTuples:
                writeFile.write('|'.join(tup) + '\n')
        """