import sys
from src import config as cfg
from src.menu import MainMenu  # Classe da aba de menu
from src.game_manager import GameManager
import pygame

class Main:
    
    def __init__(self):
        pygame.init() # Similar a inicializar "engine"

        pygame.display.set_caption(cfg.TITLE) # Nome da janela
        self.screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT)) # Tamanho
        self.clock = pygame.time.Clock() # Inicializar relógio de frames
        self.fps = cfg.FPS
        self.running = True
        
        # As telas (jogo e menu)
        self.menu = MainMenu(self.screen)
        self.game_manager = GameManager(self.screen)
        
        # Escolha da tela atual (começa no menu)
        self.state = "menu"
    
    def run_screen(self):
        
        while self.running:
            if self.state == "menu":
                self.menu_loop()

            elif self.state == "game":
                self.game_loop()
                

    """
    def menu_loop(self):
        
        command = self.menu.update()
        
        if command == "START_GAME":
            self.state = "game"
            
        elif command == "QUIT":
            self.running = False
    """      
            
    
    def game_loop(self):
        
        in_game = self.game_manager.update()
        
        if not in_game:
            self.state = 'menu'
    

if __name__ == "__main__":
    main = Main()
    main.run_screen()
    
    # Esse aqui desliga a "engine" - pygame.init()
    pygame.quit()
    
    # Esse fecha a janela (e todos os processos relacionados)
    sys.exit()