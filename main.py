import banidb
import speech_recognition as sr
import logging

# Set the logging level to DEBUG when in debugging mode
debug_mode = True  # Set this variable based on your debugging conditions

# check the logging level
if debug_mode:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

def get_shabad_query():
    """
    Gets the user input by listening to the audio and then invokes get_shabad_matches() 
    once the user input is taken and validated
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

    logging.info(f"Finding matching shabads for \"{shabad_verse}\"")
    matching_shabad_collection = {}
    probability_threshold = 0

    matching_shabads = banidb.search(shabad_query)
    logging.info("-----------Best Shabad Matches-----------")
    for matches in matching_shabads['pages_data'].values():
        for shabad in matches:
            probability_threshold = get_match_probability(shabad_verse, shabad['verse'])
            if probability_threshold > 66: 
                # 66 is based on conclusion that if two words
                # are matched out of 3 based on the smallest required query length
                logging.info(f"{len(matching_shabad_collection) + 1}. {shabad['verse']} ({shabad['source']['writer']})")
                matching_shabad_collection[len(matching_shabad_collection) + 1] = shabad

    if (len(matching_shabad_collection) == 0): logging.info("No results found") 
    else: 
        logging.info(f"{len(matching_shabad_collection)} results found.")
        while True:
            try:
                shabad_choice = eval(input("Enter shabad number: "))
                shabad_id = matching_shabad_collection[shabad_choice]['shabad_id']
            except KeyError:
                logging.info("Not a valid option!")
            except SyntaxError:
                logging.info("Enter something!")
            except NameError:
                logging.info("Try Again!")
            else:
                display_shabad(shabad_id)
                break

def get_match_probability(speech_input, shabad_verse):
    """
    Gets the matching probability between the user input and the shabad verse

    Returns 100 for exact match of shabad (should return 100 but is not returning more than 30)
    """
    matching_words = 0
    matched_words = []
    speech_input = speech_input.split()
    shabad_verse = shabad_verse.split()

    # TODO: Decide factors to reduce number of comparisons
    # TODO: Calculate probability such that it returns 100 for exact match
    for i in speech_input:
        if i in shabad_verse:
            matching_words += 1
            matched_words.append(i)
            
    return (matching_words/len(speech_input)) * 100

def display_shabad(shabad_id):
    """
    Searches banidb by the shabad_id and print the shabad part of the result after extracting it from json
    """
    chosen_shabad = banidb.shabad(shabad_id)
    for ver in chosen_shabad['verses']:
        logging.info(ver['verse'])
    banidb.clear() # Not quite sure what this does. Maybe clears the cache. But it is still making a 
                   #  cache.dat in my folder which contains a json file for shabad on reading

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
                
                logging.info("Listening...")
                # set timeout to 10 seconds
                audio = rec.listen(source, timeout=10)

                # Convert the audio to text 
                audioText = rec.recognize_google(audio, language='pa-in')

                return audioText
        except Exception:
            pass

def turn_into_bani_query(text):
    """
    Turns the user input into a bani query. i.e. Taking first letter of each word and joining together

    Returns the bani query
    """
    bani_query = ''
    for word in text.split():
        bani_query +=  word[0]
    
    # logging.debug("Turning into bani query...")
    # logging.debug("--------------------------------")
    # logging.debug("bani_query:", bani_query)
    return bani_query

# Main function
get_shabad_query()