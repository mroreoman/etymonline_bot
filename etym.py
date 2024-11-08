import sys

import requests
import bs4
import markdownify as md

class EtymResults:
    def __init__(self, word: str, results: list[(bs4.element.Tag,bs4.element.Tag)]):
        self.word = word
        self.results = results
    
    def __str__(self):
        if not self.results:
            return "could not find " + self.word + " on etymonline.com"
        else:
            out = "etymonline.com results for " + self.word + ":\n"
            for result in self.results:
                out += "--------------\n"
                out += result[0].get_text() + "\n" + result[1].get_text() + "\n"
            return out
    
    def get_results(self) -> list[dict[str, str]]:
        out = []
        for result in self.results:
            title = result[0].get_text()
            description = md.markdownify(str(result[1]), strip=["a"]) # remove links bc discord markdown doesn't support them
            url = "https://www.etymonline.com/word/" + self.word
            out.append({"title": title, "url": url, "description": description})  #FIXME check length?
        if not out:
            out.append({"title": f"could not find {self.word} on etymonline", "url": f"https://www.etymonline.com/search?q={self.word}"})
        return out

def search(word: str) -> EtymResults:
    page = requests.get("https://www.etymonline.com/word/" + word)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    entries = soup.find_all("div", class_="word--C9UPa")
    results = []
    for entry in entries:
        name = entry.find(["h1", "p"], class_="word__name--TTbAA") # ignores related words
        if name:
            definition = name.find_next_sibling("section", class_="word__defination--2q7ZH")
            results.append((name, definition))
    return EtymResults(word, results)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        sys.argv.append("free")
        print(f"no word given. using {sys.argv[1]}")
    
    result = search(sys.argv[1])
    print(result)