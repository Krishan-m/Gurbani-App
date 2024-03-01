import banidb
import speech_recognition as sr

def getShabadQuery():
    # return input("Find Shabad: ")
    speechInput = search_from_speech()
    return {'query': turn_into_bani_query(speechInput), 
            'verse': speechInput}

def getShabadMatches():
    while True:
        try:
            shabadOrg = getShabadQuery()
            shabadQuery = shabadOrg['query']
            shabadVerse = shabadOrg['verse']
            matchingShabads = banidb.search(shabadQuery, searchtype=0)
            break
        except Exception as e:
            print(e)

    matchStore = {}
    print(shabadOrg)
    for matches in matchingShabads['pages_data'].values():
        for shabad in matches:
            print(f"{len(matchStore) + 1}. {shabad['verse']} ({shabad['source']['writer']})")
            matchStore[len(matchStore) + 1] = shabad

    if (len(matchStore) == 0): print("No results found") 
    else: 
        print(f"{len(matchStore)} results found.")
        shabadChoice = eval(input("Enter shabad number: "))
        shabad_id = matchStore[shabadChoice]['shabad_id']
        displayShabad(shabad_id)
        # for num, shabad in matchStore.items():
        #     if shabad['verse'] in shabadOrg['verse']:
        #         shabad_id = matchStore[num]['shabad_id']
        #         displayShabad(shabad_id)
        #         break
        # else:
        #     print("No matching shabad found")

def displayShabad(shabad_id):
    chosenShabad = banidb.shabad(shabad_id)
    for ver in chosenShabad['verses']:
        print(ver['verse'])
    banidb.clear()

def search_from_speech():
    rec = sr.Recognizer()

    while True:
        try:
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source, duration=0.7)
                print("Listening...")
                audio = rec.listen(source)
                audioText = rec.recognize_google(audio, language='pa-in')

                return audioText
        except Exception:
            pass

def turn_into_bani_query(text):
    bani_qeury = ''
    for word in text.split():
        bani_qeury +=  word[0]
    return bani_qeury

# shabadInit = input("Find Shabad: ")
# print("Listening Shabad...")
# shabadInput = search_from_speech()
# print(shabadInput)
# shabadQuery = turn_into_bani_query(shabadInput)
# print(shabadQuery)
# getShabadMatches(shabadQuery)

# query = getShabadQuery()['query']

getShabadMatches()