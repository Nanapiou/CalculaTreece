"""
https://fr.wikipedia.org/wiki/Automate_fini
https://fr.wikipedia.org/wiki/Automate_fini_non_d%C3%A9terministe
https://fr.wikipedia.org/wiki/Automate_pond%C3%A9r%C3%A9
"""
from typing import Dict, List, Callable, Tuple
from string import ascii_letters
from copy import deepcopy
from collections.abc import Iterable
from math import sin, sqrt, pi, cos

NewStateBuilder = Tuple[int, Callable[[str], any] | str | Iterable | None] | \
                  Tuple[int, Callable[[str], any] | str | Iterable | None, any] | \
                  Callable[[str], any]
States = List[Dict[str, NewStateBuilder]]


class Automaton:
    """
    Represent an automaton

    A whole class for only one method, but who knows if this is enough?
    """

    def __init__(self, base: States):
        self.base = base

    def test(self, string: str) -> bool:
        """
        Test whether the string respect the automaton or not

        :param string:
        :return:
        """
        current_state = 0
        for elt in string:
            if elt not in self.base[current_state]:
                return False
            current_state = self.base[current_state][elt][0]
        return True

    def build(self, string: str) -> List:
        """
        Build a List from the automaton

        Raise a SyntaxError if the string doesn't respect the automaton

        :param string: The string to convert
        :return:
        """
        error_tracing = ''

        result = list()
        current_state = 0
        current_str = ''  # Used to build elements of multiple characters
        for elt in string:
            error_tracing += elt
            dic = self.base[current_state]
            if elt not in dic:
                raise SyntaxError('Invalid string, at:\n' + error_tracing + '<-')

            new, clear_old = None, False
            match (len(dic[elt])):
                case 2:
                    current_state, new = dic[elt]
                case 3:
                    current_state, new, clear_old = dic[elt]
            if new is not None:
                if hasattr(new, '__call__'):
                    new = new(current_str, elt)
                if isinstance(new, str) and new != '':  # Because a str is an iterable
                    result.append(new)
                elif isinstance(new, Iterable):  # Or hasattr(new, '__iter__')
                    for new_elt in new:
                        if e != '':  # To avoid empty strings, happens with letters in state 1 for infix for example
                            result.append(new_elt)
                else:
                    result.append(new)
                current_str = ''
            current_str += elt
            if clear_old:
                current_str = ''

        if current_str != '':
            if 'end' in self.base[current_state]:
                if self.base[current_state]['end'] is None:
                    return result
                result.append(self.base[current_state]['end'](current_str))
            else:
                print(f"Warning: State {current_state}, left '{current_str}' as old, adding it itself")
                result.append(current_str)
        return result


def gentle_assign(dic1: Dict, dic2: Dict) -> None:
    """
    Assign props of dic2 into dic1

    :param dic1:
    :param dic2:
    :return:
    """
    for k in dic2:
        if k not in dic1:
            dic1[k] = dic2[k]


def is_float(string: str) -> bool:
    """
    Return wether the procided string looks like a float or not

    """
    try:
        float(string)
        return True
    except ValueError:
        return False


"""
Automatons structure:
See types at the top of the module

Iterate over a word, and changing the state depending on:
    - The current state
    - The dict which correspond to this current state
    - The value[0] of the the dict, corresponding to the letter key, which is the new state
    While you iterate, at each new state:
        If value[1] is not None:
            Use it as: function / str / Iterable
            to create a new element of the list
        Add the element to old


[{ 'letter': (new_state, fn/new_piece/new_pieces, clearOld?)}]
"""

# --- Infix automaton ---
infix_states: States = [
    #  0
    {  # Init
        '(': (5, None),
        '-': (6, 0),
        '0': (1, None),
        '1': (1, None),
        '2': (1, None),
        '3': (1, None),
        '4': (1, None),
        '5': (1, None),
        '6': (1, None),
        '7': (1, None),
        '8': (1, None),
        '9': (1, None),
        'a': (7, None),
        's': (10, None),
        'p': (16, None),
        'c': (20, None),
    },
    #  1
    {  # Numbers
        '': (0, lambda old, _: (int(old) if old.isdigit() else float(old) if is_float(old) else old, '*')),
        '×': (2, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '÷': (18, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '*': (2, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '/': (18, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        ':': (18, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '-': (6, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '+': (6, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '^': (6, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        ')': (4, lambda old, _: int(old) if old.isdigit() else float(old) if is_float(old) else old),
        '0': (1, None),
        '1': (1, None),
        '2': (1, None),
        '3': (1, None),
        '4': (1, None),
        '5': (1, None),
        '6': (1, None),
        '7': (1, None),
        '8': (1, None),
        '9': (1, None),
        '.': (1, None),  # For float
        #  Hard coding pi...
        'end': lambda old: pi if old == 'pi' else int(old) if old.isdigit() else float(old) if is_float(old) else old
    },
    #  2
    {  # *
        '*': (3, None),
        '': (0, '*'),
    },
    #  3
    {  # *-*
        '': (0, '**'),
    },
    #  4
    {  # Closed parentheses
        ')': (4, ')'),
        '*': (2, ')'),
        '/': (18, ')'),
        '-': (0, (')', '-')),
        ':': (0, (')', ':')),
        '+': (0, (')', '+')),
        '^': (0, (')', '**')),
        '': (0, (')', '*'))
    },
    #  5
    {  # Opened parentheses
        '': (0, '('),
    },
    #  6
    {  # Other operations
        '': (0, lambda old, _: old)
    },
    #  7
    {  # A
        'b': (8, None),  # abs
        # 'c': (),  # acos
        # 's': (),  # asin
        # 't': (),  # atan
    },
    #  8
    {  # a-b
        's': (9, None),
    },
    #  9
    {  # ab-s
        '': (0, lambda old, _: abs)
    },
    #  10
    {  # S
        'q': (11, None),
        'i': (12, None)
    },
    #  11
    {  # s-q
        'r': (13, None),
    },
    #  12
    {  # s-i
        'n': (14, None),
    },
    #  13
    {  # sq-r
        't': (15, None),
    },
    #  14
    {  # si-n
        '': (0, lambda old, _: sin),
    },
    #  15
    {  # sqr-t
        '': (0, lambda old, _: sqrt)
    },
    #  16
    {  # p
        'i': (17, None),
    },
    #  17
    {  # p-i
        '': (1, pi),
    },
    #  18
    {  # Maybe integer div?
        '/': (19, None),
        '': (0, '/'),
    },
    #  19
    {  # /-/
        '': (0, '//'),
    },
    #  20
    {  # c
        'o': (21, None)
    },
    #  21
    {  # c-o
        's': (22, None)
    },
    #  20
    {  # co-s
        '': (0, lambda old, _: cos)
    }
]

# TODO The abc case (should make a*b*c, not throw an error because it fells in abs)
for letter in ascii_letters:
    index = None
    if letter in infix_states[0]:
        index = infix_states[0][letter][0]
    if index is None:
        infix_states[0][letter] = (1, letter, True)
    else:
        infix_states[index][''] = (1, (letter, '*'), True)

for e in infix_states:
    if '' in e:
        void = e['']
        copied = deepcopy(infix_states[void[0]])
        for key in copied:
            if len(key) < 2:
                copied[key] = (copied[key][0], void[1])
        gentle_assign(e, copied)
# ---

# ----------------------------------------------------------------------------------------------------------------------

# --- Postfix automaton ---
postfix_states: States = [
    # 0
    {  # Base
        ' ': (0, None, True),
        '*': (2, None),
        '/': (3, None),
        '-': (0, '-', True),
        ':': (0, ':', True),
        '+': (0, '+', True),
        '^': (0, '**', True),
        '0': (1, None),
        '1': (1, None),
        '2': (1, None),
        '3': (1, None),
        '4': (1, None),
        '5': (1, None),
        '6': (1, None),
        '7': (1, None),
        '8': (1, None),
        '9': (1, None),
        # 'end': None
    },
    # 1
    {  # Numbers
        '0': (1, None),
        '1': (1, None),
        '2': (1, None),
        '3': (1, None),
        '4': (1, None),
        '5': (1, None),
        '6': (1, None),
        '7': (1, None),
        '8': (1, None),
        '9': (1, None),
        '': (0, lambda old, elt: int(old) if elt in (' ', '*', '/') else (int(old), elt)),
    },
    # 2
    {  # *
        '*': (0, '**', True),
        '': (0, '*')
    },
    # 3
    {  # /
        '/': (0, '//', True),
        '': (0, '/')
    }
]

for e in postfix_states:
    if '' in e:
        void = e['']
        copied = deepcopy(postfix_states[void[0]])
        for key in copied:
            if len(key) < 2:
                if len(void) == 3:
                    copied[key] = (copied[key][0], void[1], void[2])
                else:
                    copied[key] = (copied[key][0], void[1])
        gentle_assign(e, copied)
# ---

if __name__ == '__main__':
    from src.Trees.transformations import clean_list_to_infix

    math_auto = Automaton(infix_states)
    lis = math_auto.build('(5x)/sqrt(x+1)')
    clean_list_to_infix(lis)
    print(lis)
