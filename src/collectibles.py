import pygame
import math # efeito de flutuar uso do seno
import random

DROP_CHANCE_HEART = 0.15
DROP_CHANCE_ICE = 0.1

class Collectible(pygame.sprite.Sprite):

    def __init__(self, x, y, img_path, size=(32, 32)):
        super().__init__()

        raw_img = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(raw_img, size)

            
        self.rect = self.image.get_rect(center=(x, y))
        self.y_start = y
        self.timer = random.random() * 10 # Random para não flutuarem sincronizados

    def update(self):
        self.timer += 0.1
        offset = math.sin(self.timer) * 5
        self.rect.centery = self.y_start + offset


# pensar em como fazer para que eles spawnem(talvez em algum tempo determinado)
class Tooth(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, '/home/gabrielbelo/IP_Projeto_Final/assets/images/items/dente.jpeg')

        # Pontuação do tooth
        self.score_value = 100 # player.score += tooth.score_value na main

class Heart(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, '/home/gabrielbelo/IP_Projeto_Final/assets/images/items/coracao.jpeg')
        
        self.heal_value = 20  # vida recuperada // player.hp += heart.heal_value

class Ice(Collectible):
    def __init__(self, x, y):
        super().__init__(x, y, '/home/gabrielbelo/IP_Projeto_Final/assets/images/items/floco_neve.jpeg')

        # Buff na move_speed
        self.boost_multiplier = 1.2 # multiplicador da velocidade * 1.2
        self.duration = 15000 # 15 segundos de duração o efeito
        

class Cage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        original_image = pygame.image.load('/home/gabrielbelo/IP_Projeto_Final/assets/images/items/jaula.jpeg').convert_alpha()
        self.image = pygame.transform.scale(original_image, (48, 48)) # A gaiola tem um tamanho maior que os coletáveis, porque faz sentido

        # Posicionamento da gaiola
        self.rect = self.image.get_rect(topleft=(x, y))
        
        # Atributos da giaola
        self.health = 60 # O dano de ataque é 20, então a gaiola pode tomar 3 hits

    def take_damage(self, damage): # função de dano tomado da cage
        self.health -= damage
        
        if self.health <= 0:
            self.kill()
            return True # Retorna True para avisar que a gaiola foi destruída
        return False
    

# funções de spawn

#spawn do coração
def try_spawn_heart(x, y, group): # x = pos_x do mob / y = pos_y do mob / group = items_group(heart)
    chance = random.random() # 0 a 1.0

    if chance < DROP_CHANCE_HEART: # drop_chance_heart_random 0.3
        new_heart = Heart(x, y)
        group.add(new_heart)
        return True
    return False

def ice_spawn(x, y, group): # x = pos_x do mob / y = pos_y do mob / group = items_group(heart)
    chance = random.random() # 0 a 1.0
    if chance > 0.3 and chance <= 0.5: 
        new_snowflake = Ice(x, y)
        group.add(new_snowflake)
        return True
    return False

def spawn_tooth(x, y, group): #
    new_tooth = Tooth(x, y)
    group.add(new_tooth)


def spawn_random_cage(screen_width, screen_height, group): # largura e altura da tela e items_group()

    min_x = 100 # margem mínima (px)
    min_y = 100 # margem mínima (px)
    max_x = screen_width - 100
    max_y = screen_height - 100

    #Disposição aleatória de nasciemnto da cage
    
    x = random.randint(min_x, max_x)
    y = random.randint(min_y, max_y)

    new_cage = Cage(x,y)
    group.add(new_cage)