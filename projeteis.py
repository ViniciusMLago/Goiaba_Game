import pygame
import random

class Projectile:

    def __init__(self, largura_tela, altura_tela):

        # posição inicial
        self.x = largura_tela
        self.y = random.randint(150, altura_tela - 80)

        # velocidade
        self.vel = 7

        # >>> TAMANHO DO PROJÉTIL
        self.largura = 40   # igual aos obstáculos
        self.altura = 20

        # rect para colisão
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

    def mover(self):
        self.x -= self.vel
        self.rect.x = int(self.x)

    def desenhar(self, tela):

        # >>> VERDE FLORESCENTE
        cor_proj = (57, 255, 20)

        pygame.draw.rect(
            tela,
            cor_proj,
            (self.x, self.y, self.largura, self.altura)
        )