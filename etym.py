import sys

import requests
import bs4
import markdownify as md

class MyConverter(md.MarkdownConverter): #TODO create custom converter to format for discord markdown
    def convert_p(self, el, text, convert_as_inline):
        pass

class EtymResults:
    md_converter = md.MarkdownConverter()
    
    def __init__(self, word: str, results: list[(bs4.element.Tag,bs4.element.Tag)]):
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
    
    def get_results(self) -> list[dict[str, str]]:
        out = []
        for result in self.results:
            title = result[0].get_text()
            description = md.markdownify(str(result[1])) #FIXME discord markdown doesn't support links
            out.append({"title": title, "description": description})
        return out

def search(word: str) -> EtymResults:
    page = requests.get("https://www.etymonline.com/word/" + word)
    soup = bs4.BeautifulSoup(page.content, "html.parser")
    entries = soup.find_all("div", class_="word--C9UPa")
    if not entries:
        return None
    else:
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
    print("\n" + result)