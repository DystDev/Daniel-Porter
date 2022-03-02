
**Daniel Porter Bot Information v1.0**

**By Alex Badman and Rowan Marshall**

**<span style="text-decoration:underline;">1 - Overview</span>**

Daniel Porter, our bot, will take input and respond intelligently based on your input, trying to emulate the act of real human conversation. This document will go over the choices in design of the bot algorithm, the files and modules we used and then go into some deeper code explanation for each function, in general order of execution.

**<span style="text-decoration:underline;">2 - Event Loop</span>**

![flowchart](/flow.png)

This is a flowchart showing the current event loop, including all methods of the **main Bot() class** that can be used to create instances of the bot. From there, the **handleConversation** method must be called to initiate the dialogue between the user and the bot. The main three methods are **askQuestion, getQueryType and composeResponse**, which in turn use their own methods to help out. The helpers seen at the top left are used to help format data and send similar messages to the user at various times. **NOTE: Dotted methods and lines represent functionality planned but not yet implemented.**

**<span style="text-decoration:underline;">3 - Other Files</span>**

In our program, to store the bot’s personal information and set phrases, we add two files, **iden.py **(for identity storage e.g. bot’s name, age, hobbies), and **phrases.py **(for storing things such as natural error messages, greeting templates, information presentation templates, which i turn can be chosen between for a more natural and randomised yet standardised response from the bot. Snippets:

**iden.py:**


```
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
}
```


**phrases.py:**


```
unk = ['Sorry, I didn\'t quite catch that. Please can you rephrase?', 'I don\'t understand, sorry', 'Hmm. I don\'t quite know about that one.', 'I don\'t get it', 'Say again? I don\'t understand.', 'I don\'t understand what you mean', 'What do you mean?']

wikiTemplates = ["I'm pretty sure CONTENT", "I think CONTENT", "CONTENT, right?"]

unknownDictionaryTemplates = ['I don\'t know what a CONTENT is', 'I have no idea what a CONTENT is', 'What\'s that? I haven\'t seen that before']

unknownPreQuestion = ['On the other hand...', 'Let me ask you something.', 'I\'ve got a question for you']
```


m

**<span style="text-decoration:underline;">4 - Code Analysis</span>**

In this section we explore the line by line analysis of the Daniel porter Code. The full code can be found at https://github.com/DystDev/Daniel-Porter/blob/main/main.py

**<span style="text-decoration:underline;">i. Imports:</span>**


```
# Imports
import iden # Identity
import phrases # Set phrases
import opinions # Storing generated opinions of the bot
import random # Add variation to the bot
from enum import Enum # Custom query types
import time # For waiting a bit -> more natural
import wikipediaapi # An API for fetching wikipedia content
import re # Regex for string manipulation
```


In this block of code we import necessary **modules** for our program. These include other python files we created i.e. iden.py, phrases.py and opinions.py (both as seen above). We import modules for these reasons:



* **random - **to add random phrase picking to make the bot more natural (see **naturalSpeechComposer**)
* **enum **- to add our custom query types, as seen here:

```
# Query types enum
class qTypes(Enum):
  IDENTITY = 'IDENTITY'
  OPINION = 'OPINION'
  WIKI = 'WIKI'
```


* **time **- this is simply for some deliberate hesitance in the bot’s response to mimic a more natural ‘thinking time’
* **wikipediaapi** - we use this api to help our requests to the site for definitions of words and fact knowledge.
* **re - **regex module, used for powerful string manipulation in data received from the fetched data from wikipedia.

**<span style="text-decoration:underline;">ii. Variables/Member Variables:</span>**


```
# Lists
queryIdentity = ['you', 'your']
queryOpinion = ['do you']
queryWiki = ['who is', 'whos', "who's", 'what is a', 'what is an', 'search up', 'define', 'what is the meaning of']

# Query types enum
class qTypes(Enum):
  IDENTITY = 'IDENTITY'
  OPINIONVERB = 'OPINIONVERB'
  OPINIONADJ = 'OPINIONADJ'
  OPINIONNOUN = 'OPINIONNOUN'
  WIKI = 'WIKI'


# API Calls
dictEndpoint = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
wikiAPI = wikipediaapi.Wikipedia('en')
```


In this section the necessary **global variables** are initiated for use by the bot, including lists, api endpoints and the qTypes enum. Query types are split into the following:



* **Identity**; asking **hardcoded features of the bot** e.g. the bot’s name **<span style="text-decoration:underline;">(e.g. ‘What is your name’)</span>**
* **OpinionVerb**; asking arbitrary opinions on if the bot ‘somethings’ something. This is not hardcoded, but instead we chose to **choose a random opinion of the bot** and** save it at runtime** **so the bot does not contradict itself** at a later question time. **<span style="text-decoration:underline;">(e.g. ‘Do you like playing the drums?’)</span>**
* **OpinionAdj**; same as verbs, but for features of the bot that we did not hardcode **<span style="text-decoration:underline;">(e.g. ‘Are you young?’)</span>**
* **OpinionNoun**; same as other opinions, but for comparing the bot to something else **<span style="text-decoration:underline;">(e.g. ‘Are you a waiter?’)</span>**
* **Wiki**; we chose this type similar to a smart assistant e.g. Alexa. **The question is parsed then information is obtained from the internet**. We **considered using this method for any question that the bot did not understand** to reduce ‘I don’t understand sorry’ however the **bot would end up contradicting itself and sounding unnatural**, so we kept the old error method. **<span style="text-decoration:underline;">(e.g. ‘Who is Donald Trump’)</span>**

**<span style="text-decoration:underline;">iii. obtainQuery</span>**

In this snippet of code, we had to allow for the following test cases:


<table>
  <tr>
   <td><strong><span style="text-decoration:underline;">Query Type:</span></strong>
   </td>
   <td><strong><span style="text-decoration:underline;">Input (question), string, </span></strong>
   </td>
   <td><strong><span style="text-decoration:underline;">Output required.</span></strong>
   </td>
  </tr>
  <tr>
   <td><strong>Identity</strong>
   </td>
   <td><strong>What is your name?</strong>
   </td>
   <td><strong>‘name’</strong>
   </td>
  </tr>
  <tr>
   <td><strong>Wiki</strong>
   </td>
   <td><strong>Who is Donald Trump?</strong>
   </td>
   <td><strong>‘Donald trump’</strong>
   </td>
  </tr>
  <tr>
   <td><strong>OpinionVerb</strong>
   </td>
   <td><strong>Do you like playing the drums?</strong>
   </td>
   <td><strong>‘Like’, ‘playing the drums’</strong>
   </td>
  </tr>
  <tr>
   <td><strong>OpinionNoun</strong>
   </td>
   <td><strong>Are you a boy?</strong>
   </td>
   <td><strong>‘boy’</strong>
   </td>
  </tr>
  <tr>
   <td><strong>OpinionAdj</strong>
   </td>
   <td><strong>Are you young?</strong>
   </td>
   <td><strong>‘young’</strong>
   </td>
  </tr>
</table>


**<span style="text-decoration:underline;"> </span>**