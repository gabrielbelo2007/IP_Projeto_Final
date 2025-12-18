from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable

import pygame

from .base import EnemyBase, EnemyStats
from .projectile import EnemyProjectile


@dataclass
class TelegraphCircle:
    pos: pygame.Vector2
    radius: float
    time_left: float


@dataclass
class BreuPool:
    rect: pygame.Rect
    time_left: float
    tick_timer: float


SpawnFactory = Callable[[str, pygame.Vector2], object]

class BossProjectile(pygame.sprite.Sprite):
    def __init__(self, pos, target_pos, speed=5):
        super().__init__()
        
        img = pygame.image.load('assets/images/characters/boss_projectile.png').convert_alpha()
        self.image = pygame.transform.scale(img, (32, 32))
        self.rect = self.image.get_rect(center=pos)
        
        vec = pygame.math.Vector2(target_pos) - pygame.math.Vector2(pos)
        if vec.length_squared() > 0:
            self.velocity = vec.normalize() * speed
        else:
            self.velocity = pygame.math.Vector2(1,0)
            
        self.pos = pygame.math.Vector2(pos)
        self.damage = 25

    def update(self):
        self.pos += self.velocity
        self.rect.center = (int(self.pos.x), int(self.pos.y))
        
        # Remove se sair da tela (muito longe)
        if self.pos.x < -200 or self.pos.x > 2000 or self.pos.y < -200 or self.pos.y > 2000:
            self.kill()

class BossBreu(EnemyBase):
    
    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=300,
                damage=25,
                move_speed=100.0,
                aggro_range=99999.0,
                attack_range=10.0,
                attack_cooldown=0.0,
            ),
            radius=70,
        )
        
        raw = pygame.image.load('assets/images/characters/boss.png').convert_alpha()
        scale_size = (int(self.radius * 2.5), int(self.radius * 2.5))
        self.image = pygame.transform.scale(raw, scale_size)

        self.rect = self.image.get_rect(center=(int(pos.x), int(pos.y)))
        
        self.projectiles_group = None # Será atribuido no spawn
        self.attack_timer = 0
        self.attack_interval = 2.0

    def set_projectile_group(self, group):
        self.projectiles_group = group

    def update(self, dt, player, walls=None):
        super().update(dt, player, walls)
        
        # Lógica de ataque especial (tiro em cone)
        self.attack_timer += dt
        if self.attack_timer > 2.0: # A cada 2 segundos
            self.fire_cone(player.rect.center)
            self.attack_timer = 0
            
    def fire_cone(self, target_pos):
        
        if self.projectiles_group is None: return
        
        # Dispara 5 projéteis em leque
        base_vec = pygame.math.Vector2(target_pos) - self.pos
        if base_vec.length() == 0: return
        
        angle_base = math.degrees(math.atan2(base_vec.y, base_vec.x))
        
        for angle_offset in [-30, -15, 0, 15, 30]:
            angle_rad = math.radians(angle_base + angle_offset)
            # Calcula ponto alvo fake baseado no angulo
            dummy_target = self.pos + pygame.math.Vector2(math.cos(angle_rad), math.sin(angle_rad)) * 100
            
            proj = BossProjectile(self.rect.center, dummy_target, speed=6)
            self.projectiles_group.add(proj)
