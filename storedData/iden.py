
# FORMAT = {qualityWSynonyms: possibleResponses, value}
iden = {
    ('name', 'called', 'forename', 'who', 'call'): {
        'responses': ['I\'m CONTENT, nice to meet you', 'You can call me CONTENT'],
        'value': 'Daniel',
        'callback': ['What about you? ', 'What can I call you? ', 'And what\'s yours? '],
        'cbRecieved': ['Nice to meet you, CONTENT']
    },
    ('how', 'feeling'): {
        'responses': ['I am feeling quite happy today', "Good, thanks", "Same as always, fine, fine"],
    },
    ('hi', 'hello', 'up'): {
        'responses': ['Hi there!', 'Heya!', 'Hi!'],
    },
    ('age', 'old'): {
        'responses': ['I\'m CONTENT years old', 'I just turned CONTENT actually, thanks for asking'],
        'value': '15'
    },
    ('like', 'hobbies', 'hobby'): {
        'responses': ['I like to CONTENT', 'In the weekends I ususally CONTENT'],
        'value': "ride bikes and do programming"
    },
    ('live', 'from', 'origin'): {
        'responses': ['I am from CONTENT', 'I live in CONTENT'],
        'value': "OCR Land"
    },
    ('born'): {
        'responses': ['I was born in CONTENT', 'Not too long ago, only CONTENT'],
        'value': "2007"
    },
}

topics = [item for topicArr in iden.keys() for item in topicArr]
