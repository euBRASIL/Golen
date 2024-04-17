import requests
import pprint

def get_public_key(address):
    # Consultar a API do blockchain.com para obter informações sobre transações relacionadas ao endereço
    url = f'https://blockchain.info/rawaddr/{address}'
    response = requests.get(url)
    data = response.json()

    # Verificar se há transações relacionadas ao endereço
    if 'txs' in data:
        # Iterar sobre as transações
        for tx in data['txs']:
            # Verificar cada saída da transação
            pprint.pprint(tx)
            for output in tx['out']:
                # Verificar se a saída contém o endereço
                if output['addr'] == address:
                    # Retornar a chave pública associada à transação
                    return output['scriptPubKey']['hex'][2:-4]

    # Se não houver transações ou se a chave pública não for encontrada, retornar None
    return None

# Endereço Bitcoin de exemplo
address = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'

# Obter a chave pública correspondente ao endereço
public_key = get_public_key(address)

# Apresentar a chave pública
if public_key:
    print("Chave pública associada ao endereço Bitcoin:", public_key)
else:
    print("Não foi possível encontrar a chave pública associada ao endereço Bitcoin.")
