# List who is in the group or if you are working alone.
# Rowan Marshall
# Alex Badman
# ---------------------------------------------------------------

# ',' in getFromWiki?
# - Add questions posed if the bot cannot understand
# - Add user info handling (i.e. can unshift name to start?)
# - Add 'question' question type
# - The wiki finder sometimes returns a "may refer to", turn this into an error message
# DONE - roadmap : add opinionfeature
# DONE - Fix iden.py formatting
# DONE - Add questions to be posed to user

# Imports
import random  # Add variation to the bot
from enum import Enum  # Custom query types
import time  # For waiting a bit -> more natural
from api import fetchWikipedia
from storedData import iden, opinions, phrases
import helpers
# Lists
punctuation = ["?", ".", ","]
queryIdentity = ['you', 'your']
queryOpinionVerb = ['do you']
queryOpinionFeature = ['are you', 'are you a', 'are you the']
queryWiki = ['who is', 'whos', "who's", 'what is a', 'what is an',
             'search up', 'define', 'what is the meaning of', 'who are']

# Query types enum


class qTypes(Enum):
    IDENTITY = 'IDENTITY'
    OPINIONVERB = 'OPINIONVERB'
    OPINIONFEATURE = 'OPINIONFEATURE'
    WIKI = 'WIKI'

# Query Types datanu/offset dictionary


qTypeFetchData = {
    qTypes.IDENTITY: [1, 1],
    qTypes.OPINIONVERB: [-2, 1],
    qTypes.OPINIONFEATURE: [-1, 1],
    qTypes.WIKI: [-1, 1]
}
# API Calls
dictEndpoint = 'https://api.dictionaryapi.dev/api/v2/entries/en/'


class Bot:  # The main bot class
    def __init__(self):  # Constructor
        self.lastKeyword = ''  # e.g. 'what is an'
        self.usrMsg = ''  # e.g. 'what is an apple'
        self.usrMsgFormat = ''  # e.g. ['what', 'is', 'an', 'apple']
        self.queryType = None  # e.g qTypes.WEB
        self.query = ''  # e.g. apple
        self.isNewQuestion = True  # e.g. wtf

    # Main method. Goes through steps of handling conversation.
    # PARAMS: N/A
    def handleConversation(self):
        self.askQuestion()
        self.getQueryType()
        self.composeResponse()

    # Poses question to user (complicated way of calling input()). If question
    # is the first asked, resets the bots and sets the local fields
    # PARAMS: Prompt: Used for the prompt used for the input.
    def askQuestion(self, prompt="What is your question? "):
        # Resets fields for each new question
        ans = input(prompt)
        if self.isNewQuestion == True:
            self.reset()
            self.isNewQuestion = False
        if self.usrMsg == '' and self.usrMsgFormat == '':
            self.usrMsg = self.formatAnswer(ans)
            self.usrMsgFormat = self.formatAnswerArray(ans)
        return ans

    # PARAMS: Prompt: Used for the prompt used for the input.
    def getQueryType(self):
        self.findSignifierFromArray(queryWiki, qTypes.WIKI)
        self.findSignifierFromArray(queryOpinionFeature, qTypes.OPINIONFEATURE)
        self.findSignifierFromArray(queryIdentity, qTypes.IDENTITY)
        self.findSignifierFromArray(queryOpinionVerb, qTypes.OPINIONVERB)

        # If the bot cannot find something to talk about, sends a random
        # misunderstand message and TODO poses question to user
        last = self.usrMsgFormat[len(self.usrMsgFormat) - 1]
        # If the topic has not been found, or the last word of the question
        # is the keyword, then find more broad topic.
        if self.queryType == None or last == self.lastKeyword:
            self.backupFindTopic()
        if self.queryType == None:
            helpers.error()
            return
        return

    # Prompts for answer question to user

    # Will remove punctuation and lower case

    def formatAnswer(self, ans):
        if ans[len(ans)-1] == '?':
            ans = ans[:len(ans)-1]
        return ans.lower()

    # Same as last, but will turn into array
    def formatAnswerArray(self, ans):
        if ans[len(ans)-1] == '?':
            ans = ans[:len(ans)-1]
        return ans.lower().split(' ')

    def composeResponse(self):
        print('Starting..., query type is', self.queryType)
        if self.queryType == None:  # If the bot has no idea what you mean :(
            helpers.error()
            return
        dataNumberRequired = qTypeFetchData[self.queryType][0]
        offset = qTypeFetchData[self.queryType][1]

        if self.query == '':
            self.query = self.obtainQuery(dataNumberRequired, offset)
        if self.query == None:
            helpers.error()
            return

        elif self.queryType == qTypes.WIKI:
            queryGotten = fetchWikipedia.getFromWiki(self.query)
            if queryGotten == None:
                print(helpers.naturalSpeechComposer(
                    phrases.unknownDictionaryTemplates, self.query))
            else:
                print(helpers.naturalSpeechComposer(
                    phrases.wikiTemplates, queryGotten))

        elif self.queryType == qTypes.IDENTITY:
            if self.query not in iden.topics:  # If the feature requested not in identity
                print('WOAH! Overriding...')
                self.queryType = qTypes.OPINIONFEATURE
                self.composeResponse()
                return
            self.queryIdentity()

        elif self.queryType == qTypes.OPINIONFEATURE:
            self.queryOpinionFeature()

        elif self.queryType == qTypes.OPINIONVERB:
            self.queryOpinionVerb()

    def findSignifierFromArray(self, arrayOfSignifier, targetQueryType):
        # Checks if query signifiers are in the user input
        for phrase in arrayOfSignifier:
            phraseSplit = phrase.split(' ')
            if ' '.join(phraseSplit) in self.usrMsg:
                # Saves query type (enum) and the used keyword for future use
                self.queryType = targetQueryType
                self.lastKeyword = phraseSplit[len(phraseSplit) - 1]

    def obtainQuery(self, dataNumberRequired, offset):
        usedKeyword = self.lastKeyword
        qArr = self.usrMsgFormat
        if dataNumberRequired == 1:
            try:
                query = qArr[qArr.index(usedKeyword) + offset]
            except (ReferenceError):
                return
            return query
        elif dataNumberRequired == -1:
            try:
                queryList = qArr[qArr.index(usedKeyword)+1:]
                query = " ".join(queryList)
            except (ReferenceError):
                return
            return query
        elif dataNumberRequired == -2:  # For verb phrase
            try:
                queryList = []
                queryList.append(qArr[qArr.index(usedKeyword)+1])
                queryList.append(qArr[qArr.index(usedKeyword)+2:])
            except (ReferenceError):
                return
            return queryList

    # More broad searching for topic, so may misunderstand and only works identity.
    # However, it will work more often to find the topic.
    def backupFindTopic(self):
        for word in self.usrMsgFormat:
            # iden.topics is found in iden.py and collects all the topics from the iden object.
            if word in iden.topics:
                self.queryType = qTypes.IDENTITY
                self.query = word

    def queryOpinionFeature(self):
        # this code is pretty mank
        if self.query not in opinions.opF.keys():
            opinions.opF[self.query] = random.randint(-2, 2)
        self.postResponse(
            phrases.featureOps[opinions.opF[self.query]], self.query)

    def queryOpinionVerb(self):
        verb = self.query[0]
        subject = ' '.join(self.query[1])
        if verb not in opinions.opV.keys():
            opinions.opV[verb] = {}
        verbSubjects = opinions.opV[verb]
        if subject not in verbSubjects.keys():
            opinions.opV[verb][subject] = random.randint(-2, 2)
        insert = verb + ' ' + subject
        insert.replace('to like', '')
        self.postResponse(
            phrases.verbOps[opinions.opV[verb][subject]], insert)

    def queryIdentity(self):
        for idenTuple in iden.iden:
            for value in idenTuple:
                if self.query == value:
                    i = iden.iden[idenTuple]
                    responseTemplates = i['responses']
                    # Pretty disgusting way to see which are provided
                    try:
                        value = i['value']
                    except (ReferenceError):
                        self.postResponse(responseTemplates)
                        return
                    try:
                        cb = i['callback']
                        cbRec = i['cbRecieved']
                    except (ReferenceError):
                        self.postResponse(responseTemplates, value)
                        return
                    self.postResponse(responseTemplates, value, cb, cbRec)

    def postResponse(self, templates, val=None, cb=None, cbRec=None):
        if val == None:
            print(random.choice(templates))
            time.sleep(0.5)
            return
        print(helpers.naturalSpeechComposer(templates, val))
        time.sleep(0.5)

        if cb != None and cbRec != None:
            usrResponse = self.askQuestion(random.choice(cb))
            print(helpers.naturalSpeechComposer(cbRec, usrResponse))

    def reset(self):
        # All examples after the question 'What is an apple?'
        self.lastKeyword = ''  # e.g. 'what is an'
        self.usrMsg = ''  # e.g. 'what is an apple'
        self.usrMsgFormat = ''  # e.g. ['what', 'is', 'an', 'apple']
        self.queryType = None  # e.g qTypes.WEB
        self.query = ''  # e.g. apple
        self.isNewQuestion = True  # e.g. wtf


# Main program
dan = Bot()  # Instance of the bot
dan.reset()  # reset i.e. init most fields
while True:
    dan.handleConversation()
