# --- Configurações Gerais ---
TITLE = "Guardiões: O CInverno das Sombras"
WIDTH = 1280  # Largura da tela
HEIGHT = 720  # Altura da tela
FPS = 60      # Frames por segundo
TIMER = 480 # Tempo minímo para liberar o boss
INIMIGOS_LIMITE = 5
AUMENTO_DIFICULDADE = 40000

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
LAYER_BACKGROUND = 0
LAYER_ITEMS = 1
LAYER_MAIN = 2 # Player e Inimigos
LAYER_UI = 3


# ==========================================
# CONFIGURAÇÕES DO JOGADOR (Área do P3)
# ==========================================
# P3, escreva suas variáveis aqui embaixo...

#tamanho do jack na tela (quadrado de 40x40 pixels)
PLAYER_WIDTH = 70        #largura do jack em pixels
PLAYER_HEIGHT = 70       #altura do jack em pixels

#cor usada para desenhar o jack na tela
PLAYER_COLOR = CYAN      #reaproveita a cor CYAN

#vida maximado do jack
PLAYER_MAX_HEALTH = PLAYER_START_HEALTH  #usa o mesmo valor da vida inicial

#quanto tempo o jack fica invencivel apos levar dano (em milisegundos)
PLAYER_INVINCIBILITY_TIME = 1000  #1s de "i-frame"

#tempo mínimo entre dois tiros (em milisegundos)
SHOOT_COOLDOWN = 400  #0.4s entre tiros

#configurações do projétil (bola de gelo)
PROJECTILE_SIZE = 10        #largura\altura do projétil
PROJECTILE_SPEED = 15      #velocidade do projétil
PROJECTILE_COLOR = (180, 230, 255)   #cor dor tiro (azul claro)

# ==========================================
# CONFIGURAÇÕES DE INIMIGOS (Área do P2)
# ==========================================
# P2, escreva suas variáveis aqui embaixo...



# ==========================================
# CONFIGURAÇÕES DE UI E ITENS (Área do P4 e Designers)
# ==========================================

BTN_JOGAR = 'botao_jogar.png'
HOVER_JOGAR = 'hover_jogar.png'
BTN_SAIR = 'botao_sair.png'
HOVER_SAIR = 'hover_sair.png'
BACKGROUND_MENU = 'background_menu.png'
LOGO_MENU = 'logo_menu.png'

BLUE_BACKGROUND = (30, 30, 30)

BACKGROUND_PAUSE = 'background_pausa.png'
BTN_CONTINUAR = 'continuar_jogando.png'
HOVER_CONTINUAR = 'hover_continuar.png'
BTN_VOLTAR = 'voltar_menu.png'
HOVER_VOLTAR = 'hover_voltar.png'

GAMEOVER = 'game_over.png'
VITORIA = 'vitoria.png'