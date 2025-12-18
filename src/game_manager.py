import random
import pygame
from . import config as cfg
from src.enemies.common import SpiritEnemy
from .player import Player
from .ui import BarraVida, Temporizador, ContadorDentes, ContadorEstrela 
from .collectibles import Cage, Tooth, Heart, Ice, DROP_CHANCE_HEART, DROP_CHANCE_ICE
from src.enemies.boss import BossBreu, BossProjectile

class GameManager:
    
    def __init__(self, screen):
        
        self.screen = screen
        
        self.bg_image = pygame.image.load("assets/images/itens_menu/background.png").convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (cfg.WIDTH, cfg.HEIGHT))
        
        self.font_medium = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_large = pygame.font.SysFont("Arial", 64, bold=True)
        
        self.reset()
        
    def reset(self):
        self.paused = False
        self.game_over = False
        self.game_won = False 
        
        self.score = 0
        self.final_time_text = "00:00"

        self.teeth_collected = 0
        self.teeth_goal = 5
        self.boss_spawned = False
        self.time_min = 5 * 60
        
        self.last_cage_spawn = pygame.time.get_ticks()
        self.cage_spawn_interval = 10000 # Spawna gaiola a cada 100 seg (exemplo)
        
        self.last_increment = pygame.time.get_ticks()
        self.increment_dificult = cfg.AUMENTO_DIFICULDADE # 2 min
        self.tempo_boss = cfg.TIMER
        self.spawn_count = cfg.INIMIGOS_LIMITE
                
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.cages = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.boss_projectiles = pygame.sprite.Group()
        
        self.player = Player((cfg.WIDTH // 2, cfg.HEIGHT // 2), self.all_sprites, self.projectiles)
        
        vida_inicial = self.player.health
        self.health_bar = BarraVida(20, 20, 200, 20, vida_inicial)
        self.timer = Temporizador(cfg.WIDTH - 20, 20)
        self.teeth_ui = ContadorDentes(20, 110)
        self.score_ui = ContadorEstrela(20, 50)
        
        # Controles do menu de pausa
        self.pause_options = ["Continuar", "Menu Principal"]
        self.gameover_options = ["Menu Principal"] 
        self.pause_index = 0
    
    
    # "Desenha" na tela os objetos de inimigos, jogador...
    def draw(self):
        
        self.screen.blit(self.bg_image, (0, 0))
        
        if self.boss_spawned:
            self.boss_projectiles.draw(self.screen)
        
        self.health_bar.desenhar(self.screen, self.player.health)
        self.timer.desenhar(self.screen)
        self.teeth_ui.desenhar(self.screen, self.teeth_goal)
        self.score_ui.desenhar(self.screen)
        
        self.cages.draw(self.screen)
        self.collectibles.draw(self.screen)
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            self.draw_pause_overlay()
            
        elif self.game_over:
            self.draw_gameover_overlay()
            
        elif self.game_won:
            self.draw_victory_overlay()
    
    
    # TEMPLATE
    def draw_text(self, text, font, x, y, color=(255, 255, 255)):
        surf = font.render(text, True, color)
        rect = surf.get_rect(center=(x, y))
        self.screen.blit(surf, rect)
    
    
    # TEMPLATE
    def draw_pause_overlay(self):
    
        overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
        overlay.set_alpha(128) 
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0,0))
        
        self.draw_text("PAUSE", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT//2 - 50)
        
        # Desenha as opções
        for i, option in enumerate(self.pause_options):
            color = (255, 255, 0) if i == self.pause_index else (255, 255, 255)
            self.draw_text(option, self.font_large, cfg.WIDTH//2, cfg.HEIGHT//2 + 20 + (i * 40), color)
        
    
    # TEMPLATE
    def draw_gameover_overlay(self):
        
        overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((50, 0, 0)) # Tom avermelhado para morte
        self.screen.blit(overlay, (0,0))

        # Títulos e Pontos
        self.draw_text("GAME OVER", self.font_large, cfg.WIDTH//2, cfg.HEIGHT//4)
        self.draw_text(f"Pontos: {self.score}", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT//2 - 20)
        self.draw_text(f"Tempo Vivo: {self.final_score_text}", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT//2 + 20)

        # Botão Selecionado
        cor = (255, 255, 0) # Amarelo para destaque
        self.draw_text("> Voltar ao Menu <", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT * 0.75, cor)
    
    
    # TEMPLATE
    def draw_victory_overlay(self):
        overlay = pygame.Surface((cfg.WIDTH, cfg.HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 50, 0)) # Verde escuro
        self.screen.blit(overlay, (0,0))
        self.draw_text("VICTORY!", self.font_large, cfg.WIDTH//2, cfg.HEIGHT//4)
        self.draw_text(f"Boss Defeated!", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT//2)
        self.draw_text("> Voltar ao Menu <", self.font_medium, cfg.WIDTH//2, cfg.HEIGHT * 0.75, (255,255,0))
    
    
    # Lida com as ações dentro do pause interno
    def pause_or_gameover(self, event):
        
        is_endgame = self.game_over or self.game_won
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
                
                elif is_endgame:
                    return "MENU"
            
        return None
    
    
    def spawn_boss(self):
        # Limpa o mapa
        self.enemies.empty() 
        self.cages.empty()
        self.collectibles.empty()
        
        # Remove do all_sprites o que não é player ou projetil do player
        for sprite in self.all_sprites:
            if sprite != self.player and sprite not in self.projectiles:
                sprite.kill()
        
        # Spawna Boss no meio
        boss = BossBreu(pygame.Vector2(cfg.WIDTH // 2, 100))
        boss.set_projectile_group(self.boss_projectiles) 
        
        self.all_sprites.add(boss)
        self.enemies.add(boss) 
        
        self.boss_spawned = True
    
    
    def spawn_enemies(self):
        
        # Sem inimigos quando boss spawna
        if self.boss_spawned: return

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


    def spawn_cages(self):
        
        if self.boss_spawned: return
        
        now = pygame.time.get_ticks()
        if now - self.last_cage_spawn > self.cage_spawn_interval and len(self.cages) < 3:
            x = random.randint(100, cfg.WIDTH - 100)
            y = random.randint(100, cfg.HEIGHT - 100)
            cage = Cage(x, y)
            self.cages.add(cage) 
            self.last_cage_spawn = now
    
    
    def check_collisions(self):

        # Isso retorna um dict - recebe dois grupos, e diz que a bala deve sumir após colisão
        projectiles_hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, False, True)

        """
        {"Nome Inimigo": num_balas, ...}
        """

        for enemy in projectiles_hits:
            enemy.take_damage(10)

            if enemy.health <= 10:
                enemy.die()
                
            if not enemy.alive:
                self.score += 10
                self.score_ui.atualizar_valor(self.score)
                
                if isinstance(enemy, BossBreu):
                    self.game_won = True
                    self.final_score_text = self.timer.texto_atual
                
                else:
                    roll = random.random()
                    if roll < DROP_CHANCE_HEART:
                        self.collectibles.add(Heart(enemy.pos.x, enemy.pos.y))
                    elif roll < DROP_CHANCE_HEART + DROP_CHANCE_ICE:
                        self.collectibles.add(Ice(enemy.pos.x, enemy.pos.y))


        enemies_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)

        if enemies_hits:

            damage = enemies_hits[0].stats.damage
            self.player.take_damage(damage)
            
            if self.player.health <= 0: 
                self.game_over = True
                self.final_score_text = self.timer.texto_atual 
        
        
        cage_hits = pygame.sprite.groupcollide(self.cages, self.projectiles, False, True)
        
        for cage in cage_hits:

            if cage.take_damage(10): 
                tooth = Tooth(cage.rect.centerx, cage.rect.centery)
                self.collectibles.add(tooth)
        
        
        items_collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        
        for item in items_collected:
            if isinstance(item, Heart):
                self.player.health = min(self.player.health + item.heal_value, self.player.max_health)
            
            elif isinstance(item, Ice):
                self.player.apply_speed_boost(item.boost_multiplier, item.duration)
                
            elif isinstance(item, Tooth):
                self.score += item.score_value
                self.score_ui.atualizar_valor(self.score)
                self.teeth_collected += 1
                self.teeth_ui.adicionar(1)
                
        if self.boss_spawned:
            boss_hits = pygame.sprite.spritecollide(self.player, self.boss_projectiles, True)
            
            if boss_hits:
                self.player.take_damage(25)
                if self.player.health <= 0:
                     self.game_over = True
                     self.final_score_text = self.timer.texto_atual
                

    def control_dificult(self):
    
        if self.boss_spawned: return
    
        time_now = pygame.time.get_ticks()

        if time_now - self.last_increment > self.increment_dificult:

            self.spawn_count += 2
            self.last_increment = time_now


    # Atualiza os frames do jogo
    def update(self, dt):
        
        for event in pygame.event.get():
            
            # Esse event é o de clicar no botão de fechar a janela do jogo (envia para o main.py)
            if event.type == pygame.QUIT:
                return "QUIT"
            
            if event.type == pygame.KEYDOWN:
                
                if not self.game_over:
                    
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused
                        self.pause_index = 0
                        
                if self.paused or self.game_over or self.game_won:
                    
                    menu_selection = self.pause_or_gameover(event)
                    
                    # Se retornar alguma coisa, envia esse retorno para o Main
                    if menu_selection:
                        return menu_selection
                    
        if not self.paused and not self.game_over:
            
            self.timer.atualizar(dt)
            
            time_elapsed = self.timer.get_seconds()
            
            if not self.boss_spawned:

                if time_elapsed >= self.time_min:
                    if self.teeth_collected >= self.teeth_goal:
                        self.spawn_boss()
            
            self.control_dificult()
            self.spawn_enemies()
            self.spawn_cages()
            
            self.player.update(self.cages)
            self.enemies.update(dt, self.player, None)
            self.projectiles.update()
            
            if self.boss_spawned:
                self.boss_projectiles.update()
            
            self.collectibles.update() 
            self.check_collisions()
            
        self.draw()