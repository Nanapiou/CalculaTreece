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

    def draw_button(self):
        """
        Draw calculator buttons
        """
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
                self.screen.blit(num, (j * 100 + 40, -i * 100 + 335))

    def run(self):
        """
        Main loop
        """
        while self.running:  # loop until the user clicks the close button
            self.handle_events()
            self.display()
            self.clock.tick(60)
            self.draw_button()
            self.draw_numbers()
            pygame.display.flip()  # update the display


"""class Button:
    def __init__(self, text, width, height, pos):
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        pygame.draw.rect(screen, self.top_color, self.top_rect)
        screen.blit(self.text_surf, self.text_rect)"""


pygame.init()
