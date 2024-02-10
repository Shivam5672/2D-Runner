from pygame import *
from sys import exit
from random import randint, choice

from pygame.sprite import Group

class Player(sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = image.load('2D Runner\Graphics\Player\man1.png').convert_alpha()
        player_walk_2 = image.load('2D Runner\Graphics\Player\man2.png').convert_alpha()
        player_walk_3 = image.load('2D Runner\Graphics\Player\man3.png').convert_alpha()
        player_walk_4 = image.load('2D Runner\Graphics\Player\man4.png').convert_alpha()
        player_walk_5 = image.load('2D Runner\Graphics\Player\man5.png').convert_alpha()
        player_walk_6 = image.load('2D Runner\Graphics\Player\man6.png').convert_alpha()
        player_walk_7 = image.load('2D Runner\Graphics\Player\man7.png').convert_alpha()
        player_walk_8 = image.load('2D Runner\Graphics\Player\man8.png').convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2, player_walk_3, player_walk_4, player_walk_5, player_walk_6, player_walk_7, player_walk_8 ]
        self.player_index = 0
        self.player_jump = image.load('2D Runner\Graphics\Player\man_jump_1.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0
        
        self.jump_sound = mixer.Sound('2D Runner\Audio\jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = key.get_pressed()
        if keys[K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -20
            self.jump_sound.play()
        

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump
        else:
            self.player_index += 0.4
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'fly':
            fly_1 = image.load('2D Runner\Graphics\Enemies\Planes\\fly1.png').convert_alpha()
            fly_2 = image.load('2D Runner\Graphics\Enemies\Planes\\fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        
        else:
            snail_1 = image.load('2D Runner\Graphics\Enemies\Snail\snails1.png').convert_alpha()
            snail_2 = image.load('2D Runner\Graphics\Enemies\Snail\snails2.png').convert_alpha()
            snail_3 = image.load('2D Runner\Graphics\Enemies\Snail\snails3.png').convert_alpha()
            snail_4 = image.load('2D Runner\Graphics\Enemies\Snail\snails4.png').convert_alpha()
            snail_5 = image.load('2D Runner\Graphics\Enemies\Snail\snails5.png').convert_alpha()
            snail_6 = image.load('2D Runner\Graphics\Enemies\Snail\snails6.png').convert_alpha()
            snail_7 = image.load('2D Runner\Graphics\Enemies\Snail\snails7.png').convert_alpha()
            snail_8 = image.load('2D Runner\Graphics\Enemies\Snail\snails8.png').convert_alpha()
            self.frames = [snail_1, snail_2, snail_3, snail_4, snail_5, snail_6, snail_7, snail_8]
            y_pos = 305

        self.animation_index = 0

        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900,1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.08
        if self.animation_index >= len(self.frames): 
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]
    
    def update(self):
        self.animation_state()
        self.rect.x -= 5
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = (time.get_ticks() // 1000) - start_time
    #Score Surface
    score_surface = score_font.render(f'Score: {current_time}', False, (64,64,64))
    score_rect = score_surface.get_rect(center = (400,50))
    screen.blit(score_surface, score_rect)
    return current_time

def collision_sprite():
    if sprite.spritecollide(player.sprite, obstacle_group, False):
        game_over = mixer.Sound('2D Runner\Audio\game_over.mp3')
        game_over.play()
        obstacle_group.empty()
        return False
    else:
        return True


init()
screen = display.set_mode((800, 400))
display.set_caption('Runner')
clock = time.Clock()
score_font = font.Font('2D Runner\Fonts\Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0

bg_music = mixer.Sound('2D Runner\Audio\\bg_music.wav')
bg_music.set_volume(0.6)
bg_music.play(loops = -1)

player = sprite.GroupSingle()
player.add(Player())

obstacle_group = sprite.Group()

# Surfaces
#Sky Surface
sky_surface = image.load('2D Runner/Graphics/sky.png').convert()
ground_surface = image.load('2D Runner\Graphics\ground.png').convert()

# Intro Screen
player_stand = image.load('2D Runner\Graphics\Player\man_jump_1.png').convert_alpha()
player_stand = transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))
game_name = score_font.render('Pixel Runner', False, (111,196,169))
game_name_rect = game_name.get_rect(center = (400,80))
game_message = score_font.render('Press Space to Run', False, (111,196,169))
game_message_rect = game_message.get_rect(center = (400,330))

# Timer
obstacle_timer = USEREVENT + 1
time.set_timer(obstacle_timer,1500)
while True:
    for events in event.get():
        if events.type == QUIT:
            quit()
            exit()
        
        if game_active:
            if events.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly', 'snail', 'snail', 'snail'])))
        else:
            if events.type == KEYDOWN and events.key == K_SPACE:
                game_active = True
                start_time = time.get_ticks() // 1000

    if game_active:   
        # Showing the Sky surface  
        screen.blit(sky_surface, (0,0))
        # Showing the Ground surface  
        screen.blit(ground_surface, (0,300))
        # Returning Score Value
        score = display_score()

        # Player
        player.draw(screen)
        player.update()

        # Obstacle
        obstacle_group.draw(screen)
        obstacle_group.update()

        # Collision
        game_active = collision_sprite()

    else:
        screen.fill((94,129,162))
        screen.blit(player_stand,player_stand_rect)

        score_message = score_font.render(f'Your Score : {score}',False, (111,196,169))
        score_message_rect = score_message.get_rect(center = (400,330))
        screen.blit(game_name, game_name_rect)
        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    # Updating Window Display
    display.update()
    # Setting the Frame Rate
    clock.tick(60)