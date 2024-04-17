import random

def is_prime(n, k=5):
    """Testa a primalidade de um número usando o teste de Miller-Rabin."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Encontra r e d tal que n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Testa a primalidade k vezes
    for _ in range(k):
        a = random.randint(2, n - 1)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_prime(digits):
    """Gera um número primo com o número especificado de dígitos."""
    while True:
        candidate = random.randrange(10**(digits-1), 10**digits)
        if is_prime(candidate):
            return candidate

# Gera um número primo com 64 casas decimais
prime_number = generate_prime(64)
print("Número primo com 64 casas decimais:", prime_number)
