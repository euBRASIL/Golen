import datetime

timestamp = 1710965937
data_legivel = datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

print("A transação ocorreu em:", data_legivel)
