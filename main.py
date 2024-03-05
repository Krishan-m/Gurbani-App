import banidb
import speech_recognition as sr

def get_shabad_query():
    """
    Gets the user input by listening to the audio and then invokes get_shabad_matches() once the user input is taken and validated
    """
    while True:
        speech_input = search_from_speech()
        shabad_query = turn_into_bani_query(speech_input)
        if len(shabad_query) > 2:
            get_shabad_matches(shabad_query, speech_input)
            break                

def get_shabad_matches(shabad_query, shabad_verse=""):
    """
    Invoked by get_shabad_query

    Prints matching shabads and asks user to select their shabad
    """
    # TODO: Display the best match of shabad based on user input

    print("Finding matching shabads...")
    matching_shabad_collection = {}
    probability_threshold = 0

    matching_shabads = banidb.search(shabad_query)
    for matches in matching_shabads['pages_data'].values():
        for shabad in matches:
            probability_threshold = get_match_probability(shabad_verse, shabad['verse'])
            if probability_threshold > 80: # 80 is just a rough guess for match probability for now
                print(f"{len(matching_shabad_collection) + 1}. {shabad['verse']} ({shabad['source']['writer']})")
                matching_shabad_collection[len(matching_shabad_collection) + 1] = shabad

    if (len(matching_shabad_collection) == 0): print("No results found") 
    else: 
        print(f"{len(matching_shabad_collection)} results found.")
        shabad_choice = eval(input("Enter shabad number: "))
        try:
            shabad_id = matching_shabad_collection[shabad_choice]['shabad_id']
        except KeyError:
            print("Not a valid option!")
        else:
            display_shabad(shabad_id)

def get_match_probability(speech_input, shabad_verse):
    """
    Gets the matching probability between the user input and the shabad verse

    Returns 100 for exact match of shabad (should return 100 but is not returning more than 30)
    """
    matching_words = 0
    speech_input = speech_input.split()
    shabad_verse = shabad_verse.split()

    # TODO: Decide factors to reduce number of comparisons
    # TODO: Calculate probability such that it returns 100 for exact match
    for i in range(len(shabad_verse)):
        try:
            if speech_input[i] in shabad_verse:
                matching_words += 1
        except IndexError:
            pass
    print((matching_words/len(shabad_verse)) * 100)
    return (matching_words/len(shabad_verse)) * 100

def display_shabad(shabad_id):
    """
    Searches banidb by the shabad_id and print the shabad part of the result after extracting it from json
    """
    chosen_shabad = banidb.shabad(shabad_id)
    for ver in chosen_shabad['verses']:
        print(ver['verse'])
    banidb.clear() # Not quite sure what this does. Maybe clears the cache. But it is still making a cache.dat in my folder which contains a json file for shabad on reading

def search_from_speech():
    """
    Gets the voice input from user

    Returns the final user input
    """
    # Initializing a Recognizer object
    rec = sr.Recognizer()
    while True: # Listens until it could interpret the input
        try:
            # Making a Microphone object
            with sr.Microphone() as source:
                rec.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = rec.listen(source)
                audioText = rec.recognize_google(audio, language='pa-in')

                return audioText
        except Exception:
            pass

def turn_into_bani_query(text):
    """
    Turns the user input into a bani query. i.e. Taking first letter of each word and joining together

    Returns the bani query
    """
    bani_qeury = ''
    for word in text.split():
        bani_qeury +=  word[0]
    return bani_qeury

get_shabad_query()