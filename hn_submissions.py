from operator import itemgetter
import requests


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

# Выводим на экран три атрибута: заголовок, ссылку на статью и количество комметраниев.
for submission_dict in submission_dicts:
    print(f"\nTitle: {submission_dict['title']}")
    print(f"Discussion link: {submission_dict['hn_link']}")
    print(f"Comments: {submission_dict['comments']}")
