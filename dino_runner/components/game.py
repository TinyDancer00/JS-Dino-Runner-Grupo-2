import pygame
from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.obstacles.cactus import Cactus
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.score import Score
from dino_runner.utils.constants import BG, DINO_START, FONT_STYLE, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, SMALL_CACTUS, TITLE, FPS


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE) ###nombre de la pestaña
        pygame.display.set_icon(ICON) ###icono de la pestaña
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) ###crear ventana a ver
        self.clock = pygame.time.Clock() ###genera un reloj
        
        self.playing = False ###variable que indica si estamos jugando
        self.game_speed = 20 ###velocidad del juego
        self.x_pos_bg = 0 ###posicion en eje x (__) en que estara el background [de izquierda a derecha]
        self.y_pos_bg = 380 ###posicion en eje y (|) en que estara el background [de arriba a abajo]
        ### pueden ponerse cosas por guera de la pantalla [valores negativos]

        self.player = Dinosaur()
        self.obstacle_manager = ObstacleManager()

        self.running = False
        self.score = Score()
        self.death_count = 0

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()

    def run(self):
        # Game loop: events - update - draw
        self.playing = True ###se empieza a jugar
        self.obstacle_manager.reset_obstacles
        while self.playing: ###mientras se este jugando ejecutar los siquientes metodos
            self.events()
            self.update()
            self.draw()
        pygame.quit() ###cuando se deja de jugar se sale

    def events(self):
        for event in pygame.event.get(): ###libreria pygame/event
            if event.type == pygame.QUIT: ###si el evento es cerrar el juego, este se termina
                self.playing = False

    def update(self): ###actualiza el estado del juego
        user_input = pygame.key.get_pressed() ###ingresa una accion por medio del usuario
        self.player.update(user_input)
        self.obstacle_manager.update(self.game_speed, self.player, self.on_death)
        self.score.update(self)

    def draw(self): ###aqui se dibujaran los objetos que necesitamos
        self.clock.tick(FPS) ### tick ayuda a refrescar la pantalla n numero de veces por segundo
        self.screen.fill((255, 255, 255)) ###screen.fill sirve para rellenar la pantalla de color RGB
        self.draw_background()  ###con este drsaw ponemos el camino que se mueve
        self.player.draw(self.screen)
        self.obstacle_manager.draw(self.screen)
        self.score.draw(self.screen)
        pygame.display.update() ###actualiza los ajustes de pantalla (relleno, color, objetos)
        pygame.display.flip()

    def draw_background(self):
        image_width = BG.get_width() ###manda llamar imagen del archivo constants
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg)) ###blit dibuja imagen las coordenadas antes mencionadas
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:### recorrera imagen a modo que se desplaze 
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg)) ###si ya paso toda la imagen, dibuja la continuacion
            self.x_pos_bg = 0 ###reinicia imagen al llegar valor 0
        self.x_pos_bg -= self.game_speed

    def show_menu(self):
        self.screen.fill((255,255,255))### pintar fondo de la pantalla
        pos_center_x = SCREEN_WIDTH // 2
        pos_center_y = SCREEN_HEIGHT // 2

        if self.death_count <= 0:
            font = pygame.font.Font(FONT_STYLE, 30)### bienvenida al juego
            text = font.render("PRESS ANY KEY TO START", True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect.center = (pos_center_x, pos_center_y)
            self.screen.blit(text, text_rect)
        else:
            ### Mostrar mensaje de reinicio
            ### Puntaje obtenido
            ### Numero de muertes
            pass

        dino_rect = DINO_START.get_rect()### mostrar imagen o logo
        dino_rect.center = (pos_center_x, pos_center_y - 80)
        self.screen.blit(DINO_START, (dino_rect))
        pygame.display.update()### actualizar pantalla

    
    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                self.run()

    def reset_obstacles(self):
        self.obstacles = []

    def on_death(self):
        self.playing = False
        self.death_count += 1
        print ("N° de Muertes:", self.death_count)