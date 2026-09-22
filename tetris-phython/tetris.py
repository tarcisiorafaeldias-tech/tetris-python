import pygame
import random
import sys

# ============================================================
# CONFIGURAÇÕES
# ============================================================

pygame.init()

LARGURA_TELA = 800
ALTURA_TELA = 700

TAMANHO_BLOCO = 30

COLUNAS = 10
LINHAS = 20

LARGURA_TABULEIRO = COLUNAS * TAMANHO_BLOCO
ALTURA_TABULEIRO = LINHAS * TAMANHO_BLOCO

POS_X = 50
POS_Y = 50

FPS = 60

tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
pygame.display.set_caption("Tetris - Python")

relogio = pygame.time.Clock()

# ============================================================
# CORES
# ============================================================

PRETO = (10, 10, 10)
BRANCO = (255, 255, 255)
CINZA = (50, 50, 50)
CINZA_CLARO = (100, 100, 100)

CYAN = (0, 240, 240)
AMARELO = (240, 240, 0)
ROXO = (160, 0, 240)
VERDE = (0, 220, 80)
VERMELHO = (240, 40, 40)
AZUL = (40, 80, 240)
LARANJA = (240, 140, 0)

# ============================================================
# PEÇAS DO TETRIS
# ============================================================

PECAS = {
    "I": {
        "forma": [
            [1, 1, 1, 1]
        ],
        "cor": CYAN
    },

    "O": {
        "forma": [
            [1, 1],
            [1, 1]
        ],
        "cor": AMARELO
    },

    "T": {
        "forma": [
            [0, 1, 0],
            [1, 1, 1]
        ],
        "cor": ROXO
    },

    "S": {
        "forma": [
            [0, 1, 1],
            [1, 1, 0]
        ],
        "cor": VERDE
    },

    "Z": {
        "forma": [
            [1, 1, 0],
            [0, 1, 1]
        ],
        "cor": VERMELHO
    },

    "J": {
        "forma": [
            [1, 0, 0],
            [1, 1, 1]
        ],
        "cor": AZUL
    },

    "L": {
        "forma": [
            [0, 0, 1],
            [1, 1, 1]
        ],
        "cor": LARANJA
    }
}

# ============================================================
# TABULEIRO
# ============================================================

def criar_tabuleiro():
    return [
        [None for _ in range(COLUNAS)]
        for _ in range(LINHAS)
    ]


tabuleiro = criar_tabuleiro()

# ============================================================
# CLASSE DA PEÇA
# ============================================================

class Peca:

    def __init__(self):
        self.tipo = random.choice(list(PECAS.keys()))

        self.forma = [
            linha.copy()
            for linha in PECAS[self.tipo]["forma"]
        ]

        self.cor = PECAS[self.tipo]["cor"]

        self.x = COLUNAS // 2 - len(self.forma[0]) // 2
        self.y = 0

    def rotacionar(self):

        # Transposição
        nova_forma = [
            list(linha)
            for linha in zip(*self.forma[::-1])
        ]

        forma_antiga = self.forma

        self.forma = nova_forma

        if colisao(self):
            self.forma = forma_antiga


# ============================================================
# COLISÃO
# ============================================================

def colisao(peca, dx=0, dy=0):

    for y, linha in enumerate(peca.forma):

        for x, valor in enumerate(linha):

            if valor == 0:
                continue

            novo_x = peca.x + x + dx
            novo_y = peca.y + y + dy

            # Limites laterais
            if novo_x < 0:
                return True

            if novo_x >= COLUNAS:
                return True

            # Fundo
            if novo_y >= LINHAS:
                return True

            # Bloco ocupado
            if novo_y >= 0:
                if tabuleiro[novo_y][novo_x] is not None:
                    return True

    return False


# ============================================================
# FIXAR PEÇA
# ============================================================

def fixar_peca(peca):

    for y, linha in enumerate(peca.forma):

        for x, valor in enumerate(linha):

            if valor == 0:
                continue

            pos_x = peca.x + x
            pos_y = peca.y + y

            if pos_y >= 0:
                tabuleiro[pos_y][pos_x] = peca.cor


# ============================================================
# LIMPAR LINHAS
# ============================================================

def limpar_linhas():

    linhas_removidas = 0

    for y in range(LINHAS - 1, -1, -1):

        if all(tabuleiro[y][x] is not None for x in range(COLUNAS)):

            del tabuleiro[y]

            tabuleiro.insert(
                0,
                [None for _ in range(COLUNAS)]
            )

            linhas_removidas += 1

    return linhas_removidas


# ============================================================
# DESENHAR TABULEIRO
# ============================================================

def desenhar_tabuleiro():

    # Fundo
    pygame.draw.rect(
        tela,
        PRETO,
        (
            POS_X,
            POS_Y,
            LARGURA_TABULEIRO,
            ALTURA_TABULEIRO
        )
    )

    # Grade
    for y in range(LINHAS):

        for x in range(COLUNAS):

            retangulo = pygame.Rect(
                POS_X + x * TAMANHO_BLOCO,
                POS_Y + y * TAMANHO_BLOCO,
                TAMANHO_BLOCO,
                TAMANHO_BLOCO
            )

            pygame.draw.rect(
                tela,
                CINZA,
                retangulo,
                1
            )

            if tabuleiro[y][x] is not None:

                pygame.draw.rect(
                    tela,
                    tabuleiro[y][x],
                    (
                        POS_X + x * TAMANHO_BLOCO + 1,
                        POS_Y + y * TAMANHO_BLOCO + 1,
                        TAMANHO_BLOCO - 2,
                        TAMANHO_BLOCO - 2
                    )
                )


# ============================================================
# DESENHAR PEÇA
# ============================================================

def desenhar_peca(peca):

    for y, linha in enumerate(peca.forma):

        for x, valor in enumerate(linha):

            if valor == 0:
                continue

            pos_x = peca.x + x
            pos_y = peca.y + y

            if pos_y < 0:
                continue

            pygame.draw.rect(
                tela,
                peca.cor,
                (
                    POS_X + pos_x * TAMANHO_BLOCO + 1,
                    POS_Y + pos_y * TAMANHO_BLOCO + 1,
                    TAMANHO_BLOCO - 2,
                    TAMANHO_BLOCO - 2
                )
            )


# ============================================================
# SOMBRA DA PEÇA
# ============================================================

def desenhar_sombra(peca):

    distancia = 0

    while not colisao(peca, dy=distancia + 1):
        distancia += 1

    for y, linha in enumerate(peca.forma):

        for x, valor in enumerate(linha):

            if valor == 0:
                continue

            pos_x = peca.x + x
            pos_y = peca.y + y + distancia

            if pos_y < 0:
                continue

            pygame.draw.rect(
                tela,
                CINZA_CLARO,
                (
                    POS_X + pos_x * TAMANHO_BLOCO + 5,
                    POS_Y + pos_y * TAMANHO_BLOCO + 5,
                    TAMANHO_BLOCO - 10,
                    TAMANHO_BLOCO - 10
                ),
                2
            )


# ============================================================
# PRÓXIMA PEÇA
# ============================================================

def desenhar_proxima(peca):

    fonte = pygame.font.SysFont("Arial", 24, bold=True)

    texto = fonte.render(
        "PRÓXIMA",
        True,
        BRANCO
    )

    tela.blit(
        texto,
        (420, 80)
    )

    tamanho = 25

    for y, linha in enumerate(peca.forma):

        for x, valor in enumerate(linha):

            if valor == 0:
                continue

            pygame.draw.rect(
                tela,
                peca.cor,
                (
                    440 + x * tamanho,
                    120 + y * tamanho,
                    tamanho - 2,
                    tamanho - 2
                )
            )


# ============================================================
# TEXTO
# ============================================================

def desenhar_textos(pontos, linhas, nivel):

    fonte = pygame.font.SysFont(
        "Arial",
        24,
        bold=True
    )

    texto_pontos = fonte.render(
        f"Pontos: {pontos}",
        True,
        BRANCO
    )

    texto_linhas = fonte.render(
        f"Linhas: {linhas}",
        True,
        BRANCO
    )

    texto_nivel = fonte.render(
        f"Nível: {nivel}",
        True,
        BRANCO
    )

    tela.blit(
        texto_pontos,
        (420, 230)
    )

    tela.blit(
        texto_linhas,
        (420, 270)
    )

    tela.blit(
        texto_nivel,
        (420, 310)
    )

    controles = [
        "CONTROLES",
        "",
        "← →  Mover",
        "↓    Descer",
        "↑    Rotacionar",
        "ESPAÇO  Queda",
        "P      Pausar",
        "ESC    Sair"
    ]

    y = 390

    for linha in controles:

        texto = fonte.render(
            linha,
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (420, y)
        )

        y += 30


# ============================================================
# GAME OVER
# ============================================================

def desenhar_game_over():

    fonte_grande = pygame.font.SysFont(
        "Arial",
        50,
        bold=True
    )

    fonte = pygame.font.SysFont(
        "Arial",
        25
    )

    texto = fonte_grande.render(
        "GAME OVER",
        True,
        VERMELHO
    )

    reiniciar = fonte.render(
        "Pressione ENTER para jogar novamente",
        True,
        BRANCO
    )

    tela.blit(
        texto,
        (
            POS_X + 20,
            POS_Y + 250
        )
    )

    tela.blit(
        reiniciar,
        (
            POS_X - 10,
            POS_Y + 320
        )
    )


# ============================================================
# NOVO JOGO
# ============================================================

def novo_jogo():

    global tabuleiro

    tabuleiro = criar_tabuleiro()

    peca_atual = Peca()
    proxima_peca = Peca()

    pontos = 0
    linhas = 0
    nivel = 1

    return (
        peca_atual,
        proxima_peca,
        pontos,
        linhas,
        nivel
    )


# ============================================================
# LOOP PRINCIPAL
# ============================================================

peca_atual, proxima_peca, pontos, linhas, nivel = novo_jogo()

tempo_queda = 0

pausado = False
game_over = False

rodando = True

while rodando:

    delta = relogio.get_rawtime()

    relogio.tick(FPS)

    tempo_queda += delta

    # ========================================================
    # EVENTOS
    # ========================================================

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:

            # Sair
            if evento.key == pygame.K_ESCAPE:
                rodando = False

            # Pausar
            if evento.key == pygame.K_p:

                if not game_over:
                    pausado = not pausado

            # Reiniciar
            if evento.key == pygame.K_RETURN:

                if game_over:

                    (
                        peca_atual,
                        proxima_peca,
                        pontos,
                        linhas,
                        nivel
                    ) = novo_jogo()

                    tempo_queda = 0
                    game_over = False
                    pausado = False

            # =================================================
            # CONTROLES DO JOGO
            # =================================================

            if not pausado and not game_over:

                # Esquerda
                if evento.key == pygame.K_LEFT:

                    if not colisao(
                        peca_atual,
                        dx=-1
                    ):
                        peca_atual.x -= 1

                # Direita
                if evento.key == pygame.K_RIGHT:

                    if not colisao(
                        peca_atual,
                        dx=1
                    ):
                        peca_atual.x += 1

                # Rotacionar
                if evento.key == pygame.K_UP:

                    peca_atual.rotacionar()

                # Queda instantânea
                if evento.key == pygame.K_SPACE:

                    while not colisao(
                        peca_atual,
                        dy=1
                    ):
                        peca_atual.y += 1

                    fixar_peca(peca_atual)

                    quantidade = limpar_linhas()

                    linhas += quantidade

                    if quantidade == 1:
                        pontos += 100

                    elif quantidade == 2:
                        pontos += 300

                    elif quantidade == 3:
                        pontos += 500

                    elif quantidade == 4:
                        pontos += 800

                    nivel = linhas // 10 + 1

                    peca_atual = proxima_peca
                    proxima_peca = Peca()

                    if colisao(peca_atual):
                        game_over = True

                    tempo_queda = 0

    # ========================================================
    # MOVIMENTO AUTOMÁTICO
    # ========================================================

    if not pausado and not game_over:

        velocidade = max(
            80,
            600 - (nivel - 1) * 50
        )

        if tempo_queda >= velocidade:

            if not colisao(
                peca_atual,
                dy=1
            ):

                peca_atual.y += 1

            else:

                fixar_peca(peca_atual)

                quantidade = limpar_linhas()

                linhas += quantidade

                if quantidade == 1:
                    pontos += 100

                elif quantidade == 2:
                    pontos += 300

                elif quantidade == 3:
                    pontos += 500

                elif quantidade == 4:
                    pontos += 800

                nivel = linhas // 10 + 1

                peca_atual = proxima_peca
                proxima_peca = Peca()

                if colisao(peca_atual):
                    game_over = True

            tempo_queda = 0

    # ========================================================
    # DESENHAR
    # ========================================================

    tela.fill((20, 20, 20))

    desenhar_tabuleiro()

    if not game_over:

        desenhar_sombra(peca_atual)
        desenhar_peca(peca_atual)

    desenhar_proxima(proxima_peca)

    desenhar_textos(
        pontos,
        linhas,
        nivel
    )

    # Pausa
    if pausado:

        fonte = pygame.font.SysFont(
            "Arial",
            50,
            bold=True
        )

        texto = fonte.render(
            "PAUSADO",
            True,
            BRANCO
        )

        tela.blit(
            texto,
            (100, 330)
        )

    # Game Over
    if game_over:
        desenhar_game_over()

    pygame.display.update()


pygame.quit()
sys.exit()