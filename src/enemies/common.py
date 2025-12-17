import pygame

from .base import EnemyBase, EnemyStats, direction_to


AGGRO_RANGE = 260.0
MELEE_RANGE = 26.0


class SpiritEnemy(EnemyBase):
    """Melee básico: persegue e bate quando chega perto."""

    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=30,
                damage=8,
                move_speed=120.0,
                aggro_range=AGGRO_RANGE,
                attack_range=MELEE_RANGE,
                attack_cooldown=0.8,
            ),
            radius=14,
        )


class RangedKnightEnemy(EnemyBase):
    """Ranged: tenta manter distância e atira projéteis."""

    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=55,
                damage=10,  # dano do projétil
                move_speed=85.0,
                aggro_range=AGGRO_RANGE,
                attack_range=MELEE_RANGE,  # distância mínima (evita encostar)
                attack_cooldown=1.1,
            ),
            radius=16,
        )

        self.shooting_range = 220.0
        self.projectile_speed = 260.0

    def update(
        self,
        dt: float,
        player,
        enemy_projectiles: list,
        walls: list[pygame.Rect] | None = None,
    ) -> None:
        # IA do cavaleiro: range + recuo
        if not self.alive:
            return

        self.attack_cooldown_timer = max(0.0, self.attack_cooldown_timer - dt)

        player_pos = pygame.Vector2(player.pos)
        distance_to_player = self.distance_to(player_pos)

        if distance_to_player > self.stats.aggro_range:
            self.state = self.STATE_IDLE
            return

        # Dentro do range: para e atira
        if distance_to_player <= self.shooting_range and self.attack_cooldown_timer <= 0.0:
            self.state = self.STATE_ATTACK
            self.attack(player, enemy_projectiles)
            self.attack_cooldown_timer = self.stats.attack_cooldown
            return

        # Fora do range de tiro: reposiciona
        self.state = self.STATE_CHASE

        if distance_to_player < self.stats.attack_range:
            self._move_away_from(player_pos, dt, walls)
        else:
            self.move_towards(player_pos, dt, walls=walls)

    def _move_away_from(
        self,
        target_pos: pygame.Vector2,
        dt: float,
        walls: list[pygame.Rect] | None,
    ) -> None:
        # Recuo simples com colisão opcional
        direction = direction_to(target_pos, self.pos)  # direção do player -> inimigo
        velocity = direction * self.stats.move_speed
        self._move_with_collision(velocity, dt, walls or [])

    def attack(self, player, enemy_projectiles: list) -> None:
        # Dispara projétil na direção do player
        from .projectile import EnemyProjectile

        player_pos = pygame.Vector2(player.pos)
        direction = player_pos - self.pos
        if direction.length_squared() == 0:
            return

        enemy_projectiles.append(
            EnemyProjectile(
                pos=self.pos,
                direction=direction.normalize(),
                speed=self.projectile_speed,
                damage=self.stats.damage,
                radius=6,
                lifetime=3.0,
            )
        )


class HorseEnemy(EnemyBase):
    """Melee agressivo: persegue e dá charge (prep + dash)."""

    def __init__(self, pos: pygame.Vector2):
        super().__init__(
            pos=pos,
            stats=EnemyStats(
                max_health=40,
                damage=16,
                move_speed=170.0,
                aggro_range=AGGRO_RANGE,
                attack_range=MELEE_RANGE,
                attack_cooldown=1.2,
            ),
            radius=15,
        )

        self.charge_range = 180.0
        self.charge_speed_multiplier = 2.5
        self.charge_prep_time = 0.4
        self.charge_duration = 0.3

        self._charge_timer = 0.0
        self._charge_dir = pygame.Vector2(0, 0)
        self._charging = False
        self._preparing_charge = False

    def update(
        self,
        dt: float,
        player,
        walls: list[pygame.Rect] | None = None,
    ) -> None:
        # IA do cavalo: preparar, dar dash e voltar a perseguir
        if not self.alive:
            return

        self.attack_cooldown_timer = max(0.0, self.attack_cooldown_timer - dt)

        player_pos = pygame.Vector2(player.pos)
        distance_to_player = self.distance_to(player_pos)

        if self._preparing_charge:
            self._update_charge_prep(dt)
            return

        if self._charging:
            self._update_charge_dash(dt, walls)
            return

        if distance_to_player > self.stats.aggro_range:
            self.state = self.STATE_IDLE
            return

        if distance_to_player <= self.charge_range and self.attack_cooldown_timer <= 0.0:
            self._start_charge(player_pos)
            return

        self.state = self.STATE_CHASE
        self.move_towards(player_pos, dt, walls=walls)

    def _start_charge(self, player_pos: pygame.Vector2) -> None:
        # Inicia telegraph do charge
        direction = player_pos - self.pos
        if direction.length_squared() == 0:
            return

        self._charge_dir = direction.normalize()
        self._preparing_charge = True
        self._charge_timer = self.charge_prep_time
        self.state = self.STATE_ATTACK

    def _update_charge_prep(self, dt: float) -> None:
        # Tempo de preparação antes do dash
        self._charge_timer -= dt
        self.state = self.STATE_ATTACK

        if self._charge_timer <= 0.0:
            self._preparing_charge = False
            self._charging = True
            self._charge_timer = self.charge_duration

    def _update_charge_dash(self, dt: float, walls: list[pygame.Rect] | None) -> None:
        # Dash em linha reta (com colisão opcional)
        velocity = (
            self._charge_dir
            * self.stats.move_speed
            * self.charge_speed_multiplier
        )
        self._move_with_collision(velocity, dt, walls or [])

        self._charge_timer -= dt
        if self._charge_timer <= 0.0:
            self._charging = False
            self.attack_cooldown_timer = self.stats.attack_cooldown
