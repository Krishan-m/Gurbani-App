import banidb

def getShabadMatches(verseInit):
    matchingShabads = banidb.search(verseInit, searchtype=0)
    matchStore = {}
    for page, matches in matchingShabads['pages_data'].items():
        # print(page, matches)
        for shabad in matches:
            print(f"{len(matchStore) + 1}. {shabad['verse']}")
            matchStore[len(matchStore) + 1] = {'shabad_id': shabad['shabad_id'], 'verse': shabad['verse']}

    if (len(matchStore) == 0): print("No results found") 
    else: 
        print(f"{len(matchStore)} results found.")
        shabadChoice = eval(input("Enter shabad number: "))
        shabad_id = matchStore[shabadChoice]['shabad_id']
        # print(shabad_id)
        displayShabad(shabad_id)

def displayShabad(shabad_id):
    chosenShabad = banidb.shabad(shabad_id)
    for ver in chosenShabad['verses']:
        print(ver['verse'])
    
shabadInit = input("Find Shabad: ")
getShabadMatches(shabadInit)