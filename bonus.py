import pygame
import random

TIPOS_BONUS = [
    "images/ferramenta_bonus.png",
    "images/bebe_bonus.png",
    "images/ppr_bonus.png",
]
PESOS_BONUS = [5, 3, 1]


class Bonus(pygame.sprite.Sprite):
    def __init__(self, tela, largura_tela, altura_tela, velocidade=6):
        super().__init__()
        self.tela = tela
        self.velocidade = velocidade
        self.y = random.randint(altura_tela - 300, altura_tela - 150)

        self.tipo = random.choices(TIPOS_BONUS, weights=PESOS_BONUS, k=1)[0]

        self.imagem = pygame.image.load(self.tipo).convert_alpha()
        self.imagem = pygame.transform.scale(self.imagem, (50, 50))
        self.rect = self.imagem.get_rect(topleft=(largura_tela, self.y))

    def mover(self):
        self.rect.x -= self.velocidade

    def fora_da_tela(self) -> bool:
        return self.rect.right < 0

    def desenhar(self):
        self.tela.blit(self.imagem, self.rect.topleft)
