"""
The pygame app
"""
import pygame


class App:
    """
    Main class for the app
    """

    def __init__(self, screen1):
        super().__init__()
        self.screen = screen1
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = "CalculaTreece"
        self.font = pygame.font.SysFont("Intro", 55)

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
        self.screen.fill("grey")  # fill the screen with grey
        pygame.display.set_caption(self.title)  # set the title of the window

    """def draw_button(self):
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.screen, "Black", (i * 100, j * 100 + 100, 100, 100), 1)
        pygame.draw.line(self.screen, "Black", (0, 100), (400, 100), 7)  # draw a line

    def draw_numbers(self):
        num0 = self.font.render("0", True, "black")
        self.screen.blit(num0, (140, 425))
        # place les chiffres en ligne de bas en haut
        for i in range(3):
            for j in range(3):
                num = self.font.render(str(3 * i + j + 1), True, "black")
                self.screen.blit(num, (j * 100 + 40, -i * 100 + 335))"""

    def button_number_0(self):
        button_0 = Button("0", 100, 75, (100, 425), self.screen)
        button_0.draw()

    def button_number_1(self):
        button_1 = Button("1", 100, 75, (0, 350), self.screen)
        button_1.draw()

    def button_number_2(self):
        button_2 = Button("2", 100, 75, (100, 350), self.screen)
        button_2.draw()

    def button_number_3(self):
        button_3 = Button("3", 100, 75, (200, 350), self.screen)
        button_3.draw()

    def button_number_4(self):
        button_4 = Button("4", 100, 75, (0, 275), self.screen)
        button_4.draw()

    def button_number_5(self):
        button_5 = Button("5", 100, 75, (100, 275), self.screen)
        button_5.draw()

    def button_number_6(self):
        button_6 = Button("6", 100, 75, (200, 275), self.screen)
        button_6.draw()

    def button_number_7(self):
        button_7 = Button("7", 100, 75, (0, 200), self.screen)
        button_7.draw()

    def button_number_8(self):
        button_8 = Button("8", 100, 75, (100, 200), self.screen)
        button_8.draw()

    def button_number_9(self):
        button_9 = Button("9", 100, 75, (200, 200), self.screen)
        button_9.draw()

    def button_operation_add(self):
        button_add = Button("+", 100, 75, (300, 350), self.screen)
        button_add.draw()

    def button_operation_sub(self):
        button_sub = Button("-", 100, 75, (300, 275), self.screen)
        button_sub.draw()

    def button_operation_mul(self):
        button_mul = Button("*", 100, 75, (300, 200), self.screen)
        button_mul.draw()

    def button_operation_div(self):
        button_div = Button("/", 100, 75, (300, 125), self.screen)
        button_div.draw()

    def button_operation_equal(self):
        button_equal = Button("=", 100, 75, (300, 425), self.screen)
        button_equal.draw()

    def button_operation_clear(self):
        button_clear = Button("C", 100, 75, (200, 125), self.screen)
        button_clear.draw()

    def run(self):
        """
        Main loop
        """
        while self.running:  # loop until the user clicks the close button
            self.handle_events()
            self.display()
            self.clock.tick(60)
            if self.running:
                self.button_number_0()
                self.button_number_1()
                self.button_number_2()
                self.button_number_3()
                self.button_number_4()
                self.button_number_5()
                self.button_number_6()
                self.button_number_7()
                self.button_number_8()
                self.button_number_9()
                self.button_operation_add()
                self.button_operation_sub()
                self.button_operation_mul()
                self.button_operation_div()
                self.button_operation_equal()
                self.button_operation_clear()
            pygame.display.flip()  # update the display


class Button:
    def __init__(self, text, width, height, pos, screen):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#000000'
        self.screen = screen

        # text
        self.text_surf = gui_font.render(text, True, '#000000')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, 3)
        self.screen.blit(self.text_surf, self.text_rect)


pygame.init()
gui_font = pygame.font.Font(None, 50)
