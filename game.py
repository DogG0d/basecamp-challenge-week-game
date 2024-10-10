# Python 3.12.6

# Locals
import sys
# import time
# Game engine
import pygame
# Game logics
import constant
from constant import *
from inputstream import InputStream
import sprites


class Game():
    def __init__(self) -> None:
        pygame.init()
        # pygame.font.init()

        ### Setup
        # Game clock
        self.clock = pygame.time.Clock()

        # Display
        self.display = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("Challangeweek - Name Unknown")
    

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                pygame.display.update()
                self.clock.tick(constant.FRAMES_PER_SECOND)    ### Handle keypresses
            input.processInput()  # Update keyboard state

            ### Update objects
            player_group.update()
            floor_group.update()

            ### Check enemy collision
            # ...

            ### Full Screen
            # if input.isKeyPressed(K_F11):
            #     print("Fullscreen toggle")
            #     pygame.display.toggle_fullscreen()

            ### Player movement horizontal
            # if input.isKeyDown(K_a) or input.isKeyDown(K_LEFT):
            #     print("KEY LEFT")
            #     player_one.direction = Direction.LEFT
                
            #     if player_one.rect.left < 400:
            #         for floor in floor_group.sprites():
            #              print(floor)
            #              floor.update(dx = player_one.new_x_pos(player_one.vel_x, floor_group))
            #     else:
            #         player_one.update(dx = -player_one.new_x_pos(player_one.vel_x, floor_group))

            # if input.isKeyDown(K_d) or input.isKeyDown(K_RIGHT):
            #     print("KEY RIGHT")
            #     player_one.direction = Direction.RIGHT
            #     if player_one.rect.left > 1200:
            #         for floor in floor_group.sprites():
            #              print(floor)
            #              floor.update(dx = -player_one.new_x_pos(player_one.vel_x, floor_group))
            #     else:
            #         player_one.update(dx = player_one.new_x_pos(player_one.vel_x, floor_group))
            
            ### movement_direction = "right"
            # if player.left > 1200:
            #     for floor in floor_list:
            #         floor.x -= player_vel_x
            # else:
            #     for floor in floor_list:
            #         player_new_x += player_vel_x

            ### Jumping and double jumping
            # if (input.isKeyPressed(K_w) or input.isKeyDown(K_UP)):
            #     print("KEY JUMP")
            #     player_one.vel_y = -JUMP_HEIGHT
            #     can_double_jump = True
            #     player_one.is_jumping = True
            # elif (input.isKeyPressed(K_w) or input.isKeyDown(K_UP)):
            #     print("KEY DOUBLE JUMP")
            #     player_one.vel_y = -JUMP_HEIGHT
            #     can_double_jump = False
            #     player_one.is_jumping = True
            # else:
            #     player_one.is_jumping = False

            # # Dashing logic
            # if input.isKeyPressed(K_e) and dash_cooldown >= constant.DASH_COOLDOWN_FRAMES and not is_dashing:
            #     print("KEY DASH")
            #     is_dashing = True
            #     dash_cooldown = constant.DASH_COOLDOWN_FRAMES
            #     if movement_direction == "right":
            #         player_vel_x = constant.DASH_SPEED
            #     elif movement_direction == "left":
            #         player_vel_x = -constant.DASH_SPEED

            ### Update dash state
            # if is_dashing:
            #     pass
                # for floor in floor_list:
                #     floor.x += player_vel_x * -1
                
                # if player_vel_x > 0:
                #     player_vel_x -= 0.5
                #     if player_vel_x > 15:
                #         player_vel_y = 0
                #     if player_vel_x == 15:
                #         player_vel_x = 5

                # elif player_vel_x < 0:
                #     player_vel_x += 0.5
                #     if player_vel_x < -15:
                #         player_vel_y = 0
                #     if player_vel_x == -15:
                #         player_vel_x = -5


            # Gravity
            vel_old = player_one.vel_y
            if not player_one.on_ground:
                player_one.vel_y = player_one.new_y_pos(min(player_one.vel_y + constant.GRAVITY, MAX_FALL_SPEED), floor_group)
                player_one.update(dy=player_one.vel_y)

            if player_one.vel_y != vel_old + constant.GRAVITY and player_one.vel_y != MAX_FALL_SPEED and not player_one.is_jumping:
                player_one.on_ground = True
                player_one.vel_y = 0
            else:
                player_one.on_ground = False
                
            # print("Comp", player_one.y_collision_compensation(min(player_one.vel_y + constant.GRAVITY, MAX_FALL_SPEED), floor_group))
            
            # if player_one.y_collision_compensation(min(player_one.vel_y + constant.GRAVITY, MAX_FALL_SPEED), floor_group) != 0:
            #     print("RUN")
            #     player_one.on_ground = False

            # player_x_check = pygame.rect()

            # Floor collision
            # if player.colliderect(floor_rect):
            #     player.bottom = floor_rect.top
            #     is_on_ground = True
            # else:
            #     is_on_ground = False

            # if player.collidelistall(floor_list):
            #     player_collision_y = True
            #     is_on_ground = True
            # else:
            #     player_collision_y = False
            #     is_on_ground = False

            # if not player_collision_x:
            #     # print("PLAYER POS X UPDATE")
            #     player.x = player_new_x
            # if not player_collision_y:
            #     # print("PLAYER POS Y UPDATE")
            #     player.y = player_new_y

            ### Draw
            self.display.fill(RGB.BLACK)

            # for floor in floor_list:
            #     pygame.draw.rect(display, RGB.GRAY, floor)
            
            # pygame.draw.rect(display, RGB.ORANGE, player)  # Player

            floor_group.draw(display)
            player_group.draw(display)

            ### HUD information
            text_timer = font_36.render(f"Time: {pygame.time.get_ticks()/1000:.2f}s", True, RGB.WHITE)
            text_dashcooldown = font_36.render(f"Dashcooldown: {dash_cooldown}/{constant.DASH_COOLDOWN_FRAMES}", True, RGB.WHITE)
            x_velocity = font_36.render(f"X_Velocity: {player_one.vel_x:.2f}", True, RGB.WHITE)
            y_velocity = font_36.render(f"Y_velocity: {player_one.vel_y:.2f}", True, RGB.WHITE)

            # Draw HUD
            self.display.blit(text_timer, (20, 20))
            self.display.blit(text_dashcooldown, (20, 45))
            self.display.blit(x_velocity, (20, 70))
            self.display.blit(y_velocity, (20, 95))

            # Update display and clock
            pygame.display.update()
            self.clock.tick(constant.FRAMES_PER_SECOND)

            # Update cooldowns
            dash_cooldown = min(dash_cooldown + 1, constant.DASH_COOLDOWN_FRAMES)
            if player_one.vel_x == 0:
                is_dashing = False
            
            ## DEBUG
            # print()


# frame = display.get_rect()
# camera = frame.copy()
font_36 = pygame.font.SysFont(pygame.font.get_default_font(), 36)

# Input manager
input = InputStream()

# Floor
floor_group = pygame.sprite.Group()
floor_group.add(sprites.Base(0, 800, 1600, 100, RGB.GRAY))
floor_group.add(sprites.Base(1700, 800, 1600, 100, RGB.GRAY))
floor_group.add(sprites.Base(1200, 700, 1600, 100, RGB.GRAY))

# Playersdddddddd
player_group = pygame.sprite.Group()
player_one = sprites.Player(400, 100, 50, 50, RGB.ORANGE, constant.PLAYER_HEALTH)
player_group.add(player_one)

# player = pygame.Rect(375, 100, 50, 50)
# player_vel_x = 0
# player_vel_y = 0
# player_new_x = player.x
# player_new_y = player.y
# player_collision_x = False
# player_collision_y = False

dash_cooldown = constant.DASH_COOLDOWN_FRAMES

is_on_ground = False
can_double_jump = False
is_dashing = False
movement_direction = "right"

