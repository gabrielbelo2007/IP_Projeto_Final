import math
import pygame
from . import config
from .projectile import Projectile

#classe do jack
class Player(pygame.sprite.Sprite):
    
    def __init__(self,pos,all_sprites_group,projectile_group):
        #inicializa o sprite e ja coloca no grupo de tudo
        super().__init__(all_sprites_group)

        #guarda os grupos para poder criar tiros
        self.all_sprites = all_sprites_group
        self.projectiles = projectile_group

        #cria a imagem do jack como um quadrado
        self.image = pygame.Surface(
            (config.PLAYER_WIDTH,config.PLAYER_HEIGHT),
            pygame.SRCALPHA
        )
        #pinta o jack com a cor definida no config
        self.image.fill(config.PLAYER_COLOR)

        #guarda uma copia da imagem original para girar depois
        self.base_image = self.image.copy()

        #rect controla posicao e colisao do jack
        self.rect = self.image.get_rect(center=pos)

        #pos guarda a posicao real (float)
        self.pos = pygame.math.Vector2(pos)

        #movimento
        self.base_speed = config.PLAYER_SPEED
        
        #buff
        self.current_speed = self.base_speed
        self.buff_end_time = 0
        
        self.direction = pygame.math.Vector2(0,0)

        #vida
        self.max_health = config.PLAYER_MAX_HEALTH
        self.health = config.PLAYER_MAX_HEALTH

        #invencibilidade (i frame)
        self.invincible = False
        self.invincible_time = config.PLAYER_INVINCIBILITY_TIME
        self.last_hit_time = 0

        #cooldown do tiro
        self.shoot_cooldown = config.SHOOT_COOLDOWN
        self.last_shot_time = 0

    #lida com teclado e mouse
    def handle_input(self):
        keys = pygame.key.get_pressed()

        #zera a direcao antes de ler as teclas
        self.direction.update(0,0)

        #wasd para mover
        if keys[pygame.K_w]:
            self.direction.y -= 1
        if keys[pygame.K_s]:
            self.direction.y += 1
        if keys[pygame.K_a]:
            self.direction.x -= 1
        if keys[pygame.K_d]:
            self.direction.x += 1

        #normaliza pra nao ficar mais rapido na diagonal
        if self.direction.length() != 0:
            self.direction = self.direction.normalize()

        #mouse: botao esquerdo atira
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0]:
            mouse_pos = pygame.mouse.get_pos()
            self.shoot(mouse_pos)
            

    def apply_speed_boost(self, multiplier, duration_ms):
        self.current_speed = self.base_speed * multiplier
        self.buff_end_time = pygame.time.get_ticks() + duration_ms
        # Efeito visual simples: Muda cor para Azul ciano
        self.image.fill((0, 255, 255)) 


    def update_buffs(self):
        if pygame.time.get_ticks() > self.buff_end_time and self.current_speed != self.base_speed:
            self.current_speed = self.base_speed
            self.image.fill(config.PLAYER_COLOR) # Volta a cor original

    #aplica o movimento
    def move(self):
        #posicao anda na direcao vezes a velocidade
        self.pos += self.direction * self.current_speed

        #atualiza o rect com a pos nova
        self.rect.center = (int(self.pos.x),int(self.pos.y))

        #mantem o jack dentro da tela
        screen_rect = pygame.Rect(0,0,config.WIDTH,config.HEIGHT)
        self.rect.clamp_ip(screen_rect)
        #atualiza a posicao real caso tenha batido na borda
        self.pos.update(self.rect.centerx,self.rect.centery)

    #faz o jack olhar para o mouse
    def look_at_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        #vetor do jack ate o mouse
        direction = pygame.math.Vector2(mouse_pos) - self.pos

        #se o mouse estiver exatamente em cima do jack, nao faz nada
        if direction.length() == 0:
            return

        #calcula o angulo em graus (pygame usa y invertido)
        angle = math.degrees(math.atan2(-direction.y,direction.x))

        #gira a imagem base do jack
        self.image = pygame.transform.rotate(self.base_image,angle)

        #recalcula o rect para manter o centro no mesmo lugar
        self.rect = self.image.get_rect(center=self.rect.center)
        
        

    #cria um tiro em direcao ao alvo (mouse) respeitando o cooldown
    def shoot(self,target_pos):
        now = pygame.time.get_ticks()

        #se ainda nao passou o tempo de cooldown, nao atira
        if now - self.last_shot_time < self.shoot_cooldown:
            return

        #cria o projetil na posicao atual do jack
        projectile = Projectile(self.rect.center,target_pos)

        #coloca o projetil nos grupos
        self.all_sprites.add(projectile)
        self.projectiles.add(projectile)

        #atualiza o momento do ultimo tiro
        self.last_shot_time = now

    #aplica dano no jack
    def take_damage(self,amount):
        now = pygame.time.get_ticks()

        #se ainda esta invencivel dentro do tempo, ignora o dano
        if self.invincible and now - self.last_hit_time < self.invincible_time:
          return

        #tira vida
        self.health -= amount
        if self.health < 0:
            self.health = 0

        #ativa modo invencivel e guarda o momento do hit
        self.invincible = True
        self.last_hit_time = now
        
        # SOM DE DANO

    #atualiza o tempo de invencibilidade
    def update_invincibility(self):
        
        if self.invincible:
            now = pygame.time.get_ticks()
            
            if (now // 100) % 2 == 0:
                self.image.set_alpha(100) # Meio transparente
            else:
                self.image.set_alpha(255) # Normal
            
            if now - self.last_hit_time >= self.invincible_time:
                self.invincible = False
                
        else:
            self.image.set_alpha(255)

    #funcao chamada todo frame pelo grupo de sprites
    def update(self):
        
        if self.current_speed > self.base_speed:
             self.image = self.base_image.copy()
             self.image.fill((0, 255, 255))
        else:
             self.image = self.base_image.copy()
        
        self.handle_input()
        self.move()
        self.look_at_mouse()
        self.update_invincibility()


#bloco de teste: permite rodar so o player.py
if __name__ == "__main__":
    print("iniciando teste do jack...")

    pygame.init()

    #cria a janela usando as configs do jogo
    screen = pygame.display.set_mode((config.WIDTH,config.HEIGHT))
    pygame.display.set_caption("teste do jack")

    clock = pygame.time.Clock()

    #grupos de sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    #cria o jack no centro da tela
    player = Player(
        (config.WIDTH // 2,config.HEIGHT // 2),
        all_sprites,
        bullets
    )
    all_sprites.add(player)

    running = True
    while running:
        #controla o fps
        dt = clock.tick(config.FPS)

        #eventos de fechar a janela
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #atualiza todos os sprites (player + tiros)
        all_sprites.update()

        #desenha fundo e sprites
        screen.fill(config.BLACK)
        all_sprites.draw(screen)

        pygame.display.flip()

    pygame.quit()