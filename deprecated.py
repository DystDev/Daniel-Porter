# REF A1
''' DEPRECATED
    if self.queryType == qTypes.WEB:
      # print('web qeustion')
      if self.query == '': 
        self.query = self.obtainQuery(-1, 1)
      if self.query == None:
        self.error()
        return
      print(self.naturalSpeechComposer(phrases.definitionTemplates, self.getFromWiki(self.query)))
    if self.queryType == qTypes.PERSON:
      # print('person qeustion')
      if self.query == '':
        self.query = self.obtainQuery(-1, 1)
      if self.query == None:
        self.error()
        return
      print(self.naturalSpeechComposer(phrases.personTemplates, self.getFromWiki(self.query)))'''

# REF A2
# DEPRECATED
  # def getDefinition(self, query):
  #   response = requests.get(dictEndpoint + query)
  #   definition = response.json()
  #   try:
  #     definitionString = definition[0]['meanings'][0]['definitions'][0]['definition']
  #   except:
  #     print(self.naturalSpeechComposer(phrases.unknownDictionaryTemplates, query))
  #     return
  #   definitionString = definitionString[:-1] # Removes full stop
  #   definitionString = definitionString[:1].lower() + definitionString[1:] # Makes first letter lowercase
  #   print(self.naturalSpeechComposer(phrases.definitionTemplates, definitionString))