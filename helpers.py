import random
from storedData import phrases

def error():
    print(random.choice(phrases.unk))


# Will choose a template from an array provided in param, and insert content
# into it
def naturalSpeechComposer(templates, content = None):
  template = random.choice(templates)
  if content == None:
    return template
  else:
    try:
      template = template.replace('CONTENT', content)
      return template
    except:
      return template
