import pygame, sys
from PIL import Image
import os


#game screen .. 100%
pygame.init()
width, height = 800, 600
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

#icon & name's bar ... 100%
pygame.display.set_caption("KITCATS")
icons = pygame.image.load("./assets/menu/cat-logo.png").convert_alpha()
pygame.display.set_icon(icons)

#Game menu element image ... 99%
background = screen.fill((226, 179, 209))
gamename = pygame.image.load("./assets/menu/name.png").convert_alpha() #Game's name image

#convert gif to show frame by frame ... 90% (ค่อนข้าง smooth)
def gifgen(gif_path, scale_factor):
    im = Image.open(gif_path)
    frames = []
    
    while True:
        frame = im.copy().convert("RGBA")
        frame = pygame.image.fromstring(frame.tobytes(), frame.size, "RGBA")
        # Scale the frame
        frame = pygame.transform.scale(frame, (int(frame.get_width() * scale_factor), int(frame.get_height() * scale_factor)))
        frames.append(frame)

        try:
            im.seek(len(frames))  # Move to the next frame
        except EOFError:
            break

    return frames

#Adjust background image
def update_background(size):
    return pygame.transform.scale(background, size)

#Adjust game's name image
def game_name(size):
    return pygame.transform.scale(gamename, size)

#Other button
close_tab = pygame.image.load("./assets/yes no btn/x.png").convert_alpha()
def closed(size):
    return pygame.transform.scale(close_tab, size)

close_tab = closed((width*0.04, height*0.06))
close_tab_pos = (width // (height-(height*9.5)) + close_tab.get_width() // width, height // height**0.8)

setting_button = pygame.image.load("./assets/setting/setting.png").convert_alpha()
def setted(size):
    return pygame.transform.scale(setting_button, size)

start_button = pygame.image.load("./assets/menu/start.png").convert_alpha() #Start button
def started(size):
    return pygame.transform.scale(start_button, size)

quit_button = pygame.image.load("./assets/menu/quit.png").convert_alpha() #Quit button
def quited(size):
        return pygame.transform.scale(quit_button, size)

mute_set = pygame.image.load("./assets/setting/mute.png").convert_alpha()
mute_set = pygame.transform.scale(mute_set, (100, 100))
nosound, nosong = True, True



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

frame_index = 0
frame_duration = 100
frame_timer = 0
frame_delay = 100
scale_factor = height/500 + 2

current_screen = "menu"

pygame.mixer.init()
# Load the music file
pygame.mixer.music.load("./assets/music/music.mp3") 
pygame.mixer.music.set_volume(0.2)  
pygame.mixer.music.play(loops=-1)

#Main Game Loop ... ??%
running = True
while running:
    screen.fill((226, 179, 209))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        screen.fill((226, 179, 209))

        #Game menu ... 90% (element ครบ)
        if current_screen == "menu":
            #Game menu screen's element
            gamename_pos = (width // 2.8 - gamename.get_width() // 2, height // 20)
            gamename = game_name((width*0.63, height*0.26))
            start_button_pos = (width // 5 - start_button.get_width() // 3, height // 2 - height/15)
            start_button = started((width*0.25, height*0.15))
            quit_button_pos = (width // 5 - quit_button.get_width() // 3, height // 2 + height/8)
            quit_button = quited((width*0.25, height*0.15))

            screen.blit(gamename, gamename_pos)

            frames = gifgen('./assets/menu/cat-gif-menu.gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                screen.blit(frame, (width*0.4 - 200,height - 490))

            #Start button
            screen.blit(start_button, start_button_pos)
            if check_button_click(start_button, *start_button_pos):
                current_screen = "level"

            #Quit button
            screen.blit(quit_button, quit_button_pos)
            if check_button_click(quit_button, *quit_button_pos):
                current_screen = "confirm"

            #Setting button
            setting_button = setted((width*0.04, height*0.05))
            setting_button_pos = (width - width*0.0625, height - height*0.96)
    
            screen.blit(setting_button,setting_button_pos)
            if check_button_click(setting_button, *setting_button_pos):
                current_screen = "setting menu"

        #Quit comfirm window
        elif current_screen == "confirm":
            screen.fill((226, 179, 209))
            confirm_page = pygame.image.load("./assets/menu/confirm.png").convert_alpha()

            #Adjust confirm window
            def confirm_quit(size):
                return pygame.transform.scale(confirm_page, size)

            #confirm window
            confirm_page = confirm_quit((600, 450))
            confirm_rect = confirm_page.get_rect(center=(width // 2, height // 2))
            screen.blit(confirm_page, confirm_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png").convert_alpha() #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - confirm_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png").convert_alpha() #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - confirm_page.get_width() // 3.6, height // height + (height*0.52))
            screen.blit(yes_confirm, yes_confirm_pos)
            screen.blit(not_confirm, not_confirm_pos)

            #Click confirm button
            if check_button_click(yes_confirm, *yes_confirm_pos):
                pygame.quit()
                sys.exit()

            #Click back to menu
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = "menu"

        #setting menu ...65% (elementครบ เหลือmute sound & song, หน้า tutorial & credits)
        if current_screen == "setting menu":
            screen.fill((226, 179, 209))
            setting_menu_tab = pygame.image.load("./assets/setting/settingtab.png").convert_alpha()

            def setting_main_menu(size):
                return pygame.transform.scale(setting_menu_tab, size)

            setting_menu_tab = setting_main_menu((width*0.7, height*0.7))
            settab_rect = setting_menu_tab.get_rect(center=(width // 2, height // 2))
            screen.blit(setting_menu_tab, settab_rect)

            scale_factor = height/500
            frames = gifgen('./assets/menu/cat-gif (1).gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                frame_rect = setting_menu_tab.get_rect(center=(width + (width//10), height // 2.2))
                screen.blit(frame, frame_rect)

            # Button in setting tab for mute/unmute sound
            speaker_button = pygame.image.load("./assets/setting/speaker.png").convert_alpha()
            speaker_button = pygame.transform.scale(speaker_button, (100, 100))
            speaker_button_pos = ((width // 2.2 - setting_menu_tab.get_width() // 400) - height//4, height // height + (height*0.36))
            screen.blit(speaker_button, speaker_button_pos)

            # Button in setting tab for mute/unmute music
            song_button = pygame.image.load("./assets/setting/song.png").convert_alpha()
            song_button = pygame.transform.scale(song_button, (100, 100))
            song_button_pos = (width // 2.2 - setting_menu_tab.get_width() // 400, height // height + (height*0.36))
            screen.blit(song_button, song_button_pos)

            howto_button = pygame.image.load("./assets/setting/How to.png").convert_alpha()
            howto_button = pygame.transform.scale(howto_button, (100, 100))
            howto_button_pos = ((width // 2.2 - setting_menu_tab.get_width() // 400) + height//4, height // height + (height*0.36))
            screen.blit(howto_button, howto_button_pos)

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (width // 6 - setting_menu_tab.get_width() // 400, height // height + (height*0.25))
            screen.blit(back_button, back_button_pos)

            credits_button = pygame.image.load("./assets/setting/credits.png").convert_alpha()
            credits_button = pygame.transform.scale(credits_button, (300, 85))
            credits_button_pos = (width // 2 - setting_menu_tab.get_width() // 400) - height//4.5, height // height + (height*0.6)
            screen.blit(credits_button, credits_button_pos)

            if check_button_click(speaker_button, *speaker_button_pos):
                nosound = not nosound
                # print("Sound Activated") > Sound always activated

            if not nosound:
                screen.blit(mute_set, speaker_button_pos)
                # mute in-game sound

            if check_button_click(song_button, *song_button_pos):
                nosong = not nosong
            if not nosong:
                pygame.mixer.music.pause()  # Stop the music if muted
                screen.blit(mute_set, song_button_pos)
            else:
                pygame.mixer.music.unpause()  # Play music again if unmuted


            if check_button_click(howto_button, *howto_button_pos):
                current_screen = "How to play"

            if check_button_click(back_button, *back_button_pos):
                current_screen = "menu"
                scale_factor = height/500 + 2

            if check_button_click(credits_button, *credits_button_pos):
                current_screen = "credits"
            
            # Load the "How to play" image
            how_to_play_image = pygame.image.load("./assets/howtoplay/HOWTOPLAY.png").convert_alpha()  # Adjust the path as needed
        
            # Scale the "How to play" image
            def scale_how_to_play_image(size):
                return pygame.transform.scale(how_to_play_image, size)   
            
        
        #Tutorial ...80% (สอนวิธีเล่น)
        elif current_screen == "How to play":
            screen.fill((226, 179, 209))

            # Scale and display the "How to play" image
            scaled_how_to_play_image = scale_how_to_play_image((width * 0.8, height * 0.8))  # Adjust size as needed
            how_to_play_rect = scaled_how_to_play_image.get_rect(center=(width // 2, height // 2))
            screen.blit(scaled_how_to_play_image, how_to_play_rect)

            # Add the back button
            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (width // 50 - setting_menu_tab.get_width() // 400, height // height + (height * 0.03))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "setting menu"
       
        #Credits ...10% (ใส่เครดิต)
        elif current_screen == "credits":
            screen.fill((226, 179, 209))

            # Load credits image or create a credits text
            credits_image = pygame.image.load("./assets/credits/creditsname.png").convert_alpha()  # Load your credits image
            credits_image = pygame.transform.scale(credits_image, (width * 0.8, height * 0.8))  # Scale if necessary
            credits_rect = credits_image.get_rect(center=(width // 2, height // 2))
            screen.blit(credits_image, credits_rect)

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (width // 50 - setting_menu_tab.get_width() // 400, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "setting menu"

        #Select level window
        elif current_screen == "level":
            screen.fill((226, 179, 209))
            levelground = pygame.image.load("./assets/cat-backgound resource/cat-background (9).png").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(levelground, size)

            levelground = update_background((width, height))
            screen.blit(levelground, (0,0))

            select_level = pygame.image.load("./assets/select_level/select text.png").convert_alpha()
            
            #Adjust select level text image
            def level_selected(size):
                return pygame.transform.scale(select_level, size)

            select_level_pos = (width // 2 - gamename.get_width() // 2.5, height // height + (height*0.05))
            select_level = level_selected((width*0.5, height*0.2))
            screen.blit(select_level, select_level_pos)

            #child play button
            level_child = pygame.image.load("./assets/select_level/click child.png").convert_alpha()
            level_child= pygame.transform.scale(level_child, (170, 220))
            level_child_pos = (width // 15 - levelground.get_width() // 50, height // height + (height*0.3))

            #easy mode button
            level_easy = pygame.image.load("./assets/select_level/click easy.png").convert_alpha()
            level_easy= pygame.transform.scale(level_easy, (170, 220))
            level_easy_pos = (width // 3.4 - levelground.get_width() // 300, height // height + (height*0.3))

            #medium mode button
            level_medium = pygame.image.load("./assets/select_level/click medium.png").convert_alpha()
            level_medium= pygame.transform.scale(level_medium, (170, 220))
            level_medium_pos = (width // 1.87 - levelground.get_width() // 550, height // height + (height*0.3))

            #hard mode button
            level_hard = pygame.image.load("./assets/select_level/click hard.png").convert_alpha()
            level_hard= pygame.transform.scale(level_hard, (170, 220))
            level_hard_pos = (width // 1.3 - levelground.get_width() // 700, height // height + (height*0.3))

            #level selected button
            screen.blit(level_child, level_child_pos)
            screen.blit(level_easy, level_easy_pos)
            screen.blit(level_medium, level_medium_pos)
            screen.blit(level_hard, level_hard_pos)
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "back menu"

            #Click select child play mode
            if check_button_click(level_child, *level_child_pos):
                current_screen = "child play"

            #Click select easy mode
            if check_button_click(level_easy, *level_easy_pos):
                current_screen = "easy mode"

            #Chick select medium mode
            if check_button_click(level_medium, *level_medium_pos):
                current_screen = "medium mode"

            #Click select hard mode
            if check_button_click(level_hard, *level_hard_pos):
                current_screen = "hard mode"

        elif current_screen == "back menu":
            screen.fill((226, 179, 209))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png").convert_alpha()

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png").convert_alpha() #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png").convert_alpha() #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - quit_level_page.get_width() // 3.6, height // height + (height*0.52))

            #Click confirm button
            screen.blit(yes_confirm, yes_confirm_pos)
            if check_button_click(yes_confirm, *yes_confirm_pos):
                current_screen = "menu"

            screen.blit(not_confirm, not_confirm_pos)
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = "level"

        #Child play mode window
        elif current_screen == "child play":
            screen.fill((226, 179, 209))
            childground = pygame.image.load("./assets/child play/Child Play.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(childground, size)

            childground = update_background((width, height))
            screen.blit(childground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "child play"

        #Easy mode window
        elif current_screen == "easy mode":
            screen.fill((226, 179, 209))
            easyground = pygame.image.load("./assets/easy mode/Easy.gif").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(easyground, size)

            easyground = update_background((width, height))
            screen.blit(easyground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "easy mode"

        #Medium mode window
        elif current_screen == "medium mode":
            screen.fill((226, 179, 209))
            mediumground = pygame.image.load("./assets/medium mode/Medium.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(mediumground, size)

            mediumground = update_background((width, height))
            screen.blit(mediumground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "medium mode"

        #Hard mode window
        elif current_screen == "hard mode":
            screen.fill((226, 179, 209))
            hardground = pygame.image.load("./assets/hard mode/Hard.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(hardground, size)

            hardground = update_background((width, height))
            screen.blit(hardground, (0,0))
            screen.blit(close_tab, close_tab_pos)

            if check_button_click(close_tab, *close_tab_pos):
                current_screen = "quit level"
                period_screen = "hard mode"

        elif current_screen == "quit level":
            screen.fill((226, 179, 209))
            quit_level_page = pygame.image.load("./assets/quit/quit level.png").convert_alpha()

            #Adjust confirm window
            def level_confirm_quit(size):
                return pygame.transform.scale(quit_level_page, size)

            #confirm window
            quit_level_page = level_confirm_quit((600, 450))
            quit_level_rect = quit_level_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_level_page, quit_level_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/yes no btn/yesconfirm.png").convert_alpha() #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (width // 2 - quit_level_page.get_width() // 400, height // height + (height*0.52))
            not_confirm = pygame.image.load("./assets/yes no btn/notconfirm.png").convert_alpha() #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (width // 2 - quit_level_page.get_width() // 3.6, height // height + (height*0.52))

            #Click confirm button
            screen.blit(yes_confirm, yes_confirm_pos)
            if check_button_click(yes_confirm, *yes_confirm_pos):
                current_screen = "level"

            #Click back to menu
            screen.blit(not_confirm, not_confirm_pos)
            if check_button_click(not_confirm, *not_confirm_pos):
                current_screen = period_screen

        pygame.display.flip()
        clock.tick(60) #FPS fixed
