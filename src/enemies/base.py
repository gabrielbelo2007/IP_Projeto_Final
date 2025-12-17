from __future__ import annotations

from dataclasses import dataclass
import pygame


def direction_to(origin: pygame.Vector2, target: pygame.Vector2) -> pygame.Vector2:
    delta = target - origin
    if delta.length_squared() == 0:
        return pygame.Vector2(0, 0)
    return delta.normalize()


@dataclass(frozen=True)
class EnemyStats:
    max_health: int
    damage: int
    move_speed: float
    aggro_range: float
    attack_range: float
    attack_cooldown: float


class EnemyBase:
    """Inimigo base com IA simples: detectar, perseguir e atacar."""

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
        return self.state != self.STATE_DEAD

    def take_damage(self, amount: int) -> None:
        if not self.alive:
            return

        self.health -= int(amount)
        if self.health <= 0:
            self.die()

    def die(self) -> None:
        self.state = self.STATE_DEAD

    def distance_to(self, position: pygame.Vector2) -> float:
        return (position - self.pos).length()

    def can_attack(self, distance_to_player: float) -> bool:
        return distance_to_player <= self.stats.attack_range and self.attack_cooldown_timer <= 0.0

    def move_towards(self, target_pos: pygame.Vector2, dt: float) -> None:
        self.pos += direction_to(self.pos, target_pos) * self.stats.move_speed * dt

    def attack(self, player) -> None:
        if hasattr(player, "take_damage"):
            player.take_damage(self.stats.damage)

    def update(self, dt: float, player) -> None:
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
        self.move_towards(player_pos, dt)

    def draw(self, screen: pygame.Surface) -> None:
        if not self.alive:
            return

        if self.state == self.STATE_IDLE:
            color = (120, 120, 120)
        elif self.state == self.STATE_CHASE:
            color = (220, 220, 220)
        else:
            color = (255, 180, 180)

        pygame.draw.circle(screen, color, (int(self.pos.x), int(self.pos.y)), self.radius)