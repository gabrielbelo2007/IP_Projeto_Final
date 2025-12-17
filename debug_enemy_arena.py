import sys
import pygame

from src.config import WIDTH, HEIGHT, FPS
from src.enemies.common import SpiritEnemy, RangedKnightEnemy, HorseEnemy


class PlayerDummy:
    def __init__(self, x: float, y: float):
        self.pos = pygame.Vector2(x, y)
        self.speed = 220.0
        self.radius = 14
        self.max_health = 100
        self.health = 100

    def take_damage(self, amount: int) -> None:
        self.health -= int(amount)
        self.health = max(0, self.health)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        move = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            move.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            move.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            move.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            move.x += 1

        if move.length_squared() > 0:
            move = move.normalize()

        self.pos += move * self.speed * dt

        # manter dentro da tela
        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, (120, 200, 255), (int(self.pos.x), int(self.pos.y)), self.radius)
    
    def attack(self, enemies: list) -> None:
        """
        Ataque simples MVP:
        - Clique esquerdo do mouse
        - Dano em inimigos dentro de um raio
        """
        mouse_buttons = pygame.mouse.get_pressed()
        if not mouse_buttons[0]:
            return

        attack_range = 36
        attack_damage = 20

        for e in enemies:
            if not e.alive:
                continue

            dist = (e.pos - self.pos).length()
            if dist <= attack_range:
                e.take_damage(attack_damage)



def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("DEBUG ARENA - Inimigos")
    clock = pygame.time.Clock()

    player = PlayerDummy(WIDTH / 2, HEIGHT / 2)

    enemies = [
        SpiritEnemy(pygame.Vector2(120, 120)),
        RangedKnightEnemy(pygame.Vector2(WIDTH - 120, 120)),
        HorseEnemy(pygame.Vector2(WIDTH / 2, HEIGHT - 120)),
    ]

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        player.update(dt)
        player.attack(enemies)


        # update inimigos
        for e in enemies:
            e.update(dt, player)

        # desenhar
        screen.fill((20, 20, 20))
        player.draw(screen)
        for e in enemies:
            e.draw(screen)

        # HUD simples no título
        pygame.display.set_caption(f"DEBUG ARENA - HP Player: {player.health}/{player.max_health}")

        pygame.display.flip()

        # condição de “morte” do teste
        if player.health <= 0:
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
