# coding:utf-8
import csv
from tempfile import NamedTemporaryFile

with open('data.csv', 'w+') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['title', 'desc'])
    writer.writerow(['row 1', 'desc 1'])
    writer.writerow(['row 2', 'desc 2'])

with open('data.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        print(row)
print('*'*20)

with open('data.csv', 'a') as csvfile:
    fields = ['title', 'desc']
    writer = csv.DictWriter(csvfile, fields)
    writer.writerow(
        {'title': 'music', 'desc':'i am musicion'},
    )
    writer.writerows(
        [
            {'title': 'it', 'desc': 'it'},
            {'title': 'workder', 'desc': 'it'},
        ]
    )

with open('data.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row)

# tmp = NamedTemporaryFile(delete=False)
# with open('data.csv', 'r') as csvfile, tmp:
#     reader = csv.DictReader(csvfile)
#     fields =  ['title', 'desc']
#
#     writer = csv.DictWriter(tmp, fieldnames=fields)
#
#     for row in reader:
#         writer.writerow(row)



