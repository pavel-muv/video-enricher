# -*- coding: utf-8 -*-
import os
import sys
import csv
import re
import logging
from datetime import datetime, timezone
from pathlib import Path

# UTF-8 console support on Windows
if os.name == "nt":
    os.system("chcp 65001 > nul")

for stream in (sys.stdin, sys.stdout, sys.stderr):
    if stream is not None and hasattr(stream, "reconfigure"):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Папка программы: рядом с EXE (PyInstaller) или рядом с main.py
if getattr(sys, "frozen", False):
    BASE_DIR = Path(sys.executable).resolve().parent
else:
    BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    filename=str(BASE_DIR / "video_enricher.log"),
    level=logging.ERROR,
    format="%(asctime)s %(levelname)s %(message)s",
    encoding="utf-8",
)

DEVELOPER = "Pavel Muv"
CONTACTS = [
    ("YouTube", "https://www.youtube.com/@Pavel_Muv_Lab"),
    ("X", "https://x.com/Pavel_muv"),
]

EXIT_WORDS = {"0", "exit", "quit", "q", "выход", "в"}
SEARCH_COST = 100  # единиц квоты за один вызов search().list
MAX_PAGES = 2

TEXT = {
    "ru": {
        "title": "VIDEO ENRICHER",
        "api_key": "Введите API-ключ YouTube Data API v3",
        "checking": "Проверка API-ключа...",
        "api_ok": "API-ключ работает.",
        "api_error": "Не удалось подключиться к YouTube API.",
        "query": "Введите запросы через запятую или с новой строки (0 — выход)",
        "next_query": "Введите следующий запрос (0 — выход)",
        "bye": "Работа завершена. До встречи!",
        "count": "Количество результатов (1–50)",
        "popularity": (
            "Тип популярности:\n"
            "1 — Популярные\n"
            "2 — Набирающие популярность\n"
            "3 — Все"
        ),
        "format_label": "Формат",
        "format_menu": (
            "Формат видео:\n"
            "1 — Все видео\n"
            "2 — Shorts\n"
            "3 — Longs"
        ),
        "sort": (
            "Сортировка:\n"
            "1 — По просмотрам\n"
            "2 — По средним просмотрам в час\n"
            "3 — По просмотрам относительно подписчиков"
        ),
        "searching": "Поиск видео и сбор статистики...",
        "search_query": "Поиск по запросу",
        "progress_videos": "Получение данных видео",
        "progress_channels": "Получение данных каналов",
        "done": "ГОТОВО! АНАЛИЗ ЗАВЕРШЁН",
        "follow": "Больше полезного — в моих соцсетях",
        "brand_line": "VIDEO ENRICHER  |  FIND. ANALYZE. GROW.",
        "found": "Найдено уникальных видео",
        "selected": "Видео после фильтров",
        "saved_to": "Сохранено в папку",
        "preview": "ИТОГИ ПОИСКА",
        "empty": "Подходящих видео не найдено.",
        "unknown": "Неизвестно",
        "popular": "Popular",
        "trending": "Trending",
        "shorts": "Shorts",
        "longs": "Longs",
        "published": "Дата публикации",
        "duration": "Длительность",
        "views": "Просмотры",
        "likes": "Лайки",
        "comments": "Комментарии",
        "channel": "Канал",
        "subs": "Подписчики",
        "age": "Возраст, дней",
        "vph": "Средние просмотры в час",
        "ratio": "Просмотры / подписчики",
        "score": "Индекс роста",
        "popularity_label": "Популярность",
        "developer": "Разработчик",
        "contacts": "Контакты",
        "invalid": "Некорректный ввод.",
        "no_results": "Попробуйте изменить запрос или фильтры.",
        "query_count": "Количество поисковых запросов",
        "quota_estimate": (
            "Расход квоты на этот запуск: около {cost} ед. "
            "(дефолтный лимит — 10 000 ед. в сутки)."
        ),
        "quota_exceeded": (
            "Квота YouTube Data API на сегодня исчерпана. "
            "Она обновляется раз в сутки (полночь по тихоокеанскому времени)."
        ),
        "key_rejected": "Ключ отклонён или доступ запрещён. Проверьте ключ и включён ли YouTube Data API v3.",
    },
    "en": {
        "title": "VIDEO ENRICHER",
        "api_key": "Enter your YouTube Data API v3 key",
        "checking": "Checking API key...",
        "api_ok": "API key is working.",
        "api_error": "Could not connect to YouTube API.",
        "query": "Enter queries separated by commas or new lines (0 to exit)",
        "next_query": "Enter the next query (0 to exit)",
        "bye": "Finished. See you!",
        "count": "Number of results (1–50)",
        "popularity": (
            "Popularity:\n"
            "1 — Popular\n"
            "2 — Trending\n"
            "3 — All"
        ),
        "format_label": "Format",
        "format_menu": (
            "Video format:\n"
            "1 — All videos\n"
            "2 — Shorts\n"
            "3 — Longs"
        ),
        "sort": (
            "Sort by:\n"
            "1 — Views\n"
            "2 — Average views per hour\n"
            "3 — Views relative to subscribers"
        ),
        "searching": "Searching videos and collecting statistics...",
        "search_query": "Searching query",
        "progress_videos": "Fetching video data",
        "progress_channels": "Fetching channel data",
        "done": "ALL DONE! ANALYSIS COMPLETE",
        "follow": "More from me — follow my channels",
        "brand_line": "VIDEO ENRICHER  |  FIND. ANALYZE. GROW.",
        "found": "Unique videos found",
        "selected": "Videos after filters",
        "saved_to": "Saved in folder",
        "preview": "SEARCH SUMMARY",
        "empty": "No matching videos found.",
        "unknown": "Unknown",
        "popular": "Popular",
        "trending": "Trending",
        "shorts": "Shorts",
        "longs": "Longs",
        "published": "Published",
        "duration": "Duration",
        "views": "Views",
        "likes": "Likes",
        "comments": "Comments",
        "channel": "Channel",
        "subs": "Subscribers",
        "age": "Age, days",
        "vph": "Average views per hour",
        "ratio": "Views / subscribers",
        "score": "Growth score",
        "popularity_label": "Popularity",
        "developer": "Developer",
        "contacts": "Contacts",
        "invalid": "Invalid input.",
        "no_results": "Try changing your query or filters.",
        "query_count": "Number of search queries",
        "quota_estimate": (
            "Estimated quota cost for this run: about {cost} units "
            "(default daily limit is 10,000 units)."
        ),
        "quota_exceeded": (
            "The YouTube Data API quota for today is exhausted. "
            "It resets once a day (midnight Pacific Time)."
        ),
        "key_rejected": "The key was rejected or access is denied. Check the key and that YouTube Data API v3 is enabled.",
    },
}


# ───────────────────────── helpers ─────────────────────────

def choose_language():
    print("\n1. Русский")
    print("2. English")

    while True:
        choice = input("> ").strip()

        if choice == "1":
            return "ru"

        if choice == "2":
            return "en"

        print("Введите 1 или 2 / Enter 1 or 2")


def parse_queries(raw):
    """Accept comma-separated, semicolon-separated or newline-separated queries."""
    queries = re.split(r"[,;\n]+", raw)
    result = []
    seen = set()

    for query in queries:
        query = query.strip()
        key = query.casefold()

        if query and key not in seen:
            result.append(query)
            seen.add(key)

    return result


def to_int(value):
    """Convert API value to int, or None if missing/hidden."""
    if value is None:
        return None

    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def parse_duration(value):
    match = re.fullmatch(
        r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?",
        value or "",
    )

    if not match:
        return None

    days, hours, minutes, seconds = (
        int(part or 0) for part in match.groups()
    )

    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def format_duration(seconds, unknown):
    if seconds is None:
        return unknown

    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)

    if hours:
        return f"{hours}:{minutes:02}:{secs:02}"

    return f"{minutes}:{secs:02}"


def is_quota_error(error):
    if not isinstance(error, HttpError):
        return False

    try:
        content = error.content.decode("utf-8", errors="ignore")
    except AttributeError:
        content = str(error)

    return "quotaExceeded" in content or "dailyLimitExceeded" in content


def is_key_error(error):
    if not isinstance(error, HttpError):
        return False

    status = getattr(error.resp, "status", None)
    return status in (400, 401, 403) and not is_quota_error(error)


def cell_text(value, empty="—"):
    return empty if value is None else str(value)


def connect_api(api_key):
    youtube = build(
        "youtube",
        "v3",
        developerKey=api_key,
        cache_discovery=False,
    )

    youtube.videos().list(
        part="snippet",
        id="dQw4w9WgXcQ",
    ).execute()

    return youtube


# ───────────────────────── console output ─────────────────────────

def print_header(lang):
    t = TEXT[lang]
    line = "=" * 68

    print("\n" + line)
    print(f"  {t['title']}  |  {t['brand_line']}")
    print(line)

    print(
        "  YouTube Data API v3  •  Video research toolkit"
        if lang == "en"
        else "  YouTube Data API v3  •  Инструмент анализа видео"
    )

    print(f"  {t['developer']}: {DEVELOPER}")
    print("-" * 68)


def show_progress(label, current, total, finish=False):
    """Display a compact progress bar in the console."""
    total = max(int(total), 1)
    current = min(max(int(current), 0), total)

    width = 28
    filled = int(width * current / total)
    bar = "█" * filled + "░" * (width - filled)
    percent = int(100 * current / total)

    line = f"  {label:<28} [{bar}] {percent:3d}%  {current}/{total}"

    print("\r" + line + ("\n" if finish else ""), end="", flush=True)


def print_section(title):
    print(f"\n{'─' * 68}\n  {title}\n{'─' * 68}")


def print_summary(videos, lang):
    t = TEXT[lang]

    print_section(t["preview"])

    print(
        f"  {'#':>2}  "
        f"{'VIEWS' if lang == 'en' else 'ПРОСМ.':>9}  "
        f"{'VPH' if lang == 'en' else 'ПРОСМ./Ч':>9}  "
        f"{'CHANNEL' if lang == 'en' else 'КАНАЛ':<22}  "
        f"{'TITLE' if lang == 'en' else 'НАЗВАНИЕ'}"
    )

    print("  " + "─" * 64)

    for index, video in enumerate(videos, 1):
        channel = video["channel"].replace("\n", " ")[:22]
        title = video["title"].replace("\n", " ")

        if len(title) > 48:
            title = title[:45] + "..."

        print(
            f"  {index:>2}  "
            f"{video['views']:>9,}  "
            f"{video['views_per_hour']:>9,.1f}  "
            f"{channel:<22}  "
            f"{title}"
        )

    print(
        "\n  "
        + (
            f"Showing {len(videos)} exported result(s)."
            if lang == "en"
            else f"В итоговый файл включено результатов: {len(videos)}."
        )
    )


# ───────────────────────── YouTube API ─────────────────────────

def search_video_ids(youtube, query, max_pages=MAX_PAGES, progress_callback=None):
    """Search for videos and return unique IDs."""
    video_ids = []
    next_page = None

    for page_index in range(max_pages):
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "order": "viewCount",
            "maxResults": 50,
        }

        if next_page:
            params["pageToken"] = next_page

        response = youtube.search().list(**params).execute()
        next_page = response.get("nextPageToken")

        for item in response.get("items", []):
            video_id = item.get("id", {}).get("videoId")

            if video_id and video_id not in video_ids:
                video_ids.append(video_id)

        if progress_callback:
            progress_callback(
                page_index + 1,
                max_pages,
                not bool(next_page) or page_index + 1 == max_pages,
            )

        if not next_page:
            break

    return video_ids


def get_video_and_channel_data(youtube, video_ids, lang):
    videos = []
    video_batches = list(range(0, len(video_ids), 50))

    for batch_index, start in enumerate(video_batches, 1):
        response = youtube.videos().list(
            part="snippet,statistics,contentDetails",
            id=",".join(video_ids[start:start + 50]),
        ).execute()

        videos.extend(response.get("items", []))

        show_progress(
            TEXT[lang]["progress_videos"],
            batch_index,
            len(video_batches),
            finish=(batch_index == len(video_batches)),
        )

    channel_ids = list(dict.fromkeys(
        item.get("snippet", {}).get("channelId", "")
        for item in videos
    ))
    channel_ids = [cid for cid in channel_ids if cid]

    channels = {}
    channel_batches = list(range(0, len(channel_ids), 50))

    for batch_index, start in enumerate(channel_batches, 1):
        response = youtube.channels().list(
            part="statistics",
            id=",".join(channel_ids[start:start + 50]),
        ).execute()

        for channel in response.get("items", []):
            channels[channel["id"]] = channel.get("statistics", {})

        show_progress(
            TEXT[lang]["progress_channels"],
            batch_index,
            len(channel_batches),
            finish=(batch_index == len(channel_batches)),
        )

    return videos, channels


# ───────────────────────── analysis ─────────────────────────

def enrich_videos(videos, channels, lang):
    t = TEXT[lang]
    now = datetime.now(timezone.utc)
    results = []

    for item in videos:
        snippet = item.get("snippet", {})
        stats = item.get("statistics", {})
        details = item.get("contentDetails", {})

        try:
            published = datetime.fromisoformat(
                snippet["publishedAt"].replace("Z", "+00:00")
            )
            age_hours = max((now - published).total_seconds() / 3600, 0.1)
            published_text = published.strftime("%Y-%m-%d %H:%M UTC")
            published_sort = published.timestamp()

        except (ValueError, KeyError):
            age_hours = None
            published_text = t["unknown"]
            published_sort = 0

        duration_seconds = parse_duration(details.get("duration", ""))

        if duration_seconds is None:
            video_format = t["unknown"]
        elif duration_seconds <= 180:
            video_format = t["shorts"]
        else:
            video_format = t["longs"]

        views = to_int(stats.get("viewCount")) or 0
        likes = to_int(stats.get("likeCount"))        # None = скрыто
        comments = to_int(stats.get("commentCount"))  # None = отключено/скрыто

        channel_id = snippet.get("channelId", "")
        channel_stats = channels.get(channel_id, {})

        if channel_stats.get("hiddenSubscriberCount"):
            subscribers = None
        else:
            subscribers = to_int(channel_stats.get("subscriberCount"))

        views_per_hour = views / age_hours if age_hours is not None else 0

        views_per_subscriber = (
            views / subscribers if subscribers else None
        )

        like_ratio = (
            likes / views * 100 if likes is not None and views else None
        )

        # Heuristic indicator, not an official YouTube metric.
        # Недоступные метрики вносят 0 в индекс.
        growth_score = (
            min(views_per_hour / 100, 40)
            + min((views_per_subscriber or 0) * 20, 40)
            + min((like_ratio or 0) * 2, 20)
        )

        video_id = item.get("id", "")

        results.append({
            "title": snippet.get("title", ""),
            "video_id": video_id,
            "url": f"https://www.youtube.com/watch?v={video_id}",
            "channel": snippet.get("channelTitle", ""),
            "published": published_text,
            "published_sort": published_sort,
            "duration": format_duration(duration_seconds, t["unknown"]),
            "format": video_format,
            "views": views,
            "likes": likes,
            "comments": comments,
            "subscribers": subscribers,
            "age_days": round(age_hours / 24, 1) if age_hours is not None else None,
            "views_per_hour": round(views_per_hour, 1),
            "views_per_subscriber": (
                round(views_per_subscriber, 3)
                if views_per_subscriber is not None else None
            ),
            "like_ratio": round(like_ratio, 2) if like_ratio is not None else None,
            "growth_score": round(growth_score, 2),
        })

    return results


def classify_popularity(videos, lang):
    t = TEXT[lang]

    by_views = sorted(videos, key=lambda v: v["views"], reverse=True)
    by_growth = sorted(videos, key=lambda v: v["growth_score"], reverse=True)

    # Each group contains the top half of the current combined search results.
    group_size = max(1, (len(videos) + 1) // 2)

    popular_ids = {v["video_id"] for v in by_views[:group_size]}
    trending_ids = {v["video_id"] for v in by_growth[:group_size]}

    for video in videos:
        video["popularity"] = []

        if video["video_id"] in popular_ids:
            video["popularity"].append(t["popular"])

        if video["video_id"] in trending_ids:
            video["popularity"].append(t["trending"])

    return videos


def apply_filters(videos, lang, popularity_choice, format_choice):
    t = TEXT[lang]
    filtered = videos

    if format_choice == "2":
        filtered = [v for v in filtered if v["format"] == t["shorts"]]
    elif format_choice == "3":
        filtered = [v for v in filtered if v["format"] == t["longs"]]

    if popularity_choice == "1":
        filtered = [v for v in filtered if t["popular"] in v["popularity"]]
    elif popularity_choice == "2":
        filtered = [v for v in filtered if t["trending"] in v["popularity"]]

    return filtered


def sort_videos(videos, sort_choice):
    if sort_choice == "1":
        return sorted(videos, key=lambda v: v["views"], reverse=True)

    if sort_choice == "2":
        return sorted(videos, key=lambda v: v["views_per_hour"], reverse=True)

    # Видео без данных о подписчиках уходят в конец
    return sorted(
        videos,
        key=lambda v: (
            v["views_per_subscriber"]
            if v["views_per_subscriber"] is not None else -1
        ),
        reverse=True,
    )


# ───────────────────────── export ─────────────────────────

def export_results(videos, lang, queries):
    t = TEXT[lang]
    output_dir = BASE_DIR / "output"
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base = output_dir / f"video_enricher_{timestamp}"
    query_text = " | ".join(queries)

    columns = [
        ("title", "Title"),
        ("url", "URL"),
        ("popularity_text", t["popularity_label"]),
        ("format", t["format_label"]),
        ("published", t["published"]),
        ("duration", t["duration"]),
        ("views", t["views"]),
        ("likes", t["likes"]),
        ("comments", t["comments"]),
        ("channel", t["channel"]),
        ("subscribers", t["subs"]),
        ("age_days", t["age"]),
        ("views_per_hour", t["vph"]),
        ("views_per_subscriber", t["ratio"]),
        ("growth_score", t["score"]),
    ]

    rows = []

    for video in videos:
        row = dict(video)
        row["popularity_text"] = ", ".join(video["popularity"])
        rows.append(row)

    # ── CSV ──
    with open(str(base) + ".csv", "w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)

        writer.writerow([t["title"]])
        writer.writerow([t["developer"], DEVELOPER])

        for name, link in CONTACTS:
            writer.writerow([name, link])

        writer.writerow(["Search queries", query_text])
        writer.writerow(["Exported", timestamp])
        writer.writerow([])

        writer.writerow([label for _, label in columns])

        for row in rows:
            writer.writerow([
                cell_text(row.get(key), empty="") for key, _ in columns
            ])

    # ── Markdown ──
    with open(str(base) + ".md", "w", encoding="utf-8") as file:
        file.write(f"# {t['title']}\n\n")
        file.write(f"**{t['developer']}:** {DEVELOPER}  \n")
        file.write(
            f"**{t['contacts']}:** "
            + " · ".join(f"[{name}]({link})" for name, link in CONTACTS)
            + "\n\n"
        )
        file.write(f"Search queries: {query_text}  \n")
        file.write(f"Exported: {timestamp}\n\n")

        file.write("| " + " | ".join(label for _, label in columns) + " |\n")
        file.write("| " + " | ".join("---" for _ in columns) + " |\n")

        for row in rows:
            cells = []

            for key, _ in columns:
                value = cell_text(row.get(key))
                value = value.replace("|", "\\|").replace("\n", " ")

                if key == "title":
                    value = f"[{value}]({row['url']})"

                cells.append(value)

            file.write("| " + " | ".join(cells) + " |\n")

    # ── TXT ──
    with open(str(base) + ".txt", "w", encoding="utf-8") as file:
        file.write(f"{t['title']}\n")
        file.write(f"{t['developer']}: {DEVELOPER}\n")

        for name, link in CONTACTS:
            file.write(f"{name}: {link}\n")

        file.write(f"\nSearch queries: {query_text}\n")
        file.write(f"Exported: {timestamp}\n\n")

        for index, row in enumerate(rows, 1):
            file.write(f"{index}. {row['title']}\n")
            file.write(f"   URL: {row['url']}\n")

            for key, label in columns[2:]:
                file.write(f"   {label}: {cell_text(row.get(key))}\n")

            file.write("\n")

    return base


# ───────────────────────── one search session ─────────────────────────

def ask_choice(prompt_text, allowed, invalid_text):
    print(f"\n  {prompt_text}")
    value = input("  > ").strip()

    if value not in allowed:
        print("  ! " + invalid_text)
        return None

    return value


def run_search(youtube, lang, first_run):
    """
    One full cycle: queries -> settings -> search -> export.
    Returns False if the user asked to exit, True otherwise.
    """
    t = TEXT[lang]

    print_section("SEARCH SETUP" if lang == "en" else "НАСТРОЙКА ПОИСКА")

    prompt = t["query"] if first_run else t["next_query"]
    raw_queries = input(f"  {prompt}: ").strip()

    if raw_queries.casefold() in EXIT_WORDS:
        return False

    queries = parse_queries(raw_queries)

    if not queries:
        print("  ! " + t["invalid"])
        return True

    if len(queries) > 10:
        print(
            "  ! Максимум 10 запросов за один запуск."
            if lang == "ru"
            else "  ! Maximum 10 queries per run."
        )
        return True

    try:
        count = int(input(f"  {t['count']}: ").strip())
    except ValueError:
        print("  ! " + t["invalid"])
        return True

    if not 1 <= count <= 50:
        print("  ! " + t["invalid"])
        return True

    popularity_choice = ask_choice(t["popularity"], ("1", "2", "3"), t["invalid"])
    if popularity_choice is None:
        return True

    format_choice = ask_choice(t["format_menu"], ("1", "2", "3"), t["invalid"])
    if format_choice is None:
        return True

    sort_choice = ask_choice(t["sort"], ("1", "2", "3"), t["invalid"])
    if sort_choice is None:
        return True

    print_section("LIVE PROGRESS" if lang == "en" else "ХОД РАБОТЫ")

    cost = len(queries) * MAX_PAGES * SEARCH_COST
    print("  " + t["quota_estimate"].format(cost=cost))
    print(f"  {t['query_count']}: {len(queries)}")

    all_ids = []
    seen_ids = set()
    failed_queries = []
    quota_hit = False

    try:
        for query_index, query in enumerate(queries, 1):
            label = (
                f"Search {query_index}/{len(queries)}"
                if lang == "en"
                else f"Поиск {query_index}/{len(queries)}"
            )

            print(f"\n  ▸ {t['search_query']}: {query}")
            show_progress(label, 0, MAX_PAGES)

            try:
                ids = search_video_ids(
                    youtube,
                    query,
                    progress_callback=lambda current, total, finish, label=label: show_progress(
                        label, current, total, finish
                    ),
                )

                for video_id in ids:
                    if video_id not in seen_ids:
                        seen_ids.add(video_id)
                        all_ids.append(video_id)

                print(
                    f"    {'Found' if lang == 'en' else 'Найдено'}: {len(ids)}  |  "
                    f"{'Unique total' if lang == 'en' else 'Уникальных всего'}: "
                    f"{len(all_ids)}"
                )

            except HttpError as error:
                logging.exception("Search query failed: %s", query)

                if is_quota_error(error):
                    quota_hit = True
                    print("\n  ✗ " + t["quota_exceeded"])
                    break

                failed_queries.append(query)

                if is_key_error(error):
                    print("\n  ✗ " + t["key_rejected"])
                    break

                print(
                    "\n  ✗ "
                    + (
                        f"Search failed: {query}"
                        if lang == "en"
                        else f"Ошибка поиска: {query}"
                    )
                )

            except Exception:
                logging.exception("Search query failed: %s", query)
                failed_queries.append(query)

                print(
                    "\n  ✗ "
                    + (
                        f"Search failed: {query}"
                        if lang == "en"
                        else f"Ошибка поиска: {query}"
                    )
                )

        if not all_ids:
            if not quota_hit:
                print("\n  ! " + t["empty"])
            return True

        print(f"\n  {t['found']}: {len(all_ids)}")
        print(f"\n  [2/4] {t['searching']}")

        raw_videos, channels = get_video_and_channel_data(youtube, all_ids, lang)

        print(
            "\n  [3/4] "
            + (
                "Calculating metrics and applying filters..."
                if lang == "en"
                else "Расчёт показателей и применение фильтров..."
            )
        )

        show_progress("Analyzing" if lang == "en" else "Анализ", 0, 1)

        videos = enrich_videos(raw_videos, channels, lang)
        videos = classify_popularity(videos, lang)
        videos = apply_filters(videos, lang, popularity_choice, format_choice)
        videos = sort_videos(videos, sort_choice)
        videos = videos[:count]

        show_progress("Analyzing" if lang == "en" else "Анализ", 1, 1, finish=True)

        if not videos:
            print("\n  ! " + t["empty"])
            print("  " + t["no_results"])
            return True

        print_summary(videos, lang)

        print(
            "\n  [4/4] "
            + ("Exporting files..." if lang == "en" else "Сохранение файлов...")
        )

        show_progress("Export" if lang == "en" else "Экспорт", 0, 1)
        base = export_results(videos, lang, queries)
        show_progress("Export" if lang == "en" else "Экспорт", 1, 1, finish=True)

        print_section(t["done"])
        print(f"  ✓ {t['selected']}: {len(videos)}")
        print(f"  ✓ {t['saved_to']}: {base.parent.resolve()}")

        print("\n  FILES / ФАЙЛЫ")

        for extension in (".csv", ".md", ".txt"):
            path = Path(str(base) + extension).resolve()
            print(f"  ✓ {path.name}")
            print(f"    {path}")

        if failed_queries:
            print(
                "\n  ! "
                + (
                    "Some searches failed: "
                    if lang == "en"
                    else "Некоторые запросы завершились ошибкой: "
                )
                + ", ".join(failed_queries)
            )

        print("\n" + "=" * 68)
        print(f"  {t['follow']}")
        print(f"  {t['developer']}: {DEVELOPER}")

        for name, link in CONTACTS:
            print(f"  {name:<8} ·  {link}")

        print("=" * 68)

    except HttpError as error:
        logging.exception("Data collection failed")

        if is_quota_error(error):
            print("\n  ✗ " + t["quota_exceeded"])
        elif is_key_error(error):
            print("\n  ✗ " + t["key_rejected"])
        else:
            print("\n  ✗ " + t["api_error"])
            print("  " + t["no_results"])

    except Exception:
        logging.exception("Search failed")
        print("\n  ✗ " + t["api_error"])
        print("  " + t["no_results"])

    return True


# ───────────────────────── entry point ─────────────────────────

def main():
    try:
        lang = choose_language()
        t = TEXT[lang]
        print_header(lang)

        api_key = input(f"\n  {t['api_key']}: ").strip()

        if not api_key:
            print(f"\n  ! {t['api_error']}")
            return

        print(f"\n  [1/4] {t['checking']}")

        try:
            youtube = connect_api(api_key)
            print("  ✓ " + t["api_ok"])

        except Exception as error:
            logging.exception("API connection failed")

            if is_quota_error(error):
                print("  ✗ " + t["quota_exceeded"])
            else:
                print("  ✗ " + t["api_error"])
                print(
                    "  Check the API key, API access, and internet connection."
                    if lang == "en"
                    else "  Проверьте API-ключ, доступ к API и подключение к интернету."
                )

            return

        first_run = True

        # Цикл: после каждого поиска снова спрашиваем запрос
        while run_search(youtube, lang, first_run):
            first_run = False

        print(f"\n  {t['bye']}\n")

    except (KeyboardInterrupt, EOFError):
        print("\n\n  Bye!\n")


if __name__ == "__main__":
    main()
    