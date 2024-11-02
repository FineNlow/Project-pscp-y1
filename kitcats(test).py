import pygame, sys
from PIL import Image

#game screen .. 100%
pygame.init()
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))

#icon & name's bar ... 100%
pygame.display.set_caption("KITCATS")
icons = pygame.image.load("./assets/menu/cat-logo.png").convert_alpha()
pygame.display.set_icon(icons)

#Game menu element image ... 99%
background = screen.fill((226, 179, 209))
gamename = pygame.image.load("./assets/menu/name.png").convert_alpha() #Game's name image

setting_button = pygame.image.load("./assets/setting/setting.png").convert_alpha()
start_button = pygame.image.load("./assets/menu/start.png").convert_alpha() #Start button
quit_button = pygame.image.load("./assets/menu/quit.png").convert_alpha() #Quit button

close_tab = pygame.image.load("./assets/yes no btn/x.png").convert_alpha()
close_tab = pygame.transform.scale(close_tab, (45,45))
close_tab_pos = (width // (height-(height*9.5)) + close_tab.get_width() // width, height // height**0.8)

mute_set = pygame.image.load("./assets/setting/mute.png").convert_alpha()
mute_set = pygame.transform.scale(mute_set, (100, 100))
nosound, nosong = True, True

setting_button = pygame.image.load("./assets/setting/setting.png").convert_alpha()

#convert gif to show frame by frame ... 20%
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

#Check button click
def check_button_click(image, x, y):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    rect = image.get_rect(topleft=(x, y))

    if rect.collidepoint(mouse):
        if click[0] == 1:
            return True
    return False

#Background Music
pygame.mixer.music.load("./assets/music/music.mp3")
pygame.mixer.music.set_volume(0.5)  # Volume is between 0.0 and 1.0
pygame.mixer.music.play(loops=-1)

#Clock for FPS control
clock = pygame.time.Clock()
frame_index = 0
frame_duration = 100

frame_timer = 0
frame_delay = 100
scale_factor = height/500 + 2

current_screen = "menu"

#Main Game Loop
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

        #Game menu ... 60% (add backgound gif)
        if current_screen == "menu":
            levelground = pygame.image.load("./assets/menu/cat-background.png")
            levelground = pygame.transform.scale(levelground,(width, height))
            screen.blit(levelground, (0,0))

            #Game menu screen's element
            gamename_pos = (width // 2.8 - gamename.get_width() // 2, height // 20)
            gamename = pygame.transform.scale(gamename, (690, 195))
            start_button_pos = (width // 5 - start_button.get_width() // 3, height // 2 - height/15)
            start_button = pygame.transform.scale(start_button, (255, 115))
            quit_button_pos = (width // 5 - quit_button.get_width() // 3, height // 2 + height/8)
            quit_button = pygame.transform.scale(quit_button, (255, 115))

            #Game's name image
            screen.blit(gamename, gamename_pos)

            scale_factor = height/500 + 2
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
            setting_button = pygame.transform.scale(setting_button, (41,38))
            setting_button_pos = (width - width*0.0625, height - height*0.96)

            screen.blit(setting_button,setting_button_pos)
            if check_button_click(setting_button, *setting_button_pos):
                current_screen = "setting menu"

        #Quit comfirm window
        elif current_screen == "confirm":
            screen.fill((226, 179, 209))
            quit_page = pygame.image.load("./assets/quit/quit level.png")

            #confirm window
            quit_page = pygame.transform.scale(quit_page, (600, 350))
            quit_page_rect = quit_page.get_rect(center=(width // 2, height // 2))
            screen.blit(quit_page, quit_page_rect)

            #Confirm button
            yes_confirm = pygame.image.load("./assets/quit/yesconfirm.png") #confirm button
            yes_confirm = pygame.transform.scale(yes_confirm, (150, 75))
            yes_confirm_pos = (300 , height // height + (height*0.55))
            not_confirm = pygame.image.load("./assets/quit/noconfirm.png") #back to menu
            not_confirm = pygame.transform.scale(not_confirm, (150, 75))
            not_confirm_pos = (560, height // height + (height*0.55))
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

            setting_menu_tab = pygame.transform.scale(setting_menu_tab, (717, 538))
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

            #button in setting tab
            speaker_button = pygame.image.load("./assets/setting/speaker.png").convert_alpha()
            speaker_button = pygame.transform.scale(speaker_button, (100, 100))
            speaker_button_pos = ((width // 2.2 - setting_menu_tab.get_width() // 400) - height//4, height // height + (height*0.36))
            screen.blit(speaker_button, speaker_button_pos)

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
            back_button_pos = (20, height // height + (height*0.03))
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
                # print("Music On") > Music always on

            if not nosong:
                screen.blit(mute_set, song_button_pos)
                #mute overall song

            if check_button_click(howto_button, *howto_button_pos):
                period_screen = "setting menu"
                current_screen = "How to play"

            if check_button_click(back_button, *back_button_pos):
                current_screen = "menu"
                scale_factor = height/500 + 2

            if check_button_click(credits_button, *credits_button_pos):
                period_screen = "setting menu"
                current_screen = "credits"

        #Tutorial ...10% (สอนวิธีเล่น)
        elif current_screen == "How to play":
            screen.fill((226, 179, 209))

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (20, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = period_screen

        #Credits ...10% (ใส่เครดิต)
        elif current_screen == "credits":
            screen.fill((226, 179, 209))

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (20, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = period_screen

        #Select level window
        elif current_screen == "level":
            screen.fill((226, 179, 209))
            levelground = pygame.image.load("./assets/menu/cat-background.png")
            levelground = pygame.transform.scale(levelground,(width, height))
            screen.blit(levelground, (0,0))

            scale_factor = height/500 + 2
            frames = gifgen('./assets/menu/cat-gif-menu.gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                screen.blit(frame, (width*0.4 - 200,height - 490))

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (20, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)
    
            select_level = pygame.image.load("./assets/select_level/select text.png").convert_alpha()
            select_level = pygame.transform.scale(select_level, (615, 115))
            select_level_pos = (50, height // height + (height*0.07))
            screen.blit(select_level, select_level_pos)

            #easy mode button
            level_easy = pygame.image.load("./assets/select_level/click easy.png").convert_alpha()
            level_easy= pygame.transform.scale(level_easy, (350, 400))
            level_easy_pos = (50, height // height + (height*0.25))

            #normal mode button
            level_normal = pygame.image.load("./assets/select_level/click normal.png").convert_alpha()
            level_normal= pygame.transform.scale(level_normal, (350, 400))
            level_normal_pos = (350, height // height + (height*0.25))

            #hard mode button
            level_hard = pygame.image.load("./assets/select_level/click hard.png").convert_alpha()
            level_hard= pygame.transform.scale(level_hard, (350, 400))
            level_hard_pos = (650, height // height + (height*0.25))

            #level selected button
            screen.blit(level_easy, level_easy_pos)
            screen.blit(level_normal, level_normal_pos)
            screen.blit(level_hard, level_hard_pos)

            if check_button_click(back_button, *back_button_pos):
                current_screen = "menu"

            #Click select easy mode
            if check_button_click(level_easy, *level_easy_pos):
                current_screen = "easy mode"

            #Chick select medium mode
            if check_button_click(level_normal, *level_normal_pos):
                current_screen = "normal mode"

            #Click select hard mode
            if check_button_click(level_hard, *level_hard_pos):
                current_screen = "hard mode"

        #Easy mode window
        elif current_screen == "easy mode":
            screen.fill((226, 179, 209))
            easyground = pygame.image.load("./assets/easy mode/Easy.gif").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(easyground, size)

            easyground = update_background((width, height))
            screen.blit(easyground, (0,0))

            #Setting button
            setting_button = pygame.transform.scale(setting_button, (41,38))
            setting_button_pos = (width - width*0.0625, height - height*0.96)

            screen.blit(setting_button,setting_button_pos)
            if check_button_click(setting_button, *setting_button_pos):
                current_screen = "pause"

        #Medium mode window
        elif current_screen == "normal mode":
            screen.fill((226, 179, 209))
            normalground = pygame.image.load("./assets/normal mode/normal.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(normalground, size)

            normalground = update_background((width, height))
            screen.blit(normalground, (0,0))

            #Setting button
            setting_button = pygame.transform.scale(setting_button, (41,38))
            setting_button_pos = (width - width*0.0625, height - height*0.96)

            screen.blit(setting_button,setting_button_pos)
            if check_button_click(setting_button, *setting_button_pos):
                current_screen = "pause"

        #Hard mode window
        elif current_screen == "hard mode":
            screen.fill((226, 179, 209))
            hardground = pygame.image.load("./assets/hard mode/Hard.jpg").convert_alpha()

            #Adjust select level background image
            def update_background(size):
                return pygame.transform.scale(hardground, size)

            hardground = update_background((width, height))
            screen.blit(hardground, (0,0))

            #Setting button
            setting_button = pygame.transform.scale(setting_button, (41,38))
            setting_button_pos = (width - width*0.0625, height - height*0.96)

            screen.blit(setting_button,setting_button_pos)
            if check_button_click(setting_button, *setting_button_pos):
                current_screen = "pause"

        if current_screen == "pause":
            screen.fill((226, 179, 209))
            pause_menu_tab = pygame.image.load("./assets/setting/pausetab.png").convert_alpha()

            pause_menu_tab = pygame.transform.scale(pause_menu_tab, (717, 538))
            settab_rect = pause_menu_tab.get_rect(center=(width // 2, height // 2))
            screen.blit(pause_menu_tab, settab_rect)

            scale_factor = height/500
            frames = gifgen('./assets/menu/cat-gif (1).gif', scale_factor)

            if frames:
                frame_timer += clock.get_time()  # 
                if frame_timer >= frame_delay:
                    frame_index = (frame_index + 1) % len(frames)
                    frame_timer = 0

                frame = frames[frame_index]
                frame_rect = pause_menu_tab.get_rect(center=(width + (width//10), height // 2.2))
                screen.blit(frame, frame_rect)

            #button in setting tab
            speaker_button = pygame.image.load("./assets/setting/speaker.png").convert_alpha()
            speaker_button = pygame.transform.scale(speaker_button, (100, 100))
            speaker_button_pos = (220, height // height + (height*0.45))
            screen.blit(speaker_button, speaker_button_pos)

            song_button = pygame.image.load("./assets/setting/song.png").convert_alpha()
            song_button = pygame.transform.scale(song_button, (100, 100))
            song_button_pos = (380, height // height + (height*0.45))
            screen.blit(song_button, song_button_pos)

            howto_button = pygame.image.load("./assets/setting/How to.png").convert_alpha()
            howto_button = pygame.transform.scale(howto_button, (100, 100))
            howto_button_pos = (540, height // height + (height*0.45))
            screen.blit(howto_button, howto_button_pos)

            back_button = pygame.image.load("./assets/setting/goback.png").convert_alpha()
            back_button = pygame.transform.scale(back_button, (40, 30))
            back_button_pos = (20, height // height + (height*0.03))
            screen.blit(back_button, back_button_pos)

            home_button = pygame.image.load("./assets/setting/home.png").convert_alpha()
            home_button = pygame.transform.scale(home_button, (100, 100))
            home_button_pos = (710, height // height + (height*0.45))
            screen.blit(home_button, home_button_pos)

            if check_button_click(speaker_button, *speaker_button_pos):
                nosound = not nosound
                # print("Sound Activated") > Sound always activated

            if not nosound:
                screen.blit(mute_set, speaker_button_pos)
                # mute in-game sound

            if check_button_click(song_button, *song_button_pos):
                nosong = not nosong
                # print("Music On") > Music always on

            if not nosong:
                screen.blit(mute_set, song_button_pos)
                #mute overall song

            if check_button_click(howto_button, *howto_button_pos):
                period_screen = "pause"
                current_screen = "How to play"

            if check_button_click(back_button, *back_button_pos):
                current_screen = "menu"
                scale_factor = height/500 + 2

            if check_button_click(home_button, *home_button_pos):
                period_screen = "pause"
                current_screen = "menu"

        pygame.display.flip()
        clock.tick(60) #FPS fixed
