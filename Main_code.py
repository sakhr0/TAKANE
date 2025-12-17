import pygame
import random
import math
from pygame import mixer
pygame.init()
mixer.init()
WIDTH, HEIGHT = 2000, 1400
speed0 = 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TAKANÉ")
title_font = pygame.font.Font("pixel_1.ttf",  150)
title2_font = pygame.font.Font("pixel_1.ttf",  120)
owner_font = pygame.font.SysFont('couriernew' , 30)
button_font = pygame.font.SysFont('couriernew', 40)
text_font = pygame.font.Font("pixel_2.ttf" , 34)
text_font2 = pygame.font.SysFont('impact', 50)
text_font0 = pygame.font.Font("pixel_2.ttf", 60)
text_font01 = pygame.font.Font("pixel_2.ttf", 30)
text2_font = pygame.font.SysFont('impact', 70)
small_font = pygame.font.SysFont('Arial', 20)
player_images = {
    "left": pygame.transform.scale(pygame.image.load('left-dir.png').convert_alpha(), (50,50)),     # Updated
    "right": pygame.transform.scale(pygame.image.load('right-dr.png').convert_alpha(), (50,50)),
    "up": pygame.transform.scale(pygame.image.load('up-dir.png').convert_alpha(), (50,50)),
    "down": pygame.transform.scale(pygame.image.load('bottom-dir.png').convert_alpha(), (50,50)),
}



BACKGROUND_COLOR = (20, 20, 40)  
BLUE = (0, 102, 204)
PURPLE = (153, 51, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
YELLOW = (255, 255, 0)  
START_MENU = 0
EXPLANATION = 1
GAME_LEVEL_1 = 2
GAME_LEVEL_2 = 3
GAME_LEVEL_3 = 4
WIN_SCREEN = 5
LOSE_SCREEN1 = 6
LOSE_SCREEN2 = 7
LOSE_SCREEN3 = 8
CREDITS = 9
MIN_SPAWN_DISTANCE = 400
current_state = START_MENU
level = 1
player = None
enemies = []
goal = None
key = None
maze = None
key_found = False    
music_playing = False


def play_music(file , x , y):
    global music_playing
    if music_playing != file:
        mixer.music.stop()
        mixer.music.load(file)
        mixer.music.set_volume(x)
        mixer.music.play(y)  # loop forever
        music_playing = file
def play_transition_sound(file , x  ):
    transition_sound = mixer.Sound(file)
    transition_sound.set_volume(x)
    transition_sound.play()        
def create_level_1():
    maze = [
        "#####################",
        "#          S        #",
        "# #### ## # ##### # #",
        "#    #    #   #     #",
        "## ##### #### # ### #",
        "#      #      #     #",
        "# ####   ######## # #",
        "# #    #          # #",
        "# # ############# # #",
        "# #      #        # #",
        "# ###  ###### ####  #",
        "#         #     G # #",
        "#####################"
    ]
    return maze
def create_level_2():
    maze = [
        "#####################",
        "#  ##G  #         # #",
        "# ## # ## # ####### #",
        "#    #    #   #  ####",
        "## ##### #### # #####",
        "#      #      #    ##",
        "# #### # ######## # #",
        "# #    #          # #",
        "# # ############# # #",
        "# #                 #",
        "# ############### ###",
        "#                S  #",
        "#####################"
    ]
    return maze
def create_level_3():
    maze = [
        "#####################",
        "#         S        ##",
        "# #### ##   ##### ###",
        "#    #   ##   #   K##",
        "## ##### ## # # #####",
        "#      #    #       #",
        "# ####   ######## # #",
        "# #   ##  #       # #",
        "# # ####  ####### # #",
        "# # ##   #   ##     #",
        "########D########## #",
        "#     ##          G #",
        "#####################"
    ]
    return maze

# Classes elements du jeu :
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = button_font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

class Player:
    def __init__(self, x, y, level , image):
        self.x = x
        self.y = y
        self.radius = 5
        self.level = level
        self.speed = speed0
        self.image = None
        
        original_image = pygame.image.load('bottom-dir.png').convert_alpha( )
        self.image = pygame.transform.scale(original_image, (50, 50)) 
                
    def draw(self, surface):
        
        image_rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, image_rect)

    def move(self, dx, dy, maze):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        
        cell_x = int(((new_x - 265) // 70))
        cell_y = int(((new_y - 245) // 70))
        
        if 0 <= cell_y < len(maze) and 0 <= cell_x < len(maze[0]):
            if maze[cell_y][cell_x] != '#':
                self.x = new_x
                self.y = new_y

class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.radius = 12
        image = None
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
        self.change_direction_timer = 0
        image = pygame.image.load('enemy.png').convert_alpha( )
        self.image = pygame.transform.scale(image, (50, 50))
    def draw(self, surface):
        image_rect = self.image.get_rect(center=(self.x, self.y))
        surface.blit(self.image, image_rect)
    def move(self, player_x, player_y, maze):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = max(1, math.sqrt(dx*dx + dy*dy))
        dx, dy = dx/dist, dy/dist
        self.direction = (dx, dy)
        new_x = self.x + self.direction[0] * self.speed
        new_y = self.y + self.direction[1] * self.speed
        
        cell_x = int(((new_x - 265) // 70))
        cell_y = int(((new_y - 245) // 70))
        
        self.x = new_x
        self.y = new_y

class Goal:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 20
        self.image = None
        if level == 1 :
            original_image = pygame.image.load('rikane.png').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50))
        if level == 2 :
            original_image = pygame.image.load('amane.png').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50))
        if level == 3 :
            original_image = pygame.image.load('takane_prison.png').convert_alpha( )
            self.image = pygame.transform.scale(original_image, (50, 50))        
                                                           
        
    def draw(self, surface):
        if self.image:
           image_rect = self.image.get_rect(center=(self.x, self.y))
           surface.blit(self.image, image_rect)

class Key:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 10
        self.collected = False
        image = None
        image = pygame.image.load('key.png').convert_alpha( )
        self.image = pygame.transform.scale(image, (30, 30))
        
    def draw(self, surface):
        if not self.collected:
            image_rect = self.image.get_rect(center=(self.x, self.y))
            surface.blit(self.image, image_rect)


play_button = Button(WIDTH//2 - 850, HEIGHT//2 , 400, 60, "JOUER", (51, 51, 0), (150, 150, 150))
credits_button = Button(WIDTH//2 - 850, HEIGHT//2  + 80, 400, 60, "CRÉDITS", (62, 62, 62), (150, 150, 150))
quit_button = Button(WIDTH//2 - 850, HEIGHT//2 + 160, 400, 60, "QUITTER", (102,0,51), GREY)
def draw_credits_screen():
    screen.fill((23,23,41))
    text0 = title2_font.render("Crédits : ", True, WHITE)
    screen.blit(text0, (WIDTH//2 - 900, HEIGHT//2 - 500))
    text1 , text5 = text_font0.render("Développeur & Designer : Aziz ben Mansour", True, (112,111,69)) , text_font0.render("- email : sakhr001k@gmail.com", True, (112,111,69))
    screen.blit(text1, (WIDTH//2 - 900, HEIGHT//2 - 320))
    screen.blit(text5, (WIDTH//2 - 850, HEIGHT//2 - 270))
    text2 ,  text3 = text_font0.render("Svetlana Kushnariova pour l'aide avec les graphismes des personnages (Les filles) ", True, (112,111,69)) , text_font0.render("- email : lana-chan@yandex.ru", True, (112,111,69))
    screen.blit(text2, (WIDTH//2 - 900, HEIGHT//2 - 170))
    screen.blit(text3, (WIDTH//2 - 850, HEIGHT//2 - 120))
    text4 = text_font0.render("Forrest H Lowe avec les graphismes des personnages (Le photographe) ", True, (112,111,69)) 
    screen.blit(text4, (WIDTH//2 - 900, HEIGHT//2 - 20))
    text8 = text_font0.render("Certains sons ont été crées par David McKee(ViRiX) :soundcloud.com/virix", True, (112,111,69)) 
    screen.blit(text8, (WIDTH//2 - 900, HEIGHT//2 + 80))
    text9 = text_font0.render("Autres Sons et Presque-Music par Will Leamon", True, (112,111,69)) 
    screen.blit(text9, (WIDTH//2 - 900, HEIGHT//2 + 180))
    text10 = text_font0.render("Son 'd'orage' par InspectorJ (www.jshaw.co.uk)", True, (112,111,69)) 
    screen.blit(text10, (WIDTH//2 - 900, HEIGHT//2 + 280))

    text6 = text_font01.render("Jeu open source, Sous LICENSE libre   -Auteur", True, (200,111,69))
    screen.blit(text6, (WIDTH//2 + 280, HEIGHT//2 + 450 ))
    text7 = text_font01.render("dernière Mise à jour à 12/17/2025 - jeu Disponible à https://github.com/sakhr0/TAKANÉ", True, WHITE)
    screen.blit(text7, (WIDTH//2 + 40 , HEIGHT//2 + 500))
    return_button.draw(screen)
def draw_start_screen():
    image = pygame.image.load("bk30.jpg")
    screen.blit(image, (0 , 0)) 
    title_surf = title_font.render("TAKANÉ", True, (224,224,224))
    title_rect = title_surf.get_rect(center=(WIDTH//2 - 580, HEIGHT//2 - 300))
    screen.blit(title_surf, title_rect)
    enonce1_surf , enonce2_surf = text_font.render("Peut-être que le photographe avait pitié de Takané,", True, (224,224,224)) , text_font.render(" mais que se passera-t-il s’il est retourné pour sauver des Takanés ? . . .", True, (224,224,224))
    enonce_rect = enonce1_surf.get_rect(center=(WIDTH//2 + 80 + 40 , HEIGHT//2 + 25))
    screen.blit(enonce1_surf, enonce_rect)
    screen.blit(enonce2_surf, (WIDTH//2 + 80 - 100 , HEIGHT//2 + 50))
    owner_surf = owner_font.render('Version 1.5 - Developpé par A.B', True, WHITE)
    screen.blit(owner_surf, (WIDTH // 2 -850 , HEIGHT //2 - 400 + 165))
    owner2_surf = owner_font.render('2 éme Science 2 ', True, WHITE)
    screen.blit(owner2_surf, (WIDTH // 2 -720 , HEIGHT //2 - 400 + 200))
    play_button.draw(screen)
    quit_button.draw(screen)
    credits_button.draw(screen)
   
facile_button = Button(WIDTH//2 - 600, HEIGHT//2 + 50, 300, 60, "Facile", GREEN, (120, 120, 120))
normal_button = Button(WIDTH//2 - 350, HEIGHT//2  + 50, 300, 60, "Normal", YELLOW, (150, 150, 150))
difficile_button = Button(WIDTH//2 - 100, HEIGHT//2 + 50, 300, 60, "Difficile", RED, GREY) 
return_button = Button(80, HEIGHT - 250, 180, 60, "<-----", BLUE, (150, 150, 150))      
    
def draw_explanation_screen():
    screen.fill((60,40,63))
    text_y = HEIGHT // 2 - 100
    text_surf1 , text_surf2 , text_surf3 , text_surf4 = text_font.render("Tu joues avec le photographe dans une labyrinthe ou les maitres te chassent . Tu dois Sauver d'abord la première esclave nommée Rikane,  " , True , WHITE ) , text_font.render ("puis la deuxième nommée Amané et enfin , collecter le clé et sauver Takané ." , True, WHITE) , text_font.render("Utilise les flèches directionnelles pour te déplacer. Évite les Maitres qui te poursuivent. Bonne chance !" , True , WHITE) , text_font.render("(Attention , les Maites seront de plus en plus rapide  ) . . .  Choisir La difficulté : ", True , WHITE)
    alarm = text_font.render('Sois Loin des Maitres et SAUVE les esclaves !', True, RED)
    title = title2_font.render("Explication : ", True, (224,224,224))
    screen.blit(title, (WIDTH/8 - 200 , HEIGHT / 2 - 450))
    screen.blit(alarm, (WIDTH/2 + 300 , HEIGHT / 2 + + 300))
    screen.blit(text_surf1, ((WIDTH/8 - 190 , HEIGHT / 2 - 300)) ) 
    screen.blit(text_surf2, ((WIDTH/8 - 190 , HEIGHT / 2 - 250)))
    screen.blit(text_surf3, ((WIDTH/8 - 190  , HEIGHT / 2 + - 160)))
    screen.blit(text_surf4, ((WIDTH/8 - 180 + 250 , HEIGHT / 2 + - 90)))
    facile_button.draw(screen)
    normal_button.draw(screen)
    difficile_button.draw(screen)
    return_button.draw(screen)
    

# dessiner labyrinthe
def draw_maze(maze):
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            rect = pygame.Rect(x * 70 + 265 , y * 70 + 245  , 50, 50)    # normal cube size
            if cell == '#':
                pygame.draw.rect(screen, (64, 10, 10), rect)        # walls        
            elif cell == 'G' :
                pygame.draw.rect(screen, (153, 153, 0), rect)
            elif cell == 'S' :
                pygame.draw.rect(screen, (64, 64, 64), rect)
            elif cell == 'K' :
                pygame.draw.rect(screen, (153, 0, 76), rect)                
            else  :
                pygame.draw.rect(screen, BACKGROUND_COLOR, rect)    # ways
            pygame.draw.rect(screen, (0, 0, 0), rect, 4)  # grid lines

def init_level(level_num):
    global player, enemies, goal, key,  maze, key_found
    
    key_found = False
    
    if level_num == 1:
        maze = create_level_1()
        player_x = player_y = goal_x = goal_y = 0
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':  # S = Start 
                    player_x, player_y =  x * 70 + 265 + 25  ,    y * 70 + 245 + 25  # 25 = half of 50
                elif cell == 'G':  # G = Goal
                    goal_x   ,    goal_y = x * 70 + 265 + 25  ,    y * 70 + 245 + 25  # Center in cell
        player = Player(player_x, player_y, 1 , None)
        goal = Goal(goal_x, goal_y)
        enemies = []
        for _ in range(2) :
           while True:
                enemy_grid_x = random.randint(1,19) 
                enemy_grid_y = random.randint(1 ,7) 
                enemy_x = enemy_grid_x * 70 + 265 + 25  # 25 = half of 50 (cell width)
                enemy_y = enemy_grid_y * 70 + 245 + 25  # Center in cell
                dist_to_player = math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2)
                if maze[enemy_grid_y][enemy_grid_x] != '#'  and dist_to_player > MIN_SPAWN_DISTANCE and (enemy_x , enemy_y) != (goal_x , goal_y):
                   enemies.append(Enemy(enemy_x, enemy_y, 2))
                   break
    elif level_num == 2:
        maze = create_level_2()
        player_x = player_y = goal_x = goal_y = 0
        
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
               if cell == 'S':  # S = Start 
                    player_x, player_y =  x * 70 + 265 + 25  ,    y * 70 + 245 + 25  
               elif cell == 'G':  # G = Goal
                    goal_x   ,    goal_y = x * 70 + 265 + 25  ,    y * 70 + 245 + 25  
        player = Player(player_x, player_y, 2 , None)
        goal = Goal(goal_x, goal_y)
        enemies = []
        for _ in range(3):
            while True:
                enemy_grid_x = random.randint(1,19) 
                enemy_grid_y = random.randint(1 ,7) 
                enemy_x = enemy_grid_x * 70 + 265 + 25  # 25 = half of 50 (cell width)
                enemy_y = enemy_grid_y * 70 + 245 + 25  # center in cell
                dist_to_player = math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2)
                if maze[enemy_grid_y][enemy_grid_x] != '#' and dist_to_player > MIN_SPAWN_DISTANCE and (enemy_x , enemy_y) != (goal_x , goal_y):
                   enemies.append(Enemy(enemy_x, enemy_y, 2.3))
                   break
            
    elif level_num == 3:
        maze = create_level_3()
        player_x = player_y = goal_x = goal_y = key_x = key_y  = 0
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                if cell == 'S':
                    player_x, player_y = x * 70 + 265 + 25, y * 70 + 245 + 25
                elif cell == 'G':
                    goal_x, goal_y = x * 70 + 265 + 25, y * 70 + 245 + 25
                elif cell == 'K':
                    key_x, key_y = x * 70 + 265 + 25, y * 70 + 245 + 25
        player = Player(player_x, player_y, 3 , None)
        goal = Goal(goal_x, goal_y)
        key = Key(key_x, key_y)
        
        enemies = []
        for _ in range(3):
            while True:
                enemy_grid_x = random.randint(1, len(maze[0])-2) 
                enemy_grid_y= random.randint(1, len(maze)-2) 
                enemy_x = enemy_grid_x * 70 + 265 + 25
                enemy_y = enemy_grid_y * 70 + 245 + 25
                dist_to_player = math.sqrt((enemy_x - player_x)**2 + (enemy_y - player_y)**2)
                if maze[enemy_grid_y][enemy_grid_x] != '#' and dist_to_player > MIN_SPAWN_DISTANCE:
                    break
            enemies.append(Enemy(enemy_x, enemy_y, 2.5))
def draw_game_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_maze(maze)
    if level == 3 and not key_found :
        key.draw(screen)
    goal.draw(screen)
    for enemy in enemies:
        enemy.draw(screen)
    player.draw(screen)

def draw_win_screen():
    screen.fill((64,64,64))
    congrats_text = title_font.render("Félicitations ! ", True, GREEN)
    congrats_rect = congrats_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(congrats_text, congrats_rect)
    sub_text = text_font0.render("Vous avez complété la mission avec succès ! ", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 150))
    screen.blit(sub_text, sub_rect)
    sub2_text = text_font0.render("(Espace pour retourner au menu)", True, WHITE)
    sub2_rect = sub2_text.get_rect(center=(WIDTH//2, HEIGHT//4 + 240))
    screen.blit(sub2_text, sub2_rect)
    or_1 , or_2 , or_3 = pygame.image.load('rikane.png').convert_alpha( ) , pygame.image.load('amane.png').convert_alpha( ) , pygame.image.load('takane.png').convert_alpha( )
    image1 , image2 , image3 = pygame.transform.scale(or_1, (100, 100)) , pygame.transform.scale(or_2, (100, 100)) , pygame.transform.scale(or_3, (100, 100))
    screen.blit(image1, (WIDTH//2 - 400 , HEIGHT//2 ))
    screen.blit(image2, (WIDTH//2 -100  , HEIGHT//2 ))
    screen.blit(image3, (WIDTH//2 + 200 , HEIGHT//2 ))

#Lose screens for different levels
orginal1, original2 , orginal3 = pygame.image.load('rikane_lose.png').convert_alpha( ) , pygame.image.load('amane_lose.png').convert_alpha( ) , pygame.image.load('takane_lose.png').convert_alpha( )

def draw_lose_screen1():
    screen.fill((52,0,0))
    lose_text = title_font.render("Photographe Attrapé!", True, RED)
    lose_rect = lose_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(lose_text, lose_rect)
    sub_text = text_font0.render("Mission échouée .  Réessayer( Espace ) ", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2 - 60, HEIGHT//4 + 200))
    screen.blit(sub_text, sub_rect)
    image1 , image2 , image3 = pygame.transform.scale(orginal1, (100, 100)) , pygame.transform.scale(original2, (100, 100)) , pygame.transform.scale(orginal3, (100, 100))

    screen.blit(image1, (WIDTH//2 - 400 , HEIGHT//2 ))
    screen.blit(image2, (WIDTH//2 -100  , HEIGHT//2 ))
    screen.blit(image3, (WIDTH//2 + 200 , HEIGHT//2 )) 
def draw_lose_screen2():
    screen.fill((52,0,0))
    lose_text = title_font.render("Photographe Attrapé!", True, RED)
    lose_rect = lose_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(lose_text, lose_rect)
    sub_text = text_font0.render("Mission échouée .  Réessayer( Espace ) ", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2 - 60, HEIGHT//4 + 200))
    screen.blit(sub_text, sub_rect)
    image1 , image2 , image3 = pygame.transform.scale(orginal1, (100, 100)) , pygame.transform.scale(original2, (100, 100)) , pygame.transform.scale(orginal3, (100, 100))

    original_1_2 =  pygame.image.load('rikane.png').convert_alpha( )
    image_1_2 = pygame.transform.scale(original_1_2, (100, 100))
    screen.blit(image_1_2, (WIDTH//2 - 400 , HEIGHT//2 ))
    screen.blit(image2, (WIDTH//2 -100  , HEIGHT//2 ))
    screen.blit(image3, (WIDTH//2 + 200 , HEIGHT//2 )) 
def draw_lose_screen3():
    screen.fill((52,0,0))
    lose_text = title_font.render("Photographe Attrapé!", True, RED)
    lose_rect = lose_text.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(lose_text, lose_rect)
    sub_text = text_font0.render("Mission échouée .  Réessayer( Espace ) ", True, WHITE)
    sub_rect = sub_text.get_rect(center=(WIDTH//2 - 60, HEIGHT//4 + 200))
    screen.blit(sub_text, sub_rect)
    image1 , image2 , image3 = pygame.transform.scale(orginal1, (100, 100)) , pygame.transform.scale(original2, (100, 100)) , pygame.transform.scale(orginal3, (100, 100))

    original_1_2 =  pygame.image.load('rikane.png').convert_alpha( )
    image_1_2 = pygame.transform.scale(original_1_2, (100, 100))
    original_2_2 = pygame.image.load('amane.png').convert_alpha( )
    image_2_2 = pygame.transform.scale(original_2_2, (100, 100))
    screen.blit(image_1_2, (WIDTH//2 - 400 , HEIGHT//2 ))
    screen.blit(image_2_2, (WIDTH//2 -100  , HEIGHT//2 ))
    screen.blit(image3, (WIDTH//2 + 200 , HEIGHT//2 )) 




# Boucle principale du jeu


clock = pygame.time.Clock()
running = True

while running:
    mouse_pos = pygame.mouse.get_pos()
    click = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if current_state == WIN_SCREEN or current_state == LOSE_SCREEN1 or current_state == LOSE_SCREEN2 or current_state == LOSE_SCREEN3:
                    current_state = START_MENU
                    level = 1
                    init_level(1)
                    key_found = False
            elif event.key == pygame.K_ESCAPE:
                if current_state == WIN_SCREEN or current_state == LOSE_SCREEN1 or current_state == LOSE_SCREEN2 or current_state == LOSE_SCREEN3:
                    running = False
    if current_state == EXPLANATION:
                    facile_button.check_hover(mouse_pos)
                    normal_button.check_hover(mouse_pos)
                    difficile_button.check_hover(mouse_pos)
                    return_button.check_hover(mouse_pos)
                    if facile_button.is_clicked(mouse_pos, click):
                        play_transition_sound('transition.wav' , 0.5  )
                        speed0 = 8
                        init_level(1)
                        current_state = GAME_LEVEL_1
                    if normal_button.is_clicked(mouse_pos, click):
                        play_transition_sound('transition.wav' , 0.5  )
                        speed0 = 5
                        init_level(1)
                        current_state = GAME_LEVEL_1
                    if difficile_button.is_clicked(mouse_pos, click):
                        play_transition_sound('transition.wav' , 0.5  )
                        speed0 = 3
                        init_level(1)
                        current_state = GAME_LEVEL_1
                    if return_button.is_clicked(mouse_pos, click):
                        play_transition_sound('transition.wav' , 0.5 )
                        current_state = START_MENU
    if current_state == START_MENU:
        play_music('rain.wav' , 0.5 , -1)
        draw_start_screen()
        play_button.check_hover(mouse_pos)
        quit_button.check_hover(mouse_pos)
        credits_button.check_hover(mouse_pos)
        
        if play_button.is_clicked(mouse_pos, click):
            play_transition_sound('transition.wav' , 0.7  )
            current_state = EXPLANATION

            
        if quit_button.is_clicked(mouse_pos, click):
            running = False
        if credits_button.is_clicked(mouse_pos, click):  
            play_transition_sound('transition.wav' , 0.7 )
            current_state = CREDITS
    if current_state == CREDITS:
             draw_credits_screen()
             return_button.check_hover(mouse_pos)
             if return_button.is_clicked(mouse_pos, click):
                        play_transition_sound('transition.wav' , 0.7  )
                        current_state = START_MENU



 
    if current_state == EXPLANATION:
        
        draw_explanation_screen()
            
    if current_state in [GAME_LEVEL_1, GAME_LEVEL_2, GAME_LEVEL_3]:
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT]:
            dx = -1
            player.image = player_images["left"]
        if keys[pygame.K_RIGHT]:
            dx = +1
            player.image = player_images["right"]
        if keys[pygame.K_UP]:
            dy = -1
            player.image = player_images["up"]
        if keys[pygame.K_DOWN]:
            dy = +1
            player.image = player_images["down"]
            
        player.move(dx, dy, maze)
        
        for enemy in enemies:
            if not keys[pygame.K_l] :                     # cheat code to disable enemies
               enemy.move(player.x, player.y, maze)
            
            dist = math.sqrt((player.x - enemy.x)**2 + (player.y - enemy.y)**2)
            if dist < player.radius + enemy.radius:
                if level == 1 :
                    current_state = LOSE_SCREEN1
                if level == 2 :
                    current_state = LOSE_SCREEN2
                if level == 3 :    
                   current_state = LOSE_SCREEN3
                play_transition_sound('loose.wav' , 0.7 )   
        
        dist_to_goal = math.sqrt((player.x - goal.x)**2 + (player.y - goal.y)**2)
        if dist_to_goal < player.radius + goal.radius :   
            if level == 1 and dist_to_goal < player.radius + goal.radius :
                play_transition_sound('transition.wav' , 0.7 )
                current_state = GAME_LEVEL_2
                level = 2
                init_level(2)
            elif level == 2 and dist_to_goal < player.radius + goal.radius : 
                play_transition_sound('transition.wav' , 0.7 )       
                current_state = GAME_LEVEL_3
                level = 3
                init_level(3)
            elif level == 3 and key_found == True  :
                   current_state = WIN_SCREEN
                   play_transition_sound('win.wav' , 0.7 )
                

        
        if level == 3 and not key_found == True:
            dist_to_key = math.sqrt((player.x - key.x)**2 + (player.y - key.y)**2)
            if dist_to_key < player.radius + key.radius:
                play_transition_sound('transition2.wav' , 0.7 )
                key_found = True
                key.collected = True
        draw_game_screen()
    elif current_state == WIN_SCREEN:
        draw_win_screen()
    elif current_state == LOSE_SCREEN1:
       
        draw_lose_screen1()
    elif current_state == LOSE_SCREEN2:
      
        draw_lose_screen2()
    elif current_state == LOSE_SCREEN3:
       
        draw_lose_screen3()
        keys = pygame.key.get_pressed()        
        if keys[pygame.K_SPACE] :
            current_state = GAME_LEVEL_1    
            level = 1
            init_level(1)
            key_found = False
            draw_game_screen()
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
