import pygame

class Board:
    SCALE_MODIFIER = 0.80
    WHITE = (240, 217, 181)
    BLACK = (181, 136, 99)

    # __init__(): Constructor, sets up board info using the passed screen dimensions
    def __init__(self, screen_width = 600, screen_height = 600):
        self.screen = pygame.display.get_surface()
        self.size = min(screen_width, screen_height) * self.SCALE_MODIFIER
        self.square_size = self.size / 6
        self.offset_x = (screen_width - self.size) / 2
        self.offset_y = (screen_height - self.size) / 2

    # draw(): Draws the board to the screen.
    def draw(self):
        for row in range(6):
            for col in range(6):
                is_even = (row + col) % 2 == 0
                color = self.WHITE if is_even else self.BLACK

                x = col * self.square_size + self.offset_x
                y = row * self.square_size + self.offset_y

                pygame.draw.rect(self.screen, color, (x, y, self.square_size, self.square_size))

        pygame.display.flip()