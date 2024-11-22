import random
import flet as ft

def criar_tabuleiro():
    """Cria um tabuleiro 7x7 com um tesouro escondido em uma célula aleatória."""
    grid = [[0 for _ in range(7)] for _ in range(7)]
    tesouro_x, tesouro_y = random.randint(0, 6), random.randint(0, 6)
    grid[tesouro_x][tesouro_y] = 1  # Coloca o tesouro
    return grid

def main(page: ft.Page):
    # Configuração inicial
    page.title = "Encontre o Tesouro"
    page.padding = 20
    page.spacing = 20
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    # Tabuleiro e estado do jogo
    grid = criar_tabuleiro()
    tentativas = ft.Text(value="Tentativas: 0", size=18)
    status = ft.Text(value="Tente encontrar o tesouro!", size=18)
    contador_tentativas = 0

    def criar_celula(x, y):
        """Cria uma célula estilizada do tabuleiro."""
        return ft.ElevatedButton(
            text="❓",
            bgcolor=ft.colors.BLUE_GREY_100,
            color=ft.colors.BLACK,
            on_click=lambda e: verificar_celula(x, y, e.control),
            width=50,
            height=50,
            style=ft.ButtonStyle(
                shape=ft.RoundedRectangleBorder(radius=8),
                overlay_color="#FFFF00AA",  # Cor âmbar com transparência (RGBA)
            ),
        )

    # Função para verificar a célula
    def verificar_celula(x, y, botao):
        nonlocal contador_tentativas
        if grid[x][y] == 1:
            botao.text = "💎"
            botao.bgcolor = ft.colors.LIGHT_GREEN
            botao.disabled = True
            status.value = "🎉 Parabéns! Você encontrou o tesouro!"
            page.update()
        elif grid[x][y] == -1:
            status.value = "⚠️ Você já tentou aqui! Escolha outra célula."
            page.update()
        else:
            botao.text = "❌"
            botao.bgcolor = ft.colors.RED_200
            botao.disabled = True
            grid[x][y] = -1
            contador_tentativas += 1
            tentativas.value = f"Tentativas: {contador_tentativas}"
            status.value = "Nada aqui! Continue procurando..."
            page.update()

    # Criação do tabuleiro gráfico
    tabuleiro = ft.Column(
        [
            ft.Row([criar_celula(x, y) for y in range(7)], spacing=5)
            for x in range(7)
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=5,
    )

    # Adicionar componentes à página
    page.add(
        ft.Text(
            value="Jogo: Encontre o Tesouro",
            size=28,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.INDIGO,
        ),
        status,
        tabuleiro,
        tentativas,
    )

# Executar a aplicação
def start_treasure_game():
    ft.app(target=main)
