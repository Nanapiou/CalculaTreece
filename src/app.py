"""
The pygame app
"""
import pygame


class App:
    """
    Main class for the app
    """

    def __init__(self, screen1):
        self.screen = screen1
        self.running = True
        self.clock = pygame.time.Clock()
        self.title = "CalculaTreece"
        self.font = pygame.font.SysFont("Arial", 36)

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
                pygame.draw.rect(self.screen, "white", (i * 100, j * 100 + 100, 100, 100), 1)

    def draw_numbers(self):
        # dessine les nombres sur les boutons en partant en bas à gauche
        for i in range(4):
            for j in range(4):
                text = self.font.render(str(4 * i + j + 1), True, "white")
                self.screen.blit(text, (i * 100 + 50, j * 100 + 150))

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


pygame.init()
