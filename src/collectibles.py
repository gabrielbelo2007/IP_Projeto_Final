import pygame
import math # efeito de flutuar uso do seno

class Tooth(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            
            original_image = pygame.image.load('../images/dente.jpeg').convert_alpha()
            #Se a imagem for muito grande, ela fica escalada em (32,32)
            self.image = pygame.transform.scale(original_image, (32, 32)) 
        except FileNotFoundError:
            print("ERRO: Imagem do dente não encontrada.")
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 255, 255)) # Branco

        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # --- ATRIBUTOS DO ITEM ---
        self.score_value = 100  
        
        # Animação de flutuar
        self.y_start = y
        self.timer = 0

    def update(self):
        # Efeito de flutuar (Senoide)
        self.timer += 0.1
        offset = math.sin(self.timer) * 5  # 5px cima ou baixo
        self.rect.centery = self.y_start + offset

class Heart(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            original_image = pygame.image.load('../images/coracao.jpeg').convert_alpha()
            self.image = pygame.transform.scale(original_image, (32, 32))
        except FileNotFoundError:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0)) # Vermelho se não achar imagem

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.heal_value = 20  # vida recuperada
        
        # Animação
        self.y_start = y
        self.timer = 0

    def update(self):
        self.timer += 0.15 # Coração bate/flutua um pouco mais rápido
        offset = math.sin(self.timer) * 3
        self.rect.centery = self.y_start + offset