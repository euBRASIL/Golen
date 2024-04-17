import ecdsa
import hashlib
import base58
import json
import sys
from tqdm import tqdm


# global contabits


def corresponde(str1, str2):
    len_str1 = len(str1)
    len_str2 = len(str2)
    min_len = min(len_str1, len_str2)
    matching_chars = sum(1 for c1, c2 in zip(str1, str2) if c1 == c2)
    return (matching_chars / min_len) * 100

def analisar_chave(chave):
    credito = 0
    for bit in chave:
        
        if bit == '1' :
            credito = credito + 1

    return credito
    
    
def chavebitcoin(iniciohex, finalhex, premio):
    inicioint = int(iniciohex, 16)
    finalint  = int(finalhex, 16)
    step = 1230000000  # Define o tamanho do passo para iterar de |10|000|000|

    numerocompleto = 0
    semChave = 0
    
    # wallet = ""
    
    salto = 123 # Este é um saldo relacional com os 9x números possiveis sem o Zero
    

    # Criar arquivo JSON com os resultados
    resultados_json = []  # Lista para armazenar os resultados
    with open(f"{iniciohex}.json", "a") as json_file:
        json.dump(resultados_json, json_file, indent=4)

    with open(f"{iniciohex}.txt", "a") as file:
        for batman in range(inicioint, finalint + 1, step):
            questao = min(batman + step - 1, finalint)
            for privadaint in tqdm(range(batman, questao + 1, salto), desc="Progresso", unit="chaves", file=sys.stdout):
                privadahex = format(privadaint, 'x').zfill(64)
                privadabyt  = bytes.fromhex(privadahex)

                saldo = analisar_chave(bin(privadaint)) # Função bin(converte), oct(converte) e hex(converte)
                
                if saldo > 25 and saldo < 35 : # Conta(bits) evita processos abaixo de determinada quantidade de bits

                    sk = ecdsa.SigningKey.from_string(privadabyt, curve=ecdsa.SECP256k1)
                    vk = sk.get_verifying_key()

                    publicabyt = bytes.fromhex("04") + vk.to_string()
                    algoritmo = hashlib.sha256(publicabyt).digest()
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
                        # tipo_saldo = "(C+)" if saldo > 0 else "(D-)"
                        valor_saldo = abs(saldo)

                        print(f"\nChave Privada (hexadecimal)  : {privadahex}")
                        print(f"Endereço Bitcoin  (credito)  : {bitcoin}")
                        print(f"Percentual de Correspondência: {percentual:.2f}%\n")
                        print(f"Conta(bits): {valor_saldo} bits \n")

                        file.write(f"Chave Privada (hexadecimal): {privadahex}\n")
                        file.write(f"Endereco Bitcoin (credito) : {bitcoin}\n")
                        file.write(f"Percentual de Correspondencia: {percentual:.2f}%\n")
                        file.write(f"Conta(bits): {valor_saldo} bits \n")
                        file.write("\n")

                        resultados_json.append({
                            "Chave Privada (hexadecimal)": privadahex,
                            "Endereco Bitcoin para crédito": bitcoin,
                            "Percentual de Correspondencia": f"{percentual:.2f}%"
                        })
                            
                        if( privadaint % 73786976294838206464 == 0.75 ): # |3|00000000|00000000| ( dividir ) |4|00000000|00000000| = 0,75
                            privadaint = privadaint + 25365184           # 55340232221128654848 / 73786976294838206464 = 0.75
                            # Diferença : 0.016666666662786156           1a Chave Privada :  25 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.76 and privadaint % 73786976294838206464 < 0.77 ): # |3|11111111| = 0.7666666666627862           
                            privadaint = privadaint + 8406352                      # 56570015159089627136 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :   8 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.78 and privadaint % 73786976294838206464 < 0.79 ): # |3|22222222| = 0.7833333333255723     
                            privadaint = privadaint + 29742564                     # 57799798097050599424 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :  29 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.79 and privadaint % 73786976294838206464 < 0.80 ): # |3|33333333| = 0.7999999999883585
                            privadaint = privadaint + 3250029                      # 59029581035011571712 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :   3 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.81 and privadaint % 73786976294838206464 < 0.82 ): # |3|44444444| = 0.8166666666511446
                            privadaint = privadaint + 96812020                     # 60259363972972544000 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :  96 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.83 and privadaint % 73786976294838206464 < 0.84 ): # |3|55555555| = 0.8333333333139308
                            privadaint = privadaint + 1                            # 61489146910933516288 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        if( privadaint % 73786976294838206464 > 0.84 and privadaint % 73786976294838206464 < 0.85 ): # |3|66666666| = 0.8499999999767169
                            privadaint = privadaint + 112166417                    # 62718929848894488576 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada : 112 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.86 and privadaint % 73786976294838206464 < 0.87 ): # |3|77777777| = 0.8666666666395031
                            privadaint = privadaint + 22351185                     # 63948712786855460864 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :  22 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.88 and privadaint % 73786976294838206464 < 0.89 ): # |3|88888888| = 0.8833333333022892
                            privadaint = privadaint + 749850942                      # 65178495724816433152 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada : 749 Milhões (velocidade 3x43)
                            
                        if( privadaint % 73786976294838206464 > 0.89 and privadaint % 73786976294838206464 < 0.90 ): # |3|99999999| = 0.8999999999650754
                            privadaint = privadaint + 2106282416                   # 66408278662777405440 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :   2 Bilhões (velocidade 2x43)
                            
                        if( privadaint % 73786976294838206464 > 0.91 and privadaint % 73786976294838206464 < 0.92 ): # |3|AAAAAAAA| = 0.9166666666278616
                            privadaint = privadaint + 29177198                     # 67638061600738377728 / 73786976294838206464
                            # Diferença : 0.016666666662786156           1a Chave Privada :  29 Milhões
                            
                        if( privadaint % 73786976294838206464 > 0.93 and privadaint % 73786976294838206464 < 0.94 ): # |3|BBBBBBBB| = 0.9333333332906477
                            privadaint = privadaint + 1000000                      # 68867844538699350016 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        if( privadaint % 73786976294838206464 > 0.94 and privadaint % 73786976294838206464 < 0.95 ): # |3|CCCCCCCC| = 0.9499999999534339
                            privadaint = privadaint + 1000000                      # 70097627476660322304 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        if( privadaint % 73786976294838206464 > 0.96 and privadaint % 73786976294838206464 < 0.97 ): # |3|DDDDDDDD| = 0.96666666661622
                            privadaint = privadaint + 1000000                      # 71327410414621294592 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        if( privadaint % 73786976294838206464 > 0.98 and privadaint % 73786976294838206464 < 0.99 ): # |3|EEEEEEEE| = 0.9833333332790062
                            privadaint = privadaint + 1000000                      # 72557193352582266880 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        if( privadaint % 73786976294838206464 > 0.99 and privadaint % 73786976294838206464 < 1 ): # |3|FFFFFFFF| = 0.9999999999417923
                            privadaint = privadaint + 1000000                      # 73786976290543239168 / 73786976294838206464
                            # Diferença : 0.016666666662786156
                            
                        print("Distância (decimal) : ", privadaint)
                        semChave = 0
                        
                    else :
                        
                        
                        if semChave == 430 : # Analisa 430 chaves privadas e salta 29 Milhões de chaves privadas
                            privadaint += 29000000
                            # 73787 |4|00000000|00000000| 73786976294838206464 / 1000000000000000 (*)Python : int('40000000000000000',16) 
                            semChave = 1
                            
                        else : semChave = semChave + 1
                        

                        
                        # if semChave > 1000000 : salto + 1
                        # if semChave > 2000000 : salto + 1
                        # if semChave > 3000000 : salto + 1
                        # if semChave > 4000000 : salto + 1
                        # if semChave > 5000000 : salto + 1
                        # if semChave > 6000000 : salto + 1
                        # if semChave > 7000000 : salto + 1
                        # if semChave > 8000000 : salto + 1
                        # if semChave > 9000000 : salto + 1
                        

if __name__ == "__main__":
    iniciohex = "0000000000000000000000000000000000000000000000032222222f534f4724" 
    finalhex  = "0000000000000000000000000000000000000000000000040000000000000000" # Tempo Médio de 1h para cada 123.000.000 de Chaves Privadas + 29M
    premio    = "13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so"
    chavebitcoin(iniciohex, finalhex, premio)


