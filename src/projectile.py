import pygame
from . import config

#classe que representa o tiro de gelo do jack
class Projectile(pygame.sprite.Sprite):
    def __init__(self,start_pos,target_pos):
        #inicializa a classe sprite do pygame
        super().__init__()

        img_raw = pygame.image.load('assets/images/characters/jack_projectile.png').convert_alpha()
        self.image = pygame.transform.scale(img_raw, (30, 30))
        
        #rect controla posicao e colisao do projetil
        #comeca com o centro na posicao inicial (jack)
        self.rect = self.image.get_rect(center=start_pos)

        #pos guarda a posicao real como vetor (aceita float)
        self.pos = pygame.math.Vector2(start_pos)

        #direcao = alvo - origem (mouse - jack)
        direction = pygame.math.Vector2(target_pos) - self.pos

        #se o vetor nao for zero, normaliza (so direcao, tamanho 1)
        if direction.length() != 0:
            direction = direction.normalize()

        #velocidade final do tiro = direcao normalizada * velocidade
        self.velocity = direction * config.PROJECTILE_SPEED

    def update(self):
        #anda um passo na direcao da velocidade
        self.pos += self.velocity

        #atualiza o rect com a nova posicao
        self.rect.center = (int(self.pos.x),int(self.pos.y))

        #se sair completamente da tela, remove o projetil
        if (
            self.rect.right < 0
            or self.rect.left > config.WIDTH
            or self.rect.bottom < 0
            or self.rect.top > config.HEIGHT
        ):
            self.kill()