"""
Functions used to transform thing to other things
"""
# TODO Create verifications functions (in another file) so we can avoid dumb errors
from typing import List
from src.Trees.trees import BinaryTree

Number = int | float


def postfix_list_to_tree(lis: List[str | Number]) -> BinaryTree:
    """
    Create a tree from the list, wrote in postfix syntax

    :param lis:
    :return:
    """
    trees: List[BinaryTree] = list()
    for e in lis:
        if isinstance(e, str):
            trees.append(BinaryTree(e).add_branches(trees.pop(-2), trees.pop()))
        elif hasattr(e, '__call__'):
            trees.append(BinaryTree(e).add_branches(trees.pop()))
        elif isinstance(e, Number):
            trees.append(BinaryTree(e))
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
            branch = infix_list_to_tree(e)  # IDK what else to do for now...
            lis[i] = branch
        elif isinstance(e, Number):
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


if __name__ == '__main__':
    lis = ['(', 8, '*', '(', 5, '+', 2, ')', '+', 9]
    clean_list_to_infix(lis)
    print(lis)
