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
        pygame.draw.rect(self.screen, self.box_color if not self.mouse_hover else self.box_hover_color, self.rect, 0, 3)
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
        self.icon = pygame.image.load("Graphique/Assets/treeIcon2.png")
        pygame.display.set_icon(self.icon)

        # Set the running flag to True
        self.running = True

        # Set the desktop size
        self.desktop_size = pygame.display.get_desktop_sizes()[0]

        # Set part sizes
        self.parts_width = 90
        self.parts_height = 90
        self.padding = 10

        # Create the text box
        self.text_box = TextBox(self.screen, 0, 0, 0, 0, pygame.font.Font("C:\Windows\Fonts\micross.ttf", 50),
                                (127, 127, 127), (0, 0, 0))

        # Creating buttons
        self.buttons_mat: List[List[Tuple[str, Color, Color]]] = [
            [("C", (255, 139, 61), (255, 157, 92)), ("(", (255, 139, 61), (255, 157, 92)),
             (")", (255, 139, 61), (255, 157, 92)), ("DEL", (255, 139, 61), (255, 157, 92))],
            [("7", (100, 100, 100), (127, 127, 127)), ("8", (100, 100, 100), (127, 127, 127)),
             ("9", (100, 100, 100), (127, 127, 127)), ("+", (255, 139, 61), (255, 157, 92))],
            [("4", (100, 100, 100), (127, 127, 127)), ("5", (100, 100, 100), (127, 127, 127)),
             ("6", (100, 100, 100), (127, 127, 127)), ("-", (255, 139, 61), (255, 157, 92))],
            [("1", (100, 100, 100), (127, 127, 127)), ("2", (100, 100, 100), (127, 127, 127)),
             ("3", (100, 100, 100), (127, 127, 127)), ("*", (255, 139, 61), (255, 157, 92))],
            [(".", (255, 139, 61), (255, 157, 92)), ("0", (100, 100, 100), (127, 127, 127)),
             ("=", (255, 139, 61), (255, 157, 92)), ("/", (255, 139, 61), (255, 157, 92))]
        ]
        gui_font = pygame.font.Font(None, 50)
        self.buttons: List[Button] = []
        for i, row in enumerate(self.buttons_mat):
            for j, (value, bg_color, hover_color) in enumerate(row):
                self.buttons.append(
                    Button(0, 0, 0, 0, value, value, bg_color, hover_color, (0, 0, 0), self.button_callback,
                           self.screen, gui_font))
        self.resize_parts()

    @property
    def screen_size(self):
        """
        Return the screen size
        """
        return self.screen.get_size()

    def resize_parts(self, screen_size: Tuple[int, int] | None = None):
        """
        Resize the parts of the screen (buttons and text box)
        """
        # If screen_size is not provided, use the screen_size attribute of the class
        # Otherwise, use the provided screen_size
        screen_width, screen_height = self.screen_size if screen_size is None else self.screen_size

        # Calculate the number of rows and columns of buttons
        height_part_count = len(self.buttons_mat) + 1
        width_part_count = len(self.buttons_mat[0])

        # Calculate the width and height of each screen part based on the screen size and number of rows and columns
        self.parts_width = (screen_width - self.padding * (width_part_count + 1)) // width_part_count
        self.parts_height = (screen_height - self.padding * (height_part_count + 1)) // height_part_count

        # Loop through each button and update its position and size based on the calculated width and height of the
        # screen parts
        for i, button in enumerate(self.buttons):
            button.x = self.padding + i % 4 * (self.parts_width + self.padding)
            button.y = self.text_box.height + self.padding * 2 + i // 4 * (self.parts_height + self.padding)
            button.width = self.parts_width
            button.height = self.parts_height
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

        # Update the position and size of the text box
        self.text_box.x = self.padding
        self.text_box.y = self.padding
        self.text_box.width = screen_width - self.padding * 2
        self.text_box.height = self.parts_height

        # Update the text in the text box
        self.text_box.write_value(self.text_box.text)

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
                self.text_box.clean_write(self.text_box.calculate())
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
                elif event.type == pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            self.running = False
                        case pygame.K_BACKSPACE:
                            self.text_box.write_value(self.text_box.text[:-1])
                        case pygame.K_RETURN | pygame.K_KP_ENTER | pygame.K_KP_EQUALS | pygame.K_EQUALS:
                            self.text_box.clean_write(self.text_box.calculate())
                        case pygame.K_c:
                            self.text_box.write_value("")
                        case pygame.K_0 | pygame.K_KP0:
                            self.text_box.write_value(self.text_box.text + "0")
                        case pygame.K_1 | pygame.K_KP1:
                            self.text_box.write_value(self.text_box.text + "1")
                        case pygame.K_2 | pygame.K_KP2:
                            self.text_box.write_value(self.text_box.text + "2")
                        case pygame.K_3 | pygame.K_KP3:
                            self.text_box.write_value(self.text_box.text + "3")
                        case pygame.K_4 | pygame.K_KP4:
                            self.text_box.write_value(self.text_box.text + "4")
                        case pygame.K_5 | pygame.K_KP5:
                            self.text_box.write_value(self.text_box.text + "5")
                        case pygame.K_6 | pygame.K_KP6:
                            self.text_box.write_value(self.text_box.text + "6")
                        case pygame.K_7 | pygame.K_KP7:
                            self.text_box.write_value(self.text_box.text + "7")
                        case pygame.K_8 | pygame.K_KP8:
                            self.text_box.write_value(self.text_box.text + "8")
                        case pygame.K_9 | pygame.K_KP9:
                            self.text_box.write_value(self.text_box.text + "9")
                        case pygame.K_KP_PERIOD:
                            self.text_box.write_value(self.text_box.text + ".")
                        case pygame.K_KP_PLUS:
                            self.text_box.write_value(self.text_box.text + "+")
                        case pygame.K_KP_MINUS:
                            self.text_box.write_value(self.text_box.text + "-")
                        case pygame.K_KP_DIVIDE:
                            self.text_box.write_value(self.text_box.text + "/")
                        case pygame.K_KP_MULTIPLY:
                            self.text_box.write_value(self.text_box.text + "*")
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_parts((event.w, event.h))
                for button in self.buttons:
                    button.handle_event(event)

            # Update the screen
            self.update()

            # Limit the frame rate to 40 FPS
            self.clock.tick(40)

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
