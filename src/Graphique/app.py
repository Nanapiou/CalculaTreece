"""
The pygame app
"""
import pygame
from src.Trees.transformations import infix_list_to_tree, clean_list_to_infix
from src.Trees.automaton import Automaton, infix_states
from src.Trees.calculator import calculate_tree

infix_automaton = Automaton(infix_states)


class App:
    """
    Main class for the app
    """

    def __init__(self, screen1):
        self.screen = screen1
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = "CalculaTreece"
        self.icon = pygame.image.load("Graphique/Assets/icon.ico")
        self.font = pygame.font.SysFont("Intro", 55)
        self.textbox = TextBox(self.screen)
        self.numberstring = ""

        # Create buttons
        self.buttons = []
        for i in range(10):
            self.buttons.append(Button(str(i), 100, 75, (5 + 105 * (i % 3), 360 - 80 * (i // 3)), self.screen))

    def handle_events(self):
        """
        Handle events
        """
        for event in pygame.event.get():  # get all events
            if event.type == pygame.QUIT:  # if the event is QUIT
                self.running = False  # stop the loop

    def display(self):
        """
        Global display of the app
        """
        # Background
        self.screen.fill("White")  # fill the screen with grey
        pygame.display.set_caption(self.title)  # set the title of the window
        pygame.display.set_icon(self.icon)  # set the icon of the window

    def button_number_0(self):
        button_0 = Button("0", 100, 75, (110, 440), self.screen)
        button_0.draw()
        if button_0.check_click():
            self.numberstring += "0"

    def button_number_1(self):
        button_1 = Button("1", 100, 75, (5, 360), self.screen)
        button_1.draw()
        if button_1.check_click():
            self.numberstring += "1"

    def button_number_2(self):
        button_2 = Button("2", 100, 75, (110, 360), self.screen)
        button_2.draw()
        if button_2.check_click():
            self.numberstring += "2"

    def button_number_3(self):
        button_3 = Button("3", 100, 75, (215, 360), self.screen)
        button_3.draw()
        if button_3.check_click():
            self.numberstring += "3"

    def button_number_4(self):
        button_4 = Button("4", 100, 75, (5, 280), self.screen)
        button_4.draw()
        if button_4.check_click():
            self.numberstring += "4"

    def button_number_5(self):
        button_5 = Button("5", 100, 75, (110, 280), self.screen)
        button_5.draw()
        if button_5.check_click():
            self.numberstring += "5"

    def button_number_6(self):
        button_6 = Button("6", 100, 75, (215, 280), self.screen)
        button_6.draw()
        if button_6.check_click():
            self.numberstring += "6"

    def button_number_7(self):
        button_7 = Button("7", 100, 75, (5, 200), self.screen)
        button_7.draw()
        if button_7.check_click():
            self.numberstring += "7"

    def button_number_8(self):
        button_8 = Button("8", 100, 75, (110, 200), self.screen)
        button_8.draw()
        if button_8.check_click():
            self.numberstring += "8"

    def button_number_9(self):
        button_9 = Button("9", 100, 75, (215, 200), self.screen)
        button_9.draw()
        if button_9.check_click():
            self.numberstring += "9"

    def button_operation_add(self):
        button_add = Button("+", 100, 75, (320, 360), self.screen)
        button_add.draw_operation_button()
        if button_add.check_click():
            self.numberstring += "+"

    def button_operation_sub(self):
        button_sub = Button("-", 100, 75, (320, 280), self.screen)
        button_sub.draw_operation_button()
        if button_sub.check_click():
            self.numberstring += "-"

    def button_operation_mul(self):
        button_mul = Button("*", 100, 75, (320, 200), self.screen)
        button_mul.draw_operation_button()
        if button_mul.check_click():
            self.numberstring += "*"

    def button_operation_div(self):
        button_div = Button("/", 100, 75, (320, 120), self.screen)
        button_div.draw_operation_button()
        if button_div.check_click():
            self.numberstring += "/"

    def button_operation_equal(self):
        button_equal = Button("=", 100, 75, (320, 440), self.screen)
        button_equal.draw_operation_button()
        if button_equal.check_click():
            self.textbox.calculate()
            # convert into an integer if there is no decimal
            if self.textbox.calculate() % 1 == 0:
                self.numberstring = f'{int(self.textbox.calculate())}'
            else:
                self.numberstring = f'{self.textbox.calculate()}'

    def button_point(self):
        button_point = Button(".", 100, 75, (215, 440), self.screen)
        button_point.draw()
        if button_point.check_click():
            self.numberstring += "."

    def button_operation_clear(self):
        button_clear = Button("C", 100, 75, (5, 440), self.screen)
        button_clear.draw()
        if button_clear.check_click():
            self.numberstring = ""

    def button_change_mode_fix(self):
        button_prefixe = Button("Fix", 100, 75, (110, 120), self.screen)
        button_prefixe.draw()
        if button_prefixe.check_click():
            print("Fix")

    def button_change_mode_color(self):
        button_color = Button("Color", 100, 75, (5, 120), self.screen)
        button_color.draw()
        if button_color.check_click():
            print("Color")

    def button_operation_remains(self):
        button_rest = Button("%", 100, 75, (215, 120), self.screen)
        button_rest.draw_operation_button()
        if button_rest.check_click():
            self.textbox.writeValue("%")

    # buttons functions
    allFuncs = [button_number_0, button_number_1, button_number_2, button_number_3, button_number_4, button_number_5,
                button_number_6, button_number_7, button_number_8, button_number_9, button_operation_add,
                button_operation_sub, button_operation_mul, button_operation_div, button_operation_equal, button_point,
                button_operation_clear, button_change_mode_fix, button_change_mode_color, button_operation_remains]

    def run(self):
        """
        Main loop
        """
        while self.running:  # loop until the user clicks the close button
            self.handle_events()
            self.display()
            self.clock.tick(60)
            if self.running:

                for f in self.allFuncs:
                    if callable(f):
                        f(self)

            self.textbox.draw()
            self.textbox.writeValue(self.numberstring)

            if self.numberstring == "None":
                self.numberstring = ""
            pygame.display.flip()  # update the display


class Button:
    def __init__(self, text, width, height, pos, screen):
        self.pressed = False
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#808080'
        self.screen = screen

        # text
        self.text_surf = gui_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, 0, 3)
        self.screen.blit(self.text_surf, self.text_rect)
        if self.top_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, 'Black', self.top_rect, 3, 5)
                self.screen.blit(self.text_surf, self.text_rect)
                return 'Number Pressed'
            else:
                pygame.draw.rect(self.screen, '#9E9E9E', self.top_rect, 0, 3)
                self.screen.blit(self.text_surf, self.text_rect)

    def draw_operation_button(self):
        pygame.draw.rect(self.screen, 'Orange', self.top_rect, 0, 3)
        self.screen.blit(self.text_surf, self.text_rect)
        if self.top_rect.collidepoint(pygame.mouse.get_pos()):
            if pygame.mouse.get_pressed()[0]:
                pygame.draw.rect(self.screen, '#f9bc60', self.top_rect, 3, 3)
                self.screen.blit(self.text_surf, self.text_rect)
            else:
                pygame.draw.rect(self.screen, '#f9bc60', self.top_rect, 0, 3)
                self.screen.blit(self.text_surf, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()  # get the mouse position
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                # add time delay to prevent double click
                pygame.time.delay(100)
                return True
            else:
                return False


class TextBox:
    def __init__(self, screen):
        self.screen = screen
        self.text = ''
        self.text_surf = mode_font.render(self.text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=(160, 50))

    def draw(self):
        pygame.draw.rect(self.screen, 'Grey', (0, 0, 425, 115), 0, 0)
        self.screen.blit(self.text_surf, self.text_rect)

    def writeValue(self, value):
        self.text = value
        self.text_surf = mode_font.render(self.text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=(200, 60))
        # if text is too long, cut it

    def calculate(self):
        # calculate the result and if there is more than one operation, calculate it
        # result = 0
        # if self.text.count('+') > 1:
        #     for c, i in enumerate(self.text.split('+')):
        #         if c == 0:
        #             result += float(i)
        #         else:
        #             result += float(i)
        # elif self.text.count('+') == 1:
        #     result = float(self.text.split('+')[0]) + float(self.text.split('+')[1])
        # elif self.text.count('-') > 1:
        #     for c, i in enumerate(self.text.split('-')):
        #         if c == 0:
        #             result += float(i)
        #         else:
        #             result -= float(i)
        # elif self.text.count('-') == 1:
        #     result = float(self.text.split('-')[0]) - float(self.text.split('-')[1])
        # elif self.text.count('*') > 1:
        #     for c, i in enumerate(self.text.split('*')):
        #         if c == 0:
        #             result += float(i)
        #         else:
        #             result *= float(i)
        # elif self.text.count('*') == 1:
        #     result = float(self.text.split('*')[0]) * float(self.text.split('*')[1])
        # elif self.text.count('/') > 1:
        #     for c, i in enumerate(self.text.split('/')):
        #         if c == 0:
        #             result += float(i)
        #         else:
        #             result /= float(i)
        # elif self.text.count('/') == 1:
        #     result = float(self.text.split('/')[0]) / float(self.text.split('/')[1])
        # return result
        lis = infix_automaton.build(self.text)
        clean_list_to_infix(lis)
        tree = infix_list_to_tree(lis)
        return calculate_tree(tree)


pygame.init()
gui_font = pygame.font.Font(None, 50)
mode_font = pygame.font.Font("C:\Windows\Fonts\micross.ttf", 50)
