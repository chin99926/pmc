from typing import List
from species_parser import SpeciesParser


# Calculate status for Pokemon tachi!
class PokemonStat:

    prefix = ""
    prefix_err = prefix + "Error: "

    def __init__(self, sp: SpeciesParser):
        self._sp = sp
        self._name = ""
        self._species = list()
        self._nature = [1] * 6
        self._base = [0] * 6
        self._individ = [31] * 6
        self._level = 1
        self._stat = list()
    
    def set_species(self, args):
        if len(args) == 1:
            self._name = args[0]
            self._species = self._sp.get_pokemon_spec_list(args[0])
            if not self._species:
                self._name = ""
                self._print_err("pokemon {} cannot be found".format(args[0]))
        else:
            self._print_err("more than 1 pokemon is specified")
    
    def set_nature(self, args):
        if len(args) == 6:
            self._nature = [float(args[i]) for i in range(len(args))]
        else:
            self._print_err("arg length ({}) does not match for nature".format(len(args)))
    
    def set_base(self, args):
        if len(args) == 6:
            self._base = [int(args[i]) for i in range(len(args))]
        else:
            self._print_err("arg length ({}) does not match for base".format(len(args)))
    
    def set_individ(self, args):
        if len(args) == 6:
            self._individ = [int(args[i]) for i in range(len(args))]
        else:
            self._print_err("arg length ({}) does not match for individ".format(len(args)))

    def set_level(self, args):
        if len(args) == 1 and args[0].isnumeric():
            self._level = int(args[0])
            if self._level < 1 or self._level > 100:
                self._print_err("level must be in range: 1 - 100")
                self._level = 1
        else:
            self._print_err("level must be a single int")
    
    def set_stat(self, args):
        if len(args) == 6:
            self._stat = [int(args[i]) for i in range(len(args))]
            self._calculate_individ()
        else:
            self._print_err("arg length ({}) does not match for stat".format(len(args)))

    def _calculate_stat(self):
        if not self._species:
            self.prefix_err("species must be set before calculating stat")
        self._stat = [self._get_stat_hp()] + \
                     [self._get_stat_A2E(i) for i in range(1, 6)]

    def _get_stat_hp(self):
        i = 0
        # (spec * 2 + ind + base / 4) * lvl / 100 + 10 + lvl
        return int((self._species[i] * 2 + self._individ[i] + int(self._base[i] / 4)) \
                   * self._level / 100 + 10 + self._level)

    def _get_stat_A2E(self, i: int):
        # nat * ((spec * 2 + ind + base / 4) * lvl / 100 + 5)
        return int(((self._species[i] * 2 + self._individ[i] + int(self._base[i] / 4)) \
                   * self._level / 100 + 5) * self._nature[i])

    def _calculate_individ(self):
        if not self._species or not self._stat:
            self._print_err("species and stat must be set before calculating individ")
        self._individ = [self._get_individ_hp()] + \
                        [self._get_individ_A2E(i) for i in range(1, 6)]
    
    def _get_individ_hp(self):
        i = 0
        return round((self._stat[i] - 10 - self._level) * 100 / self._level \
                     - self._species[i] * 2 - int(self._base[i] / 4))

    def _get_individ_A2E(self, i: int):
        return round((self._stat[i] / self._nature[i] - 5) * 100 / self._level \
                     - self._species[i] * 2 - int(self._base[i] / 4))

    def show_result(self, args):
        show_type = {'stat', 'ind'}
        if not len(args) == 1 or args[0] not in show_type:
            self._print_err("arg show be either \'stat\' or \'ind\'")
            return
        
        if args[0] == 'stat':
            self._calculate_stat()
        else:
            self._calculate_individ()

        line_name = "name: " + self._name + ", level: " + str(self._level)
        self._print_info(line_name)

        status_head = ["HP", "Att", "Def", "SpA", "SpD", "Spe"]
        line_format = '{:>10} {:>5} {:>5} {:>5} {:>5} {:>5} {:>5}'
        print(line_format.format('', *status_head))
        print(line_format.format('Species:', *self._species))
        print(line_format.format('Nature:', *self._nature))
        print(line_format.format('Base:', *self._base))
        print(line_format.format('Individ:', *self._individ))
        print(line_format.format('Status:', *self._stat))
    
    def _print_info(self, msg: str):
        print(PokemonStat.prefix, msg)

    def _print_err(self, msg: str):
        print(PokemonStat.prefix_err, msg)


if __name__ == "__main__":

    sp = SpeciesParser()
    pm = PokemonStat(sp)
    pm.set_species(['敲音猴'])
    pm.set_level(['50'])

    pm.calculate_stat()
    # [125, 85, 70, 60, 60, 85]
    print(">>> Calculate stat at level 50 <<<")
    pm.show_status()

    print('-----------------')

    pm.set_stat([125, 85, 70, 45, 45, 70])
    pm.calculate_individ()
    # [30-31, 30-31, 30-31, 0, 0, 0]
    print(">>> Calculate individ with given stat <<<")
    pm.show_status()