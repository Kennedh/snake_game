import pygame
import random
import sys

pygame.init()

# Configurações de tamanho e blocos
LARGURA_TELA = 600
ALTURA_TELA = 600
TAMANHO_BLOCO = 20

# Paleta de Cores, são tuplas com três posições pq é RGB :-)
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
VERDE_ESCURO = (0, 150, 0)
CINZA = (50, 50, 50)  # Um cinza mais escuro pras linhas ficarem discretas

TELA = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Jogo da Cobrinha")
relogio = pygame.time.Clock()

fonte = pygame.font.Font(None, 36)
fonte_pequena = pygame.font.Font(None, 28)
fonte_titulo = pygame.font.Font(None, 72)


class Cobra:
    def __init__(self):
        self.tamanho = 1
        self.posicoes = [(LARGURA_TELA // 2, ALTURA_TELA // 2)]
        self.direcao = random.choice(['DIREITA', 'ESQUERDA', 'CIMA', 'BAIXO'])

    def mover(self):
        x, y = self.posicoes[0]

        if self.direcao == 'DIREITA':
            x += TAMANHO_BLOCO
        elif self.direcao == 'ESQUERDA':
            x -= TAMANHO_BLOCO
        elif self.direcao == 'CIMA':
            y -= TAMANHO_BLOCO
        elif self.direcao == 'BAIXO':
            y += TAMANHO_BLOCO

        nova_cabeca = (x, y)
        self.posicoes.insert(0, nova_cabeca)

        if len(self.posicoes) > self.tamanho:
            self.posicoes.pop()

    def crescer(self):
        self.tamanho += 1

    def colisao(self):
        cabeca = self.posicoes[0]
        # Bateu na parede?
        if cabeca[0] < 0 or cabeca[0] >= LARGURA_TELA or cabeca[1] < 0 or cabeca[1] >= ALTURA_TELA:
            return True
        # Se auto-canibalizou?
        if cabeca in self.posicoes[1:]:
            return True
        return False

    def mudar_direcao(self, nova_direcao):
        if nova_direcao == 'DIREITA' and self.direcao != 'ESQUERDA':
            self.direcao = nova_direcao
        elif nova_direcao == 'ESQUERDA' and self.direcao != 'DIREITA':
            self.direcao = nova_direcao
        elif nova_direcao == 'CIMA' and self.direcao != 'BAIXO':
            self.direcao = nova_direcao
        elif nova_direcao == 'BAIXO' and self.direcao != 'CIMA':
            self.direcao = nova_direcao

    def desenhar(self, tela):
        for i, posicao in enumerate(self.posicoes):
            cor = VERDE if i == 0 else VERDE_ESCURO
            pygame.draw.rect(tela, cor, (posicao[0], posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
            pygame.draw.rect(tela, PRETO, (posicao[0], posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO), 1)


class Comida:
    def __init__(self):
        self.posicao = (0, 0)
        self.gerar_nova_posicao()

    def gerar_nova_posicao(self, posicoes_cobra=None):
        while True:
            x = random.randrange(0, LARGURA_TELA, TAMANHO_BLOCO)
            y = random.randrange(0, ALTURA_TELA, TAMANHO_BLOCO)
            self.posicao = (x, y)
            if not posicoes_cobra or self.posicao not in posicoes_cobra:
                break

    def desenhar(self, tela):
        pygame.draw.rect(tela, VERMELHO, (self.posicao[0], self.posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO))
        pygame.draw.rect(tela, PRETO, (self.posicao[0], self.posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO), 1)


def mostrar_game_over(tela, pontuacao, dificuldade):
    overlay = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    overlay.set_alpha(180)
    overlay.fill(PRETO)
    tela.blit(overlay, (0, 0))

    texto_go = fonte_titulo.render("GAME OVER", True, VERMELHO)
    tela.blit(texto_go, texto_go.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 100)))

    texto_pts = fonte.render(f"Pontuação Final: {pontuacao}", True, BRANCO)
    tela.blit(texto_pts, texto_pts.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 - 30)))

    # Mensagem bem pau no cu se o jogador perder no medio ou dificil kkkkkk
    if dificuldade in ["Normal", "Difícil"]:
        msg_zoacao = "Muito ruinzinho... Se quiser temos a dificuldade fácil hahaha"
        texto_zoacao = fonte_pequena.render(msg_zoacao, True, VERMELHO)
        tela.blit(texto_zoacao, texto_zoacao.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 20)))

    texto_voltar = fonte.render("Pressione ESPAÇO para voltar ao Menu", True, BRANCO)
    tela.blit(texto_voltar, texto_voltar.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2 + 100)))

    pygame.display.update()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    return

def jogo(velocidade, nome_dificuldade):
    cobra = Cobra()
    comida = Comida()
    pontuacao = 0
    pausado = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    pausado = not pausado

                if not pausado:
                    if evento.key == pygame.K_RIGHT:
                        cobra.mudar_direcao('DIREITA')
                    elif evento.key == pygame.K_LEFT:
                        cobra.mudar_direcao('ESQUERDA')
                    elif evento.key == pygame.K_UP:
                        cobra.mudar_direcao('CIMA')
                    elif evento.key == pygame.K_DOWN:
                        cobra.mudar_direcao('BAIXO')

        if pausado:
            TELA.fill(PRETO)
            texto_pausa = fonte.render("PAUSADO - Pressione ESPAÇO para continuar", True, BRANCO)
            TELA.blit(texto_pausa, texto_pausa.get_rect(center=(LARGURA_TELA // 2, ALTURA_TELA // 2)))
            pygame.display.update()
            continue

        cobra.mover()

        if cobra.colisao():
            mostrar_game_over(TELA, pontuacao, nome_dificuldade)
            return  # Volta pro menu principal

        if cobra.posicoes[0] == comida.posicao:
            cobra.crescer()
            pontuacao += 1
            comida.gerar_nova_posicao(cobra.posicoes)

        TELA.fill(PRETO)

        # Desenha grade, mas é opicional. Fiquei com preguiça de colocar no menu
        # Caso algum ser veja esse lindo código e não queira grade apenas comente os dois for abaixo
        for x in range(0, LARGURA_TELA, TAMANHO_BLOCO):
            pygame.draw.line(TELA, CINZA, (x, 0), (x, ALTURA_TELA), 1)
        for y in range(0, ALTURA_TELA, TAMANHO_BLOCO):
            pygame.draw.line(TELA, CINZA, (0, y), (LARGURA_TELA, y), 1)

        cobra.desenhar(TELA)
        comida.desenhar(TELA)

        # Placarzinho basicão no topo
        texto_pontos = fonte.render(f"Pontos: {pontuacao} ({nome_dificuldade})", True, BRANCO)
        TELA.blit(texto_pontos, (10, 10))

        pygame.display.update()
        relogio.tick(velocidade)


def tela_menu():
    # Definição das dificuldades se baseando na velocidade. No pygame é FPS
    opcoes = [("Fácil", 6), ("Normal", 10), ("Difícil", 18)]
    selecionado = 1  # Começa apontando para o "Normal"

    while True:
        TELA.fill(PRETO)

        titulo = fonte_titulo.render("JOGO DA COBRINHA", True, VERDE)
        TELA.blit(titulo, titulo_rect := titulo.get_rect(center=(LARGURA_TELA // 2, 100)))

        instrucoes = [
            "Use as SETAS para navegar no menu e jogar",
            "Pressione ESPAÇO para selecionar a dificuldade",
            "Pressione ESPAÇO durante o jogo para Pausar"
        ]

        y_inst = 180
        for inst in instrucoes:
            txt_inst = fonte_pequena.render(inst, True, BRANCO)
            TELA.blit(txt_inst, txt_inst.get_rect(center=(LARGURA_TELA // 2, y_inst)))
            y_inst += 30

        # Renderiza os botões de seleção de dificuldade
        y_opcao = 360
        for i, (nome, _) in enumerate(opcoes):
            if i == selecionado:
                texto_menu = fonte.render(f">  {nome}  <", True, VERDE)
            else:
                texto_menu = fonte.render(f"   {nome}   ", True, BRANCO)

            TELA.blit(texto_menu, texto_menu.get_rect(center=(LARGURA_TELA // 2, y_opcao)))
            y_opcao += 50

        pygame.display.update()

        # Controles do menu
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    selecionado = (selecionado - 1) % len(opcoes)
                elif evento.key == pygame.K_DOWN:
                    selecionado = (selecionado + 1) % len(opcoes)
                elif evento.key == pygame.K_SPACE:
                    # Coleta qual velocidade foi escolhida e inicia a partida
                    nome_dif, vel_dif = opcoes[selecionado]
                    jogo(vel_dif, nome_dif)


if __name__ == "__main__":
    tela_menu()