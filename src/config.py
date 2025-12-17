# --- Configurações Gerais ---
TITLE = "Jack's Nightmare"
WIDTH = 1280  # Largura da tela
HEIGHT = 720  # Altura da tela
FPS = 60      # Frames por segundo
TIMER = 480 # Tempo minímo para liberar o boss
INIMIGOS_LIMITE = 5
AUMENTO_DIFICULDADE = 120000

# --- Cores (Padrão RGB) ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255) # Cor do Gelo/Jack

# --- Configurações do Jogador ---
PLAYER_SPEED = 5
PLAYER_START_HEALTH = 100

# --- Camadas (Z-Index) ---
# Isso ajuda a desenhar coisas na ordem certa (chão embaixo, player em cima)
LAYER_BACKGROUND = 0
LAYER_ITEMS = 1
LAYER_MAIN = 2 # Player e Inimigos
LAYER_UI = 3


# ==========================================
# CONFIGURAÇÕES DO JOGADOR (Área do P3)
# ==========================================
# P3, escreva suas variáveis aqui embaixo...

#tamanho do jack na tela (quadrado de 40x40 pixels)
PLAYER_WIDTH = 40        #largura do jack em pixels
PLAYER_HEIGHT = 40       #altura do jack em pixels

#cor usada para desenhar o jack na tela
PLAYER_COLOR = CYAN      #reaproveita a cor CYAN

#vida maximado do jack
PLAYER_MAX_HEALTH = PLAYER_START_HEALTH  #usa o mesmo valor da vida inicial

#quanto tempo o jack fica invencivel apos levar dano (em milisegundos)
PLAYER_INVINCIBILITY_TIME = 1000  #1s de "i-frame"

#tempo mínimo entre dois tiros (em milisegundos)
SHOOT_COOLDOWN = 300  #0.3s entre tiros

#configurações do projétil (bola de gelo)
PROJECTILE_SIZE = 8        #largura\altura do projétil
PROJECTILE_SPEED = 15      #velocidade do projétil
PROJECTILE_COLOR = (180, 230, 255)   #cor dor tiro (azul claro)

# ==========================================
# CONFIGURAÇÕES DE INIMIGOS (Área do P2)
# ==========================================
# P2, escreva suas variáveis aqui embaixo...



# ==========================================
# CONFIGURAÇÕES DE UI E ITENS (Área do P4 e Designers)
# ==========================================
# P4, escreva suas variáveis aqui embaixo...