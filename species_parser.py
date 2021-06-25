from bs4 import BeautifulSoup
import urllib.parse
import urllib.request


class SpeciesParser:

    spec_file = "all_spec.html"
    spec_url = 'https://wiki.52poke.com/zh-hant/' + urllib.parse.quote('種族值列表（第八世代）')

    def __init__(self, offline=False):
        if not offline:
            # Query online
            fp = urllib.request.urlopen(SpeciesParser.spec_url)
        else:
            # Use offline local file
            fp = open(SpeciesParser.spec_file, 'r', encoding='utf-8')
        
        self.soup = BeautifulSoup(fp, 'html.parser')
        fp.close()
    
    def get_pokemon_spec_list(self, name):
        pms = self._find_pm_by_name(name)
        if len(pms) == 0:
            print("Pokemon not found: ", name)
            return list()
        elif len(pms) > 1:
            self._print_all_match(pms)
            idx = int(input("Choose target: "))
        else:
            idx = 0
        
        return self._get_spec(pms[idx])
    
    def _find_pm_by_name(self, name):
        def match_name(tag):
            return tag.has_attr('title') and tag['title'] == name and tag.string == name
        
        return self.soup.find_all(match_name)


    def _print_all_match(self, pms):
        def form_tag(pm):
            if pm.next_sibling.next_sibling:
                return pm.next_sibling.next_sibling.string
            else:
                return ''
        
        for i, pm in enumerate(pms):
            print(i, pm.string, form_tag(pm))

    def _get_spec(self, pm):
        tag = pm.parent.next_sibling.next_sibling
        spec = list()
        while len(spec) < 6:
            value = tag.string.strip('\n')
            spec.append(int(value))
            tag = tag.next_sibling.next_sibling
        
        return spec


if __name__ == "__main__":

    sparser = SpeciesParser()

    # Test 1: 綠毛蟲
    print("綠毛蟲: ", sparser.get_pokemon_spec_list("綠毛蟲"), '\n')

    # Test 2: 哭哭面具
    print("哭哭面具: ", sparser.get_pokemon_spec_list("哭哭面具"), '\n')
    
    # Test 3: 後欸
    print("後欸: ", sparser.get_pokemon_spec_list("後欸"), '\n')

    # Test 4: online parser
    sparser2 = SpeciesParser(online=True)
    print("木木梟: ", sparser.get_pokemon_spec_list("木木梟"), '\n')