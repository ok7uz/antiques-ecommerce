import requests
from json import load

json_file = open('../../product_data.json', encoding='utf-8')
data = load(json_file)

for item in data:
    id = item['image_id']
    url = f'https://antikdecor.ru/?c=Resize&dir=dbf/model&w=2000&h=2000&id={id}'
    response = requests.get(url)

    with open('{0}.jpg'.format(id), 'wb') as file:
        file.write(response.content)
        file.close()

    print(id)
