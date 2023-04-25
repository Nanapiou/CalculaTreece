"""
Text box class, used to display text in pygame
"""
import pygame
from typing import Tuple
from src.Trees.automaton import Automaton, infix_states
from src.Trees.transformations import clean_list_to_infix, infix_list_to_tree
from src.Trees.calculator import calculate_infix
from src.Literal.equation import Equation

infix_automaton = Automaton(infix_states)
Color = Tuple[int, int, int] | str


class TextBox:
    """
    A class to manage the text box
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, font_src: str,
                 bg_color: Color, text_color: Color):
        self.screen: pygame.Surface = screen
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.font_src: str = font_src
        self.bg_color: Color = bg_color
        self.text_color: Color = text_color
        self.text: str = ''
        self.text_surf: pygame.Surface = self.font.render(self.text, True, self.text_color)
        self.text_rect: pygame.Rect = self.text_surf.get_rect(right=x + width - 10, centery=y + height // 2)
        self.previous_text: str = ''

    def __repr__(self) -> str:
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
        self.text_rect = self.text_surf.get_rect(right=self.x + self.width - 8, centery=self.y + (self.height // 4) * 3)

    def draw(self):
        """
        Draw the textbox
        """
        pygame.draw.rect(self.screen, self.bg_color, (self.x, self.y, self.width, self.height), 0, 2)
        self.screen.blit(self.text_surf, self.text_rect)

        # Draw previous calculation if exists
        if self.previous_text:
            prev_font = pygame.font.Font(self.font_src, self.height // 3)
            prev_surf = prev_font.render(self.previous_text, True, (200, 200, 200))
            prev_rect = prev_surf.get_rect(right=self.text_rect.right, centery=self.y + self.height // 4)
            self.screen.blit(prev_surf, prev_rect)

    def write_value(self, value):
        """
        Write the value on the screen
        """
        self.text = value
        self.text_surf = self.font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(right=self.x + self.width - 8, centery=self.y + (self.height // 4) * 3)

        # if text is too long, cut it

    def calculate(self):  # Fonction will calculate the result of the expression
        """
        Calculate the result of the expression
        """
        try:
            if '=' in self.text:
                list_equation = self.text.split('=')

                lis_left = infix_automaton.build(list_equation[0])
                lis_right = infix_automaton.build(list_equation[1])

                clean_list_to_infix(lis_left)
                clean_list_to_infix(lis_right)

                left = infix_list_to_tree(lis_left)
                right = infix_list_to_tree(lis_right)

                unknown = None

                for side in [left, right]:
                    for branch in side.iter_branches():
                        if str(branch.value).isalpha():
                            unknown = branch.value
                            break

                if unknown is None:
                    raise SyntaxError("No unknown found")

                eq = Equation(unknown)

                result = eq.resolve(left, right)

                if result is None:
                    raise SyntaxError("Quadratics equations are not supported yet")

                round_result = []
                len_floats = 0
                for i in result:
                    len_floats += len(str(i))
                if len_floats > 20:
                    for i in result:
                        round_result.append(round(i, 17 // len(result)))
                else:
                    round_result = result

                values = ', '.join(str(v) for v in round_result)
                return values

            else:
                self.previous_text = self.text + " ="
                return calculate_infix(self.text)
        except (SyntaxError, TypeError, IndexError) as e:
            print('-' * 20)
            print(e)
            return "Error"

    def clean_write(self, value):
        """
        Write the value on the screen

        :param value: the value to write
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
