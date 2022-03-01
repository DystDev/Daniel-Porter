# Turing Test
# List who is in the group or if you are working alone.
# Rowan Marshall
# Alex Badman
# ---------------------------------------------------------------

# TODO: fat mog
# ',' in getFromWiki?
# - Add questions posed if the bot cannot understand
# - Add user info handling (i.e. can unshift name to start?)
# - Add 'question' question type
# - The wiki finder sometimes returns a "may refer to", turn this into an error message
# DONE - Fix iden.py formatting
# DONE - Add questions to be posed to user


# Imports
import iden # Identity
import phrases # Set phrases
import random # Add variation to the bot
from enum import Enum # Custom query types
import time # For waiting a bit -> more natural
import wikipediaapi # An API for wikipedia (surprisingly)
import re # Regex for funky string manipulation
# Lists
punctuation = ["?",".",","]
queryIdentity = ['you', 'your']
queryOpinion = ['do you']
queryWiki = ['who is', 'whos', "who's", 'what is a', 'what is an', 'search up', 'define', 'what is the meaning of']

# Query types enum
class qTypes(Enum):
  IDENTITY = 'IDENTITY'
  OPINION = 'OPINION'
  WIKI = 'WIKI'

# API Calls
dictEndpoint = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
wikiAPI = wikipediaapi.Wikipedia('en')



class Bot: # The main bot class
  def __init__(self): # Constructor
    pass

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
      self.isNewQuestion == False
    if self.usrMsg == '' and self.usrMsgFormat == '':
      self.usrMsg = self.formatAnswer(ans)
      self.usrMsgFormat = self.formatAnswerArray(ans)
    return ans

  # PARAMS: Prompt: Used for the prompt used for the input.
  def getQueryType(self):
    self.findSignifierFromArray(queryIdentity, qTypes.IDENTITY)
    self.findSignifierFromArray(queryWiki, qTypes.WIKI)
    # If the bot cannot find something to talk about, sends a random 
    # misunderstand message and TODO poses question to user
    last = self.usrMsgFormat[len(self.usrMsgFormat) -1]
    # If the topic has not been found, or the last word of the question
    # is the keyword, then find more broad topic.
    if self.queryType == None or last == self.lastKeyword: 
      self.backupFindTopic()
    if self.queryType == None:
      self.error()
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
    # REF A1 in deprecated.py
    if self.queryType == qTypes.WIKI:
      # print('wik qeustion')
      if self.query == '':
        self.query = self.obtainQuery(-1, 1)
      if self.query == None:
        self.error()
        return
      queryGotten = self.getFromWiki(self.query)
      if queryGotten == None:
        print(self.naturalSpeechComposer(phrases.unknownDictionaryTemplates, self.query))
      else:
        print(self.naturalSpeechComposer(phrases.wikiTemplates, queryGotten))
    if self.queryType == qTypes.IDENTITY:
      # print('identiyy question')
      if self.query == '': 
        self.query = self.obtainQuery(1, 1)
      if self.query == None or self.query not in iden.topics: # If the feature requested not in identity
        self.error()
        return
      self.queryIdentity()

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
      except:
        return
      return query
    elif dataNumberRequired == -1:
      try:
        queryList = qArr[qArr.index(usedKeyword)+1:]
        query = " ".join(queryList)
      except:
        return
      return query
    else:
      queryData = []
      try:
        for i in range(0, dataNumberRequired):
          queryData.append(qArr[qArr.index(usedKeyword) + offset + dataNumberRequired])
      except:
        return
      return queryData
  # REF A2 deprecated.py
  

  def getFromWiki(self, query):
    page = wikiAPI.page(query)
    pageData = page.summary
    pageData = pageData.split(".")[0]
    # It's regex time lets go
    pageData = re.sub(r"\(|\)", "", re.sub(r"\(.*?\)", "", pageData)) # Obliterates bracket phrases
    pageData = re.sub(r" ,", ",", pageData) # Annihilates " ," generated by bracket phrases
    pageData = re.sub(r"  ", " ", pageData)
    pageData = re.sub(r" ,", ",", pageData)# Annihiltes thingy again (cause yeh)
    if pageData == "" or pageData == None:
      pageData = None
    return pageData

    
  # Will choose a template from an array provided in param, and insert content
  # into it
  def naturalSpeechComposer(self, templates, content = None):
    template = random.choice(templates)
    if content == None:
      return template
    else:
      try:
        template = template.replace('CONTENT', content)
        return template
      except:
        return template


  # More broad searching for topic, so may misunderstand and only works identity.
  # However, it will work more often to find the topic.
  def backupFindTopic(self):
    for word in self.usrMsgFormat:
      # iden.topics is found in iden.py and collects all the topics from the iden object.
      if word in iden.topics:
        self.queryType = qTypes.IDENTITY
        self.query = word

  def queryIdentity(self):
    for tuple in iden.iden:
      for value in tuple:
        if self.query == value:
          i = iden.iden[tuple]
          responseTemplates = i['responses']
          # Pretty disgusting way to see which are provided
          try:
            value = i['value']
          except:
            self.postResponse(responseTemplates)
            return
          try:
            cb = i['callback']
            cbRec = i['cbRecieved']
          except:
            self.postResponse(responseTemplates, value)
            return
          self.postResponse(responseTemplates, value, cb, cbRec)
              
  def postResponse(self, templates, val = None, cb = None, cbRec = None):
    if val == None:
      print(random.choice(templates))
      time.sleep(0.5)
      return
    print(self.naturalSpeechComposer(templates, val))
    time.sleep(0.5)
    
    if cb != None and cbRec != None:
      usrResponse = self.askQuestion(random.choice(cb))
      print(self.naturalSpeechComposer(cbRec, usrResponse))
    
  def reset(self):
    # All examples after the question 'What is an apple?'
    self.lastKeyword = '' # e.g. 'what is an'
    self.usrMsg = '' # e.g. 'what is an apple'
    self.usrMsgFormat = '' # e.g. ['what', 'is', 'an', 'apple']
    self.queryType = None # e.g qTypes.WEB
    self.query = '' # e.g. apple
    self.isNewQuestion = True # e.g. wtf
    
  def error(self):
    print(random.choice(phrases.unk))
  



# Main program
dan = Bot() # Instance of the bot
dan.reset() # reset i.e. init most fields
while True:
  dan.handleConversation()