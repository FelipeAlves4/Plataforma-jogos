import flet as ft
import random
import sqlite3
import time



# Configuração do banco de dados
def init_db():
    conn = sqlite3.connect("ranking.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ranking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            tentativas INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Função para inserir nova pontuação no ranking
def insert_score(nome, tentativas):
    conn = sqlite3.connect("ranking.db")
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO ranking (nome, tentativas)
        VALUES (?, ?)
    ''', (nome, tentativas))
    conn.commit()
    conn.close()

# Função para obter o ranking ordenado por tentativas
def get_ranking():
    conn = sqlite3.connect("ranking.db")
    cursor = conn.cursor()
    cursor.execute('''
        SELECT nome, tentativas FROM ranking
        ORDER BY tentativas ASC
        LIMIT 10
    ''')
    ranking = cursor.fetchall()
    conn.close()
    return ranking

# Função principal
def main(page: ft.Page):
    page.title = "Desafio do Código: Humano vs Máquina"
    page.bgcolor = "#1c1c1c"
    page.padding = 50
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "adaptive"

    # Inicializa o banco de dados
    init_db()

    # Variáveis globais
    global input_box, result_text, attempts_text, ranking_listview, target_number, user_attempts, name_field
    target_number = random.randint(0, 100)
    user_attempts = 0

    # Título
    title = ft.Text(
        "Desafio do Código: Humano vs Máquina",
        color="#FFFF00",
        size=40,
        weight="bold",
        text_align=ft.TextAlign.CENTER
    )
    # Campo de texto para o nome do jogador
    name_field = ft.TextField(
        label="Nome do Jogador", 
        width=300, 
        text_style=ft.TextStyle(color=ft.colors.WHITE)
    )

    # Caixa de entrada para o chute do número
    input_box = ft.TextField(
        label="Chute um número entre 0 e 100",
        width=300,
        keyboard_type=ft.KeyboardType.NUMBER,
        text_style=ft.TextStyle(color=ft.colors.WHITE)
    )

    # Mensagem de resultado
    result_text = ft.Text(
        value="",
        color="#FFD700",
        size=20,
        weight="bold",
        text_align=ft.TextAlign.CENTER
    )

    # Texto para mostrar o número de tentativas
    attempts_text = ft.Text(
        value=f"Tentativas: {user_attempts}",
        color="#00CED1",
        size=18,
        text_align=ft.TextAlign.CENTER
    )

    # Lista de ranking com rolagem
    ranking_listview = ft.ListView(
        height=300,
        width=400,
        padding=10,
        spacing=10,
        auto_scroll=False
    )

    # Função para processar o chute
    def guess_number(e):
        global user_attempts, target_number  # Define as variáveis como globais

        try:
            user_guess = int(input_box.value)
        except ValueError:
            result_text.value = "Por favor, insira um número válido."
            page.update()
            return

        user_attempts += 1

        if user_guess == target_number:
            result_text.value = f"Parabéns! Você acertou com {user_guess} tentativas!"
            #time.sleep(5)
            result_text.color = ft.colors.LIME_ACCENT
            insert_score(name_field.value, user_attempts)  # Insere no ranking
            target_number = random.randint(0, 100)  # Gera novo número
            user_attempts = 0
            #update_ranking()VERIFICAR SE ESSA FUNÇÃO ESTARÁ DENTRO DO IF.
            #time.sleep(5) TIME SLEEP PARA PARAR EM SEGUNDOS
            #result_text.value = "Insira um número acima, entre 0 e 100."
            #name_field.value ="" LIMPAR A CAIXA DO NOME.
        elif user_guess < target_number:
            result_text.value = "Seu chute foi menor que o número alvo."
            result_text.color = ft.colors.AMBER
        else:
            result_text.value = "Seu chute foi maior que o número alvo."
            result_text.color = ft.colors.RED_ACCENT

        attempts_text.value = f"Tentativas: {user_attempts}"
        input_box.value = ""  # Limpa a caixa de entrada
        update_ranking()

        page.update()

    # Função para atualizar o ranking
    def update_ranking():
        ranking = get_ranking()
        ranking_listview.controls.clear()

        for idx, (nome, tentativas) in enumerate(ranking):
            # Estilo para o ranking
            rank_container = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Text(f"{idx + 1}º", size=20, color=ft.colors.LIME_ACCENT),
                        ft.Text(f"{nome}: {tentativas} tentativas", size=18, color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.colors.BLUE_GREY_900,
                padding=ft.padding.all(10),
                border_radius=ft.border_radius.all(10),
                gradient=ft.LinearGradient(
                    begin=ft.alignment.top_left,
                    end=ft.alignment.bottom_right,
                    colors=[ft.colors.CYAN_400, ft.colors.INDIGO_900]
                ),
                shadow=ft.BoxShadow(
                    spread_radius=1,
                    blur_radius=8,
                    color=ft.colors.BLACK12,
                    offset=ft.Offset(2, 2)
                ),
                alignment=ft.alignment.center,
            )
            ranking_listview.controls.append(rank_container)
        page.update()

    # Botão de enviar
    submit_button = ft.ElevatedButton(
        text="Enviar",
        on_click=guess_number
    )

    # Adiciona os elementos à página
    page.add(
        title,
        name_field,
        input_box,
        submit_button,
        result_text,
        attempts_text,
        ft.Text("Ranking:", color="#00CED1", size=24, weight="bold", text_align=ft.TextAlign.CENTER),
        ranking_listview
    )

    # Atualiza o ranking na primeira execução
    update_ranking()

def start_guess_game():
    ft.app(target=main)  # Inicia o jogo no Flet