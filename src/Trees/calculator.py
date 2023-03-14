"""
Calculation.
"""
from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
from src.Trees.trees import BinaryTree
from turtle import Turtle, done
from src.Trees.automaton import Automaton, infix_states, postfix_states
from typing import Generator, Callable


infix_automaton = Automaton(infix_states)
postfix_automaton = Automaton(postfix_states)
Number = int | float


def calculate_tree(tree: BinaryTree) -> Number:
    """
    Calculate the provided tree

    :param tree:
    :return:
    """
    branches = tree.branches
    match len(branches):
        case 0:
            return tree.value
        case 1:
            t_a = branches[0]
            a = t_a.value if t_a.is_leaf() else calculate_tree(t_a)
            if hasattr(tree.value, '__call__'):
                return tree.value(a)
            else:
                raise TypeError(type(tree.value))  # For now...
        case 2:
            t_a, t_b = branches
            a = t_a.value if t_a.is_leaf() else calculate_tree(t_a)
            b = t_b.value if t_b.is_leaf() else calculate_tree(t_b)
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
                case '²' | '^':
                    return a ** b


def infix_iter_with_parentheses(tree: BinaryTree) -> Generator[str | Number | Callable, None, None]:
    """
    Iterate over the tree in infix syntax, with parentheses

    :param tree:
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

    :param string:
    """
    lis = infix_automaton.build(string)
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    return calculate_tree(tree)


if __name__ == '__main__':
    lis = infix_automaton.build(input('Give me an infix expression :\n'))
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)

    t = Turtle()
    t.penup()
    t.goto(0, 300)
    tree.draw(t, 50)
    t.penup()
    t.setheading(90)
    t.forward(50)
    t.write(str(calculate_tree(tree)), align='center', font=('', 20, ''))
    done()
