import pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock = pygame.time.Clock()
running = True
delta = 0

pygame.display.set_caption("Los Alamos Chess")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("purple")
    pygame.display.flip()
    delta = clock.tick(60) / 1000

pygame.quit()


    

    




    


