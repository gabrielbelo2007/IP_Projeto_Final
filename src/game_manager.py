import sys
import pygame
from . import config as cfg

class GameManager:
    
    
    def __init__(self, screen):
        
        self.screen = screen
        self.paused = False
        self.running = True
        
        self.tempo_boss = cfg.TIMER
        self.spawn_count = cfg.INIMIGOS_INICIAS
                
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # self.jogador = Jack()  # Construção do objeto jogador (img e caixa de colisão)
        self.all_sprites.add(self.jogador)
        
        # Controles do menu de pausa
        # self.pause_options = ["Continuar", "Sair para o Menu"]
        # self.pause_index = 0


    # Atualiza os frames do jogo
    def update(self):
        
        # Fora do menu de pause interno
        if not self.paused:
            
            self.all_sprits.update()
            self.check_collisions()
            
        # Jogo no pause interno
        else:
            self.update_pause_menu()
    
    
    # "Desenha" na tela os objetos de inimigos, jogador...
    def draw(self):
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            self.draw_pause_overlay()
    
    
    def draw_pause_overlay(self):
    
        overlay = pygame.Surface(self.screen.get_width(), self.screen.get_height()) # Só para criar a "tela" sobreposta
        # COMPLETAR
    
    
    # Lida com as ações dentro do pause interno
    def events_pause(self, event):
        
        if event.type == pygame.KEYDOWN:
            
            # Seleciona o botão com as setas
            if event.key == pygame.K_UP:
                self.pause_index = (self.pause_index - 1) % len(self.pause_options)
            
            elif event.key == pygame.K_DOWN:
                self.pause_index = (self.pause_index + 1) % len(self.pause_options)
                
            # Aperta o botão com o enter
            elif event.key == pygame.K_RETURN:
                
                if self.pause_index == 0: # Tem que colocar o índice correspondente a posição na lista de opçõe
                    self.paused = False 
                
                elif self.pause_index == 1:
                    self.running = False
            


    def run_loop(self):
        
        for event in pygame.event.get():
            
            # Esse event é o de clicar no botão de fechar a janela do jogo (não é tão indicado)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Esse é avaliado toda vez que uma tecla é apertada
            if event.type == pygame.KEYDOWN:
                
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused # Dessa forma pq aperta "esc" já estando no menu volta pro jogo
                    
        self.update()
        self.draw()
        
        if not self.running:
            return "back_menu"
    
    
    # collisions
    
    # def spawn_inimigos(self):
        
    #def new_game(self):
 