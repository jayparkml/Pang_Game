import pygame 
import os

#########################################################################

# Basic Resetting(Must do things)
pygame.init() # Resetting : Must

# Setting up the game screen size
screen_width = 640  # Width of game
screen_height = 480 # Height
screen = pygame.display.set_mode((screen_width, screen_height)) # setting up the size

# Game Title set up
pygame.display.set_caption("Jay's Pang") # Name of the Game

# FPS Setting
clock = pygame.time.Clock()

#########################################################################

# 1. User game setting(background, game image, coordination, speed, font etc)

current_path = os.path.dirname(__file__) # this file's location
image_path = os.path.join(current_path, "images") # images folder location

# Background
background = pygame.image.load(os.path.join(image_path, "background.png")) #calling background image in images folder

# Stage
stage = pygame.image.load(os.path.join(image_path, "stage.png")) #calling background image in images folder
stage_size = stage.get_rect().size
stage_height = stage_size[1] # stage's height info to use

# Character
character = pygame.image.load(os.path.join(image_path, "character.png")) 
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width) / 2 #position character at the middle of screen
character_y_pos = screen_height - character_height - stage_height # position character on the stage

# Character movement
character_to_x_left = 0
character_to_x_right = 0

# Character Speed
character_speed = 5

# weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# you can shoot weapon several times
weapons = []

# weapon speed
weapon_speed = 10

# creating balloons (4 balloons)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1.png")),
    pygame.image.load(os.path.join(image_path, "balloon2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3.png")),
    pygame.image.load(os.path.join(image_path, "balloon4.png")) ]

# initial speed for each balloon sizes
ball_speed_y = [-18, -15, -12, -9] # index 0, 1, 2, 3 values

# balloons
balls = []

# initial balloon
balls.append({
    "pos_x" : 50, # ball's x coord
    "pos_y" : 50, # ball's y coord
    "img_idx" : 0, # which balloon to use, 0 is the first balloon = image index
    "to_x" : 3, # ball's x coord movement diretion : -3 is left / 3 is right
    "to_y" : -6, # y coord movement direction
    "init_speed_y" : ball_speed_y[0]}) # y initial speed

# Weapon, balloon disappearing data
weapon_to_remove = -1
ball_to_remove = -1

# Font definition
game_font = pygame.font.Font(None, 40)
total_time = 100
start_ticks = pygame.time.get_ticks() # starting time tick


# Game over message / time out, mission complete, game over
game_result = "GAME OVER"


running = True # Game is in progress
while running:
    dt = clock.tick(30) # game fps setting



    # 2. Event Handling (keyboard, mouse etc)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #left key pressed,
                character_to_x_left -= character_speed
            elif event.key == pygame.K_RIGHT: #left key pressed,
                character_to_x_right += character_speed
            elif event.key == pygame.K_SPACE:
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos,weapon_y_pos]) # save weapon shoot data to weapons[]

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_left = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_right = 0
            
    # 3. Game character position definition
    
    character_x_pos += character_to_x_left + character_to_x_right

    # limit
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

    # weapon position
    # example : (100, 200) -> (100, 180) -> (100, 160) : y coord changes
    weapons = [ [w[0], w[1] - weapon_speed] for w in weapons] # shooting weapon upward

    # removing weapon that reach the top
    weapons = [[ w[0], w[1]] for w in weapons if w[1] > 0] # when y become 0 it disappear from weapons

    # balloon position 
    for ball_inx, ball_val in enumerate(balls): # enumerate : index, value
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        # when the ball hit the wall, it bounces to opposite direction
        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1 

        # y direction : bounce to stage
        if ball_pos_y >= screen_height - stage_height - ball_height:
            ball_val["to_y"] = ball_val['init_speed_y']
        else: # ball in the air -> decrease in speed
            ball_val["to_y"] += 0.5

        ball_val["pos_x"] += ball_val['to_x']
        ball_val["pos_y"] += ball_val['to_y']


    # 4. Collision handling

    # character rect info update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

       # ball's rect info update
        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        # Collide check between ball, character
        if character_rect.colliderect(ball_rect):
            running = False
            break

        # Collide check between weapon, and ball
        for weapon_idx, weapon_val in enumerate(weapons): 
            weapon_pos_x = weapon_val[0]
            weapon_pos_y = weapon_val[1]

            # weapon rect info update
            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            # Collision check
            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = weapon_idx # value setting to remove weapon
                ball_to_remove = ball_idx # value for removing ball
                
                # if ball is not smallest, divide the ball
                if ball_img_idx < 3:
                    # ball size info update
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    # Divided ball info
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]


                    # Smaller ball goes to left
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width/2 - small_ball_width/2, # ball's x coord
                        "pos_y" : ball_pos_y + ball_height/2 - small_ball_height/2, # ball's y coord
                        "img_idx" : ball_img_idx + 1, # which balloon to use, 0 is the first balloon = image index
                        "to_x" : -3, # ball's x coord movement diretion : -3 is left / 3 is right
                        "to_y" : -6, # y coord movement direction
                        "init_speed_y" : ball_speed_y[ball_img_idx + 1]})
                        
                    # Smaller ball goes to right
                    balls.append({
                        "pos_x" : ball_pos_x + ball_width/2 - small_ball_width/2, # ball's x coord
                        "pos_y" : ball_pos_y + ball_height/2 - small_ball_height/2, # ball's y coord
                        "img_idx" : ball_img_idx + 1, # which balloon to use, 0 is the first balloon = image index
                        "to_x" : 3, # ball's x coord movement diretion  : -3 is left / 3 is right
                        "to_y" : -6, # y coord movement direction
                        "init_speed_y" : ball_speed_y[ball_img_idx + 1]})

                break
        else: # keep process the game
            continue # inner for condition is not matched, continue. outer for condition keep going
        break # when meeting inner break, then able to get into this break.

    # Ball or weapon removing
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1


    # when all balls removed, game close(complete)
    if len(balls) == 0:
        game_result = "MISSION COMPLETE"
        running = False



    # 5. Filling in screen

    screen.blit(background, (0,0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos)) # draw weapon as in weapons
    # put weapon 2nd to hide it behind the character. blit draw from the top.
    
    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val['pos_y']
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))

    screen.blit(stage, (0,screen_height - stage_height))

    screen.blit(character, (character_x_pos,character_y_pos))

    # elapsed time calculation
    elapsed_time = (pygame.time.get_ticks() - start_ticks)/ 1000 # ms -> s
    timer = game_font.render("Time : {}".format(int(total_time - elapsed_time)), True, (255, 255, 255))
    screen.blit(timer, (10,10))

    # When time over
    if total_time - elapsed_time <= 0:
        game_result = "TIME OVER"
        running = False

    pygame.display.update() 

# Game over message
msg = game_font.render(game_result, True, (255,255,0)) # Yellow
msg_rect = msg.get_rect(center=(int(screen_width/2), int(screen_height/2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 2 sec delay
pygame.time.delay(2000)

# Game end
pygame.quit()
