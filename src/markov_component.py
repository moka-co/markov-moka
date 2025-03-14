import sys
import requests 
import re
import random


# TEMPORARY: Function to download
# https://ia903406.us.archive.org/16/items/castle01kafk/castle01kafk_djvu.txt

def download_novel():

    url="https://ia903406.us.archive.org/16/items/castle01kafk/castle01kafk_djvu.txt"
    novel_path="./src/data/the_castle_kafka.txt" #Todo: find a smarter way so that it works even without being in the main directory
    response = requests.get(url)

    # Todo: implement, if the file already exist don't download it again.
    if response.status_code == 200:
            with open(novel_path,"w", encoding="utf-8") as f:
                f.write(response.text)

def count_words():
    word_count=0
    txt=[]
    novel_path= "./src/data/the_castle_kafka.txt" # Todo: find a better way to pass this
    count = 0
    with open(novel_path,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if line !='':
                words = re.findall(r'\b\w+\b',line)
                word_count += len(words)
                txt.extend(words)
    print("Number of words =", len(txt))
    return txt

# Markov Model
def make_markov_model(cleaned_text, n_gram=3):

    markov_model = {} # It's an hash table i.e a python dictionary
    for i in range(len(cleaned_text) - n_gram): # Iterate over every word in the novel - num of grams
        curr_state, next_state= "","" # Initialize curr state and next state 
        for j in range(n_gram): # itierate over the num of grams
            curr_index = i+j # index is equal to index of word in the text + iter of the gram
            if curr_index < len(cleaned_text): #if current index is within the number of words
                curr_state += cleaned_text[curr_index] + " " #add current word to current state
            next_index= i+j+n_gram  # Next index is simply iter of the current word + iter of current gram + number of grams
            if next_index < len(cleaned_text): # If the next index is within max number of words
                next_state += cleaned_text[next_index] + " " # add to next state, the next index
    
    # At the end of this section, we have a curr index and next index composed of successive words
        curr_state = curr_state.strip()
        next_state = next_state.strip()

        # If current state is not in markov model, create it and initialize next state to 1
        # Else, increase probability or add next_state in markov_mode[curr_state] 
        if curr_state not in markov_model: 
            markov_model[curr_state] = {}
            markov_model[curr_state][next_state]=1 
        else:
            if next_state in markov_model[curr_state]:
                markov_model[curr_state][next_state] +=1
            else:
                markov_model[curr_state][next_state] = 1
        
    for curr_state, transition in markov_model.items():
        total=sum(transition.values()) 
        for state, count in transition.items():
            markov_model[curr_state][state] = count / total 
    return markov_model    


def generate_story(markov_model, limit=100, start='Hello'):
    # TODO: if start is null, use a random key as 
    n = 0
    curr_state = start 
    next_state = None 
    story = ""
    story = curr_state + " "
    while n < limit:
        next_state = random.choices(list(markov_model[curr_state].keys()),
                                    list(markov_model[curr_state].values()))  
        curr_state = next_state[0]
        story+= curr_state + " "
        n+=1
    return story


class MarkovFacade:
    def __init__(self):
        self.limit=100
        self.novel_path= "./src/data/the_castle_kafka.txt"
        self.n_gram=2
        self.story_start='dark lantern'

    def get_story(self):
        download_novel()
        cleaned_text= count_words()
        markov_model = make_markov_model(cleaned_text,self.n_gram)
        story = generate_story(markov_model=markov_model,start=self.story_start)
        return story
