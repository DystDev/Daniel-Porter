# Turing Test
# List who is in the group or if you are working alone.
# Rowan Marshall
# Alex Badman
# ---------------------------------------------------------------

# TODO:
# - Fix iden.py formatting
# - Add questions to be posed to user
# - Add questions posed if the bot cannot understand
# - Add user info handling (i.e. can unshift name to start?)



# Imports
import iden # Identity
import phrases # Set phrases
import random # Add variation to the bot
from enum import Enum # Custom query types
import requests # For API calls
import time # For waiting a bit -> more natural
import wikipediaapi # An API for wikipedia (surprisingly)
# Lists
punctuation = ["?",".",","]
queryIdentity = ['you', 'your']
queryWeb = ['what is a', 'what is an', 'search up', 'define', 'what is the meaning of']
queryOpinion = ['do you']
queryPerson = ['who is', 'whos', "who's"]

# TODO:
# - Add 'question' question type
# - Add 'person' question type

# Query types enum
class qTypes(Enum):
  IDENTITY = 'IDENTITY'
  WEB = 'WEB'
  OPINION = 'OPINION'
  PERSON = 'PERSON'

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

  # 
  # PARAMS: Prompt: Used for the prompt used for the input.
  def getQueryType(self):
    self.findSignifierFromArray(queryIdentity, True, qTypes.IDENTITY)
    self.findSignifierFromArray(queryWeb, False, qTypes.WEB)
    self.findSignifierFromArray(queryPerson, False, qTypes.PERSON)
    # If the bot cannot find something to talk about, sends a random 
    # misunderstand message and TODO poses question to user
    last = self.usrMsgFormat[len(self.usrMsgFormat) -1]
    # If the topic has not been found, or the last word of the question
    # is the keyword, then find more broad topic.
    if self.queryType == None or last == self.usedKeyword: 
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
    if self.queryType == qTypes.WEB:
      # print('web qeustion')
      if self.query == '': 
        self.query = self.obtainQuery(True, 1)
      if self.query == None:
        self.error()
        return
      self.getDefinition(self.query)
    if self.queryType == qTypes.PERSON: # TODO - actually make this work rowan
      # print('person qeustion')
      if self.query == '':
        self.query = self.obtainQuery(True, 1)
      if self.query == None:
        self.error()
        return
    if self.queryType == qTypes.IDENTITY:
      # print('identiyy question')
      if self.query == '': 
        self.query = self.obtainQuery(False, 1)
      if self.query == None or self.query not in iden.topics: # If the feature requested not in identity
        self.error()
        return
      self.queryIdentity()

  def findSignifierFromArray(self, arrayOfSignifier, usesFormatted, targetQueryType):
    # Checks if query signifiers are in the user input
    for phrase in arrayOfSignifier:
      if usesFormatted:
        if phrase in self.usrMsgFormat:
          # Saves query type (enum) and the used keyword for future use
          self.queryType = targetQueryType
          self.usedKeyword = phrase
      else:
        if phrase in self.usrMsg:
          self.queryType = targetQueryType
          self.usedKeyword = phrase
  
  def obtainQuery(self, wasPhrase, futureIndex):
    usedKeyword = self.usedKeyword
    if wasPhrase:
      splitUserKeyword = usedKeyword.split(' ')
      usedKeyword = splitUserKeyword[len(splitUserKeyword) - 1]
    qArr = self.usrMsg.split(' ')
    try:
      query = qArr[qArr.index(usedKeyword) + futureIndex]
    except:
      return
    return query

  def getDefinition(self, query):
    response = requests.get(dictEndpoint + query)
    definition = response.json()
    try:
      definitionString = definition[0]['meanings'][0]['definitions'][0]['definition']
    except:
      print(self.naturalSpeechComposer(phrases.unknownDictionaryTemplates, query))
      return
    definitionString = definitionString[:-1] # Removes full stop
    definitionString = definitionString[:1].lower() + definitionString[1:] # Makes first letter lowercase
    print(self.naturalSpeechComposer(phrases.definitionTemplates, definitionString))

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
    self.usedKeyword = '' # e.g. 'what is an'
    self.usrMsg = '' # e.g. 'what is an apple'
    self.usrMsgFormat = '' # e.g. ['what', 'is', 'an', 'apple']
    self.queryType = None # e.g qTypes.WEB
    self.query = '' # e.g. apple
    self.isNewQuestion = True # e.g. wtf
    
  def error(self):
    print(random.choice(phrases.unk))
  



# Main program
dan = Bot() # Instance of the bot
dan.reset()
while True:
  dan.handleConversation()