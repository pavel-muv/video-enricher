# Video Enricher

# Video Enricher

**YouTube Video Research Tool**

Video Enricher is a Python tool for researching YouTube videos, collecting publicly available statistics, comparing performance metrics, and exporting search results for further analysis.

Video Enricher — инструмент на Python для исследования видео YouTube, сбора общедоступной статистики, сравнения показателей и экспорта результатов поиска для дальнейшего анализа.

---

# Русский

## Возможности

- **Множественный поиск:** поиск видео по нескольким ключевым словам и фразам за один запуск.
- **Удаление дубликатов:** одно и то же видео не добавляется в результаты повторно.
- **Фильтрация по популярности:**
  - `Popular` — популярные видео среди найденных результатов.
  - `Trending` — видео с высокими расчётными показателями.
  - `All` — все найденные видео.
- **Фильтрация по продолжительности:** все видео, Shorts и длинные видео.
- **Сортировка результатов:**
  - по общему количеству просмотров;
  - по среднему количеству просмотров в час;
  - по соотношению просмотров и подписчиков канала.
- **Анализ статистики:** дата публикации, продолжительность, просмотры, лайки, комментарии и количество подписчиков, если эти данные доступны.
- **Дополнительные метрики:** возраст видео, средние просмотры в час, отношение просмотров к числу подписчиков и расчётный показатель роста.
- **Экспорт данных:** CSV, Markdown и TXT.
- **Два языка интерфейса:** русский и английский.

## Требования

- Windows, если используется готовая сборка EXE.
- Python, если программа запускается из исходного кода.
- Подключение к интернету.
- API-ключ YouTube Data API v3.

## Установка

Клонируйте репозиторий:

```bash
git clone <repository-url>
cd video-enricher
```

Установите зависимости:

```bash
python -m pip install -r requirements.txt
```

Если файла `requirements.txt` нет, установите основную зависимость вручную:

```bash
python -m pip install google-api-python-client
```

## Получение API-ключа

Для поиска используется YouTube Data API v3.

1. Откройте [Google Cloud Console](https://console.cloud.google.com/).
2. Создайте проект или выберите существующий.
3. Включите **YouTube Data API v3**.
4. Создайте API-ключ в разделе учётных данных.
5. Используйте полученный ключ при запуске программы.

Доступ к API регулируется квотами Google. Количество поисковых запросов влияет на расход квоты.

## Запуск

Из корневой папки проекта выполните:

```bash
python main.py
```

При запуске программа предлагает выбрать язык интерфейса и ввести API-ключ. Затем необходимо указать параметры поиска и следовать инструкциям в консоли.

### Поисковые запросы

Можно указать несколько запросов за один запуск. Разделяйте их запятыми, точками с запятой или переносами строк.

Программа собирает результаты по запросам и удаляет дубликаты по идентификаторам видео.

### Фильтры

**Popularity**
- `Popular`
- `Trending`
- `All`

**Video format**
- `All videos`
- `Shorts`
- `Longs`

### Сортировка

Результаты можно сортировать по общему числу просмотров, среднему числу просмотров в час или отношению просмотров к количеству подписчиков канала.

## Доступные данные

| Поле | Описание |
|---|---|
| Title | Название видео |
| Channel | Название канала |
| Published | Дата публикации |
| Duration | Продолжительность |
| Views | Общее количество просмотров |
| Likes | Количество лайков, если доступно |
| Comments | Количество комментариев, если доступно |
| Subscribers | Количество подписчиков канала, если доступно |
| Age (days) | Возраст видео в днях |
| Views/hour | Средние просмотры в час с момента публикации |
| Views/subscribers | Отношение просмотров к числу подписчиков |
| Growth score | Расчётный показатель на основе доступных метрик |

## Экспорт результатов

Результаты сохраняются в папку `output`.

- **CSV** — для анализа в Excel и других табличных редакторах.
- **Markdown** — для заметок и документации.
- **TXT** — для просмотра в обычном текстовом редакторе.

Путь к папке результатов зависит от того, как в коде организовано сохранение файлов и из какого рабочего каталога запущена программа.

## Ограничения

- `Popular` и `Trending` — внутренние расчётные категории программы, а не официальные категории YouTube.
- Показатель роста рассчитывается по доступным метрикам и не является измерением реального изменения количества просмотров во времени.
- Определение Shorts основано на продолжительности видео и может быть неточным.
- Число лайков, комментариев и подписчиков зависит от доступности данных через API.
- Количество результатов ограничено настройками поиска и квотой YouTube Data API.

## Журнал ошибок

Для диагностики проблем используется файл `video_enricher.log`, если его создание и запись предусмотрены текущей конфигурацией программы.

## Запуск EXE

Для Windows также может предоставляться готовая сборка `VideoEnricher.exe`. Она позволяет запускать программу без отдельной установки Python.

Исходный код остаётся доступным в репозитории.

---

# English

## Features

- **Multi-query search:** search YouTube using multiple keywords or phrases in one run.
- **Duplicate removal:** videos are deduplicated by their video IDs.
- **Popularity filters:**
  - `Popular` — popular videos among the collected results.
  - `Trending` — videos with high calculated indicators.
  - `All` — all collected videos.
- **Duration filters:** all videos, Shorts, and long-form videos.
- **Sorting options:**
  - total views;
  - average views per hour;
  - views-to-subscribers ratio.
- **Statistics collection:** publication date, duration, views, likes, comments, and subscriber counts when available.
- **Additional metrics:** video age, average views per hour, views-to-subscribers ratio, and a calculated growth score.
- **Data export:** CSV, Markdown, and TXT.
- **Bilingual interface:** Russian and English.

## Requirements

- Windows for the prebuilt EXE version.
- Python for running from source.
- An internet connection.
- A YouTube Data API v3 key.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd video-enricher
```

Install the dependencies:

```bash
python -m pip install -r requirements.txt
```

If `requirements.txt` is not available, install the main dependency manually:

```bash
python -m pip install google-api-python-client
```

## Getting an API key

The application uses YouTube Data API v3.

1. Open the [Google Cloud Console](https://console.cloud.google.com/).
2. Create a project or select an existing one.
3. Enable **YouTube Data API v3**.
4. Create an API key in the credentials section.
5. Enter the key when starting the application.

API usage is subject to Google's quotas. Search requests consume quota.

## Running the application

Run the following command from the project directory:

```bash
python main.py
```

At startup, the application asks you to select the interface language and enter an API key. You can then configure the search and follow the console prompts.

### Search queries

Multiple search queries can be entered in one run. Separate them with commas, semicolons, or new lines.

Results from different queries are combined, and duplicate video IDs are removed.

### Filters

**Popularity**
- `Popular`
- `Trending`
- `All`

**Video format**
- `All videos`
- `Shorts`
- `Longs`

### Sorting

Results can be sorted by total views, average views per hour, or the views-to-subscribers ratio.

## Available data

| Field | Description |
|---|---|
| Title | Video title |
| Channel | Channel name |
| Published | Publication date |
| Duration | Video duration |
| Views | Total views |
| Likes | Like count, when available |
| Comments | Comment count, when available |
| Subscribers | Channel subscriber count, when available |
| Age (days) | Video age in days |
| Views/hour | Average views per hour since publication |
| Views/subscribers | Ratio of views to subscribers |
| Growth score | Calculated indicator based on available metrics |

## Export

Results are saved in the `output` directory.

- **CSV** — for Excel and other spreadsheet applications.
- **Markdown** — for notes and documentation.
- **TXT** — for standard text editors.

The exact output location depends on the file-saving implementation and the current working directory.

## Limitations

- `Popular` and `Trending` are internal calculated classifications, not official YouTube categories.
- The growth score is based on available metrics and does not measure actual changes in view velocity over time.
- Shorts detection is based on video duration and may be inaccurate.
- Like, comment, and subscriber data depend on API availability.
- The number of results is limited by the search configuration and YouTube Data API quota.

## Error log

The application uses `video_enricher.log` for troubleshooting when logging is enabled in the current configuration.

## EXE version

A prebuilt `VideoEnricher.exe` may also be provided for Windows users who prefer not to install Python separately.

The source code remains available in the repository.

---

## License

Add the applicable license here if the project is distributed under an open-source license.

