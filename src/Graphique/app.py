"""
The pygame app
"""
import pygame
from typing import Callable, Tuple, List
from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
from src.Trees.automaton import Automaton, infix_states
from src.Trees.calculator import calculate_tree

infix_automaton = Automaton(infix_states)
Color = Tuple[int, int, int] | str


class Button:
    """
    A button class
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str, value: str,
                 box_color: Color, box_hover_color: Color, text_color: Color, callback: Callable,
                 screen: pygame.Surface,
                 font: pygame.font.Font):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.value = value
        self.box_color = box_color
        self.box_hover_color = box_hover_color
        self.text_color = text_color
        self.callback = callback
        self.screen = screen
        self.font = font
        self.rect = pygame.Rect(x, y, width, height)

        self.clicked = False

    @property
    def mouse_hover(self) -> bool:
        """
        Check if the mouse is hovering over the button
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def draw(self):
        """
        Draw the button on the screen
        """
        self.screen.fill(self.box_hover_color if self.mouse_hover and not self.clicked else self.box_color, self.rect)
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect()
        text_rect.center = (self.x + self.width / 2, self.y + self.height / 2)
        self.screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        """
        Handle mouse events for the button
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse is within the button's rect
            if self.rect.collidepoint(event.pos):
                # Call the button's callback function
                self.callback(self)
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False


class TextBox:
    """
    A class to manage the text box
    """

    def __init__(self, screen: pygame.Surface, x: int, y: int, width: int, height: int, font: pygame.font.Font,
                 bg_color: Tuple[int, int, int], text_color: Tuple[int, int, int]):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.text = ''
        self.text_surf = font.render(self.text, True, self.text_color)
        self.text_rect = self.text_surf.get_rect(center=(x + width // 2, y + height // 2))

    def draw(self):
        """
        Draw the textbox
        """
        pygame.draw.rect(self.screen, self.bg_color, (self.x, self.y, self.width, self.height), 0, 0)
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


class App:
    """
    The pygame app
    """

    def __init__(self, screen: pygame.Surface):
        # Set the screen
        self.screen = screen

        # Set the background color
        self.bg_color = (255, 255, 255)  # White

        # Set the clock
        self.clock = pygame.time.Clock()

        # Set the title
        self.title = "CalculaTreece"
        pygame.display.set_caption(self.title)

        # Set the icon
        self.icon = pygame.image.load("Graphique/Assets/icon.ico")
        pygame.display.set_icon(self.icon)

        # Set the running flag to True
        self.running = True

        # Create the text box
        self.text_box = TextBox(self.screen, 10, 10, 390, 100, pygame.font.Font("C:\Windows\Fonts\micross.ttf", 50),
                                (127, 127, 127), (0, 0, 0))

        # Creating buttons
        buttons_mat = [
            ["C", "(", ")", "DEL"],
            ["7", "8", "9", "+"],
            ["4", "5", "6", "-"],
            ["1", "2", "3", "*"],
            [".", "0", "=", "/"]
        ]
        gui_font = pygame.font.Font(None, 20)
        self.buttons: List[Button] = []
        for i, row in enumerate(buttons_mat):
            for j, value in enumerate(row):
                self.buttons.append(Button(10 + j * 100, 120 + i * 100, 90, 90, value, value, (127, 127, 127),
                                           (100, 100, 100), (0, 0, 0), self.button_callback, self.screen, gui_font))

    def button_callback(self, button: Button):
        """
        Handle button clicks
        """
        match button.value:
            case "C":
                self.text_box.write_value("")
            case "DEL":
                self.text_box.write_value(self.text_box.text[:-1])
            case "=":
                result = self.text_box.calculate()
                if isinstance(result, str):
                    self.text_box.write_value(result)
                elif isinstance(result, float):
                    if result.is_integer():
                        self.text_box.write_value(str(int(result)))
                    else:
                        self.text_box.write_value(str(result))
                else:
                    self.text_box.write_value(str(result))
            case _:
                self.text_box.write_value(self.text_box.text + button.value)

    def run(self):
        """
        Run the app
        """
        while self.running:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                for button in self.buttons:
                    button.handle_event(event)

            # Update the screen
            self.update()

            # Limit the frame rate to 60 FPS
            self.clock.tick(60)

    def update(self):
        """
        Update the screen
        """
        # Clear the screen
        self.screen.fill(self.bg_color)

        for button in self.buttons:
            button.draw()

        self.text_box.draw()

        # Update the display
        pygame.display.update()
