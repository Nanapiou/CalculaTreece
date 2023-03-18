"""
Functions used to transform thing to other things
"""
# TODO Create verifications functions (in another file) so we can avoid dumb errors
from typing import List
from string import ascii_letters
from src.Trees.trees import BinaryTree
from copy import deepcopy

Number = int | float


def postfix_list_to_tree(lis: List[str | Number]) -> BinaryTree:
    """
    Create a tree from the list, wrote in postfix syntax

    :param lis:
    :return:
    """
    trees: List[BinaryTree] = list()
    for e in lis:
        if isinstance(e, Number) or e in ascii_letters:
            trees.append(BinaryTree(e))
        elif isinstance(e, str):
            trees.append(BinaryTree(e).add_branches(trees.pop(-2), trees.pop()))
        elif hasattr(e, '__call__'):
            trees.append(BinaryTree(e).add_branches(trees.pop()))
        else:
            raise TypeError(type(e))
    return trees[0]


def tree_to_postfix_list(tree: BinaryTree) -> List[str | Number]:
    """
    Create a tree from the list, wrote in infix syntax

    :param tree:
    :return:
    """
    return list(tree.postfix_iter())


# TODO Broken cuz of functions, fix it
def infix_list_to_tree(lis: List[str | Number | BinaryTree]) -> BinaryTree:
    """
    Create a tree from the list, wrote in infix syntax

    :param lis:
    :return:
    """
    if len(lis) == 0:
        return BinaryTree(0)
    for i in range(len(lis)):
        e = lis[i]
        if isinstance(e, list):
            lis[i] = infix_list_to_tree(e)  # IDK what else to do for now...
        elif not hasattr(e, '__call__') and (isinstance(e, Number) or e in ascii_letters):
            lis[i] = BinaryTree(e)

    # First priority operations
    i = 0
    while i < len(lis):
        e = lis[i]
        if hasattr(e, '__call__'):
            if isinstance(lis[i + 1], str):
                raise TypeError('Invalid infix expression, received a str after a function')
            branch = BinaryTree(e).set_branches(lis[i + 1])
            lis.pop(i + 1)
            lis[i] = branch
            i -= 1
        else:
            match e:
                case '**' | '^':
                    branch = BinaryTree(e).set_branches(lis[i - 1], lis[i + 1])
                    lis.pop(i - 1)
                    lis.pop(i)
                    lis[i - 1] = branch
                    i -= 1
        i += 1

    # Second priority operations
    i = 0
    while i < len(lis):
        e = lis[i]
        match e:
            case '*' | '/' | '//' | ':':
                branch = BinaryTree(e).set_branches(lis[i - 1], lis[i + 1])
                lis.pop(i - 1)
                lis.pop(i)
                lis[i - 1] = branch
                i -= 1
        i += 1

    # Third priority operations
    i = 0
    while i < len(lis):
        e = lis[i]
        match e:
            case '+' | '-':
                branch = BinaryTree(e).set_branches(lis[i - 1], lis[i + 1])
                lis.pop(i - 1)
                lis.pop(i)
                lis[i - 1] = branch
                i -= 1
        i += 1
    return lis[0]


def clean_list_to_infix(lis: List[str | Number | List]) -> None:
    """
    Clean the list, to get a proper infix syntax.

    **Change the list itself.**

    :param lis:
    :return:
    """
    pad = -1
    start_i = 0
    i = 0
    while i < len(lis):
        e = lis[i]
        if e == '(':
            if pad == -1:
                start_i = i
            pad += 1
        elif e == ')':
            if pad == 0:
                temp: List[str | Number] = lis[start_i + 1:i]
                for j in range(start_i + 1, i + 1):
                    lis.pop(start_i)
                    i -= 1
                clean_list_to_infix(temp)
                lis[start_i] = temp
            pad -= 1
        i += 1
    if pad != -1:
        raise SyntaxError('Too many ' + ('closed' if pad < -1 else 'opened') + ' parentheses')


def tree_to_infix_list(tree: BinaryTree) -> List[str | Number]:
    """
    Create a tree from the list, wrote in infix syntax, and respect priority
    A little overkill, but it's the only way I found to do it

    :param tree:
    :return:
    """
    branches = tree.branches
    result = list()
    if tree.is_leaf():
        result.append(tree.value)
    else:
        if len(branches) == 1:
            result.append(tree.value)
            result.append(tree_to_infix_list(branches[0]))
        elif len(branches) == 2:
            result.append(tree_to_infix_list(branches[0]))
            result.append(tree.value)
            result.append(tree_to_infix_list(branches[1]))
        else:
            raise ValueError('Invalid tree')
    return result

def stringify_infix_list(lis: List[str | Number]) -> str:
    """
    Transform a list in postfix syntax to a string

    :param lis:
    :return:
    """
    new = deepcopy(lis)
    for i in range(len(lis)):
        e = new[i]
        if isinstance(e, list):
            new[i] = stringify_infix_list(e)
        elif hasattr(e, '__call__'):
            new[i] = e.__name__
    return ' '.join(map(str, new)) if len(lis) < 2 else ('(' + ' '.join(map(str, new)) + ')')


if __name__ == '__main__':
    from automaton import Automaton, infix_states
    auto = Automaton(infix_states)
    lis = auto.build('(5x^2+3x+2)//sqrt(x+1)')
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    lis_bis = tree_to_infix_list(tree)
    print(stringify_infix_list(lis_bis))
