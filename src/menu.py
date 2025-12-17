import pygame
from . import config

class MainMenu:
    
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.SysFont("Arial", 64, bold=True)
        self.font_options = pygame.font.SysFont("Arial", 40)
        
        # Opções do menu
        self.options = ["START_GAME", "QUIT"]
        self.index = 0 # Qual opção está selecionada agora

    def update(self):
        # 1. Captura de Eventos (Teclado)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.index = (self.index - 1) % len(self.options)
                elif event.key == pygame.K_DOWN:
                    self.index = (self.index + 1) % len(self.options)
                elif event.key == pygame.K_RETURN:
                    # Retorna o nome da opção selecionada para o main.py
                    return self.options[self.index]

        # 2. Desenho da Tela
        self.draw()
        
        # Se nenhuma tecla de ação foi pressionada, continua no menu
        return "WAIT"

    def draw(self):
        self.screen.fill((30, 30, 60)) # Fundo azul escuro

        # Desenhar Título
        title_surf = self.font_title.render("MEU JOGO PYGAME", True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(self.screen.get_width()//2, 150))
        self.screen.blit(title_surf, title_rect)

        # Desenhar Opções
        for i, opt in enumerate(self.options):
            # Se for a opção selecionada, fica amarela, senão branca
            color = (255, 255, 0) if i == self.index else (255, 255, 255)
            text = "> " + opt + " <" if i == self.index else opt
            
            opt_surf = self.font_options.render(text, True, color)
            opt_rect = opt_surf.get_rect(center=(self.screen.get_width()//2, 350 + i * 80))
            self.screen.blit(opt_surf, opt_rect)
