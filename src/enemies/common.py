import pygame
from .base import EnemyBase, EnemyStats

AGGRO_RANGE = 260.0
ATTACK_RANGE = 26.0


class SpiritEnemy(EnemyBase):
    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=30,
                damage=8,
                move_speed=120.0,
                aggro_range=AGGRO_RANGE,
                attack_range=ATTACK_RANGE,
                attack_cooldown=0.8,
            ),
            radius=14,
        )


class RangedKnightEnemy(EnemyBase):
    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=55,
                damage=12,
                move_speed=90.0,
                aggro_range=AGGRO_RANGE,
                attack_range=ATTACK_RANGE,
                attack_cooldown=1.1,
            ),
            radius=16,
        )


class HorseEnemy(EnemyBase):
    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=40,
                damage=16,
                move_speed=170.0,
                aggro_range=AGGRO_RANGE,
                attack_range=ATTACK_RANGE,
                attack_cooldown=1.2,
            ),
            radius=15,
        )