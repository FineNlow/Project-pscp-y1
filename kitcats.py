import pygame
import sys

pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

#Icon & Name's bar
pygame.display.set_caption("KITCATS")
icons = pygame.image.load("./assets/geometry.png")
pygame.display.set_icon(icons)

#Game menu element image
background = pygame.image.load("./assets/Menu.jpg") #Menu's background image
gamename = pygame.image.load("./assets/name.png") #Game's name image
start_button = pygame.image.load("./assets/start.png") #Start button
quit_button = pygame.image.load("./assets/quit.png") #Quit button

#start & quit button size
start_button = pygame.transform.scale(start_button, (200, 70))
quit_button = pygame.transform.scale(quit_button, (200, 70))

#Adjust background image
def update_background(size):
    return pygame.transform.scale(background, size)

#Adjust game's name image
def game_name(size):
    return pygame.transform.scale(gamename, size)

#Check button click
def check_button_click(image, x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = image.get_rect(topleft=(x, y))

    if rect.collidepoint(mouse):
        if click[0] == 1:
            return True
    return False

#Clock for FPS control
clock = pygame.time.Clock()

current_screen = "menu"

#Main Game Loop
running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        background = update_background((width, height))
        screen.blit(background, (0,0))

        #Game menu screen's element
        gamename_pos = (width // 2 - gamename.get_width() // 2, height // 8)
        gamename = game_name((width*0.63, height*0.26))
        start_button_pos = (width // 2 - start_button.get_width() // 2, height // 2 - 50)
        quit_button_pos = (width // 2 - quit_button.get_width() // 2, height // 2 + 40)

        #Game's name image
        screen.blit(gamename, gamename_pos)

        if current_screen == "menu":
            #Start button
            screen.blit(start_button, start_button_pos)
            if check_button_click(start_button, *start_button_pos):
                print("Start Game!")

            #Quit button
            screen.blit(quit_button, quit_button_pos)
            if check_button_click(quit_button, *quit_button_pos):
                current_screen = "confirm"

        elif current_screen == "confirm":
            screen.fill((0,0,0))
            confirm_page = pygame.image.load("./assets/confirm.png")

            def confirm_quit(size):
                return pygame.transform.scale(confirm_page, size)

            confirm_page = confirm_quit((600, 450))
            confirm_rect = confirm_page.get_rect(center=(width // 2, height // 2))
            screen.blit(confirm_page, confirm_rect)

            yes_confirm = pygame.image.load("./assets/yesconfirm.png") #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - confirm_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/notconfirm.png") #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - confirm_page.get_width() // 3.6, height // height + (height*0.52))
            screen.blit(yes_confirm, yes_confirm_pos)
            screen.blit(not_confirm, not_confirm_pos)

            if check_button_click(yes_confirm, *yes_confirm_pos):
                pygame.quit()
                sys.exit()

            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = "menu"

        pygame.display.flip()
        clock.tick(60) #FPS fixed
