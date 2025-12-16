import sys
import pygame
from . import config as cfg

class GameManager:
    
    def __init__(self, screen):
        
        self.screen = screen
        self.paused = False
        self.running = True
        
        self.score = 0

        self.last_increment = pygame.time.get_ticks()
        self.increment_dificult = 120000 # 2 min em milisegundos

        self.tempo_boss = cfg.TIMER
        self.spawn_count = cfg.INIMIGOS_INICIAS
                
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        
        # self.jogador = Jack()  # Construção do objeto jogador (img e caixa de colisão)
        self.all_sprites.add(self.jogador)
        
        # Controles do menu de pausa
        # self.pause_options = ["Continuar", "Sair para o Menu"]
        # self.pause_index = 0
    
    
    # "Desenha" na tela os objetos de inimigos, jogador...
    def draw(self):
        self.all_sprites.draw(self.screen)
        
        if self.paused:
            self.draw_pause_overlay()
    
    
    def draw_pause_overlay(self):
    
        overlay = pygame.Surface(self.screen.get_width(), self.screen.get_height()) # Só para criar a "tela" sobreposta
        # COMPLETAR
    
    
    # Lida com as ações dentro do pause interno
    def events_pause(self, event):
        
        if event.type == pygame.KEYDOWN:
            
            # Seleciona o botão com as setas
            if event.key == pygame.K_UP:
                self.pause_index = (self.pause_index - 1) % len(self.pause_options)
            
            elif event.key == pygame.K_DOWN:
                self.pause_index = (self.pause_index + 1) % len(self.pause_options)
                
            # Aperta o botão com o enter
            elif event.key == pygame.K_RETURN:
                
                if self.pause_index == 0: # Tem que colocar o índice correspondente a posição na lista de opçõe
                    self.paused = False 
                
                elif self.pause_index == 1:
                    self.running = False

                # Adicionar botão para silenciar músicas, e outro para silecias sfx        

    
    def check_collisions(self):

        # Isso retorna um dict - recebe dois grupos, e diz que a bala deve sumir após colisão
        hits_player = pygame.sprite.groupcollide(self.enemies, self.bullets, False, True)

        """
        {"Nome Inimigo": num_balas, ...}
        """

        for enemy in hits_player:

            for bullet in hits_player[enemy]:
                enemy.hp -= 10

            if enemy.hp <= 10:
                enemy.kill()
                self.score += 100


        hits_enemies = pygame.sprite.groupcollid(self.player, self.enemies, False)

        if hits_enemies: # Adicionar invencibilidade?

            self.player.health -= 1
            
            if self.player.health <= 0:
                self.running = False


    def spawn_inimigos(self):

        if len(self.enemies) < self.spawn_count:

            # Construção do inimigo
            # enemy = Enemy()  
            # self.all_sprites.add(enemy)
            # self.enemies.add(enemy)
            pass


    def shoot(self):
        
        # Construção da bala
        # bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
        # self.all_sprites.add(bullet)
        # self.bullets.add(bullet)
        pass


    def control_dificult(self):
    
        time_now = pygame.time.get_ticks()

        if time_now - self.last_increment > self.increment_dificult:

            self.spawn_count += 2
            self.increment_dificult = time_now


    # Atualiza os frames do jogo
    def update(self):
        
        # Fora do menu de pause interno
        if not self.paused:
            
            self.control_dificult()
            self.spawn_enemies()
            self.all_sprites.update()
            self.check_collisions()
            
        # Jogo no pause interno
        else:
            self.update_pause_menu()


    def run_loop(self):
        
        for event in pygame.event.get():
            
            # Esse event é o de clicar no botão de fechar a janela do jogo (não é tão indicado)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if not self.paused:
                # Esse é avaliado toda vez que uma tecla é apertada
                if event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_SPACE:
                        self.shoot()
                    
                    if event.key == pygame.K_ESCAPE:
                        self.paused = True

        self.update()
        self.draw()
        
        if not self.running:
            return "back_menu"