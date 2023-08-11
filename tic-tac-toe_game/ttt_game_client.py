import socket

def print_board(board):
    for row in board:
        print(' | '.join(row))
        print('-' * 5)

def main():
    HOST = '127.0.0.1'  # Change to your server's IP address
    PORT = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        while True:
            data = s.recv(1024).decode()
            board, status = data.rsplit('\n', 1)
            board = [list(row.split()) for row in board.strip().split('\n')]
            print_board(board)
            print(f"Status: {status}")

            if status in ["WIN", "LOSE", "DRAW"]:
                print("Game over.")
                break

            if status == 'X' or status == 'O':
                row = int(input("Enter row (0-2): "))
                col = int(input("Enter column (0-2): "))
                s.sendall(f"{row} {col}".encode())

if __name__ == "__main__":
    main()
