import ecdsa
import hashlib
import base58
import json
import sys
from tqdm import tqdm

from numba import jit, njit
# @jit(nopython='True') ou @njit


def corresponde(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)

    min_len = min(len_str1, len_str2)
    matching_chars = sum(1 for c1, c2 in zip(str1, str2) if c1 == c2)

    return (matching_chars / min_len) * 100


def chavebitcoin(iniciohex, finalhex, premio):
    inicioint = int(iniciohex, 16)
    finalint  = int(finalhex, 16)
    step = 10000000  # Define o tamanho do passo para iterar de |10|000|000|

    numerocompleto = 0
    wallet = ""

    resultados_json = []  # Lista para armazenar os resultados
    
    with open("32%.txt", "a") as file:
        for batman in range(inicioint, finalint + 1, step):
            questao = min(batman + step - 1, finalint)
            for privadaint in tqdm(range(batman, questao + 1), desc="Progresso", unit="chaves", file=sys.stdout):
                privadahex = format(privadaint, 'x').zfill(64)
                privadaby  = bytes.fromhex(privadahex)



                # print("Chave Privada :", privadahex)



                sk = ecdsa.SigningKey.from_string(privadaby, curve=ecdsa.SECP256k1)
                vk = sk.get_verifying_key()

                # Gerar a chave privada no formato WIF
                wif = base58.b58encode_check(b'\x80' + privadaby).decode()

                publicaby = vk.to_string()
                algoritmo = hashlib.sha256(publicaby).digest()
                ripemd160 = hashlib.new('ripemd160', algoritmo).digest()
                extendida = b'\x00' + ripemd160
                checksum  = hashlib.sha256(hashlib.sha256(extendida).digest()).digest()[:4]
                address   = extendida + checksum
                bitcoin   = base58.b58encode(address).decode()

                percentual = corresponde(premio, bitcoin)
                if percentual > numerocompleto :
                    numerocompleto = percentual
                    wallet = bitcoin

                if percentual > 26 and bitcoin.startswith("13"):
                    print(f"\nChave Privada (hexadecimal): {privadahex}")
                    print(f"Chave Privada (WIF): {wif}")
                    print(f"Endereço Bitcoin: {bitcoin}")
                    print(f"Percentual de Correspondência: {percentual:.2f}%\n")

                    file.write(f"Chave Privada (hexadecimal): {privadahex}\n")
                    file.write(f"Chave Privada (WIF): {wif}\n")
                    file.write(f"Endereco Bitcoin: {bitcoin}\n")
                    file.write(f"Percentual de Correspondencia: {percentual:.2f}%\n")
                    file.write("\n")

                    resultados_json.append({
                        "Chave Privada (hexadecimal)": privadahex,
                        "Chave Privada (WIF)": wif,
                        "Endereco Bitcoin": bitcoin,
                        "Percentual de Correspondencia": f"{percentual:.2f}%"
                    })

    # Criar arquivo JSON com os resultados
    with open("32%.json", "a") as json_file:
        json.dump(resultados_json, json_file, indent=4)
        json.dump(resultados_json, json_file, indent=4)

if __name__ == "__main__":
    iniciohex = "000000000000000000000000000000000000000000000003555555550000000000" 
    finalhex  = "00000000000000000000000000000000000000000000000355555555ffffffff"
    premio    = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
    chavebitcoin(iniciohex, finalhex, premio)
