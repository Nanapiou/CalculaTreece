"""
Button instance, used in pygame with the app.
"""
from typing import Callable, Tuple
import pygame

Color = Tuple[int, int, int] | str


class Button:
    """
    A button class
    """

    def __init__(self, x: int, y: int, width: int, height: int, text: str, value: str, box_color: Color,
                 box_hover_color: Color, text_color: Color, callback: Callable[[any], None], screen: pygame.Surface):
        self.x: int = x
        self.y: int = y
        self.width: int = width
        self.height: int = height
        self.text: str = text
        self.value: str = value
        self.box_color: Color = box_color
        self.box_hover_color: Color = box_hover_color
        self.text_color: Color = text_color
        self.callback: Callable[[pygame.event.Event], None] = callback
        self.screen: pygame.Surface = screen
        self.rect: pygame.Rect = pygame.Rect(x, y, width, height)

        self.clicked: bool = False

    def __repr__(self):
        return f"Button({self.x}, {self.y}, {self.width}, {self.height}, {self.text}, {self.value}, {self.box_color},\
         {self.box_hover_color}, {self.text_color}, {self.callback}, {self.screen}, {self.font})"

    @property
    def font(self):
        """
        Return the font of the button
        """
        return pygame.font.Font(None, self.height // 2)

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

        :param event: pygame event
        """
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Check if the mouse is within the button's rect
            if self.mouse_hover:
                # Call the button's callback function
                self.callback(self)
                self.clicked = True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.clicked = False
