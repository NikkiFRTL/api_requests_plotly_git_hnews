import requests
from plotly.graph_objs import Bar
from plotly import offline


# Создание вызова API и сохранение ответа.
url = 'https://api.github.com/search/repositories?q=language:python&sort=stars'
headers = {'Accept': 'application/vnd.github.v3+json'}
# Сохранение ответа в переменной.
r = requests.get(url, headers)
print(f'Status code: {r.status_code}')

# Обработка результатов.

# Сохранение ответа API в виде словаря.
response_dict = r.json()
repo_dicts = response_dict['items']

# Создание словарей с данными о именах проектов, количествах звезд и описанием проекта.
# Plotly позволяет использовать HTML в текстовых элементах. Пожтому имена будут кликабельные с ссылкой на проект.
# Якорный тег HTML для создания ссылки: <a href='URL'> текст ссылки </a>.
repo_links = [f"<a href='{repo_dict['html_url']}'>{repo_dict['name']}</a>" for repo_dict in repo_dicts]
stars = [repo_dict['stargazers_count'] for repo_dict in repo_dicts]
# <br /> текст с разрывом строки для HTML.
labels = [f"{repo_dict['owner']['login']}<br />{repo_dict['description']}" for repo_dict in repo_dicts]

# Построение визуализации - столбцевой диаграммы проект-звезды.
data = [{
    'type': 'bar',
    'x': repo_links,
    'y': stars,
    # Добавление описания проекта при наведении на столбец.
    'hovertext': labels,
    # Назначение столбцам синего цвета и границам стоблцов серого цвета.
    'marker': {
        'color': 'rgb(60, 100, 150)',
        'line': {'width': 1.5, 'color': 'rgb(25, 25, 25)'}
    },
    # Прозрачность столбцов.
    'opacity': 0.6,
}]
# Импортировать класс Layout не нужно, т.к. для определения макета используется словарь.
my_layout = {
    # Заголовок
    'title': 'Most-Starred Python Projects on Github',
    'titlefont': {'size': 28},
    # Метки по осям х, у
    'xaxis': {
        'title': 'Repository',
        'titlefont': {'size': 20},
        'tickfont': {'size': 14}
    },
    'yaxis': {
        'title': 'Stars',
        'titlefont': {'size': 20},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='Top Github Python Projects.html')
