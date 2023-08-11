import socket

def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 10)

def is_winner(board, player):
    # Check rows, columns, and diagonals
    for row in board:
        if all(s == player for s in row):
            return True
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def is_draw(board):
    return all(all(cell != ' ' for cell in row) for row in board)

def handle_game(client1, client2):
    players = {'X': client1, 'O': client2}
    board = [[' ' for _ in range(3)] for _ in range(3)]
    turn = 0
    symbols = 'XO'

    while True:
        current_player = symbols[turn % 2]
        opponent_player = symbols[(turn + 1) % 2]
        client1.sendall(board, current_player)
        client2.sendall(board, opponent_player)

        row, col = players[current_player].recv_move()

        if board[row][col] != ' ':
            continue

        board[row][col] = current_player

        if is_winner(board, current_player):
            client1.sendall(board, "WIN" if current_player == 'X' else "LOSE")
            client2.sendall(board, "WIN" if current_player == 'O' else "LOSE")
            break

        if is_draw(board):
            client1.sendall(board, "DRAW")
            client2.sendall(board, "DRAW")
            break

        turn += 1

class ClientHandler:
    def __init__(self, conn):
        self.conn = conn

    def sendall(self, board, status):
        # Convert the board to a string and send it along with the status
        data = '\n'.join([' '.join(row) for row in board]) + '\n' + status
        self.conn.sendall(data.encode())

    def recv_move(self):
        # Receive the player's move
        data = self.conn.recv(1024).decode()
        row, col = map(int, data.strip().split())
        return row, col

def main():
    HOST = '127.0.0.1'  # Change to your server's IP address
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Waiting for players to connect...")
        conn1, _ = s.accept()
        conn2, _ = s.accept()
        print("Both players connected. Starting the game.")

        client1 = ClientHandler(conn1)
        client2 = ClientHandler(conn2)
        handle_game(client1, client2)

        print("Game over.")

if __name__ == "__main__":
    main()
