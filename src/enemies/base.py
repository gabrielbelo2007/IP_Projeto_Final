from __future__ import annotations

from dataclasses import dataclass
import pygame


def direction_to(origin: pygame.Vector2, target: pygame.Vector2) -> pygame.Vector2:
    # Direção normalizada origin -> target
    delta = target - origin
    if delta.length_squared() == 0:
        return pygame.Vector2()
    return delta.normalize()


@dataclass
class EnemyStats:
    # Stats compartilhados
    max_health: int
    damage: int
    move_speed: float
    aggro_range: float
    attack_range: float
    attack_cooldown: float


class EnemyBase:
    # Base: detecta, persegue e ataca

    STATE_IDLE = "IDLE"
    STATE_CHASE = "CHASE"
    STATE_ATTACK = "ATTACK"
    STATE_DEAD = "DEAD"

    def __init__(self, pos: pygame.Vector2, stats: EnemyStats, radius: int = 14):
        self.pos = pygame.Vector2(pos)
        self.stats = stats
        self.radius = radius

        self.health = stats.max_health
        self.state = self.STATE_IDLE
        self.attack_cooldown_timer = 0.0

    @property
    def alive(self) -> bool:
        # Vivo enquanto não for DEAD
        return self.state != self.STATE_DEAD

    def take_damage(self, amount: int) -> None:
        # Aplica dano e verifica morte
        if not self.alive:
            return

        self.health -= int(amount)
        if self.health <= 0:
            self.die()

    def die(self) -> None:
        # Ponto oficial de morte
        self.state = self.STATE_DEAD
        self.on_death()

    def on_death(self) -> None:
        # Hook para drops/efeitos (outro time)
        pass

    def distance_to(self, position: pygame.Vector2) -> float:
        # Distância até um ponto
        return (position - self.pos).length()

    def can_attack(self, distance_to_player: float) -> bool:
        # Range + cooldown
        return (
            distance_to_player <= self.stats.attack_range
            and self.attack_cooldown_timer <= 0.0
        )

    def move_towards(
        self,
        target_pos: pygame.Vector2,
        dt: float,
        walls: list[pygame.Rect] | None = None,
    ) -> None:
        # Move com colisão opcional
        direction = direction_to(self.pos, target_pos)
        velocity = direction * self.stats.move_speed
        self._move_with_collision(velocity, dt, walls or [])

    def attack(self, player) -> None:
        # Ataque base: dano direto
        if hasattr(player, "take_damage"):
            player.take_damage(self.stats.damage)

    def update(
        self,
        dt: float,
        player,
        walls: list[pygame.Rect] | None = None,
    ) -> None:
        # IA simples: idle/chase/attack
        if not self.alive:
            return

        self.attack_cooldown_timer = max(0.0, self.attack_cooldown_timer - dt)

        player_pos = pygame.Vector2(player.pos)
        distance_to_player = self.distance_to(player_pos)

        if distance_to_player > self.stats.aggro_range:
            self.state = self.STATE_IDLE
            return

        if self.can_attack(distance_to_player):
            self.state = self.STATE_ATTACK
            self.attack(player)
            self.attack_cooldown_timer = self.stats.attack_cooldown
            return

        self.state = self.STATE_CHASE
        self.move_towards(player_pos, dt, walls=walls)

    def draw(self, screen: pygame.Surface) -> None:
        # Placeholder visual
        if not self.alive:
            return

        if self.state == self.STATE_IDLE:
            color = (120, 120, 120)
        elif self.state == self.STATE_CHASE:
            color = (220, 220, 220)
        else:
            color = (255, 180, 180)

        pygame.draw.circle(screen, color, (int(self.pos.x), int(self.pos.y)), self.radius)

    def get_rect(self) -> pygame.Rect:
        # Hitbox simples
        return pygame.Rect(
            int(self.pos.x - self.radius),
            int(self.pos.y - self.radius),
            self.radius * 2,
            self.radius * 2,
        )

    def _move_with_collision(
        self,
        velocity: pygame.Vector2,
        dt: float,
        walls: list[pygame.Rect],
    ) -> None:
        # Resolve colisão por eixo (slide simples)

        self.pos.x += velocity.x * dt
        rect = self.get_rect()
        for wall in walls:
            if rect.colliderect(wall):
                if velocity.x > 0:
                    self.pos.x = wall.left - self.radius
                elif velocity.x < 0:
                    self.pos.x = wall.right + self.radius
                rect = self.get_rect()

        self.pos.y += velocity.y * dt
        rect = self.get_rect()
        for wall in walls:
            if rect.colliderect(wall):
                if velocity.y > 0:
                    self.pos.y = wall.top - self.radius
                elif velocity.y < 0:
                    self.pos.y = wall.bottom + self.radius
                rect = self.get_rect()
