import random
from typing import List, Dict
from itertools import takewhile


def find_match(First: List[str], First_pref: List[List[str]], First_bool: List[int], First_posi_map: Dict[str, int],
               Second: List[str], Second_pref: List[List[str]], Second_bool: List[int],
               Second_posi_map: Dict[str, int]):
    for first_posi, first_pref in enumerate(First_pref):
        match_second_posi = First_bool[first_posi]
        if match_second_posi != -1:
            match_second = Second[match_second_posi]
            for second in takewhile(lambda x: x != match_second, first_pref):
                if Second_bool[Second_posi_map[second]] == -1:
                    First_bool[first_posi] = Second_posi_map[second]
                    Second_bool[Second_posi_map[second]] = first_posi
                    Second_bool[Second_posi_map[match_second]] = -1
                    break
                else:
                    matched_first = First[Second_bool[Second_posi_map[second]]]
                    _cond = [_i == First[first_posi]
                             for _i in takewhile(lambda x: x != matched_first,
                                                 Second_pref[Second_posi_map[second]])]
                    if any(_cond):
                        First_bool[First_posi_map[matched_first]] = -1
                        First_bool[first_posi] = Second_posi_map[second]
                        Second_bool[Second_posi_map[second]] = first_posi
                        Second_bool[Second_posi_map[match_second]] = -1
                        break
        else:
            match_second = None
            for second in first_pref:
                if Second_bool[Second_posi_map[second]] == -1:
                    First_bool[first_posi] = Second_posi_map[second]
                    Second_bool[Second_posi_map[second]] = first_posi
                    break


def print_match(First, Second, match):
    for i, j in enumerate(match):
        print(First[i] if i != -1 else -1, Second[j] if j != -1 else -1)


if __name__ == '__main__':
    random_arrange = False
    if random_arrange:
        Male = list('ABCDEFGHI')
        Female = list('LMNOPQRST')
        Male_pref = []
        for _ in range(len(Male)):
            _f = Female.copy()
            random.shuffle(_f)
            Male_pref.append(_f)

        Female_pref = []
        for _ in range(len(Female)):
            _m = Male.copy()
            random.shuffle(_m)
            Female_pref.append(_m)
    else:
        Male = list('ABCDEF')
        Female = list('LMNOPQ')
        Male_pref = [
            ['P', 'N', 'L', 'M', 'O', 'Q'],  # A
            ['P', 'N', 'O', 'Q', 'L', 'M'],  # B
            ['N', 'M', 'L', 'Q', 'O', 'P'],  # C
            ['Q', 'P', 'O', 'M', 'N', 'L'],  # D
            ['Q', 'O', 'M', 'N', 'P', 'L'],  # E
            ['L', 'P', 'N', 'Q', 'O', 'M']]  # F

        Female_pref = [
            ['B', 'F', 'E', 'C', 'A', 'D'],  # L
            ['F', 'D', 'E', 'A', 'B', 'C'],  # M
            ['C', 'D', 'A', 'E', 'F', 'B'],  # N
            ['E', 'C', 'D', 'F', 'B', 'A'],  # O
            ['A', 'C', 'E', 'F', 'B', 'D'],  # P
            ['E', 'D', 'B', 'F', 'A', 'C']]  # Q

    for c, i in enumerate(Male_pref):
        print(Male[c], ' -> ', i)
    print('-' * 30)
    # Male_pref_Rank = [dict(list(enumerate(i))) for i in Male_pref]
    for c, i in enumerate(Female_pref):
        print(Female[c], ' -> ', i)

    Male_posi_map = {j: i for i, j in enumerate(Male)}
    Female_posi_map = {j: i for i, j in enumerate(Female)}

    print(Male_posi_map)
    print(Female_posi_map)

    Male_bool = [-1] * len(Male)
    Female_bool = [-1] * len(Female)

    print('-' * 10)
    count = 0
    while True:
        count += 1
        print('=' * 10, f' [Iteration: {count}] ', '=' * 10)

        find_match(Male, Male_pref, Male_bool, Male_posi_map,
                   Female, Female_pref, Female_bool, Female_posi_map)

        print(' ' * 10, ' [After Male pref] ')

        print_match(Male, Female, Male_bool)

        find_match(Female, Female_pref, Female_bool, Female_posi_map,
                   Male, Male_pref, Male_bool, Male_posi_map)

        print(' ' * 10, ' [After Female pref] ')
        print_match(Male, Female, Male_bool)
        if all(i > -1 for i in Male_bool):
            break
