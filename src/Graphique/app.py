"""
The pygame app
"""
import pygame
from typing import Tuple, List
from src.Graphique.button import Button
from src.Graphique.text_box import TextBox
from src.Trees.transformations import clean_list_to_infix, infix_list_to_tree, tree_to_infix_list, stringify_infix_list
from src.Trees.automaton import infix_states, Automaton
from src.Trees.calculator import calculate_tree
from src.Trees.trees import BinaryTree
from src.Literal.derivation import derive, simplify
import turtle

infix_automaton = Automaton(infix_states)

Color = Tuple[int, int, int] | str


class App:
    """
    The pygame app
    """

    def __init__(self, screen: pygame.Surface):
        # Set the screen
        self.screen: pygame.Surface = screen

        # Set the background color
        self.bg_color: Color = (49, 58, 66)  # Grey

        # Set the clock
        self.clock: pygame.time.Clock = pygame.time.Clock()

        # Set the title
        self.title: str = "CalculaTreece"
        pygame.display.set_caption(self.title)

        # Set the icon
        self.icon: pygame.Surface = pygame.image.load("./src/Graphique/Assets/treeIcon2.png")
        pygame.display.set_icon(self.icon)

        # Set the running flag to True
        self.running: bool = True

        self.calculation: str = ""

        # Set the desktop size
        info = pygame.display.Info()
        self.desktop_size = (info.current_w, info.current_h)

        # Set the default screen size
        self.default_size: Tuple[int, int] = screen.get_size()

        # Set part sizes
        self.parts_width: int | None = None  # Will be set in the resize_parts method
        self.parts_height: int | None = None  # Will be set in the resize_parts method
        self.padding: int = 10

        # Create the text box, at 0, 0, with a width and height of 0 (just to initialize it)
        self.text_box: TextBox = TextBox(self.screen, 0, 0, 0, 0, "C:\\Windows\\Fonts\\micross.ttf", (127, 127, 127),
                                         (0, 0, 0))

        # Creating buttons
        # Structure of each tuple: (text/value, bg_color, bg_hover_color)
        self.buttons_mat: List[List[Tuple[str, Color, Color]]] = [
            [("(", (255, 139, 61), (255, 157, 92)), (")", (255, 139, 61), (255, 157, 92)),
             ("C", (255, 139, 61), (255, 157, 92)), ("DEL", (255, 139, 61), (255, 157, 92))],
            [("7", (100, 100, 100), (127, 127, 127)), ("8", (100, 100, 100), (127, 127, 127)),
             ("9", (100, 100, 100), (127, 127, 127)), ("÷", (255, 139, 61), (255, 157, 92))],
            [("4", (100, 100, 100), (127, 127, 127)), ("5", (100, 100, 100), (127, 127, 127)),
             ("6", (100, 100, 100), (127, 127, 127)), ("×", (255, 139, 61), (255, 157, 92))],
            [("1", (100, 100, 100), (127, 127, 127)), ("2", (100, 100, 100), (127, 127, 127)),
             ("3", (100, 100, 100), (127, 127, 127)), ("-", (255, 139, 61), (255, 157, 92))],
            [(".", (255, 139, 61), (255, 157, 92)), ("0", (100, 100, 100), (127, 127, 127)),
             ("√", (255, 139, 61), (255, 157, 92)), ("+", (255, 139, 61), (255, 157, 92))],
            [("d/dx", (255, 102, 0), (255, 120, 31)), ("x^n", (255, 102, 0), (255, 120, 31)),
             ("x", (255, 102, 0), (255, 120, 31)), ("²", (255, 139, 61), (255, 157, 92))],
            [("Draw", (255, 255, 0), (255, 240, 150)), ("Hist.", (255, 255, 0), (255, 240, 150))],
            [("=", (255, 139, 61), (255, 157, 92)), ("EXE", (174, 181, 187), (146, 153, 158))],
        ]

        self.height_part_count: int = len(self.buttons_mat)
        self.width_part_count: int = len(self.buttons_mat[0])
        self.buttons: List[Button] = []
        for row in self.buttons_mat:
            for value, bg_color, hover_color in row:
                # Adding a button at 0, 0 with a width and height of 0 (just to initialize the button)
                self.buttons.append(
                    Button(0, 0, 0, 0, value, value, bg_color, hover_color, (0, 0, 0), self.button_callback,
                           self.screen))

        # Resize the parts of the screen
        self.resize_parts()
        self.previous_calculation: str = ""

        # Executed
        self.executed: bool = False

        # Previous result
        self.previous_result: str = ""

        # History
        self.buttons_history: List[Button] = [
            Button(0, 0, 0, 0, "Return to calculator", "Hist.", (255, 255, 0), (255, 240, 150), (0, 0, 0),
                   self.button_callback, self.screen)]
        self.is_not_in_history: bool = True
        self.max_history: int = 8

        self.buttons_save = None

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

        :param screen_size: The size of the screen (width, height)
        """
        # If screen_size is not provided, use the screen_size attribute of the class
        # Otherwise, use the provided screen_size
        screen_width, screen_height = screen_size or self.screen_size

        # Calculate the number of rows and columns of buttons
        height_part_count = self.height_part_count
        width_part_count = self.width_part_count

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

        :param button: The button that was clicked
        """
        if self.executed and button.value in "0123456789":  # isdigit() doesn't work because it includes operators
            self.text_box.write_value("")

        self.executed = False
        match button.value:
            case "Hist.":
                self.history()
            case "=":
                if "=" not in self.text_box.text:
                    self.text_box.write_value(self.text_box.text + "=")
            case "C":
                self.text_box.write_value("")
                self.text_box.previous_text = ""
            case "DEL":
                self.text_box.write_value(self.text_box.text[:-1])
            case "EXE":
                result = self.text_box.calculate()
                if result != "Error":
                    self.buttons_history.insert(1,
                                                Button(0, 0, 0, 0, self.text_box.text, str(result), (100, 100, 100),
                                                       (127, 127, 127), (0, 0, 0), self.button_callback,
                                                       self.screen))
                    if len(self.buttons_history) > self.max_history:
                        self.buttons_history.pop()
                self.text_box.clean_write(result)
                self.executed = True
            case "√":
                self.text_box.write_value(self.text_box.text + 'sqrt')
            case "²":
                self.text_box.write_value(self.text_box.text + '^2')
            case "x^n":
                self.text_box.write_value(self.text_box.text + '^')
            case "Draw":
                self.draw_tree()
            case "Ans":
                if self.executed:
                    self.text_box.write_value(self.previous_calculation)
            case "d/dx":
                self.derive()
            case _:
                self.text_box.write_value(self.text_box.text + button.value)

    def draw_tree(self):
        """
        Draw the tree
        """
        expression = self._get_expression()
        tree, result = self._build_tree_and_calculate_result(expression)

        if tree is not None:
            self._draw_tree_with_turtle(tree, result)
        else:
            self.text_box.write_value("Error")

    def _get_expression(self):
        """
        Get the expression from the text box
        """
        try:
            float(self.text_box.text)
            return self.text_box.previous_text[:-2]
        except ValueError:
            return self.text_box.text

    @staticmethod
    def _build_tree_and_calculate_result(expression):
        """
        Build the tree and calculate the result

        :param expression: The expression to build the tree from
        """
        try:
            lis = infix_automaton.build(expression)
            clean_list_to_infix(lis)
            tree = infix_list_to_tree(lis)
            try:
                result = calculate_tree(tree)
                return tree, result
            except (ZeroDivisionError, TypeError):
                return tree, None
        except (SyntaxError, IndexError):
            return None, None

    def _draw_tree_with_turtle(self, tree, result):
        """
        Draw the tree with turtle

        :param tree: The tree to draw
        :param result: The result of the calculation
        """
        t = turtle.Turtle()

        turtle.bgcolor("#FFFFFF")

        t.hideturtle()
        t.speed(0)
        t.penup()

        t.goto(0, 300)
        t.pendown()

        tree.draw(t)

        if result is not None:
            self._write_result(t, result)

        turtle.done()
        turtle.TurtleScreen._RUNNING = True

    @staticmethod
    def _write_result(t, result):
        t.penup()
        t.color("Red")
        style = ("Verdana", 20, "italic")
        result_str = (
            str(int(result))
            if isinstance(result, float) and result.is_integer()
            else ("≈" + str(round(result, 4)) if round(result, 4) != result else str(round(result, 4)))
        )
        t.goto(0, 300)

        if "≈" not in result_str:
            result_as_float = float(result_str)
            if len(str(int(result_as_float))) > 7:
                result_str = f"{result_as_float:.7e}"
                result_str = result_str.replace("e+0", " e+")
        t.write(result_str, align="center", font=style)

    def derive(self):
        """
        Derive the current expression, and draw the tree
        """
        try:
            lis: List[str | int | float | list] = infix_automaton.build(
                self.text_box.text)  # Convert the expression to a list
            clean_list_to_infix(lis)  # Clean the list
            tree: BinaryTree = infix_list_to_tree(lis)  # Convert the list to a tree
        except SyntaxError:
            return self.text_box.write_value('Error')
        tree_d: BinaryTree = simplify(derive(tree, 'x'))  # Derive the tree and simplify it
        new: str = stringify_infix_list(tree_to_infix_list(tree_d))
        self.text_box.write_value(new)

        t = turtle.Turtle()  # Create a turtle
        t.speed(0)
        t.penup()
        t.goto(0, 300)
        t.pendown()
        tree_d.draw(t)  # Draw the tree

        turtle.done()
        turtle.TurtleScreen._RUNNING = True  # This is a hack to make turtle work with pygame

    def run(self):
        """
        Run the app
        """
        self.buttons_save = self.buttons.copy()
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
                        case pygame.K_RETURN | pygame.K_KP_ENTER:
                            self.text_box.clean_write(self.text_box.calculate())
                        case pygame.K_KP_EQUALS | pygame.K_EQUALS:
                            self.text_box.write_value(self.text_box.text + "=")
                        case pygame.K_c:
                            self.text_box.write_value("")
                            self.text_box.previous_text = ""
                        case pygame.K_KP0:
                            self.text_box.write_value(self.text_box.text + "0")
                        case pygame.K_KP1:
                            self.text_box.write_value(self.text_box.text + "1")
                        case pygame.K_KP2:
                            self.text_box.write_value(self.text_box.text + "2")
                        case pygame.K_KP3:
                            self.text_box.write_value(self.text_box.text + "3")
                        case pygame.K_KP4:
                            self.text_box.write_value(self.text_box.text + "4")
                        case pygame.K_KP5:
                            self.text_box.write_value(self.text_box.text + "5")
                        case pygame.K_KP6:
                            self.text_box.write_value(self.text_box.text + "6")
                        case pygame.K_KP7:
                            self.text_box.write_value(self.text_box.text + "7")
                        case pygame.K_KP8:
                            self.text_box.write_value(self.text_box.text + "8")
                        case pygame.K_KP9:
                            self.text_box.write_value(self.text_box.text + "9")
                        case pygame.K_5:
                            self.text_box.write_value(self.text_box.text + "(")
                        case 41:  # Closed parenthesis, didn't find in pygame props
                            self.text_box.write_value(self.text_box.text + ")")
                        case pygame.K_KP_PERIOD:
                            self.text_box.write_value(self.text_box.text + ".")
                        case pygame.K_KP_PLUS:
                            self.text_box.write_value(self.text_box.text + "+")
                        case pygame.K_KP_MINUS:
                            self.text_box.write_value(self.text_box.text + "-")
                        case pygame.K_KP_DIVIDE:
                            self.text_box.write_value(self.text_box.text + "÷")
                        case pygame.K_KP_MULTIPLY:
                            self.text_box.write_value(self.text_box.text + "×")
                        case pygame.K_F11:
                            self.toggle_fullscreen()
                        case 178:  # Square, didn't find in pygame props
                            self.text_box.write_value(self.text_box.text + "^2")
                        case _:  # If the key is not handled, try each letter
                            for letter_key in range(pygame.K_a, pygame.K_z + 1):
                                if event.key == letter_key:
                                    self.text_box.write_value(self.text_box.text + chr(letter_key))
                elif event.type == pygame.VIDEORESIZE:  # Resize parts of the app (buttons, textbox, etc.)
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

    def history(self):
        """
        Show the calculation history
        """
        if self.is_not_in_history:
            self.buttons = self.buttons_history
            self.width_part_count = 1
            self.height_part_count = max(len(self.buttons_history), 6) + 1
        else:
            self.buttons = self.buttons_save
            self.width_part_count = len(self.buttons_mat[0])
            self.height_part_count = len(self.buttons_mat)
        self.resize_parts()

        self.is_not_in_history = not self.is_not_in_history
