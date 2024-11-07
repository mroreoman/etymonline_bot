import sys
import requests
from bs4 import BeautifulSoup

class EtymResults:
    def __init__(self, word: str, results: list[(str,str)]):
        self.word = word
        self.results = results
    
    def __str__(self):
        if not self.results:
            return "could not find " + self.word + " on etymonline.com"
        else:
            out = "etymonline.com results for " + self.word + "\n"
            for result in self.results:
                out += "\n" + result[0] + "\n" + result[1] + "\n"
            return out
        
    def strShort(self) -> list[str]:
        return ["result too long bro",]

def search(word: str) -> EtymResults:
    page = requests.get("https://www.etymonline.com/word/" + word)
    soup = BeautifulSoup(page.content, "html.parser")
    entries = soup.find_all("div", class_="word--C9UPa")
    if not entries:
        return None
    else:
        results = []
        for entry in entries:
            name = entry.find(["h1", "p"], class_="word__name--TTbAA") # ignores related words
            if name:
                definition = name.find_next_sibling("section", class_="word__defination--2q7ZH")
                results.append((name.get_text(), definition.get_text())) # formatting is lost in definition (blackquote, italics, links)
        return EtymResults(word, results)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("no word given. using bye\n")
        sys.argv.append("bye")
    print(search(sys.argv[1]))