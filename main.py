import sys
import requests
from bs4 import BeautifulSoup

def search(word):
    page = requests.get("https://www.etymonline.com/word/" + word)
    soup = BeautifulSoup(page.content, "html.parser")
    entries = soup.find_all("div", class_="word--C9UPa")
    if not entries:
        return "could not find " + word + " on etymonline.com"
    else:
        out = ("etymonline.com results for " + word + "\n\n")
        for entry in entries:
            name = entry.find(["h1", "p"], class_="word__name--TTbAA") # ignores related words
            if name:
                out += (name.get_text() + "\n")
                definition = name.find_next_sibling("section", class_="word__defination--2q7ZH")
                out += (definition.get_text() + "\n\n") # formatting is lost (blackquote, italics, links)
        return out


if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("no word given. using bye\n")
        sys.argv.append("bye")
    print(search(sys.argv[1]))