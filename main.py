import sys
import requests
from bs4 import BeautifulSoup

if len(sys.argv) == 1:
    print("no word given. using bye\n")
    sys.argv.append("bye")

word = sys.argv[1].strip()
page = requests.get("https://www.etymonline.com/word/" + word)
soup = BeautifulSoup(page.content, "html.parser")
entries = soup.find_all("div", class_="word--C9UPa")
if not entries:
    print("could not find " + word + " on etymonline.com")
else:
    print("etymonline.com results for " + word + "\n")
    for entry in entries:
        name = entry.find(["h1", "p"], class_="word__name--TTbAA") # ignores related words
        if name:
            print(name.get_text())
            definition = name.find_next_sibling("section", class_="word__defination--2q7ZH")
            print(definition.get_text() + "\n") # formatting is lost (blackquote, italics, links)