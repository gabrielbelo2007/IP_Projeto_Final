import random
import pygame
from . import config as cfg
from src.enemies.common import SpiritEnemy
from .player import Player

class GameManager:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.reset()
        
    def reset(self):
        self.paused = False
        self.game_over = False
        
        self.score = 0

        self.start_time = pygame.time.get_ticks()
        
        self.last_increment = pygame.time.get_ticks()
        self.increment_dificult = cfg.AUMENTO_DIFICULDADE # 2 min
        self.tempo_boss = cfg.TIMER
        self.spawn_count = cfg.INIMIGOS_LIMITE
                
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        
        self.player = Player((cfg.WIDTH // 2, cfg.HEIGHT // 2), self.all_sprites, self.projectiles)
        
        # Controles do menu de pausa
        self.pause_options = ["Continuar", "Menu Principal"]
        self.gameover_options = ["Menu Principal"] 
        self.pause_index = 0
    
    
    # "Desenha" na tela os objetos de inimigos, jogador...
    def draw(self):
        
        self.screen.fill((0, 0, 0))
        
        # AQUI FICA A UI TAMBÉM
        
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            self.draw_pause_overlay()
            
        elif self.game_over:
            self.draw_gameover_overlay()
        
    
    # TEMPLATE
    def draw_pause_overlay(self):
    
        overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
        overlay.set_alpha(128) 
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        self.draw_text("PAUSE", 50, cfg.WIDTH//2, cfg.HEIGHT//2 - 50)
        
        # Desenha as opções
        for i, option in enumerate(self.pause_options):
            color = (255, 255, 0) if i == self.pause_index else (255, 255, 255)
            self.draw_text(option, 30, cfg.WIDTH//2, cfg.HEIGHT//2 + 20 + (i * 40), color)
        
    
    # TEMPLATE
    def draw_gameover_overlay(self):
        
        overlay = pygame.Surface(self.screen.get_width(), self.screen.get_height())
        overlay.set_alpha(200)
        overlay.fill((50, 0, 0)) # Tom avermelhado para morte
        self.screen.blit(overlay, (0,0))

        # Títulos e Pontos
        self.draw_text("GAME OVER", 64, cfg.WIDTH//2, cfg.HEIGHT//4)
        self.draw_text(f"Pontos: {self.score}", 32, cfg.WIDTH//2, cfg.HEIGHT//2 - 20)
        self.draw_text(f"Tempo: {self.total_time}s", 32, cfg.WIDTH//2, cfg.HEIGHT//2 + 20)

        # Botão Selecionado
        cor = (255, 255, 0) # Amarelo para destaque
        self.draw_text("> Voltar ao Menu <", 40, cfg.WIDTH//2, cfg.HEIGHT * 0.75, cor)
    
    
    # TEMPLATE
    def draw_text(self, text, size, x, y, color=(255, 255, 255)):
        font = pygame.font.SysFont("Arial", size, bold=True)
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
    
    
    # Lida com as ações dentro do pause interno
    def pause_or_gameover(self, event):
        
        current_options = self.pause_options if self.paused else self.gameover_options
        
        if event.type == pygame.KEYDOWN:
            
            # Seleciona o botão com as setas
            if event.key == pygame.K_UP:
                self.pause_index = (self.pause_index - 1) % len(current_options)
            
            elif event.key == pygame.K_DOWN:
                self.pause_index = (self.pause_index + 1) % len(current_options)
                
            # Aperta o botão com o enter
            elif event.key == pygame.K_RETURN:
                
                if self.paused:
                    if self.pause_index == 0: # O índice correspondente a posição na lista de opções
                        self.paused = False 
                    
                    elif self.pause_index == 1:
                        return "MENU"
                
                elif self.game_over:
                    return "MENU"
            
        return None
    
    
    def spawn_enemies(self):

        if len(self.enemies) < self.spawn_count:

            side = random.choice(["top", "bottom", "left", "right"])
            
            if side == 'top':
                pos = pygame.Vector2(random.randint(0, cfg.WIDTH), -50)
            elif side == 'bottom':
                pos = pygame.Vector2(random.randint(0, cfg.WIDTH), cfg.HEIGHT + 50)
            elif side == 'left':
                pos = pygame.Vector2(-50, random.randint(0, cfg.HEIGHT))
            else:
                pos = pygame.Vector2(cfg.WIDTH + 50, random.randint(0, cfg.HEIGHT))
            
            enemy = SpiritEnemy(pos)
            
            self.all_sprites.add(enemy)
            self.enemies.add(enemy)

    
    def check_collisions(self):

        # Isso retorna um dict - recebe dois grupos, e diz que a bala deve sumir após colisão
        projectiles_hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)

        """
        {"Nome Inimigo": num_balas, ...}
        """

        for enemy in projectiles_hits:
            enemy.take_damage(10)

            if enemy.hp <= 10:
                enemy.die()
                self.score += 10


        enemies_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)

        if enemies_hits:

            self.player.health -= enemies_hits[0].stats.damage
            
            if self.player.health <= 0:
                self.game_over = True
                self.total_time = (pygame.time.get_ticks() - self.start_ticks) // 1000
                

    def control_dificult(self):
    
        time_now = pygame.time.get_ticks()

        if time_now - self.last_increment > self.increment_dificult:

            self.spawn_count += 2
            self.increment_dificult = time_now


    # Atualiza os frames do jogo
    def update(self, dt):
        
        for event in pygame.event.get():
            
            # Esse event é o de clicar no botão de fechar a janela do jogo (envia para o main.py)
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                
                if not self.game_over:
                    
                    if event.key == pygame.K_SPACE:
                        self.player.shoot()
                    
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        self.pause_index = 0
                        
                if self.paused or self.game_over:
                    
                    menu_selection = self.pause_or_gameover(event)
                    
                    # Se retornar alguma coisa, envia esse retorno para o Main
                    if menu_selection:
                        return menu_selection
                    
        if not self.paused and not self.game_over:
            
            self.control_dificult()
            self.spawn_enemies()
            
            self.player.update()
            self.enemies.update(dt, self.player, None)
            self.projectiles.update()
            
            self.check_collisions()
            
        # Jogo no pause interno
        else:
            self.update_pause_menu()
            
        self.draw()