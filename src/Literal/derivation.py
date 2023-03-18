"""
Used to derive trees.
"""
from src.Trees.trees import BinaryTree
from math import sqrt, cos, sin

Number = int | float

def derive(tree: BinaryTree, variable: str) -> BinaryTree:
    """
    Derive the tree with respect to the variable
    """
    branches = tree.branches
    match len(branches):
        case 0:
            if tree.value == variable:
                return BinaryTree(1)
            else:
                return BinaryTree(0)
        case 1:
            t_a = branches[0]
            a = derive(t_a, variable)
            if hasattr(tree.value, '__call__'):
                match tree.value.__name__:
                    case 'sqrt':
                        return BinaryTree('/').add_branches(a, BinaryTree('*').add_branches(BinaryTree(2), BinaryTree(sqrt).add_branches(t_a)))
                    case 'sin':
                        return BinaryTree('*').add_branches(a, BinaryTree(cos).add_branches(t_a))
                    case 'cos':
                        return BinaryTree('*').add_branches(BinaryTree('-').add_branches(BinaryTree(0), a), BinaryTree(sin).add_branches(t_a))
                    case _:
                        raise NotImplementedError(f'Function {tree.value.__name__} is not implemented')
            else:
                raise TypeError(type(tree.value))
        case 2:
            u, v = branches
            a = derive(u, variable)
            b = derive(v, variable)
            match tree.value:
                case '*':
                    return BinaryTree('+').add_branches(BinaryTree('*').add_branches(a, v), BinaryTree('*').add_branches(u, b))
                case '+':
                    return BinaryTree('+').add_branches(a, b)
                case '-':
                    return BinaryTree('-').add_branches(a, b)
                case '/' | '//':
                    return BinaryTree(tree.value).add_branches(BinaryTree('-').add_branches(BinaryTree('*').add_branches(a, v), BinaryTree('*').add_branches(u, b)), BinaryTree('^').add_branches(v, BinaryTree(2)))
                case '%':
                    return BinaryTree('%').add_branches(BinaryTree('-').add_branches(BinaryTree('*').add_branches(a, v), BinaryTree('*').add_branches(u, b)), BinaryTree('^').add_branches(v, BinaryTree(2)))
                case '**' | '^':
                    return BinaryTree('*').add_branches(BinaryTree('*').add_branches(BinaryTree('^').add_branches(u, BinaryTree('-').add_branches(v, BinaryTree(1))), v), a)


def simplify(tree: BinaryTree) -> BinaryTree:
    """
    Simplify a tree (make possible calculations), including letters
    """
    branches = tree.branches
    match len(branches):
        case 0:
            return tree
        case 1:
            t_a = branches[0]
            a = simplify(t_a)
            if hasattr(tree.value, '__call__'):
                match tree.value.__name__:
                    case 'sqrt':
                        if isinstance(a.value, Number) and a.value >= 0:
                            return BinaryTree(sqrt(a.value))
                        else:
                            return BinaryTree(sqrt).add_branches(a)
                    case 'sin':
                        if isinstance(a.value, Number):
                            return BinaryTree(sin(a.value))
                        else:
                            return BinaryTree(sin).add_branches(a)
                    case 'cos':
                        if isinstance(a.value, Number):
                            return BinaryTree(cos(a.value))
                        else:
                            return BinaryTree(cos).add_branches(a)
                    case _:
                        raise NotImplementedError(f'Function {tree.value.__name__} is not implemented')
            else:
                raise TypeError(type(tree.value))
        case 2:
            u, v = branches
            a = simplify(u)
            b = simplify(v)
            match tree.value:
                case '*':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value * b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return BinaryTree(0)
                    elif isinstance(b.value, Number) and b.value == 0:
                        return BinaryTree(0)
                    elif isinstance(a.value, Number) and a.value == 1:
                        return b
                    elif isinstance(b.value, Number) and b.value == 1:
                        return a
                    else:
                        return BinaryTree('*').add_branches(a, b)
                case '+':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value + b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return b
                    elif isinstance(b.value, Number) and b.value == 0:
                        return a
                    else:
                        return BinaryTree('+').add_branches(a, b)
                case '-':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value - b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return BinaryTree('-').add_branches(b)
                    elif isinstance(b.value, Number) and b.value == 0:
                        return a
                    else:
                        return BinaryTree('-').add_branches(a, b)
                case '/' | '//':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value / b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return BinaryTree(0)
                    elif isinstance(b.value, Number) and b.value == 1:
                        return a
                    else:
                        return BinaryTree(tree.value).add_branches(a, b)
                case '%':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value % b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return BinaryTree(0)
                    elif isinstance(b.value, Number) and b.value == 1:
                        return BinaryTree(0)
                    else:
                        return BinaryTree(tree.value).add_branches(a, b)
                case '**' | '^':
                    if isinstance(a.value, Number) and isinstance(b.value, Number):
                        return BinaryTree(a.value ** b.value)
                    elif isinstance(a.value, Number) and a.value == 0:
                        return BinaryTree(0)
                    elif isinstance(b.value, Number) and b.value == 0:
                        return BinaryTree(1)
                    elif isinstance(b.value, Number) and b.value == 1:
                        return a
                    elif hasattr(a.value, '__call__') and a.value.__name__ == 'sqrt' and isinstance(b.value, Number) and b.value == 2:
                        return a.branches[0]
                    else:
                        return BinaryTree(tree.value).add_branches(a, b)



if __name__ == '__main__':
    from src.Trees.automaton import Automaton, infix_states
    from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
    from turtle import Turtle, done
    auto = Automaton(infix_states)
    lis = auto.build('(x^2+2x+1)/sqrt(x^2+1)')
    clean_list_to_infix(lis)
    tree = infix_list_to_tree(lis)
    tree_d = derive(tree, 'x')
    tree_d_s = simplify(tree_d)
    t = Turtle()
    t.speed(0)
    t.penup()
    t.goto(0, 300)
    t.pendown()
    tree_d_s.draw(t)
    done()
