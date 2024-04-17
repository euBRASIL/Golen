def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def next_prime(n):
    prime = n + 1
    while True:
        if is_prime(prime):
            return prime
        prime += 1

def espiral(numero):
    spiral = [[' ' for _ in range(8)] for _ in range(8)]

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    x, y = 0, 0
    direction_index = 0

    for digit in str(numero):
        spiral[x][y] = digit
        dx, dy = directions[direction_index]
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < 8 and 0 <= new_y < 8 and spiral[new_x][new_y] == ' ':
            x, y = new_x, new_y
        else:
            direction_index = (direction_index + 1) % 4
            dx, dy = directions[direction_index]
            x, y = x + dx, y + dy

    for row in spiral:
        print(" ".join(row))


# if __name__ == "__main__":

# tabuleiro = next_prime(primo64)

print( espiral( 1111111222222233333334444444555555566666667777777888888899999990 ) )



