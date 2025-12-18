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
        
        img_original = pygame.image.load("assets/images/characters/jack.png").convert_alpha()
        self.image = pygame.transform.scale(img_original, (config.PLAYER_WIDTH, config.PLAYER_HEIGHT))

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
        
        
    #aplica o movimento
    def move(self, cages):

        self.pos.x += self.direction.x * self.current_speed
        self.rect.centerx = int(self.pos.x)
        
        # Checa colisão horizontal com as gaiolas
        if cages:
            hits = pygame.sprite.spritecollide(self, cages, False)
            if hits:
                wall = hits[0] 
                
                if self.direction.x > 0:
                    self.rect.right = wall.rect.left

                elif self.direction.x < 0:
                    self.rect.left = wall.rect.right
                
                self.pos.x = self.rect.centerx

        self.pos.y += self.direction.y * self.current_speed
        self.rect.centery = int(self.pos.y)

        if cages:
            hits = pygame.sprite.spritecollide(self, cages, False)
            if hits:
                wall = hits[0]

                if self.direction.y > 0:
                    self.rect.bottom = wall.rect.top

                elif self.direction.y < 0:
                    self.rect.top = wall.rect.bottom
                
                self.pos.y = self.rect.centery

        # Mantém dentro da tela
        screen_rect = pygame.Rect(0, 0, config.WIDTH, config.HEIGHT)
        self.rect.clamp_ip(screen_rect)
        self.pos.update(self.rect.centerx, self.rect.centery)
        

    #faz o jack olhar para o mouse
    def look_at_mouse(self):
        mouse_pos = pygame.mouse.get_pos()
        #vetor do jack ate o mouse
        direction = pygame.math.Vector2(mouse_pos) - self.pos

        #se o mouse estiver exatamente em cima do jack, nao faz nada
        if direction.length() == 0:return

        #calcula o angulo em graus (pygame usa y invertido)
        angle = math.degrees(math.atan2(-direction.y,direction.x))
       
        #recalcula o rect para manter o centro no mesmo lugar
        self.rect = self.image.get_rect(center=self.rect.center)
        
        temp_img = self.base_image.copy()
        if self.current_speed > self.base_speed:
            temp_img.fill((0, 100, 100), special_flags=pygame.BLEND_ADD) 
        

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


    def apply_speed_boost(self, multiplier, duration_ms):
        self.current_speed = self.base_speed * multiplier
        self.buff_end_time = pygame.time.get_ticks() + duration_ms


    def update_buffs(self):
        if pygame.time.get_ticks() > self.buff_end_time and self.current_speed != self.base_speed:
            self.current_speed = self.base_speed
            self.image.fill(config.PLAYER_COLOR) # Volta a cor original


    #funcao chamada todo frame pelo grupo de sprites
    def update(self, cages):
        
        if self.current_speed > self.base_speed:
            self.base_image.fill((0, 255, 255), special_flags=pygame.BLEND_MULT) 
        
        self.handle_input()
        self.move(cages)
        self.look_at_mouse()
        self.update_invincibility()