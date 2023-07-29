"""
Calculation.
"""
from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
from src.Trees.trees import BinaryTree
from src.Trees.automaton import Automaton, infix_states, postfix_states
from typing import Generator, Callable


infix_automaton = Automaton(infix_states)
postfix_automaton = Automaton(postfix_states)
Number = int | float


def calculate_tree(tree: BinaryTree) -> Number:
    """
    Calculate the provided tree

    :param tree: The tree to calculate
    :return:
    """
    branches = tree.branches
    match len(branches):
        case 0:
            if isinstance(tree.value, str):
                raise TypeError(f"{type(tree.value)} is not a valid type to calculate")  # For now...
            return tree.value
        case 1:
            t_a = branches[0]
            a = calculate_tree(t_a)
            if hasattr(tree.value, '__call__'):
                return tree.value(a)
            else:
                raise TypeError(type(tree.value))  # For now...
        case 2:
            t_a, t_b = branches
            a = calculate_tree(t_a)
            b = calculate_tree(t_b)
            match tree.value:
                case '*':
                    return a * b
                case '+':
                    return a + b
                case '-':
                    return a - b
                case '/' | ':':
                    return a / b
                case '//':
                    return a // b
                case '%':
                    return a % b
                case '**' | '^':
                    return a ** b


def infix_iter_with_parentheses(tree: BinaryTree) -> Generator[str | Number | Callable, None, None]:
    """
    Iterate over the tree in infix syntax, with parentheses

    :param tree: The tree to iterate over
    :return:
    """
    branches = tree.branches
    match len(branches):
        case 0:
            yield tree.value
        case 1:
            yield '('
            yield from infix_iter_with_parentheses(branches[0])
            yield tree.value
            yield ')'
        case 2:
            yield '('
            yield from infix_iter_with_parentheses(branches[0])
            yield tree.value
            yield from infix_iter_with_parentheses(branches[1])
            yield ')'


def calculate_infix(string: str) -> Number:
    """
    Return the result of the expression (or throw a syntax error)

    :param string: The expression to calculate
    """
    lis = infix_automaton.build(string)
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    return calculate_tree(tree)


if __name__ == '__main__':
    li = infix_automaton.build('sqrt(8x+3)')
    clean_list_to_infix(li)
    print(li)
    # tree = infix_list_to_tree(lis)
    # tree.draw(Turtle())
    # done()
