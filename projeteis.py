import random

import pygame


class Projectile(pygame.sprite.Sprite):
    """Projectile that can spawn on ground or mid-air lanes."""

    LANE_GROUND = "ground"
    LANE_AIR = "air"

    COR_GROUND = (255, 90, 60)
    COR_AIR = (57, 255, 20)

    def __init__(self, largura_tela, altura_tela, velocidade=7, lane=None):
        super().__init__()

        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.vel = velocidade + random.randint(0, 2)

        self.largura = 44
        self.altura = 20

        self.lane = lane or self._sortear_lane()
        self.x = float(largura_tela)
        self.y = self._sortear_altura()

        self.image = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        self.rect = self.image.get_rect(topleft=(int(self.x), int(self.y)))
        self._redesenhar()

    @classmethod
    def criar_aleatorio(cls, largura_tela, altura_tela, velocidade=7):
        return cls(largura_tela, altura_tela, velocidade=velocidade)

    def _sortear_lane(self):
        return random.choices(
            (self.LANE_GROUND, self.LANE_AIR),
            weights=(60, 40),
            k=1,
        )[0]

    def _sortear_altura(self):
        if self.lane == self.LANE_GROUND:
            margem_chao = 30
            jitter = random.randint(0, 14)
            return self.altura_tela - margem_chao - self.altura - jitter

        altura_min = max(180, self.altura_tela // 3)
        altura_max = max(altura_min + 40, self.altura_tela - 180)
        return random.randint(altura_min, altura_max)

    def _cor(self):
        return self.COR_GROUND if self.lane == self.LANE_GROUND else self.COR_AIR

    def _redesenhar(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(
            self.image,
            self._cor(),
            (0, 0, self.largura, self.altura),
            border_radius=5,
        )
        if self.lane == self.LANE_AIR:
            pygame.draw.rect(
                self.image,
                (255, 255, 255),
                (6, 6, self.largura - 12, self.altura - 12),
                width=1,
                border_radius=4,
            )

    def mover(self):
        self.x -= self.vel
        self.rect.x = int(self.x)

    def fora_da_tela(self):
        return self.rect.right < 0

    def desenhar(self, tela):
        tela.blit(self.image, self.rect.topleft)
