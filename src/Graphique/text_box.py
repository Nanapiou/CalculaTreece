"""
Text box class, used to display text in pygame
"""

import pygame
from typing import Tuple
from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
from src.Trees.automaton import Automaton, infix_states
from src.Trees.calculator import calculate_tree

infix_automaton = Automaton(infix_states)


class TextBox:
    """
    A class to manage the text box
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, font_src: str,
                 bg_color: Tuple[int, int, int], text_color: Tuple[int, int, int]):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font_src = font_src
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = ''
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(x + width // 2, y + height // 2))

    def __repr__(self):
        return self.text

    @property
    def font(self):
        """
        Return the font of the textbox
        """
        return pygame.font.Font(self.font_src, self.height // 2)

    def rewrite_text(self):
        """
        Rewrite the text on the screen
        """
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))

    def draw(self):
        """
        Draw the textbox
        """
        pygame.draw.rect(self.screen, self.bg_color, (self.x, self.y, self.width, self.height), 0, 2)
        self.screen.blit(self.text_surf, self.text_rect)

    def write_value(self, value):
        """
        Write the value on the screen
        """
        self.text = value
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(self.x + self.width // 2, self.y + self.height // 2))
        # if text is too long, cut it

    def calculate(self):
        """
        Calculate the result of the expression
        """
        try:
            lis = infix_automaton.build(self.text)
            clean_list_to_infix(lis)
            tree = infix_list_to_tree(lis)
            return calculate_tree(tree)
        except (SyntaxError, TypeError) as e:
            print('-' * 20)
            print(e)
            return "Error"

    def clean_write(self, value):
        """
        Write the value on the screen
        """
        if isinstance(value, str):
            self.write_value(value)
        elif isinstance(value, float):
            if value.is_integer():
                self.write_value(str(int(value)))
            else:
                self.write_value(str(value))
        else:
            self.write_value(str(value))
