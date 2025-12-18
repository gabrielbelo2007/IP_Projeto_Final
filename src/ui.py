from . import config as cfg
import pygame

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


class Temporizador:

    def __init__(self, x, y):
        
        self.total_time = 0
        
        # Configuração Visual
        self.fonte = pygame.font.SysFont("Consolas", 32, bold=True)
        self.x = x
        self.y = y
        self.texto_atual = "00:00"

    def atualizar(self, dt):
        # Calcula quanto tempo passou desde o início (em milissegundos)
        self.total_time += dt * 1000
        
        # Matemática do relógio (Conversão de ms para min:seg)
        segundos_totais = int(self.total_time // 1000)
        minutos = segundos_totais // 60
        segundos = segundos_totais % 60
        
        # Formata o texto
        self.texto_atual = f"{minutos:02}:{segundos:02}"

    def get_seconds(self):
        return self.total_time / 1000.0

    def desenhar(self, surface):
        cor_texto = cfg.WHITE
            
        superficie_texto = self.fonte.render(self.texto_atual, True, cor_texto)
        
        # Posiciona o texto (topright)
        rect_texto = superficie_texto.get_rect()
        rect_texto.topright = (self.x, self.y)
        
        surface.blit(superficie_texto, rect_texto)
        
class ContadorDentes:

    def __init__(self, x, y):
        self.quantidade = 0
        self.x = x
        self.y = y
        
        img_original = pygame.image.load("assets/images/itens/dentinho.png").convert_alpha()
        self.icone = pygame.transform.scale(img_original, (32, 32))
        
        #configuração visual
        self.fonte = pygame.font.SysFont("Consolas", 24, bold=True)
        self.padding = 10
        self.bg_color = (50, 50, 50) 
        self.border_color = cfg.WHITE
        
    def adicionar(self, valor=1):
        self.quantidade += valor

    def desenhar(self, surface, meta=3):
        
        cor_texto = cfg.WHITE
        if self.quantidade >= meta:
            cor_texto = (255, 255, 0) # Amarelo se completou
        
        texto_surf = self.fonte.render(f" {self.quantidade}/{meta}", True, cor_texto)
        
        # Cálculos de tamanho para o fundo cinza
        largura_icone = self.icone.get_width()
        largura_texto = texto_surf.get_width()
        altura_conteudo = max(self.icone.get_height(), texto_surf.get_height())
        
        largura_total = largura_icone + largura_texto + (self.padding * 3) + 5
        altura_total = altura_conteudo + (self.padding * 2)
        
        rect_fundo = pygame.Rect(self.x, self.y, largura_total, altura_total)

        #Fundo e Borda
        pygame.draw.rect(surface, self.bg_color, rect_fundo, border_radius=8)
        pygame.draw.rect(surface, self.border_color, rect_fundo, 2, border_radius=8)

        # icone (dentinho.png)
        pos_y_icone = self.y + (altura_total - self.icone.get_height()) // 2
        surface.blit(self.icone, (self.x + self.padding, pos_y_icone))
        
        # Desenha Texto
        pos_x_texto = self.x + self.padding + largura_icone + 5
        pos_y_texto = self.y + (altura_total - texto_surf.get_height()) // 2
        surface.blit(texto_surf, (pos_x_texto, pos_y_texto))

class ContadorEstrela:

    def __init__(self, x, y):
        self.quantidade = 0
        self.x = x
        self.y = y
        
        img_original = pygame.image.load("assets/images/itens_menu/estrela.png").convert_alpha()
        self.icone = pygame.transform.scale(img_original, (32, 32))
            
        #configuração visual
        self.fonte = pygame.font.SysFont("Consolas", 24, bold=True)
        self.padding = 10
        self.bg_color = (50, 50, 50) 
        self.border_color = cfg.WHITE
        
    def atualizar_valor(self, valor):
        self.quantidade = valor

    def desenhar(self, surface):
        
        texto_surf = self.fonte.render(f" {self.quantidade}", True, cfg.WHITE)
        
        # Cálculos de tamanho para o fundo cinza
        largura_icone = self.icone.get_width()
        largura_texto = texto_surf.get_width()
        altura_conteudo = max(self.icone.get_height(), texto_surf.get_height())
        
        largura_total = largura_icone + largura_texto + (self.padding * 3) + 5
        altura_total = altura_conteudo + (self.padding * 2)
        
        rect_fundo = pygame.Rect(self.x, self.y, largura_total, altura_total)

        #Fundo e Borda
        pygame.draw.rect(surface, self.bg_color, rect_fundo, border_radius=8)
        pygame.draw.rect(surface, self.border_color, rect_fundo, 2, border_radius=8)

        # icone (dentinho.png)
        pos_y_icone = self.y + (altura_total - self.icone.get_height()) // 2
        surface.blit(self.icone, (self.x + self.padding, pos_y_icone))
        
        # Desenha Texto
        pos_x_texto = self.x + self.padding + largura_icone + 5
        pos_y_texto = self.y + (altura_total - texto_surf.get_height()) // 2
        surface.blit(texto_surf, (pos_x_texto, pos_y_texto))