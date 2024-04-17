import random

def is_probable_prime(n, k=5):
    """Teste de primalidade de Miller-Rabin."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    # Encontrando r e d tal que n-1 = 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1

    # Realiza o teste de Miller-Rabin k vezes
    for iteration in range(1, k+1):
        print(f"Iteração {iteration}:")
        a = random.randint(2, n - 1)
        print(f"  Escolha aleatória de a: {a}")
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            print(f"  Resultado do teste: Passou na primeira etapa")
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            print(f"  x elevado ao quadrado: {x}")
            if x == n - 1:
                print(f"  Resultado do teste: Passou na etapa {r - 1}")
                break
        else:
            print(f"  Resultado do teste: Falhou na etapa {r - 1}")
            return False
    return True

number = 9268071999261168524896084886644810981052305037076905124351297833
if is_probable_prime(number):
    print("O número é provavelmente primo.")
else:
    print("O número não é primo.")
