import pygame
import math # efeito de flutuar uso do seno
import random


drop_chance_heart_random = 0.3 # 10% de chance de dropar coração dos mobs

# pensar em como fazer para que eles spawnem(talvez em algum tempo determinado)
class Tooth(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        try:
            original_image = pygame.image.load('../assets/images/items/dente.jpeg').convert_alpha()
            #Se a imagem for muito grande, ela fica escalada em (32,32)
            self.image = pygame.transform.scale(original_image, (32, 32)) 

        except FileNotFoundError:
            print("ERRO: Imagem do dente não encontrada.")
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 255, 255)) # uma imagem em branco

        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Pontuação do tooth
        self.score_value += 100 # player.score += tooth.score_value na main
        
        # Para animação de flutuar
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
            original_image = pygame.image.load('../assets/images/items/coracao.jpeg').convert_alpha() #convert_alpha() deixa a imagem transaprente
            self.image = pygame.transform.scale(original_image, (32, 32))

        except FileNotFoundError:
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 0, 0)) # Vermelho se não achar imagem

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        self.heal_value = 20  # vida recuperada // player.hp += heart.heal_value
        
        # Animação
        self.y_start = y
        self.timer = 0

    def update(self):
        self.timer += 0.15 # Coração bate/flutua um pouco mais rápido
        offset = math.sin(self.timer) * 3
        self.rect.centery = self.y_start + offset

class Cage(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # Carregar a imagem da gaiola
        try:
            original_image = pygame.image.load('../assets/images/items/cage.png').convert_alpha()
            self.image = pygame.transform.scale(original_image, (48, 48)) # A gaiola tem um tamanho maior que os coletáveis, porque faz sentido

        except FileNotFoundError:
            # Se não carregar a gaiola, gera uma imagem cinzenta pra representa a gaiola com um x pra parecer fechada
            self.image = pygame.Surface((48, 48))
            self.image.fill((169, 169, 169)) # cor DarkGray
            pygame.draw.line(self.image, (0, 0, 0), (0, 0), (48, 48), 3) # desenho de uma diagonal do x
            pygame.draw.line(self.image, (0, 0, 0), (48, 0), (0, 48), 3) # desenho da outra diagonal do x

        # Posicionamento da gaiola
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # Atributos da giaola
        self.health = 60 # O dano de ataque é 20, então a gaiola pode tomar 3 hits

    def take_damage(self): # função de dano tomado da cage
        if self.health <= 0:
            self.kill()
            return True # Retorna True para avisar que a gaiola foi destruída
        return False
    
class Ice():
    def __init__(self, x, y):
        super().__init__()
        
        try:
            original_image = pygame.image.load('../assets/images/items/floco_neve.jpeg').convert_alpha()
            self.image = pygame.transform.scale(original_image, (32, 32)) 

        except FileNotFoundError:
            print("ERRO: Imagem do floco de neve não encontrada.")
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 255, 255)) # uma imagem em branco

        
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Buff na move_speed
        self.boost_multiplier = 1.2 # multiplicador da velocidade * 1.2
        self.duration = 15000 # 15 segundos de duração o efeito
        
        # Para animação de flutuar
        self.y_start = y
        self.timer = 0

    def update(self):
        # Efeito de flutuar (Senoide)
        self.timer += 0.1
        offset = math.sin(self.timer) * 5  
        self.rect.centery = self.y_start + offset

# funções de spawn

#spawn do coração
def try_spawn_heart(x, y, group): # x = pos_x do mob / y = pos_y do mob / group = items_group(heart)
    chance = random.random() # 0 a 1.0

    if chance < drop_chance_heart_random: # drop_chance_heart_random 0.3
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
