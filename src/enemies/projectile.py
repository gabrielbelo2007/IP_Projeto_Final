import pygame


class EnemyProjectile:
    """Projétil disparado por inimigos ranged."""

    def __init__(
        self,
        pos: pygame.Vector2,
        direction: pygame.Vector2,
        speed: float,
        damage: int,
        radius: int = 6,
        lifetime: float = 3.0,
    ):
        self.pos = pygame.Vector2(pos)
        self.velocity = pygame.Vector2(direction) * speed

        self.damage = int(damage)
        self.radius = radius

        # Tempo máximo em cena
        self.lifetime = lifetime
        self.alive = True

    def update(self, dt: float) -> None:
        # Move o projétil e controla tempo de vida
        if not self.alive:
            return

        self.pos += self.velocity * dt
        self.lifetime -= dt

        if self.lifetime <= 0:
            self.alive = False

    def collides_with_player(self, player) -> bool:
        # Colisão circular simples com o player
        player_pos = pygame.Vector2(player.pos)
        player_radius = getattr(player, "radius", 14)

        distance = (player_pos - self.pos).length()
        return distance <= (self.radius + player_radius)

    def on_hit_player(self, player) -> None:
        # Aplica dano e destrói o projétil
        if hasattr(player, "take_damage"):
            player.take_damage(self.damage)

        self.alive = False

    def draw(self, screen: pygame.Surface) -> None:
        # Visual simples (placeholder)
        if not self.alive:
            return

        pygame.draw.circle(
            screen,
            (180, 220, 255),
            (int(self.pos.x), int(self.pos.y)),
            self.radius,
        )