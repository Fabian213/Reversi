import copy
import tkinter as tk
import tkinter.messagebox

# Define la clase para el tablero de Reversi


class ReversiBoard:
    def __init__(self, tamano_tablero, dificultad):
        self.tamano_tablero = tamano_tablero
        self.board = [[' ' for _ in range(tamano_tablero)] for _ in range(tamano_tablero)]
        self.initialize_board()
        self.current_player = 'X'  # El jugador siempre será 'X'
        self.dificultad = dificultad
        self.generando_jugadas = False

    def initialize_board(self):
        middle = self.tamano_tablero // 2
        # Coloca las fichas blancas y negras en las posiciones iniciales
        self.board[middle - 1][middle - 1] = 'O'  # Ficha blanca arriba a la izquierda
        self.board[middle][middle] = 'O'  # Ficha blanca abajo a la derecha
        self.board[middle - 1][middle] = 'X'  # Ficha negra abajo a la izquierda
        self.board[middle][middle - 1] = 'X'  # Ficha negra arriba a la derecha

    def is_valid_move(self, x, y, player):
        if self.board[x][y] != ' ':
            # La casilla ya está ocupada, no es un movimiento válido
            return False

        # Definir las direcciones en las que se pueden voltear las fichas
        direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

        for dx, dy in direcciones:
            # Iniciar desde la posición actual y moverse en la dirección especificada
            i, j = x + dx, y + dy
            fichas_para_voltear = []

            while 0 <= i < self.tamano_tablero and 0 <= j < self.tamano_tablero:
                if self.board[i][j] == ' ':
                    break
                if self.board[i][j] == player:
                    if fichas_para_voltear:
                        # Se encontró al menos una ficha del jugador en la dirección
                        return True
                    break
                else:
                    # La ficha en esta dirección pertenece al oponente
                    fichas_para_voltear.append((i, j))
                i += dx
                j += dy

        return False

    def permite_salto(self, coordenada: list, color: int) -> bool:
        """Esta función evalúa si al posicionar una ficha en la coordenada de tablero pasada como parámetro es posible
        saltar al menos una ficha del rival. Para esto, se evalúan las 8 direcciones posibles hasta llegar al límite del
        tablero en busca de una o varias fichas del color contrario seguidas por una ficha del color que se pasa como
        parámetro.

        En caso de encontrar dicha situación, la función convertirá automáticamente todas las fichas del color contrario
        al color pasado como parámetro. Una vez analizadas las 8 direcciones, la función retornará verdadero si en al
        menos una dirección se pudo realizar el salto, de lo contrario, retornará falso"""

        # Coordenadas
        fila = coordenada[0]
        columna = coordenada[1]

        # Lista de direcciones en las que se puede saltar
        key = [False] * 8

        # La coordenada en donde se desea posicionar la ficha debe ser adyacente a alguna ficha ya puesta
        if self.es_adyacente(coordenada):

            # Por cada dirección se analiza si permite el salto

            # Abajo
            aux = columna + 1
            if 0 < aux < 5:
                if color == 1:
                    if self.board[fila][aux] == 2:
                        for i in range(5 - aux):
                            if self.board[fila][aux + i + 1] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, aux], [fila, aux + i + 1], "derecha", 1)
                                key[0] = True
                if color == 2:
                    if self.board[fila][aux] == 1:
                        for i in range(5 - aux):
                            if self.board[fila][aux + i + 1] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, aux], [fila, aux + i + 1], "derecha", 2)
                                key[0] = True

            # Arriba
            aux = columna - 1
            if 0 < aux < 5:
                if color == 1:
                    if self.board[fila][aux] == 2:
                        for i in range(aux):
                            if self.board[fila][aux - i - 1] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, aux], [fila, aux - i - 1], "izquierda", 1)
                                key[1] = True
                if color == 2:
                    if self.board[fila][aux] == 1:
                        for i in range(aux):
                            if self.board[fila][aux - i - 1] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, aux], [fila, aux - i - 1], "izquierda", 2)
                                key[1] = True

            # Derecha
            aux = fila + 1
            if 0 < aux < 5:
                if color == 1:
                    if self.board[aux][columna] == 2:
                        for i in range(5 - aux):
                            if self.board[aux + i + 1][columna] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux + i + 1, columna], "abajo", 1)
                                key[2] = True
                if color == 2:
                    if self.board[aux][columna] == 1:
                        for i in range(5 - aux):
                            if self.board[aux + i + 1][columna] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux + i + 1, columna], "abajo", 2)
                                key[2] = True

            # Izquierda
            aux = fila - 1
            if 0 < aux < 5:
                if color == 1:
                    if self.board[aux][columna] == 2:
                        for i in range(aux):
                            if self.board[aux - i - 1][columna] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, columna], "arriba", 1)
                                key[3] = True
                if color == 2:
                    if self.board[aux][columna] == 1:
                        for i in range(aux):
                            if self.board[aux - i - 1][columna] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, columna], "arriba", 2)
                                key[3] = True

            # Abajo-Izquierda
            aux = fila - 1
            aux2 = columna + 1
            if 0 < aux < 5 and 0 < aux2 < 5:
                par = [aux, 5 - aux2]
                if color == 1:
                    rango = min(par)
                    if self.board[aux][aux2] == 2:
                        for i in range(rango):
                            if self.board[aux - i - 1][aux2 + i + 1] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, aux2 + i + 1], "arriba-derecha", 1)
                                key[4] = True
                if color == 2:
                    rango = min(par)
                    if self.board[aux][aux2] == 1:
                        for i in range(rango):
                            if self.board[aux - i - 1][aux2 + i + 1] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, aux2 + i + 1], "arriba-derecha", 2)
                                key[4] = True

            # Arriba-Izquierda
            aux = fila - 1
            aux2 = columna - 1
            if 0 < aux < 5 and 0 < aux2 < 5:
                par = [aux, aux2]
                if color == 1:
                    rango = min(par)
                    if self.board[aux][aux2] == 2:
                        for i in range(rango):
                            if self.board[aux - i - 1][aux2 - i - 1] == 1:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, aux2 - i - 1], "arriba-izquierda", 1)
                                key[5] = True
                if color == 2:
                    rango = min(par)
                    if self.board[aux][aux2] == 1:
                        for i in range(rango):
                            if self.board[aux - i - 1][aux2 - i - 1] == 2:
                                if not self.generando_jugadas:
                                    self.convertir([fila, columna], [aux - i - 1, aux2 - i - 1], "arriba-izquierda", 2)
                                key[5] = True

                    # Abajo-Derecha
                aux = fila + 1
                aux2 = columna + 1
                if 0 < aux < 5 and 0 < aux2 < 5:
                    par = [5 - aux, 5 - aux2]
                    if color == 1:
                        rango = min(par)
                        if self.board[aux][aux2] == 2:
                            for i in range(rango):
                                if self.board[aux + i + 1][aux2 + i + 1] == 1:
                                    if not self.generando_jugadas:
                                        self.convertir([fila, columna], [aux + i + 1, aux2 + i + 1], "abajo-derecha", 1)
                                    key[6] = True
                    if color == 2:
                        rango = min(par)
                        if self.board[aux][aux2] == 1:
                            for i in range(rango):
                                if self.board[aux + i + 1][aux2 + i + 1] == 2:
                                    if not self.generando_jugadas:
                                        self.convertir([fila, columna], [aux + i + 1, aux2 + i + 1], "abajo-derecha", 2)
                                    key[6] = True

                # Arriba-Derecha
                aux = fila + 1
                aux2 = columna - 1
                if 0 < aux < 5 and 0 < aux2 < 5:
                    par = [5 - aux, aux2]
                    if color == 1:
                        rango = min(par)
                        if self.board[aux][aux2] == 2:
                            for i in range(rango):
                                if self.board[aux + i + 1][aux2 - i - 1] == 1:
                                    if not self.generando_jugadas:
                                        self.convertir([fila, columna], [aux + i + 1, aux2 - i - 1], "abajo-izquierda",
                                                       1)
                                    key[7] = True
                    if color == 2:
                        rango = min(par)
                        if self.board[aux][aux2] == 1:
                            for i in range(rango):
                                if self.board[aux + i + 1][aux2 - i - 1] == 2:
                                    if not self.generando_jugadas:
                                        self.convertir([fila, columna], [aux + i + 1, aux2 - i - 1], "abajo-izquierda",
                                                       2)
                                    key[7] = True

                if True in key:
                    return True
                else:
                    return False
            else:
                return False

    def esta_vacia(self, coordenada):
        """Esta función verifica si la coordenada del tablero en donde se desea poner una ficha no está ocupada."""
        fila, columna = coordenada[0], coordenada[1]
        if self.board[fila][columna] == ' ':
            return True
        else:
            return False

    def es_adyacente(self, coordenada):
        x = coordenada[0]  # FILA
        y = coordenada[1]  # COLUMNA

        # Verificar si la coordenada está dentro de los límites del tablero
        if 0 <= x < self.tamano_tablero and 0 <= y < self.tamano_tablero:
            # Coordenada dentro del tablero, verifique si alguna casilla adyacente tiene una ficha
            direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

            for dx, dy in direcciones:
                nueva_x = x + dx
                nueva_y = y + dy

                if 0 <= nueva_x < self.tamano_tablero and 0 <= nueva_y < self.tamano_tablero \
                        and self.board[nueva_x][nueva_y] != ' ':
                    return True

        return False

    def convertir(self, inicio, fin, direccion, color):
        """Esta función trabaja en conjunto con la función Permite_salto().
        Se encarga de transformar las fichas de un color al color que se le pase como parámetro.
        No realiza ningún tipo de análisis, solo realiza la transformación."""

        # Coordenada de inicio
        x1, y1 = inicio

        # Coordenada de destino
        x2, y2 = fin

        if direccion == "derecha":
            while y1 != y2:
                self.board[x1][y1] = color
                y1 += 1
        elif direccion == "izquierda":
            while y1 != y2:
                self.board[x1][y1] = color
                y1 -= 1
        elif direccion == "arriba":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 -= 1
        elif direccion == "abajo":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 += 1
        elif direccion == "arriba-derecha":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 -= 1
                y1 += 1
        elif direccion == "arriba-izquierda":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 -= 1
                y1 -= 1
        elif direccion == "abajo-derecha":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 += 1
                y1 += 1
        elif direccion == "abajo-izquierda":
            while x1 != x2:
                self.board[x1][y1] = color
                x1 += 1
                y1 -= 1

    def jugar(self, coordenada, color):
        """Esta función sirve para posicionar la ficha en el tablero.
        Utiliza las tres anteriores funciones para verificar que es posible posicionar la ficha del color que se le
        pase como parámetro."""

        if self.esta_vacia(coordenada) and self.es_adyacente(coordenada) and self.permite_salto(coordenada, color):
            self.board[coordenada[0]][coordenada[1]] = color
            return True
        else:
            return False

    def generador_jugadas_validas(self, color):
        """ Esta función retornará una lista con las posibles jugadas para el color que se le pase como parámetro.
        Para hacerlo, utiliza las funciones que usa la función Jugar() salvo la función convertir(),
        pues no queremos modificar el tablero de juego mientras llenamos la lista."""

        # Se fija esta variable en True para que la función Permite_salto() no convierta ninguna ficha del tablero
        self.generando_jugadas = True
        jugadas_posibles = []

        for i in range(self.tamano_tablero):
            for j in range(self.tamano_tablero):
                if self.esta_vacia([i, j]) and self.es_adyacente([i, j]) and self.permite_salto([i, j], color):
                    jugadas_posibles.append([i, j])

        self.generando_jugadas = False
        return jugadas_posibles

    def evaluar(self, tablero):
        """Esta función calcula la utilidad de un estado del juego en función del tablero proporcionado."""
        blancas = 0  # Número de fichas blancas en el tablero
        negras = 0  # Número de fichas negras en el tablero

        for i in range(len(tablero)):
            for j in range(len(tablero[0])):
                if tablero[i][j] == 1:
                    blancas += 1
                elif tablero[i][j] == 2:
                    negras += 1

        utilidad = negras - blancas
        return utilidad

    def estado_final(self, tablero, profundidad):
        """Esta función verifica si se ha alcanzado un estado terminal o la profundidad deseada."""
        if self.tablero_completo(tablero) or profundidad == self.dificultad:
            return True
        else:
            return False

    def devolver_estado(self, estado):
        """Se utiliza en el algoritmo de minimax o alfabeta para devolver el tablero al estado previo del análisis
        de la jugada."""
        for i in range(6):
            for j in range(6):
                # Usamos deepcopy para que el minimax o alfabeta realice cambios en copias y no en el tablero
                self.board[i][j] = copy.deepcopy(estado[i][j])

    def puede_jugar(self, jugador):
        """Evalúa si el jugador puede seguir jugando dado un estado del tablero."""

        if jugador == 1:
            jugadas_posibles = self.generador_jugadas_validas(1)
        else:
            jugadas_posibles = self.generador_jugadas_validas(2)

        return len(jugadas_posibles) > 0

    def tablero_completo(self, matriz):
        """Evalúa si ya se ha llenado todo el tablero de juego."""
        for i in range(6):
            for j in range(6):
                if matriz[i][j] == 0:
                    return False
        return True

    def contar_fichas(self, color):
        """Cuenta el número de fichas del color que se le pase como parámetro en un estado específico del juego."""
        fichas = 0
        if color == 1:
            for i in range(6):
                for j in range(6):
                    if self.board[i][j] == 1:
                        fichas += 1
        if color == 2:
            for i in range(6):
                for j in range(6):
                    if self.board[i][j] == 2:
                        fichas += 1
        return fichas

    def get_score(self):
        """Obtiene la puntuación de los jugadores."""
        player_x_score = sum(row.count('X') for row in self.board)
        player_o_score = sum(row.count('O') for row in self.board)
        return player_x_score, player_o_score

    def resetear_tablero(self):
        for i in range(6):
            for j in range(6):
                self.board[i][j] = 0
        self.board[2][2] = 1
        self.board[3][3] = 1
        self.board[3][2] = 2
        self.board[2][3] = 2

    def make_move(self, x, y, player):
        # Verificar si el movimiento es válido
        if self.is_valid_move(x, y, player):
            # Actualizar la casilla con el color del jugador actual
            self.board[x][y] = player

            # Definir las direcciones en las que se pueden voltear las fichas
            direcciones = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]

            for dx, dy in direcciones:
                i, j = x + dx, y + dy
                fichas_para_voltear = []

                while 0 <= i < self.tamano_tablero and 0 <= j < self.tamano_tablero:
                    if self.board[i][j] == ' ':
                        break
                    if self.board[i][j] == player:
                        if fichas_para_voltear:
                            # Se encontró al menos una ficha del jugador en la dirección
                            for f, c in fichas_para_voltear:
                                self.board[f][c] = player
                        break
                    else:
                        # La ficha en esta dirección pertenece al oponente
                        fichas_para_voltear.append((i, j))
                    i += dx
                    j += dy

            return True
        return False

    def is_game_over(self):
        # El juego termina cuando no hay más movimientos válidos para ningún jugador o el tablero está lleno
        return not self.puede_jugar(1) and not self.puede_jugar(2) or self.tablero_completo(self.board)

    def get_winner(self):
        player_x_score, player_o_score = self.get_score()

        if player_x_score > player_o_score:
            return 'Jugador X'
        elif player_o_score > player_x_score:
            return 'Jugador O'
        else:
            return 'Empate'


# Define la clase para el agente de Reversi
class ReversiAgent:
    def __init__(self, player):
        self.player = player

    def make_move(self):
        global board, current_player

        if board is not None and not board.is_game_over() and current_player == self.player:
            # Obtener las jugadas posibles para la IA
            jugadas_posibles = board.generador_jugadas_validas(2)

            if jugadas_posibles:
                # Inicializar variables para el algoritmo alfa-beta
                profundidad_maxima = 4  # Puedes ajustar la profundidad según la dificultad deseada
                mejor_movimiento = None
                mejor_valor = float('-inf')  # Inicializa con un valor muy bajo
                alfa = float('-inf')
                beta = float('inf')

                # Iterar a través de las jugadas posibles y aplicar el algoritmo alfa-beta
                for jugada in jugadas_posibles:
                    # Realizar el movimiento en una copia del tablero
                    board_copia = copy.deepcopy(board)
                    board_copia.jugar(jugada[0], jugada[1], 2)

                    # Calcular el valor del movimiento
                    valor = alfabeta(board_copia, board_copia.board, 0, -1, alfa, beta, [], [])[0]

                    # Actualizar el mejor movimiento y alfa
                    if valor > mejor_valor:
                        mejor_movimiento = jugada
                        alfa = valor

                # Realizar el mejor movimiento encontrado por la IA
                if mejor_movimiento:
                    board.jugar(mejor_movimiento[0], mejor_movimiento[1], 2)

                # Actualizar el tablero y cambia al siguiente jugador
                dibujar_tablero(board.board)
                if not board.is_game_over():
                    cambiar_jugador()
                else:
                    # El juego ha terminado, muestra el ganador y la puntuación
                    ganador = board.get_winner()
                    puntuacion_player_x, puntuacion_player_o = board.get_score()
                    mensaje = f"¡El ganador es {ganador}!\n"
                    mensaje += f"Puntuación - Jugador X: {puntuacion_player_x}\n"
                    mensaje += f"Puntuación - Jugador O: {puntuacion_player_o}"
                    tk.messagebox.showinfo("Juego Terminado", mensaje)

                    # Puedes agregar aquí cualquier otra acción que desees realizar al finalizar el juego

        return mejor_movimiento


# Función para manejar los clics en el lienzo (canvas)
def handle_click(event):
    global board, current_player

    if board is not None and not board.is_game_over() and current_player == 'X':
        # Obtener las coordenadas del clic en el lienzo
        x, y = event.x, event.y
        # Calcular la fila y columna en función de las coordenadas del clic
        fila = y // CASILLA_TAMANO
        columna = x // CASILLA_TAMANO

        # Verificar si el movimiento es válido y realizarlo
        if board.make_move(fila, columna, board.current_player):
            # Actualizar el tablero y cambiar al siguiente jugador
            dibujar_tablero(board.board)
            if not board.is_game_over():
                cambiar_jugador()

                # Después de que el jugador humano haya realizado su movimiento
                if not board.is_game_over() and current_player == 'X':
                    # Llama a la función alfabeta() para calcular el mejor movimiento para el jugador humano
                    mejor_movimiento = alfabeta(board, board.board, 0, -1)
                    board.make_move(mejor_movimiento[1][0], mejor_movimiento[1][1], board.current_player)

            else:
                # El juego ha terminado, muestra el ganador y la puntuación
                ganador = board.get_winner()
                puntuacion_player_x, puntuacion_player_o = board.get_score()
                mensaje = f"¡El ganador es {ganador}!\n"
                mensaje += f"Puntuación - Jugador X: {puntuacion_player_x}\n"
                mensaje += f"Puntuación - Jugador O: {puntuacion_player_o}"
                tk.messagebox.showinfo("Juego Terminado", mensaje)


# Función para cambiar al siguiente jugador
def cambiar_jugador():
    global current_player
    current_player = 'X' if current_player == 'O' else 'O'
    # Actualizar la etiqueta del jugador actual en la interfaz gráfica
    etiqueta_jugador.config(text=f"Jugador Actual: {current_player}")


# Función para iniciar el juego con las opciones seleccionadas
def iniciar_juego():
    global board, current_player
    ia = ReversiAgent('O')  # 'O' representa al jugador controlado por la IA

    tamano_seleccionado = tamano_var.get()
    dificultad_seleccionada = dificultad_var.get()
    ayuda_habilitada = ayuda_var.get()

    if not isinstance(tamano_seleccionado, str):
        tamano_seleccionado = str(tamano_seleccionado)

    # Lógica para iniciar el juego con las opciones seleccionadas
    # Debes implementar esto según las necesidades de tu juego

    # Ejemplo de impresión de las opciones seleccionadas
    print("Tamaño del tablero:", tamano_seleccionado)
    print("Nivel de dificultad:", dificultad_seleccionada)
    print("Ayuda habilitada:", ayuda_habilitada)

    # Configurar la dificultad del juego en función de la selección
    if dificultad_seleccionada == "Fácil":
        # Configura el juego para la dificultad fácil
        # (por ejemplo, establece valores bajos para la IA)
        ia.profundidad_maxima = 1
    elif dificultad_seleccionada == "Intermedio":
        # Configura el juego para la dificultad intermedia
        # (ajusta los valores de la IA según la dificultad)
        ia.profundidad_maxima = 2
    elif dificultad_seleccionada == "Difícil":
        # Configura el juego para la dificultad difícil
        # (usa valores más altos para la IA)
        ia.profundidad_maxima = 3

    # Crear el tablero y mostrarlo al iniciar el juego
    tamano_tablero = int(tamano_seleccionado.split('x')[0])
    board = ReversiBoard(tamano_tablero, dificultad_seleccionada)  # Pasar dificultad_seleccionada como argumento
    current_player = 'X'
    dibujar_tablero(board.board)
    etiqueta_jugador.config(text=f"Jugador Actual: {board.current_player}")

    # También puedes restablecer el tablero aquí si es necesario
    # board.resetear_tablero()  # Agrega esta línea si deseas restablecer el tablero al inicio del juego

    # Obtener el mejor movimiento para la IA
    mejor_movimiento = ia.make_move()

    # Realizar el movimiento de la IA
    board.make_move(mejor_movimiento[0], mejor_movimiento[1], 2)

    # Actualizar el tablero y cambiar al siguiente jugador
    dibujar_tablero(board.board)
    if not board.is_game_over():
        cambiar_jugador()
    else:
        # El juego ha terminado, muestra el ganador y la puntuación
        ganador = board.get_winner()
        puntuacion_player_x, puntuacion_player_o = board.get_score()
        mensaje = f"¡El ganador es {ganador}!\n"
        mensaje += f"Puntuación - Jugador X: {puntuacion_player_x}\n"
        mensaje += f"Puntuación - Jugador O: {puntuacion_player_o}"
        tk.messagebox.showinfo("Juego Terminado", mensaje)

    # Puedes agregar aquí cualquier otra acción que desees realizar al finalizar el juego


# Función para crear el tablero de Reversi con un tamaño específico
def crear_tablero(tamano):
    tablero = [[' ' for _ in range(tamano)] for _ in range(tamano)]
    tablero[tamano // 2 - 1][tamano // 2 - 1] = 'W'
    tablero[tamano // 2][tamano // 2] = 'W'
    tablero[tamano // 2 - 1][tamano // 2] = 'B'
    tablero[tamano // 2][tamano // 2 - 1] = 'B'
    return tablero


# Función para dibujar el tablero en el lienzo
def dibujar_tablero(tablero):
    global board

    canvas.delete("all")  # Borrar el contenido anterior en el lienzo

    tamano_tablero = len(tablero)  # Obtener el tamaño del tablero
    tamano_ventana = min(canvas.winfo_width(), canvas.winfo_height())  # Obtener el tamaño del lienzo

    tamano_casilla = tamano_ventana // tamano_tablero  # Calcular el tamaño de la casilla

    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            x0 = columna * tamano_casilla
            y0 = fila * tamano_casilla
            x1 = x0 + tamano_casilla
            y1 = y0 + tamano_casilla
            color_fondo = "green" if (fila + columna) % 2 == 0 else "dark green"
            canvas.create_rectangle(x0, y0, x1, y1, fill=color_fondo, outline="black")

            # Dibuja las fichas en función de los valores del tablero
            if tablero[fila][columna] == 'X':
                canvas.create_oval(x0, y0, x1, y1, fill="black")
            elif tablero[fila][columna] == 'O':
                canvas.create_oval(x0, y0, x1, y1, fill="white")

    # Mostrar la puntuación de los jugadores
    puntuacion_player_x, puntuacion_player_o = board.get_score()
    etiqueta_puntuacion.config(
        text=f"Puntuación - Jugador X: {puntuacion_player_x}\nPuntuación - Jugador O: {puntuacion_player_o}")

    # Realiza el movimiento de la IA
    if board is not None and not board.is_game_over() and current_player == 2:
        # Obtener el mejor movimiento para la IA
        mejor_movimiento = alfabeta(board, board.board, 0, -1, -float('inf'), float('inf'), [], [])

        # Realiza el mejor movimiento encontrado por la IA
        if mejor_movimiento:
            board.make_move(mejor_movimiento[0], mejor_movimiento[1], 2)

        # Actualiza el tablero y cambia al siguiente jugador
        dibujar_tablero(board.board)
        if not board.is_game_over():
            cambiar_jugador()
    else:
        # El juego ha terminado, muestra el ganador y la puntuación
        ganador = board.get_winner()
        puntuacion_player_x, puntuacion_player_o = board.get_score()
        mensaje = f"¡El ganador es {ganador}!\n"
        mensaje += f"Puntuación - Jugador X: {puntuacion_player_x}\n"
        mensaje += f"Puntuación - Jugador O: {puntuacion_player_o}"
        tk.messagebox.showinfo("Juego Terminado", mensaje)


def alfabeta(juego: ReversiBoard, estado_inicial: list, profundidad: int, etapa: int, alfa: int, beta: int,
             secuencia: list, secuencias: list) -> list:
    if juego.estado_final(estado_inicial, profundidad):
        secuencias.append(secuencia.copy())
        return [-1 * juego.evaluar(juego.board)]

    if etapa == 1:
        valor = [-1000, None]
        jugadas_posibles = juego.generador_jugadas_validas(1)
    else:
        valor = [1000, None]
        jugadas_posibles = juego.generador_jugadas_validas(2)

    for jugada in jugadas_posibles:
        juego.devolver_estado(estado_inicial)

        if etapa == 1:
            juego.jugar(jugada, 1)
        else:
            juego.jugar(jugada, 2)

        copia = copy.deepcopy(juego.board)
        secuencia.append(jugada)

        opcion = alfabeta(juego, copia, profundidad + 1, etapa * -1, alfa, beta, secuencia, secuencias)

        if etapa == 1:
            if valor[0] < opcion[0]:
                valor = [opcion[0], jugada]
            if valor[0] > alfa:
                alfa = valor[0]
            if valor[0] >= beta:
                juego.devolver_estado(estado_inicial)
                secuencia.pop()
                break
        else:
            if valor[0] > opcion[0]:
                valor = [opcion[0], jugada]
            if valor[0] < beta:
                beta = valor[0]
            if valor[0] <= alfa:
                juego.devolver_estado(estado_inicial)
                secuencia.pop()
                break

        juego.devolver_estado(estado_inicial)
        secuencia.pop()

    return valor


# Crear la ventana principal de la aplicación
ventana = tk.Tk()
ventana.title("Juego de Reversi")

# Declara board como global al principio del script
current_player = 'X'
board = None

# Crear variables para almacenar las opciones seleccionadas
tamano_var = tk.StringVar()
dificultad_var = tk.StringVar()
ayuda_var = tk.BooleanVar()

# Etiqueta para el tamaño del tablero
tamano_label = tk.Label(ventana, text="Tamaño del Tablero:")
tamano_label.pack()

# Menú desplegable para seleccionar el tamaño del tablero
tamano_options = ["6x6", "8x8"]
tamano_menu = tk.OptionMenu(ventana, tamano_var, *tamano_options)
tamano_menu.pack()

# Etiqueta para el nivel de dificultad
dificultad_label = tk.Label(ventana, text="Nivel de Dificultad:")
dificultad_label.pack()

# Menú desplegable para seleccionar el nivel de dificultad
dificultad_options = ["Fácil", "Intermedio", "Difícil"]
dificultad_menu = tk.OptionMenu(ventana, dificultad_var, *dificultad_options)
dificultad_menu.pack()

# Casilla de verificación para habilitar la ayuda
ayuda_checkbox = tk.Checkbutton(ventana, text="Solicitar Ayuda", variable=ayuda_var)
ayuda_checkbox.pack()

# Crear un lienzo (canvas) para dibujar el tablero
CASILLA_TAMANO = 50  # Tamaño de la casilla del tablero en píxeles
canvas = tk.Canvas(ventana, width=400, height=400)
canvas.pack()

# Asociar la función handle_click al clic en el lienzo
canvas.bind("<Button-1>", handle_click)

# Etiqueta para mostrar el jugador actual
etiqueta_jugador = tk.Label(ventana, text="Jugador Actual: ")
etiqueta_jugador.pack()

# Etiqueta para mostrar la puntuación
etiqueta_puntuacion = tk.Label(ventana, text="Puntuación - Jugador X: 2\nPuntuación - Jugador O: 2")
etiqueta_puntuacion.pack()

# Botón para iniciar el juego
boton_iniciar = tk.Button(ventana, text="Iniciar Juego", command=iniciar_juego)
boton_iniciar.pack()

# Iniciar la interfaz gráfica
ventana.mainloop()
