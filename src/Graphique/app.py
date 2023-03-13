"""
The pygame app
"""
import pygame
from typing import Tuple, List
from src.Graphique.button import Button
from src.Graphique.text_box import TextBox
from src.Trees.transformations import clean_list_to_infix, infix_list_to_tree
from src.Trees.automaton import infix_states, Automaton
import turtle

infix_automaton = Automaton(infix_states)

Color = Tuple[int, int, int] | str


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

        self.calculation = ""

        # Set the desktop size
        self.desktop_size = pygame.display.get_desktop_sizes()[0]

        # Set the default screen size
        self.default_size = screen.get_size()

        # Set part sizes
        self.parts_width = None  # Will be set in the resize_parts method
        self.parts_height = None  # Will be set in the resize_parts method
        self.padding = 10

        # Create the text box, at 0, 0, with a width and height of 0 (just to initialize it)
        self.text_box = TextBox(self.screen, 0, 0, 0, 0, "C:\Windows\Fonts\micross.ttf", (127, 127, 127), (0, 0, 0))

        # Creating buttons
        # Structure of each tuple: (text/value, bg_color, bg_hover_color)
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
             ("=", (255, 139, 61), (255, 157, 92)), ("/", (255, 139, 61), (255, 157, 92))],
            [("Draw", (255, 255, 0), (255, 240, 150)), ("Full", (255, 255, 0), (255, 240, 150))],
            [("²", (255, 139, 61), (255, 157, 92)), ("√", (255, 139, 61), (255, 157, 92))],
        ]
        self.buttons: List[Button] = []
        for row in self.buttons_mat:
            for value, bg_color, hover_color in row:
                # Adding a button at 0, 0 with a width and height of 0 (just to initialize the button)
                self.buttons.append(
                    Button(0, 0, 0, 0, value, value, bg_color, hover_color, (0, 0, 0), self.button_callback,
                           self.screen))

        # Resize the parts of the screen
        self.resize_parts()
        self.previous_calculation = ""

    @property
    def screen_size(self):
        """
        Return the screen size
        """
        return self.screen.get_size()

    def is_fullscreen(self):
        """
        Return True if the app is fullscreen
        """
        return self.screen.get_flags() & pygame.FULLSCREEN

    def toggle_fullscreen(self):
        """
        Toggle the fullscreen mode
        """
        # If the app is fullscreen, set it to windowed mode
        if self.is_fullscreen():
            self.screen = pygame.display.set_mode(self.default_size, pygame.RESIZABLE)
        # Otherwise, set it to fullscreen mode
        else:
            self.screen = pygame.display.set_mode(self.desktop_size, pygame.FULLSCREEN | pygame.RESIZABLE)

        # Resize the parts of the screen
        self.resize_parts()

    def resize_parts(self, screen_size: Tuple[int, int] | None = None):
        """
        Resize the parts of the screen (buttons and text box)
        """
        # If screen_size is not provided, use the screen_size attribute of the class
        # Otherwise, use the provided screen_size
        screen_width, screen_height = screen_size or self.screen_size

        # Calculate the number of rows and columns of buttons
        height_part_count = len(self.buttons_mat)
        width_part_count = len(self.buttons_mat[0])

        # Calculate the width and height of the buttons and there is no padding on the right and bottom
        self.parts_width = (screen_width - self.padding * (width_part_count + 1)) / width_part_count
        self.parts_height = (screen_height - self.padding * (height_part_count + 1)) // height_part_count

        # Loop through each button and update its position and size based on the calculated width and height of the
        # screen parts
        for i, button in enumerate(self.buttons):
            button.x = self.padding + i % width_part_count * (self.parts_width + self.padding)
            button.y = self.parts_height + self.padding * 2 + i // width_part_count * (self.parts_height + self.padding)
            button.width = self.parts_width
            button.height = self.parts_height
            button.rect = pygame.Rect(button.x, button.y, button.width, button.height)

        # Update the position and size of the text box
        self.text_box.x = self.padding
        self.text_box.y = self.padding
        self.text_box.width = screen_width - self.padding * 2
        self.text_box.height = self.parts_height
        self.text_box.draw()

        # Rewrite the text box value
        self.text_box.rewrite_text()

    def button_callback(self, button: Button):
        """
        Handle button clicks
        """
        match button.value:
            case "C":
                self.text_box.write_value("")
                self.text_box.previous_text = ""
            case "DEL":
                self.text_box.write_value(self.text_box.text[:-1])
            case "=":
                self.text_box.clean_write(self.text_box.calculate())
            case "√":
                self.text_box.write_value(self.text_box.text + 'sqrt')
            case "²":
                self.text_box.write_value(self.text_box.text + '**2')
            case "Draw":
                self.draw_tree()
            case "Full":
                self.toggle_fullscreen()
            case _:
                if self.text_box.text == "Error":
                    self.text_box.write_value("")
                self.text_box.write_value(self.text_box.text + button.value)

    def draw_tree(self):
        """
            Draw the tree
            """
        # Get the expression from the text box
        r = None
        if self.text_box.previous_text: # If there is a previous text, use it
            expression = self.text_box.previous_text.replace('=', '').rstrip() # Remove the '=' and the spaces at the end
            print(expression)
        else: # Otherwise, use the current text
            expression = self.text_box.text
            r = self.text_box.calculate()
            print(r)

        # Convert the expression into a tree
        try:
            lis = infix_automaton.build(expression) # Convert the expression to a list
            clean_list_to_infix(lis) # Clean the list
            tree = infix_list_to_tree(lis) # Convert the list to a tree
        except SyntaxError:
            return self.text_box.write_value('Error') # If there is an error, return"""

        print(tree) # Print the tree

        # Then draw using the method
        tree.draw(turtle.Turtle()) # Draw the tree
        turtle.color("Red")
        try: # If there is a result, write it
            if r == int(r): # If the result is an integer, write it as an integer
                turtle.write(f"{int(r)}", align="center", font=("Arial", 20, "normal"))  # Write the expression
            else:
                turtle.write(f"{r}", align="center", font=("Arial", 20, "normal"))
        except: # If there is no result, write the expression
            if int(self.text_box.text) == float(self.text_box.text): # If the result is an integer, write it as an integer
                turtle.write(f"{int(self.text_box.text)}", align="center", font=("Arial", 20, "normal"))  # Write the expression
            else:
                print(self.text_box.text)
                turtle.write(f"{self.text_box.text}", align="center", font=("Arial", 20, "normal"))  # Write the expression

        # Done
        turtle.hideturtle()
        turtle.done() #  Window won't close without this line

        turtle.TurtleScreen._RUNNING = True # This is a hack to make turtle work with pygame

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
                        case pygame.K_F11:
                            self.toggle_fullscreen()
                elif event.type == pygame.VIDEORESIZE:
                    self.resize_parts(event.size)
                for button in self.buttons:
                    button.handle_event(event)
                    if button.value.isnumeric() or button.value in ["+", "-", "*", "/"]:
                        self.calculation += button.value

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


def display_popup(screen, message, font_size=32, font_color=(0, 0, 0), background_color=(255, 255, 255)):
    """
    Display a popup message on the screen
    """
    # Get the screen dimensions
    screen_width, screen_height = screen.get_size()

    # Create a font object
    font = pygame.font.Font(None, font_size)

    # Render the message text
    message_text = font.render(message, True, font_color, background_color)

    # Get the dimensions of the message text
    message_width, message_height = message_text.get_size()

    # Calculate the coordinates for the top-left corner of the message text
    message_x = (screen_width - message_width) // 2
    message_y = (screen_height - message_height) // 2

    # Blit the message text onto the screen
    screen.blit(message_text, (message_x, message_y))

    # Update the display
    pygame.display.update()
