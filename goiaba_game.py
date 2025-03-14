import pygame
import random

pygame.init()

# Configuração da janela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Goiabinha")

# Cores e FPS
branco = (255,255,255)
preto = (0,0,0)
clock = pygame.time.Clock()

# Carregamento das imagens
img_goiabinha = pygame.sprite("player.png")                 # Player
img_arCondicionado = pygame.image.load("Ar_Condicionado.png")   # Obstáculo 1
img_bebedouro = pygame.image.load("Bebedouro.png")              # Obstáculo 2
img_vazamento = pygame.image.load("Vazamento1.png")             # Obstáculo 3
img_ppr_bonus = pygame.image.load("ppr_bonus.png")          # Bonus 1
img_ferramenta = pygame.image.load("ferramenta_bonus.png")  # Bonus 2
img_fralda = pygame.image.load("bebe_bonus.png")            # Bonus 3

# Escalando as imagens para tamanhos apropriados
img_goiabinha = pygame.transform.scale(img_goiabinha, (70,70))
img_arCondicionado = pygame.transform.scale(img_arCondicionado, (64,64))
img_bebedouro = pygame.transform.scale(img_bebedouro, (64,64))
img_vazamento = pygame.transform.scale(img_vazamento, (64,64))
img_ppr_bonus = pygame.transform.scale(img_ppr_bonus, (50,50))
img_ferramenta = pygame.transform.scale(img_ferramenta, (50,50))
img_fralda = pygame.transform.scale(img_fralda, (50,50))

# Classes dos elementos do jogo
class Player:
    def __init__(self):
        self.x = 50
        self.y = altura_tela - 100
        self.altura_salto = 300
        self.velocidade_y = 0
        self.no_chao = True

    def desenhar(self):
        tela.blit(img_goiabinha, (self.x, self.y))    

    def pular(self):
        if self.no_chao:
            self.velocidade_y = -16 # Força do salto
            self.no_chao = False

    def atualizar(self):
        self.y += self.velocidade_y
        self.velocidade_y += 1 # Gravidade

        if self.y >= altura_tela - 100:
            self.y = altura_tela - 100
            self.no_chao = True

class Obstaculo:
    def __init__(self, tipo):
        self.x = largura_tela
        self.y = altura_tela - 100
        self.tipo = tipo
        if tipo == 1:
            self.imagem = img_arCondicionado
        if tipo == 2:
            self.imagem = img_bebedouro
        else:
            self.imagem = img_vazamento                

    def desenhar(self):
        tela.blit(self.imagem, (self.x, self.y))

    def mover(self):
        self.x -= 8 # velocidade de movimento

class Bonus:
    def __init__(self, tipo):
        self.x = largura_tela
        self.y = random.randint(altura_tela - 200, altura_tela - 150) # Aleatório no ar
        self.tipo = tipo
        if tipo == 1:
            self.imagem = img_ferramenta
        if tipo == 2:
            self.imagem = img_fralda
        else:
            self.imagem = img_ppr_bonus        

    def desenhar(self):
        tela.blit(self.imagem, (self.x, self.y))

    def mover(self):
        self.x -= 6 # velocidade de movimento

# Inicialização dos objetos
player = Player()
obstaculos = []
bonus = []

rodando = True
while rodando:
    # Atualizações no jogo
    tela.fill(branco)  # Limpa a tela
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                player.pular()

    # Atualizar e desenhar o player
    player.atualizar()
    player.desenhar()           

    # Criar obstáculos aleatórios
    if random.randint(1, 100) == 1: # 1% de chance de aparecer um obstáculo
        obstaculos.append(Obstaculo(random.choice([1,2,3])))

    # Criar bonus aleatórios
    if random.randint(1, 200) == 1: # 0,5% de chance de aparecer um bonus
        bonus.append(Bonus(random.choice([1,2,3])))   
    
    # Atualizar e desenhar os obstáculos
    for obstaculo in obstaculos[:]:
        obstaculo.mover()
        obstaculo.desenhar()
        if obstaculo.x < -50: # Remover obstáculos fora da tela
            obstaculos.remove(obstaculo)

    # Atualizar e desenhar os bonus
    for b in bonus[:]:
        b.mover()
        b.desenhar()
        if b.x < -50: # Remover bonus fora da tela
            bonus.remove(b)        

    pygame.display.update()
    clock.tick(60)  # Limita o FPS a 60

pygame.quit()
