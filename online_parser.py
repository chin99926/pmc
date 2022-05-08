from typing import Dict
from bs4 import BeautifulSoup
import urllib.parse
import urllib.request
import json


default_spec_file = 'spec.json'


class OnlineParser:

    spec_url = 'https://wiki.52poke.com/zh-hant/' + urllib.parse.quote('種族值列表（第八世代）')

    def __init__(self, spec_file=default_spec_file) -> None:
        # Get html online
        fp = urllib.request.urlopen(OnlineParser.spec_url)
        self.soup = BeautifulSoup(fp, 'html.parser')
        fp.close()
        # Save to local csv file
        self.spec_file = spec_file

    def get_pokemon_spec_dict(self) -> Dict:
        pm_dict = dict()
        spec_length = 6

        pm_list = self.soup.find_all('tr', {'class': 'bgwhite'})
        for tag in pm_list:
            # Get number and name (with label name)
            number_tag = tag.td
            # Where to save number?
            number = int(number_tag.string)
            name_tag = number_tag.next_sibling.next_sibling.next_sibling.next_sibling
            name = name_tag.a.string
            if name_tag.find('small'):
                name = name + ': ' + name_tag.small.a.string
            pm_dict[name] = list()

            # Get stat's: HP, Att, Def, SpA, SpD, Spe
            stat_tag = name_tag.next_sibling.next_sibling
            for i in range(spec_length):
                pm_dict[name].append(int(stat_tag.string))
                stat_tag = stat_tag.next_sibling.next_sibling

        self.save_pokemon_spec_file(pm_dict)
        return pm_dict

    def save_pokemon_spec_file(self, pm_dict) -> None:
        with open(self.spec_file, 'w', encoding='utf-8') as jsonfile:
            json.dump(pm_dict, jsonfile)


class JsonParser:
    
    def __init__(self, spec_file=default_spec_file) -> None:
        self.spec_file = spec_file

    def get_pokemon_spec_dict(self) -> Dict:
        with open(self.spec_file, encoding='utf-8') as jsonfile:
            pm_dict = json.load(jsonfile)
        return pm_dict


if __name__ == "__main__":
    pass