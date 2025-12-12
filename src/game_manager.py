import pygame
from . import config as cfg

class GameManager:
    
    def __init__(self):
        pass

    def run_loop(self):
        pygame.init() # Similar a inicializar "engine"

        pygame.display.set_caption(cfg.TITLE) # Nome da janela
        screen = pygame.display.set_mode((cfg.WIDTH, cfg.HEIGHT)) # Tamanho
        clock = pygame.time.Clock() # Inicializar relógio de frames

        running = True
        while running:
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            pygame.display.update()
            clock.tick(cfg.FPS)

        pygame.quit()