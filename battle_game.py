import random
import flet as ft

# Configuração do tabuleiro
tamanho_tabuleiro = 8
tamanhos_navios = [3, 2, 2]  # Tamanhos dos navios

# Cores
COR_ACERTO = "#D32F2F"  # Vermelho escuro para acerto
COR_ERRO = "#1976D2"    # Azul forte para erro
COR_PADRAO = "#4B0082"  # Indigo para o fundo
COR_NAVIO = "#388E3C"   # Verde escuro para navios

# Cores do texto
COR_TEXTO_PADRAO = "#FFFFFF"  # Branco para maior contraste
COR_TEXTO_VITORIA = "#00FF00"  # Verde claro para mensagens de vitória
COR_TEXTO_DERROTA = "#FF0000"  # Vermelho para mensagens de derrota

# Função para posicionar navios aleatoriamente
def posicionar_navios(tabuleiro, tamanhos):
    navios = []
    for tamanho in tamanhos:
        while True:
            direcao = random.choice(["horizontal", "vertical"])
            if direcao == "horizontal":
                x = random.randint(0, tamanho_tabuleiro - 1)
                y = random.randint(0, tamanho_tabuleiro - tamanho)
                posicoes = [(x, y + i) for i in range(tamanho)]
            else:
                x = random.randint(0, tamanho_tabuleiro - tamanho)
                y = random.randint(0, tamanho_tabuleiro - 1)
                posicoes = [(x + i, y) for i in range(tamanho)]

            if all(tabuleiro[x][y] == "~" for x, y in posicoes):
                for x, y in posicoes:
                    tabuleiro[x][y] = "N"
                navios.extend(posicoes)
                break
    return navios

# Inicialização dos tabuleiros
def inicializar_tabuleiros():
    tabuleiro = [["~"] * tamanho_tabuleiro for _ in range(tamanho_tabuleiro)]
    navios = posicionar_navios(tabuleiro, tamanhos_navios)
    return tabuleiro, navios

# Função principal do jogo
def main(page: ft.Page):
    page.title = "Batalha Naval com Flet"
    page.padding = 20
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.bgcolor = "#1c1c1c"  # Fundo escuro

    # Inicializa os tabuleiros
    tabuleiro_jogador, navios_jogador = inicializar_tabuleiros()
    tabuleiro_computador, navios_computador = inicializar_tabuleiros()
    jogador_turno = True

    # Função para criar um botão de célula
    def criar_celula(x, y, tabuleiro, navios, is_computador, is_jogador):
        cor_fundo = COR_PADRAO
        if not is_computador and tabuleiro[x][y] == "N":
            cor_fundo = COR_NAVIO

        def ao_clicar(e):
            nonlocal jogador_turno
            # Jogador só pode atacar o tabuleiro do computador
            if is_computador and tabuleiro[x][y] not in ["X", "O"] and jogador_turno:
                if (x, y) in navios:
                    e.control.bgcolor = COR_ACERTO
                    tabuleiro[x][y] = "X"
                    navios.remove((x, y))
                    if verificar_vitoria():
                        return
                else:
                    e.control.bgcolor = COR_ERRO
                    tabuleiro[x][y] = "O"
                    e.control.update()

                # O computador revide imediatamente após o clique
                ataque_computador()

        return ft.Container(
            width=50,
            height=50,
            bgcolor=cor_fundo,
            border_radius=5,
            alignment=ft.alignment.center,
            on_click=ao_clicar,
        )

    # Função de ataque do computador
    def ataque_computador():
        nonlocal jogador_turno
        while True:
            x = random.randint(0, tamanho_tabuleiro - 1)
            y = random.randint(0, tamanho_tabuleiro - 1)
            if tabuleiro_jogador[x][y] not in ["X", "O"]:
                break
        if (x, y) in navios_jogador:
            tabuleiro_jogador[x][y] = "X"
        else:
            tabuleiro_jogador[x][y] = "O"
        jogador_turno = True
        if verificar_vitoria():
            return

    # Função para verificar vitória
    def verificar_vitoria():
        if not navios_computador:
            status_text.value = "Você venceu!"
            status_text.color = COR_TEXTO_VITORIA
            status_text.update()
            return True
        elif not navios_jogador:
            status_text.value = "O computador venceu!"
            status_text.color = COR_TEXTO_DERROTA
            status_text.update()
            return True
        return False

    # Layout do tabuleiro do jogador
    jogador_grid = ft.GridView(
        expand=True,
        max_extent=50,
        spacing=2,
        run_spacing=2,
        controls=[
            criar_celula(x, y, tabuleiro_jogador, navios_jogador, False, True)
            for x in range(tamanho_tabuleiro)
            for y in range(tamanho_tabuleiro)
        ],
    )

    # Layout do tabuleiro do computador
    computador_grid = ft.GridView(
        expand=True,
        max_extent=50,
        spacing=2,
        run_spacing=2,
        controls=[
            criar_celula(x, y, tabuleiro_computador, navios_computador, True, False)
            for x in range(tamanho_tabuleiro)
            for y in range(tamanho_tabuleiro)
        ],
    )

    # Status do jogo
    status_text = ft.Text(
        "Sua vez de atacar!",
        size=20,
        color=COR_TEXTO_PADRAO,  # Texto padrão em branco
    )

    # Layout geral
    page.add(
        ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Seu Tabuleiro", color=COR_TEXTO_PADRAO, size=16),
                        ft.Text("Tabuleiro do Computador", color=COR_TEXTO_PADRAO, size=16),
                    ],
                    alignment="center",
                ),
                ft.Row([jogador_grid, computador_grid], alignment="center"),
                status_text,
            ],
            spacing=20,
            alignment="center",
        )
    )

ft.app(target=main)
