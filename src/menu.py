import pygame
from . import config
import os

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.fonte = pygame.font.match_font(config.FONTE)
        self.carregar_arquivos()

    def carregar_arquivos(self):
        #carrega as imagens
        diretorio_imagens = os.path.join(os.getcwd(), 'assets\images\itens_menu')

        #background
        self.img_fundo = pygame.image.load(os.path.join(diretorio_imagens, config.BACKGROUND_MENU)).convert()

        self.img_fundo = pygame.transform.scale(self.img_fundo, (config.WIDTH, config.HEIGHT))
        self.fundo_rect = self.img_fundo.get_rect()

        #botão jogar
        self.img_jogar = pygame.image.load(os.path.join(diretorio_imagens, config.BTN_JOGAR)).convert_alpha()
        self.img_jogar_hover = pygame.image.load(os.path.join(diretorio_imagens, config.HOVER_JOGAR)).convert_alpha()

        self.btn_jogar_rect = self.img_jogar.get_rect()
        self.btn_jogar_rect.center = (config.WIDTH / 2, 250)

        #botão sair
        self.img_sair = pygame.image.load(os.path.join(diretorio_imagens, config.BTN_SAIR)).convert_alpha()
        self.img_sair_hover = pygame.image.load(os.path.join(diretorio_imagens, config.HOVER_SAIR)).convert_alpha()

        self.btn_sair_rect = self.img_sair.get_rect()
        self.btn_sair_rect.center = (config.WIDTH / 2, 350)

        #logo
        self.logo = pygame.image.load(os.path.join(diretorio_imagens, config.LOGO_MENU)).convert_alpha()
        self.logo_rect = self.logo.get_rect(center=(config.WIDTH / 2, 100))

    def mostrar_tela_start(self):
        #loop do menu
        esperando = True
        while esperando:
            self.clock.tick(config.FPS)
            mouse_pos = pygame.mouse.get_pos() #posição do mouse

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    esperando = False
                    return 'QUIT'
                
                #clique no botão do mouse
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1: #botão esquerdo do mouse
                        if self.btn_jogar_rect.collidepoint(mouse_pos):
                            return "START_GAME" #retorna ação para o loop principal
                        
                        elif self.btn_sair_rect.collidepoint(mouse_pos):
                            esperando = False
                            return 'QUIT'
            
            #desenhar
            self.screen.fill(config.BLACK) #limpar a tela
            self.screen.blit(self.img_fundo, (0, 0)) #adiciona o background em cima do fundo preto
            self.screen.blit(self.logo, self.logo_rect) #desenha a logo

            #lógica de hover
            if self.btn_jogar_rect.collidepoint(mouse_pos): #botão jogar
                self.screen.blit(self.img_jogar_hover, self.btn_jogar_rect)

            else: #botão sair
                self.screen.blit(self.img_jogar, self.btn_jogar_rect)

            pygame.display.flip()