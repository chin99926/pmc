from pokemon_stat import PokemonStat
from species_parser import SpeciesParser
import argparse


parser = argparse.ArgumentParser(description="Status calculator for Pokemon Gen 8 Sword/Shield.")
parser.add_argument('-o', '--offline', action='store_true',
                    help="search online for species data")
args = parser.parse_args()

prompt = 'pmc>> '
sp = SpeciesParser(args.offline)
pm = PokemonStat(sp)

cli_command = {'pm': pm.set_species,
               'ntr': pm.set_nature,
               'bs': pm.set_base,
               'ind': pm.set_individ,
               'lvl': pm.set_level,
               'stat': pm.set_stat,
               'show': pm.show_result,
               'exit': exit}

while(True):
    cmd = input(prompt).lower().split()
    if not cmd:
        continue
    elif cmd[0] not in cli_command:
        print("Command not found!")
    
    token = cmd[0]
    args = cmd[1:]
    if token == 'exit':
        args = None
    
    cli_command[token](args)



