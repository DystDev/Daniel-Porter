
# FORMAT = {qualityWSynonyms: possibleResponses, value}
iden = {
  ('name', 'called', 'forename', 'who', 'call'):{
    'responses':['I\'m CONTENT, nice to meet you', 'You can call me CONTENT'],
    'value':'Daniel',
    'callback':['What about you? ', 'What can I call you? ', 'And what\'s yours?'],
    'cbRecieved':['Nice to meet you, CONTENT']
  },
  ('hi', 'hello'):{
    'responses':['Hi there!', 'Heya!', 'Hi!'],
  },
  ('age', 'old'):{
    'responses':['I\'m CONTENT years old', 'I just turned CONTENT actually, thanks for asking'],
    'value':'15'
  },
  ('like', 'hobbies', 'hobby'):{
    'responses':['I like to CONTENT', 'In the weekends I ususally CONTENT'],
    'value':'ride bikes and do programming'
  },
  ('how'):{
    'responses':['I\'m alright thanks', 'Not bad today.', 'Same as always, fine fine'],
    'value':'Daniel',
    'response':['What about you? ', 'What can I call you? ', 'And what\'s yours?'],
    'callback':['Nice to meet you, CONTENT']
  }
}

topics = []

for topicArr in iden.keys():
  for topic in topicArr:
    topics.append(topic)
