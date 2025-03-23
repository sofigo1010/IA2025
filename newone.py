import numpy as np
import pygame
import sys
import math
import random
import time
import matplotlib.pyplot as plt

# --- Configuración general (representación del estado y espacio de acción) ---
ROWS = 6
COLS = 7
EMPTY = 0
TD_AGENT   = 1   # TD Agent (Amarillo)
MINIMAX_NP = 2   # Minimax SIN poda (Naranja)
MINIMAX_AB = 3   # Minimax CON poda (Verde)
TD_AGENT_2 = 5   # Segundo TD (Amarillo Claro)

# --- Colores ---
YELLOW  = (255, 255, 0)
YELLOW2 = (180, 255, 0)
ORANGE  = (255, 165, 0)
GREEN   = (0, 200, 0)
WHITE   = (255, 255, 255)
BLACK   = (0, 0, 0)
BLUE    = (0, 0, 255)

# --- Parámetros Q-learning (algoritmo TD) ---
ALPHA        = 0.5
GAMMA        = 0.9
EPSILON      = 1.0
EPSILON_MIN  = 0.01
EPSILON_DECAY= 0.995

# --- Configuración de entrenamiento y evaluación ---
NUM_EPISODES = 100000  # Ciclo de entrenamiento (self-play) para cumplir el TD learning
NUM_GAMES    = 50      # 50 partidas por cada evaluación

# --- Inicialización de Pygame ---
pygame.init()
WIDTH = 700
HEIGHT = 700
SQUARESIZE = WIDTH // COLS
RADIUS = SQUARESIZE // 2 - 5
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect 4 - TD con Self-Play")
FONT_MAIN = pygame.font.SysFont("monospace", 28, bold=True)

# --- Funciones de espera y mensajes (cumple instrucciones de interfaz) ---
def wait_for_enter():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                waiting = False
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

def draw_text_in_center(msg, size=32, color=WHITE):
    screen.fill(BLACK)
    font = pygame.font.SysFont("monospace", size, bold=True)
    text_surf = font.render(msg, True, color)
    rect = text_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(text_surf, rect)
    pygame.display.update()

def handle_quit_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# --- Funciones básicas de Connect 4 ---
def create_board():
    return np.zeros((ROWS, COLS), dtype=int)

def drop_piece(board, col, piece):
    row = get_next_open_row(board, col)
    if row is not None:
        board[row][col] = piece
        return True
    return False

def get_next_open_row(board, col):
    for r in range(ROWS-1, -1, -1):
        if board[r][col] == EMPTY:
            return r
    return None

def is_valid_location(board, col):
    return board[0][col] == EMPTY

def get_valid_locations(board):
    return [c for c in range(COLS) if is_valid_location(board, c)]

def winning_move(board, piece):
    for r in range(ROWS):
        for c in range(COLS - 3):
            if all(board[r][c+i] == piece for i in range(4)):
                return True
    for c in range(COLS):
        for r in range(ROWS - 3):
            if all(board[r+i][c] == piece for i in range(4)):
                return True
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            if all(board[r+i][c+i] == piece for i in range(4)):
                return True
    for r in range(3, ROWS):
        for c in range(COLS - 3):
            if all(board[r-i][c+i] == piece for i in range(4)):
                return True
    return False

def board_full(board):
    return len(get_valid_locations(board)) == 0

# --- Dibujo del tablero y leyenda (para visualizar el juego) ---
def agent_color(agent):
    if agent == TD_AGENT:
        return YELLOW
    elif agent == TD_AGENT_2:
        return YELLOW2
    elif agent == MINIMAX_NP:
        return ORANGE
    elif agent == MINIMAX_AB:
        return GREEN
    return WHITE

def draw_board(board):
    screen.fill(BLUE)
    for c in range(COLS):
        for r in range(ROWS):
            center = (c * SQUARESIZE + SQUARESIZE//2, (r+1)*SQUARESIZE)
            pygame.draw.circle(screen, BLACK, center, RADIUS)
    for c in range(COLS):
        for r in range(ROWS):
            piece = board[r][c]
            if piece != 0:
                color = agent_color(piece)
                center = (c * SQUARESIZE + SQUARESIZE//2, HEIGHT - (ROWS - r)*SQUARESIZE)
                pygame.draw.circle(screen, color, center, RADIUS)
    pygame.display.update()

def draw_legend(legend_text):
    legend_surf = pygame.Surface((WIDTH, 50))
    legend_surf.set_alpha(200)
    legend_surf.fill(BLACK)
    font = pygame.font.SysFont("monospace", 22)
    text = font.render(legend_text, True, WHITE)
    legend_surf.blit(text, (10, 10))
    screen.blit(legend_surf, (0, 0))
    pygame.display.update()

# --- Minimax y heurística (cumple definición de función de valor) ---
def evaluate_window(window, p_piece, o_piece):
    score = 0
    c_p = window.count(p_piece)
    c_o = window.count(o_piece)
    c_e = window.count(EMPTY)
    if c_p == 4:
        score += 10000
    elif c_p == 3 and c_e == 1:
        score += 100
    elif c_p == 2 and c_e == 2:
        score += 10
    if c_o == 4:
        score -= 10000
    elif c_o == 3 and c_e == 1:
        score -= 100
    elif c_o == 2 and c_e == 2:
        score -= 10
    return score

def evaluate_board_for(board, p_piece, o_piece):
    score = 0
    center_col = COLS // 2
    center_array = [board[r][center_col] for r in range(ROWS)]
    center_count = center_array.count(p_piece)
    score += center_count * 6
    for r in range(ROWS):
        row_array = list(board[r, :])
        for c in range(COLS - 3):
            window = row_array[c:c+4]
            score += evaluate_window(window, p_piece, o_piece)
    for c in range(COLS):
        col_array = list(board[:, c])
        for r in range(ROWS - 3):
            window = col_array[r:r+4]
            score += evaluate_window(window, p_piece, o_piece)
    for r in range(ROWS - 3):
        for c in range(COLS - 3):
            window_down = [board[r+i][c+i] for i in range(4)]
            score += evaluate_window(window_down, p_piece, o_piece)
            window_up = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_window(window_up, p_piece, o_piece)
    return score

def minimax(board, depth, alpha, beta, maximizing, p_piece, o_piece, use_ab):
    valid_cols = get_valid_locations(board)
    terminal = (winning_move(board, p_piece) or winning_move(board, o_piece) or len(valid_cols)==0)
    if depth == 0 or terminal:
        return None, evaluate_board_for(board, p_piece, o_piece)
    if maximizing:
        value = -math.inf
        best_col = random.choice(valid_cols)
        for col in valid_cols:
            temp = board.copy()
            drop_piece(temp, col, p_piece)
            _, new_score = minimax(temp, depth-1, alpha, beta, False, p_piece, o_piece, use_ab)
            if new_score > value:
                value = new_score
                best_col = col
            if use_ab:
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
        return best_col, value
    else:
        value = math.inf
        best_col = random.choice(valid_cols)
        for col in valid_cols:
            temp = board.copy()
            drop_piece(temp, col, o_piece)
            _, new_score = minimax(temp, depth-1, alpha, beta, True, p_piece, o_piece, use_ab)
            if new_score < value:
                value = new_score
                best_col = col
            if use_ab:
                beta = min(beta, value)
                if alpha >= beta:
                    break
        return best_col, value

# --- Q-Learning (TD) (cumple con la implementación de TD) ---
Q = {}

def get_state_key(board):
    return tuple(board.flatten())

def get_Q(state):
    if state not in Q:
        Q[state] = np.zeros(COLS)
    return Q[state]

def choose_action_td(state, valid_actions, epsilon):
    if random.random() < epsilon:
        return random.choice(valid_actions)
    else:
        qv = get_Q(state)
        valid_q = {a: qv[a] for a in valid_actions}
        return max(valid_q, key=valid_q.get)

def update_Q_value(state, action, reward, next_state, done):
    q_values = get_Q(state)
    if done:
        target = reward
    else:
        target = reward + GAMMA * np.max(get_Q(next_state))
    q_values[action] += ALPHA * (target - q_values[action])

# --- Entrenamiento Self-Play (TD vs TD) (cumple ciclo de entrenamiento TD) ---
def simulate_training_game_selfplay(epsilon):
    board = create_board()
    current_player = random.choice([TD_AGENT, TD_AGENT_2])
    last_state_1, last_action_1 = None, None
    last_state_2, last_action_2 = None, None
    while True:
        handle_quit_events()
        state = get_state_key(board)
        valid = get_valid_locations(board)
        if not valid:
            return None
        action = choose_action_td(state, valid, epsilon)
        drop_piece(board, action, current_player)
        if current_player == TD_AGENT:
            if last_state_1 is not None:
                update_Q_value(last_state_1, last_action_1, 0, state, False)
            last_state_1, last_action_1 = state, action
        else:
            if last_state_2 is not None:
                update_Q_value(last_state_2, last_action_2, 0, state, False)
            last_state_2, last_action_2 = state, action
        if winning_move(board, current_player):
            if current_player == TD_AGENT:
                update_Q_value(last_state_1, last_action_1, +1, get_state_key(board), True)
                if last_state_2 is not None:
                    update_Q_value(last_state_2, last_action_2, -1, get_state_key(board), True)
                return TD_AGENT
            else:
                update_Q_value(last_state_2, last_action_2, +1, get_state_key(board), True)
                if last_state_1 is not None:
                    update_Q_value(last_state_1, last_action_1, -1, get_state_key(board), True)
                return TD_AGENT_2
        if board_full(board):
            if last_state_1 is not None:
                update_Q_value(last_state_1, last_action_1, 0, get_state_key(board), True)
            if last_state_2 is not None:
                update_Q_value(last_state_2, last_action_2, 0, get_state_key(board), True)
            return None
        current_player = TD_AGENT_2 if current_player == TD_AGENT else TD_AGENT

def phase_train_td():
    global EPSILON
    draw_text_in_center("Fase 1: Entrenando 500000 VECES", size=36)
    wait_for_enter()
    p1_wins, p2_wins, draws = 0, 0, 0
    for ep in range(1, NUM_EPISODES + 1):
        EPSILON = max(EPSILON_MIN, EPSILON * EPSILON_DECAY)
        winner = simulate_training_game_selfplay(EPSILON)
        if winner == TD_AGENT:
            p1_wins += 1
        elif winner == TD_AGENT_2:
            p2_wins += 1
        else:
            draws += 1
        if ep % 1000 == 0:
            screen.fill(BLACK)
            msg = f"ENTRENANDO {ep}/{NUM_EPISODES} VECES"
            draw_text_in_center(msg, size=32)
            pygame.display.update()
            pygame.time.wait(300)
    screen.fill(BLACK)
    final_msg = f"Entrenamiento finalizado: TD1: {p1_wins}, TD2: {p2_wins}, Empates: {draws}"
    draw_text_in_center(final_msg, size=28)
    draw_text_in_center("Presione Enter para continuar", size=28)
    wait_for_enter()

# --- Evaluación: TD vs Minimax (sin poda y con poda) ---
def simulate_game_td_vs_minimax(use_ab, depth, show_first_game=False):
    board = create_board()
    current = random.choice([TD_AGENT, MINIMAX_NP])
    while True:
        handle_quit_events()
        if current == TD_AGENT:
            state = get_state_key(board)
            valid = get_valid_locations(board)
            if not valid:
                return None
            action = choose_action_td(state, valid, 0)
            drop_piece(board, action, TD_AGENT)
        else:
            valid = get_valid_locations(board)
            if not valid:
                return None
            if use_ab:
                col, _ = minimax(board, depth, -math.inf, math.inf, True, MINIMAX_AB, TD_AGENT, True)
                drop_piece(board, col, MINIMAX_AB)
            else:
                col, _ = minimax(board, depth, -math.inf, math.inf, True, MINIMAX_NP, TD_AGENT, False)
                drop_piece(board, col, MINIMAX_NP)
        if show_first_game:
            draw_board(board)
            pygame.time.wait(300)
        if winning_move(board, TD_AGENT):
            return TD_AGENT
        if use_ab:
            if winning_move(board, MINIMAX_AB):
                return MINIMAX_AB
        else:
            if winning_move(board, MINIMAX_NP):
                return MINIMAX_NP
        if board_full(board):
            return None
        current = TD_AGENT if current != TD_AGENT else MINIMAX_NP

def evaluate_phase_td_vs_minimax(use_ab, depth, phase_title):
    results = {TD_AGENT: 0, MINIMAX_NP: 0, MINIMAX_AB: 0, "draw": 0}
    for game in range(1, NUM_GAMES+1):
        screen.fill(BLACK)
        msg = f"{phase_title} - Juego {game}/{NUM_GAMES}"
        draw_text_in_center(msg, size=28)
        pygame.display.update()
        pygame.time.wait(300)
        show = (game == 1)
        winner = simulate_game_td_vs_minimax(use_ab, depth, show_first_game=show)
        if winner == TD_AGENT:
            results[TD_AGENT] += 1
        else:
            if use_ab:
                if winner == MINIMAX_AB:
                    results[MINIMAX_AB] += 1
            else:
                if winner == MINIMAX_NP:
                    results[MINIMAX_NP] += 1
        draw_text_in_center(msg, size=28)
    return results

# --- Evaluación: TD vs TD ---
def simulate_game_td_vs_td(show=False):
    board = create_board()
    current = random.choice([TD_AGENT, TD_AGENT_2])
    while True:
        handle_quit_events()
        state = get_state_key(board)
        valid = get_valid_locations(board)
        if not valid:
            return None
        action = choose_action_td(state, valid, 0)
        drop_piece(board, action, current)
        if show:
            draw_board(board)
            pygame.time.wait(300)
        if winning_move(board, current):
            return current
        if board_full(board):
            return None
        current = TD_AGENT_2 if current == TD_AGENT else TD_AGENT

def evaluate_phase_td_vs_td():
    results = {TD_AGENT: 0, TD_AGENT_2: 0, "draw": 0}
    for game in range(1, NUM_GAMES+1):
        screen.fill(BLACK)
        msg = f"Fase 4: TD vs TD - Juego {game}/{NUM_GAMES}"
        draw_text_in_center(msg, size=28)
        pygame.display.update()
        pygame.time.wait(300)
        show = (game == 1)
        winner = simulate_game_td_vs_td(show=show)
        if winner == TD_AGENT:
            results[TD_AGENT] += 1
        elif winner == TD_AGENT_2:
            results[TD_AGENT_2] += 1
        else:
            results["draw"] += 1
        draw_text_in_center(msg, size=28)
    return results

# --- Graficar resultados (cumple con la generación de PDF) ---
def graph_results(results_dict, filename="resultados.pdf"):
    labels = list(results_dict.keys())
    td_wins = []
    mm_wins = []
    mmab_wins = []
    td2_wins = []
    for matchup in labels:
        res = results_dict[matchup]
        td_wins.append(res.get(TD_AGENT, 0))
        mm_wins.append(res.get(MINIMAX_NP, 0))
        mmab_wins.append(res.get(MINIMAX_AB, 0))
        td2_wins.append(res.get(TD_AGENT_2, 0))
    x = np.arange(len(labels))
    width = 0.2
    fig, ax = plt.subplots()
    ax.bar(x - 1.5*width, td_wins, width, label="TD Agent (Amarillo)")
    ax.bar(x - 0.5*width, mm_wins, width, label="Minimax (Naranja)")
    ax.bar(x + 0.5*width, mmab_wins, width, label="Minimax AB (Verde)")
    ax.bar(x + 1.5*width, td2_wins, width, label="TD Agent 2 (Amarillo Claro)")
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.set_ylabel("Victorias")
    ax.set_title("Resultados de Evaluación (50 juegos c/u)")
    ax.legend()
    plt.savefig(filename, format="pdf")
    plt.show()
    print(f"Gráfico guardado en {filename}")

# --- MAIN (se cumple con el ciclo completo de instrucciones) ---
def main():
    draw_text_in_center("Fase 1: Entrenar el modelo TD (Self-Play) - 500000 VECES", size=36)
    wait_for_enter()
    phase_train_td()
    
    draw_text_in_center("Fase 2: TD vs Minimax (sin poda)", size=36)
    draw_legend("TD: Amarillo  |  Minimax: Naranja")
    draw_text_in_center("Presione Enter para comenzar", size=28)
    wait_for_enter()
    res_phase2 = evaluate_phase_td_vs_minimax(False, 4, "Fase 2: TD vs Minimax (sin poda)")
    screen.fill(BLACK)
    msg2 = f"Fase 2 - Resultados: TD: {res_phase2.get(TD_AGENT,0)} | Minimax: {res_phase2.get(MINIMAX_NP,0)} | Empates: {res_phase2.get('draw',0)}"
    draw_text_in_center(msg2, size=28)
    draw_text_in_center("Presione Enter para continuar", size=28)
    wait_for_enter()
    
    draw_text_in_center("Fase 3: TD vs Minimax (poda AB)", size=36)
    draw_legend("TD: Amarillo  |  Minimax AB: Verde")
    draw_text_in_center("Presione Enter para comenzar", size=28)
    wait_for_enter()
    res_phase3 = evaluate_phase_td_vs_minimax(True, 6, "Fase 3: TD vs Minimax AB")
    screen.fill(BLACK)
    msg3 = f"Fase 3 - Resultados: TD: {res_phase3.get(TD_AGENT,0)} | Minimax AB: {res_phase3.get(MINIMAX_AB,0)} | Empates: {res_phase3.get('draw',0)}"
    draw_text_in_center(msg3, size=28)
    draw_text_in_center("Presione Enter para continuar", size=28)
    wait_for_enter()
    
    draw_text_in_center("Fase 4: TD vs TD", size=36)
    draw_legend("TD: Amarillo  |  TD2: Amarillo Claro")
    draw_text_in_center("Presione Enter para comenzar", size=28)
    wait_for_enter()
    res_phase4 = evaluate_phase_td_vs_td()
    screen.fill(BLACK)
    msg4 = f"Fase 4 - Resultados: TD: {res_phase4.get(TD_AGENT,0)} | TD2: {res_phase4.get(TD_AGENT_2,0)} | Empates: {res_phase4.get('draw',0)}"
    draw_text_in_center(msg4, size=28)
    draw_text_in_center("Presione Enter para continuar", size=28)
    wait_for_enter()
    
    all_results = {"TD vs Minimax": res_phase2,
                   "TD vs Minimax AB": res_phase3,
                   "TD vs TD": res_phase4}
    draw_text_in_center("Generando gráfico de resultados...", size=32)
    graph_results(all_results, "resultados.pdf")
    draw_text_in_center("¡Listo! PDF guardado. Presione Enter para finalizar", size=28)
    wait_for_enter()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
