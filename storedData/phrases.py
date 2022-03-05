unk = ['Sorry, I didn\'t quite catch that. Please can you rephrase?', 'I don\'t understand, sorry', 'Hmm. I don\'t quite know about that one.', 'I don\'t get it', 'Say again? I don\'t understand.', 'I don\'t understand what you mean', 'What do you mean?']

wikiTemplates = ["CONTENT, I'm pretty sure ", "CONTENT, I think", "CONTENT, right?"]

unknownDictionaryTemplates = ['I don\'t know what a CONTENT is', 'I have no idea what a CONTENT is', 'What\'s that? I haven\'t seen that before']

unknownPreQuestion = ['On the other hand...', 'Let me ask you something.', 'I\'ve got a question for you']


# Feature response set phrases
featureOps = {
  -2: ['No, of course I\'m not CONTENT!', 'I\'m not CONTENT....', 'Umm? No - I\'m not CONTENT'], 
  -1: ['No, I\'m not CONTENT', 'Unfortunately, I\'m not CONTENT', 'Nope, not CONTENT'], 
  0: ['I\'m not really sure if I\'m CONTENT or not.', 'I could be CONTENT, I haven\'t really thought about that though.', 'Umm, maybe? I could be CONTENT.'], 
  1: ['Yes, I\'m CONTENT', 'Fortunately, I am CONTENT', 'Yeah, I am CONTENT actually'], 
  2: ['Yes, I\'m CONTENT! Thanks for asking', 'Thankfully, I\'m CONTENT!', 'Yeah, I really like being CONTENT!']}

# Verb response set phrases

verbOps =  {
  -2: ["No, I hate to CONTENT, what are you on about??", 'No no no, I never CONTENT - I really don\'t like it'], 
  -1: ["No, I don't CONTENT much"], 
  0: ["Uh, I'm not really sure if I CONTENT"], 
  1: ["Yeah, I CONTENT a bit"], 
  2: ["Yeah, I CONTENT, its pretty fun"]}
