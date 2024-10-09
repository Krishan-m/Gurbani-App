# Database for gurbani resources
import banidb 

# Help recognize speech
import speech_recognition as sr 

# Convert Gurmukhi into Unicode and vice versa
from gurmukhiutils.constants import VOWEL_LETTERS, BASE_LETTERS

# ---- Ignore this part of the code ----
# Keep in mind - "L", "S", "Z" for later referrence
# MATRA_UNICODE = ["i", "o", "u", "w", "y", "H", "I", "M", "N", "O", "R", "U", "W", "Y", "[", "]", "`", "~", "@", "ü", "®", "\u00b4", "\u00a8", "µ", "æ", "Í", "Î", "Ï", "Ò", "Ú", "\u02c6", "\u02dc", "ਂ\u200dੀ"]
# --------------------------------------

def get_shabad_query() -> None:
    """
    Gets the user input by listening to the audio and then invokes get_shabad_matches() once the user input is taken and validated
    """
    while True:
        speech_input = search_from_speech()
        shabad_query = turn_into_bani_query(speech_input)
        if len(shabad_query) > 2:
            get_shabad_matches(shabad_query, speech_input)
            break                

def get_shabad_matches(shabad_query, shabad_verse="") -> None:
    """
    Invoked by get_shabad_query.
    
    Prints matching shabads and asks user to select their shabad.
    """
    # TODO: Display the best match of shabad based on user input
    print(f"Finding matching shabads for \"{shabad_verse}\"")
    print(f"Bani Query: {shabad_query}")
    
    matching_shabad_collection = {}
    probability_threshold = 0
    max_matched_shabad_probability = 0
    max_matched_shabad_number = ""
    max_matched_shabad_id = 0

    matching_shabads = banidb.search(shabad_query)
    if (matching_shabads['total_results'] == 0): print("No results found") 
    else: 
        print("-----------Best Shabad Matches-----------")
        for matches in matching_shabads['pages_data'].values():
            for shabad in matches:
                probability_threshold = get_match_probability(shabad_verse, shabad['verse'])
                if (probability_threshold > 66) and (probability_threshold > max_matched_shabad_probability): # 66 is based on conclusion that if two words are matched out of 3 based on the smallest required query length
                    # print(f"{len(matching_shabad_collection) + 1}. {shabad['verse']} ({shabad['source']['writer']})")
                    # matching_shabad_collection[len(matching_shabad_collection) + 1] = shabad
                    max_matched_shabad_id = shabad['shabad_id']
                    max_matched_shabad_probability = probability_threshold
        display_shabad(max_matched_shabad_id)

        # print(f"{len(matching_shabad_collection)} results found.")
        # while True:
        #     try:
        #         shabad_choice = eval(input("Enter shabad number: "))
        #         shabad_id = matching_shabad_collection[shabad_choice]['shabad_id']
        #     except KeyError:
        #         print("Not a valid option!")
        #     except SyntaxError:
        #         print("Enter something!")
        #     except NameError:
        #         print("Try Again!")
        #     else:
        #         display_shabad(shabad_id)
        #         break

def get_match_probability(speech_input, shabad_verse):
    """
    Gets the matching probability between the user input and the shabad verse

    Returns 100 for exact match of shabad (should return 100 but is not returning more than 30)
    """
    matched_words = []
    speech_input = speech_input.split()
    shabad_verse = shabad_verse.split()

    # TODO: Decide factors to reduce number of comparisons
    # TODO: Calculate probability such that it returns 100 for exact match
    for i in speech_input:
        if i in shabad_verse:
            matched_words.append(i)

    print(matched_words)    
    return (len(matched_words)/len(speech_input)) * 100

def display_shabad(shabad_id):
    """
    Searches banidb by the shabad_id and print the shabad part of the result after extracting it from json
    """
    chosen_shabad = banidb.shabad(shabad_id)
    for ver in chosen_shabad['verses']:
        print(ver['verse'])
    banidb.clear() # Not quite sure what this does. Maybe clears the cache. But it is still making a cache.dat in the folder which contains a json file for shabad on reading

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
                audio = rec.listen(source, 5) # To limit the recording duration, the parameter phrase_time_limit could be given
                audioText = rec.recognize_google(audio, language='pa-in') # set language to 'punjabi'
                return audioText
        except Exception:
            pass

def turn_into_bani_query(text):
    """
    NOTE: It is only removing matravas and correcting vowels
    TODO: Remove all kinds of special characters
    Turns the user input into a bani query. i.e. Taking first letter of each word and joining together

    Returns the bani query
    """
    bani_qeury = ''
    for word in text.split():
        word_initial = word[0]
        if word_initial in VOWEL_LETTERS: # Turn vowels into simple letters
            match word_initial:
                case "ਅ" | "ਆ" | "ਐ" | "ਔ":
                    word_initial = "ਅ"
                case "ਏ" | "ਇ" | "ਈ":
                    word_initial = "ੲ"
                case "ਓ" | "ਉ" | "ਊ":
                    word_initial = "ੳ"
        elif word_initial not in BASE_LETTERS:
            word_initial = ""
        bani_qeury +=  word_initial # Filtered word
    return bani_qeury

get_shabad_query()
banidb.clear()