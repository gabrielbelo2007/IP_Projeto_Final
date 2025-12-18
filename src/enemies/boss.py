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


class BossBreu(EnemyBase):
    # Boss: persegue em janelas e alterna padrões

    STATE_INTRO = "INTRO"
    STATE_CHASING = "CHASING"
    STATE_PATTERN_CONE = "PATTERN_CONE"
    STATE_PATTERN_RAIN = "PATTERN_RAIN"
    STATE_SUMMONING = "SUMMONING"
    STATE_ENRAGED = "ENRAGED"
    STATE_DEAD = "DEAD"

    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=300,
                damage=14,
                move_speed=90.0,
                aggro_range=99999.0,
                attack_range=0.0,
                attack_cooldown=0.0,
            ),
            radius=26,
        )

        # Fases
        self.current_phase = 1
        self.phase_thresholds = (0.70, 0.30)
        self._pending_phase: int | None = None

        # Janelas (move/ataque)
        self.move_time = 1.6
        self.attack_time = 0.7
        self._window_timer = self.move_time
        self._in_attack_window = False

        # Cooldowns atuais
        self._cone_cd = 0.0
        self._rain_cd = 0.0
        self._summon_cd = 0.0
        self._pool_cd = 0.0

        # Cooldowns base (por fase)
        self._cone_base_cd = 1.4
        self._rain_base_cd = 2.4
        self._summon_base_cd = 5.0
        self._pool_base_cd = 3.2

        # Cone
        self.cone_range = 360.0
        self.cone_projectile_speed = 270.0
        self.cone_projectile_lifetime = 3.2
        self.cone_shots = 7
        self.cone_spread_degrees = 55.0

        # Chuva
        self.rain_radius = 18.0
        self.rain_warning_time = 0.7
        self.rain_damage = 12
        self.rain_count = 6
        self._telegraphs: list[TelegraphCircle] = []

        # Poça (DOT)
        self.pool_size = (90, 90)
        self.pool_lifetime = 4.0
        self.pool_tick_damage = 6
        self.pool_tick_interval = 0.5
        self._pools: list[BreuPool] = []

        # Intro
        self.state = self.STATE_INTRO
        self._intro_time = 0.6

        self._apply_phase_tuning()

    # -------------------------
    # Loop
    # -------------------------

    def update(
        self,
        dt: float,
        player,
        enemy_projectiles: list[EnemyProjectile],
        spawn_callback: SpawnFactory | None = None,
    ) -> list[object]:
        if not self.alive:
            return []

        spawns: list[object] = []

        self._tick_cooldowns(dt)
        self._update_intro(dt)

        self._update_telegraphs(dt, player)
        self._update_pools(dt, player)

        if self.state == self.STATE_INTRO:
            return spawns

        self._window_timer -= dt
        if self._window_timer <= 0.0:
            self._toggle_window()

        # aplica mudança de fase em ponto seguro
        self._apply_pending_phase_if_safe()

        player_pos = pygame.Vector2(player.pos)

        if self._in_attack_window:
            self._do_attack_window(player_pos, enemy_projectiles, spawns, spawn_callback)
            return spawns

        self.state = self.STATE_CHASING
        self.move_towards(player_pos, dt)
        return spawns

    # -------------------------
    # Fases
    # -------------------------

    def take_damage(self, amount: int) -> None:
        if not self.alive:
            return

        super().take_damage(amount)
        if not self.alive:
            return

        hp_ratio = self.health / float(self.stats.max_health)
        self._queue_phase_if_needed(hp_ratio)

    def _queue_phase_if_needed(self, hp_ratio: float) -> None:
        if self.current_phase == 1 and hp_ratio <= self.phase_thresholds[0]:
            self._pending_phase = 2
        elif self.current_phase == 2 and hp_ratio <= self.phase_thresholds[1]:
            self._pending_phase = 3

    def _apply_pending_phase_if_safe(self) -> None:
        if self._pending_phase is None:
            return

        # não troca no meio de telegraph/pool ou janela de ataque
        if self._in_attack_window:
            return
        if self._telegraphs:
            return

        self.current_phase = self._pending_phase
        self._pending_phase = None
        self._apply_phase_tuning()

    def _apply_phase_tuning(self) -> None:
        if self.current_phase == 1:
            self.move_time = 1.7
            self.attack_time = 0.7
            self.cone_shots = 7
            self.cone_spread_degrees = 55.0
            self._set_skill_cooldowns(cone=1.4, rain=2.4, summon=5.0, pool=3.2)
            self.stats.move_speed = 90.0

        elif self.current_phase == 2:
            self.move_time = 1.4
            self.attack_time = 0.75
            self.cone_shots = 9
            self.cone_spread_degrees = 65.0
            self.rain_count = 8
            self._set_skill_cooldowns(cone=1.2, rain=2.0, summon=4.2, pool=2.8)
            self.stats.move_speed = 105.0

        else:
            self.state = self.STATE_ENRAGED
            self.move_time = 1.2
            self.attack_time = 0.85
            self.cone_shots = 11
            self.cone_spread_degrees = 75.0
            self.rain_count = 10
            self._set_skill_cooldowns(cone=1.0, rain=1.7, summon=3.6, pool=2.3)
            self.stats.move_speed = 120.0

        self._window_timer = self.move_time
        self._in_attack_window = False

    def _set_skill_cooldowns(self, cone: float, rain: float, summon: float, pool: float) -> None:
        self._cone_base_cd = cone
        self._rain_base_cd = rain
        self._summon_base_cd = summon
        self._pool_base_cd = pool

    # -------------------------
    # Janelas
    # -------------------------

    def _toggle_window(self) -> None:
        self._in_attack_window = not self._in_attack_window
        self._window_timer = self.attack_time if self._in_attack_window else self.move_time

    def _do_attack_window(
        self,
        player_pos: pygame.Vector2,
        enemy_projectiles: list[EnemyProjectile],
        spawns: list[object],
        spawn_callback: SpawnFactory | None,
    ) -> None:
        options: list[str] = []

        if self._cone_cd <= 0.0:
            options.append("cone")
        if self._rain_cd <= 0.0:
            options.append("rain")
        if self._pool_cd <= 0.0:
            options.append("pool")
        if self._summon_cd <= 0.0:
            options.append("summon")

        if not options:
            self.state = self.STATE_ATTACK
            return

        if self.current_phase == 3:
            weights = {"cone": 40, "rain": 30, "pool": 20, "summon": 10}
        else:
            weights = {"cone": 40, "rain": 25, "pool": 20, "summon": 15}

        pick = random.choices(options, weights=[weights[o] for o in options], k=1)[0]

        if pick == "cone":
            self.state = self.STATE_PATTERN_CONE
            self._fire_cone(player_pos, enemy_projectiles)
            self._cone_cd = self._cone_base_cd
            return

        if pick == "rain":
            self.state = self.STATE_PATTERN_RAIN
            self._start_rain(player_pos)
            self._rain_cd = self._rain_base_cd
            return

        if pick == "pool":
            self.state = self.STATE_ATTACK
            self._spawn_pool(player_pos)
            self._pool_cd = self._pool_base_cd
            return

        self.state = self.STATE_SUMMONING
        if spawn_callback:
            spawns.extend(self._summon_minions(player_pos, spawn_callback))
        self._summon_cd = self._summon_base_cd

    # -------------------------
    # Ataques
    # -------------------------

    def _fire_cone(self, player_pos: pygame.Vector2, enemy_projectiles: list[EnemyProjectile]) -> None:
        base_dir = player_pos - self.pos
        if base_dir.length_squared() == 0:
            return

        base_angle = math.atan2(base_dir.y, base_dir.x)

        if self.cone_shots <= 1:
            angles = [base_angle]
        else:
            half = math.radians(self.cone_spread_degrees) / 2.0
            step = (2.0 * half) / (self.cone_shots - 1)
            angles = [base_angle - half + i * step for i in range(self.cone_shots)]

        for ang in angles:
            direction = pygame.Vector2(math.cos(ang), math.sin(ang))
            enemy_projectiles.append(
                EnemyProjectile(
                    pos=self.pos,
                    direction=direction,
                    speed=self.cone_projectile_speed,
                    damage=self.stats.damage,
                    radius=7,
                    lifetime=self.cone_projectile_lifetime,
                )
            )

    def _start_rain(self, player_pos: pygame.Vector2) -> None:
        self._telegraphs.clear()

        for _ in range(self.rain_count):
            offset = pygame.Vector2(random.uniform(-90, 90), random.uniform(-90, 90))
            self._telegraphs.append(
                TelegraphCircle(
                    pos=pygame.Vector2(player_pos) + offset,
                    radius=self.rain_radius,
                    time_left=self.rain_warning_time,
                )
            )

    def _update_telegraphs(self, dt: float, player) -> None:
        if not self._telegraphs:
            return

        player_pos = pygame.Vector2(player.pos)
        player_radius = getattr(player, "radius", 14)

        remaining: list[TelegraphCircle] = []
        for t in self._telegraphs:
            t.time_left -= dt
            if t.time_left > 0:
                remaining.append(t)
                continue

            if (player_pos - t.pos).length() <= (t.radius + player_radius):
                if hasattr(player, "take_damage"):
                    player.take_damage(self.rain_damage)

        self._telegraphs = remaining

    def _spawn_pool(self, player_pos: pygame.Vector2) -> None:
        x = int(player_pos.x - self.pool_size[0] / 2)
        y = int(player_pos.y - self.pool_size[1] / 2)
        rect = pygame.Rect(x, y, self.pool_size[0], self.pool_size[1])

        self._pools.append(
            BreuPool(
                rect=rect,
                time_left=self.pool_lifetime,
                tick_timer=self.pool_tick_interval,
            )
        )

    def _update_pools(self, dt: float, player) -> None:
        if not self._pools:
            return

        pr = getattr(player, "radius", 14)
        player_rect = pygame.Rect(
            int(player.pos.x - pr),
            int(player.pos.y - pr),
            pr * 2,
            pr * 2,
        )

        alive_pools: list[BreuPool] = []
        for pool in self._pools:
            pool.time_left -= dt
            if pool.time_left <= 0:
                continue

            pool.tick_timer -= dt
            if pool.tick_timer <= 0:
                pool.tick_timer = self.pool_tick_interval
                if pool.rect.colliderect(player_rect):
                    if hasattr(player, "take_damage"):
                        player.take_damage(self.pool_tick_damage)

            alive_pools.append(pool)

        self._pools = alive_pools

    def _summon_minions(self, player_pos: pygame.Vector2, spawn_callback: SpawnFactory) -> list[object]:
        spawns: list[object] = []

        count = 2 if self.current_phase == 1 else (3 if self.current_phase == 2 else 4)
        types = ["spirit", "knight", "horse"]

        for _ in range(count):
            enemy_type = random.choice(types)
            offset = pygame.Vector2(random.uniform(-140, 140), random.uniform(-140, 140))
            spawns.append(spawn_callback(enemy_type, pygame.Vector2(player_pos) + offset))

        return spawns

    # -------------------------
    # Morte
    # -------------------------

    def die(self) -> None:
        if not self.alive:
            return

        self.state = self.STATE_DEAD
        self._telegraphs.clear()
        self._pools.clear()
        self._pending_phase = None

        # trava skills
        self._cone_cd = 999.0
        self._rain_cd = 999.0
        self._summon_cd = 999.0
        self._pool_cd = 999.0

        self.on_death()

    # -------------------------
    # Debug draw
    # -------------------------

    def draw(self, screen: pygame.Surface) -> None:
        super().draw(screen)

        for t in self._telegraphs:
            pygame.draw.circle(
                screen,
                (120, 80, 160),
                (int(t.pos.x), int(t.pos.y)),
                int(t.radius),
                2,
            )

        for pool in self._pools:
            pygame.draw.rect(screen, (60, 30, 80), pool.rect, 2)

    # -------------------------
    # Helpers
    # -------------------------

    def _tick_cooldowns(self, dt: float) -> None:
        self._cone_cd = max(0.0, self._cone_cd - dt)
        self._rain_cd = max(0.0, self._rain_cd - dt)
        self._summon_cd = max(0.0, self._summon_cd - dt)
        self._pool_cd = max(0.0, self._pool_cd - dt)

    def _update_intro(self, dt: float) -> None:
        if self.state != self.STATE_INTRO:
            return

        self._intro_time -= dt
        if self._intro_time <= 0.0:
            self.state = self.STATE_CHASING
