import sys
import requests 
import re


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


# Main
def main():
    print("Hello")
    # download_novel() # i comment this temporary because it's already downloaded
    count_words()


if __name__=='__main__':
    sys.exit(main())