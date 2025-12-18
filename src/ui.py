from . import config as cfg
import pygame

# CLASSE: Barra de Vida
class BarraVida:
    def __init__(self, x, y, largura, altura, vida_maxima):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.vida_maxima = vida_maxima

    def desenhar(self, surface, vida_atual):
        # Garante que a vida não seja negativa para o desenho
        if vida_atual < 0:
            vida_atual = 0
            
        # Calcula a proporção (0.0 a 1.0)
        ratio = vida_atual / self.vida_maxima
        
        # Define os retângulos
        bg_rect = pygame.Rect(self.x, self.y, self.largura, self.altura)
        vida_rect = pygame.Rect(self.x, self.y, self.largura * ratio, self.altura)

        # 1. Fundo (Vermelho/Dano)
        pygame.draw.rect(surface, cfg.RED, bg_rect)
        
        # 2. Vida Atual (Verde)
        pygame.draw.rect(surface, cfg.GREEN, vida_rect)
        
        # 3. Borda (Branca) - espessura 2
        pygame.draw.rect(surface, cfg.WHITE, bg_rect, 2)

# CLASSE Temporizador

class Temporizador:

    def __init__(self, x, y):
        self.start_ticks = pygame.time.get_ticks()
        
        # Configuração Visual
        self.fonte = pygame.font.SysFont("Consolas", 32, bold=True)
        self.x = x
        self.y = y
        self.texto_atual = "00:00"

    def atualizar(self):
        # Calcula quanto tempo passou desde o início (em milissegundos)
        tempo_decorrido_ms = pygame.time.get_ticks() - self.start_ticks
        
        # Matemática do relógio (Conversão de ms para min:seg)
        segundos_totais = tempo_decorrido_ms // 1000
        minutos = segundos_totais // 60
        segundos = segundos_totais % 60
        
        # Formata o texto
        self.texto_atual = f"{minutos:02}:{segundos:02}"

    def desenhar(self, surface):
        cor_texto = cfg.WHITE
            
        superficie_texto = self.fonte.render(self.texto_atual, True, cor_texto)
        
        # Posiciona o texto (topright)
        rect_texto = superficie_texto.get_rect()
        rect_texto.topright = (self.x, self.y)
        
        surface.blit(superficie_texto, rect_texto)
