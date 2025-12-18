import sys
import pygame

from src.config import WIDTH, HEIGHT, FPS
from src.enemies.boss import BossBreu
from src.enemies.common import SpiritEnemy, RangedKnightEnemy, HorseEnemy


# Player (debug)
PLAYER_RADIUS = 14
PLAYER_SPEED = 220.0
PLAYER_MAX_HEALTH = 100

# Melee (debug)
MELEE_RANGE = 36.0
MELEE_DAMAGE = 20


class PlayerDummy:
    # Player mínimo pra arena

    def __init__(self, pos: pygame.Vector2):
        self.pos = pygame.Vector2(pos)
        self.radius = PLAYER_RADIUS
        self.speed = PLAYER_SPEED
        self.max_health = PLAYER_MAX_HEALTH
        self.health = PLAYER_MAX_HEALTH

    def take_damage(self, amount: int) -> None:
        # Aplica dano
        self.health = max(0, self.health - int(amount))

    def update(self, dt: float) -> None:
        # Move e limita na tela
        move_dir = self._read_movement()
        self.pos += move_dir * self.speed * dt
        self._clamp_to_screen()

    def melee_attack(self, enemies: list) -> None:
        # Clique esquerdo: dano curto em área
        if not pygame.mouse.get_pressed()[0]:
            return

        for enemy in enemies:
            if not getattr(enemy, "alive", True):
                continue

            if (enemy.pos - self.pos).length() <= MELEE_RANGE:
                enemy.take_damage(MELEE_DAMAGE)

    def draw(self, screen: pygame.Surface) -> None:
        # Desenha player
        pygame.draw.circle(
            screen,
            (120, 200, 255),
            (int(self.pos.x), int(self.pos.y)),
            self.radius,
        )

    def _read_movement(self) -> pygame.Vector2:
        # WASD / setas
        keys = pygame.key.get_pressed()
        direction = pygame.Vector2(0, 0)

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            direction.y -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            direction.y += 1
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            direction.x -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            direction.x += 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

        return direction

    def _clamp_to_screen(self) -> None:
        # Mantém dentro da janela
        self.pos.x = max(self.radius, min(WIDTH - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(HEIGHT - self.radius, self.pos.y))


def spawn_enemy(enemy_type: str, pos: pygame.Vector2):
    # Factory simples (debug)
    if enemy_type == "spirit":
        return SpiritEnemy(pos)
    if enemy_type == "knight":
        return RangedKnightEnemy(pos)
    if enemy_type == "horse":
        return HorseEnemy(pos)

    raise ValueError(f"unknown enemy_type: {enemy_type}")


def find_boss(enemies: list) -> BossBreu | None:
    # Pega o boss atual (se existir)
    for enemy in enemies:
        if isinstance(enemy, BossBreu):
            return enemy
    return None


def force_boss_phase(boss: BossBreu, phase: int) -> None:
    # Força fase via HP (debug)
    phase = max(1, min(3, int(phase)))

    max_hp = boss.stats.max_health
    if phase == 1:
        boss.health = max_hp
    elif phase == 2:
        boss.health = int(max_hp * 0.69)  # abaixo de 70%
    else:
        boss.health = int(max_hp * 0.29)  # abaixo de 30%

    boss.take_damage(0)  # dispara checagem sem mudar HP
    boss.attack_cooldown_timer = 0.0  # evita sensação de “travado”


def update_enemies(
    dt: float,
    player: PlayerDummy,
    enemies: list,
    enemy_projectiles: list,
) -> list:
    # Atualiza inimigos e retorna spawns (boss)
    new_spawns = []

    for enemy in enemies:
        if isinstance(enemy, RangedKnightEnemy):
            enemy.update(dt, player, enemy_projectiles)

        elif isinstance(enemy, BossBreu):
            spawned = enemy.update(
                dt,
                player,
                enemy_projectiles,
                spawn_callback=spawn_enemy,
            )
            new_spawns.extend(spawned)

        else:
            enemy.update(dt, player)

    return new_spawns


def update_projectiles(
    dt: float,
    player: PlayerDummy,
    enemy_projectiles: list,
) -> list:
    # Move projéteis e aplica hit
    for proj in enemy_projectiles:
        proj.update(dt)

        if proj.alive and proj.collides_with_player(player):
            proj.on_hit_player(player)

    return [p for p in enemy_projectiles if p.alive]


def draw_frame(
    screen: pygame.Surface,
    player: PlayerDummy,
    enemies: list,
    enemy_projectiles: list,
) -> None:
    # Render básico
    screen.fill((20, 20, 20))
    player.draw(screen)

    for enemy in enemies:
        enemy.draw(screen)

    for proj in enemy_projectiles:
        proj.draw(screen)


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    pygame.display.set_caption("DEBUG ARENA - Boss")

    player = PlayerDummy(pygame.Vector2(WIDTH / 2, HEIGHT / 2))

    enemies = [
        SpiritEnemy(pygame.Vector2(120, 120)),
        BossBreu(pygame.Vector2(WIDTH - 180, HEIGHT / 2)),
        HorseEnemy(pygame.Vector2(WIDTH / 2, HEIGHT - 120)),
    ]

    enemy_projectiles = []

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Debug: força fase do boss
            if event.type == pygame.KEYDOWN:
                boss = find_boss(enemies)
                if boss:
                    if event.key == pygame.K_1:
                        force_boss_phase(boss, 1)
                    elif event.key == pygame.K_2:
                        force_boss_phase(boss, 2)
                    elif event.key == pygame.K_3:
                        force_boss_phase(boss, 3)

        # Player
        player.update(dt)
        player.melee_attack(enemies)

        # Inimigos + projéteis
        new_spawns = update_enemies(dt, player, enemies, enemy_projectiles)
        enemies.extend(new_spawns)
        enemy_projectiles = update_projectiles(dt, player, enemy_projectiles)

        # Render
        draw_frame(screen, player, enemies, enemy_projectiles)

        boss = find_boss(enemies)
        if boss:
            pygame.display.set_caption(
                f"DEBUG ARENA - HP: {player.health}/{player.max_health} | "
                f"Boss HP: {boss.health}/{boss.stats.max_health} | "
                f"Phase: {getattr(boss, 'current_phase', '?')}"
            )
        else:
            pygame.display.set_caption(f"DEBUG ARENA - HP: {player.health}/{player.max_health}")

        pygame.display.flip()

        if player.health <= 0:
            running = False

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()