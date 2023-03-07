import csv

with open('data.csv', 'r', encoding='utf8') as f:
    data = csv.reader(f)
    k = [i[0] for i in data]
key_data =','.join(k)