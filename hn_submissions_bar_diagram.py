from operator import itemgetter
import requests
from plotly import offline

# Создание вызова API и сохранение ответа.
url = 'https://hacker-news.firebaseio.com/v0/topstories.json'
r = requests.get(url)
print(f"Status: {r.status_code}")

# Обработка информации о каждой статьи.
submission_ids = r.json()
submission_dicts = []
for submission_id in submission_ids[0:30]:
    try:
        # Создание отдельного вызова API для каждой статьи
        url = f"https://hacker-news.firebaseio.com/v0/item/{submission_id}.json"
        r = requests.get(url)
        print(f"id: {submission_id}\tstatus: {r.status_code}")
        response_dict = r.json()

        # Построение словаря для каждой статьи с нужной информацией.
        submission_dict = {
            'title': response_dict['title'],
            'hn_link': f"http://news.ycombinator.com/item?id={submission_id}",
            'comments': response_dict['descendants'],
        }
    except KeyError:
        print('No data')
    else:
        # Забрасываем каждую статью в виде словарей в список.
        submission_dicts.append(submission_dict)

# Сортировка по количеству комментариев, operator.itemgetter() получает ключ и извлекает каждое значение связанное
# с данным ключом из каждого словаря в списке submission_dicts.
submission_dicts = sorted(submission_dicts, key=itemgetter('comments'), reverse=True)

# Списки с данными для создания столбцевой диаграммы.
hn_links = [f"<a href='{submission_dict['hn_link']}'>{submission_dict['title']}</a>"
            for submission_dict in submission_dicts]

all_comments = [submission_dict['comments'] for submission_dict in submission_dicts]

labels = [submission_dict['title'] for submission_dict in submission_dicts]

# Создание диаграммы
data = [{
    'type': 'bar',
    'x': hn_links,
    'y': all_comments,
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
    'title': 'Most-Commented Titles on Hacker-News',
    'titlefont': {'size': 28},
    # Метки по осям х, у
    'xaxis': {
        'title': 'Titles',
        'titlefont': {'size': 20},
        'tickfont': {'size': 14}
    },
    'yaxis': {
        'title': 'Comments',
        'titlefont': {'size': 20},
        'tickfont': {'size': 14},
    },
}

fig = {'data': data, 'layout': my_layout}
offline.plot(fig, filename='Most-Commented Titles on Hacker-News.html')
