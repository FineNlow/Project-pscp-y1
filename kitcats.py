import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("KITCATS")
icons = pygame.image.load("geometry.png")
pygame.display.set_icon(icons)

running = True
while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # player()
    pygame.display.update()
