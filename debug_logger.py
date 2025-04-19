
import os
from datetime import datetime
from collections import defaultdict

DEBUG_LOG_PATH = "logs/debug_log.txt"
STATS_LOG_PATH = "logs/stats_log.txt"

# Логування повідомлень
def add_debug(message):
    os.makedirs("logs", exist_ok=True)
    with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"[DEBUG] {message}\n")

# Отримання вмісту логу
def get_debug_log():
    if not os.path.exists(DEBUG_LOG_PATH):
        return "Debug лог порожній."
    with open(DEBUG_LOG_PATH, "r", encoding="utf-8") as f:
        return f.read()

# Статистика маршрутів
def update_stats(city_from, city_to):
    date = datetime.now().strftime("%Y-%m-%d")
    with open(STATS_LOG_PATH, "a", encoding="utf-8") as f:
        f.write(f"{date},{city_from},{city_to}\n")

# Зведення статистики за день
def get_route_stats():
    today = datetime.now().strftime("%Y-%m-%d")
    stats = defaultdict(int)
    if not os.path.exists(STATS_LOG_PATH):
        return "Немає статистики за сьогодні."
    with open(STATS_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            date, city_from, city_to = line.strip().split(",")
            if date == today:
                stats[(city_from, city_to)] += 1
    if not stats:
        return "Немає даних за сьогодні."
    return "\n".join([f"{k[0]} ➡ {k[1]} — {v} разів" for k, v in stats.items()])

# Топ-10 міст
def get_top_cities():
    today = datetime.now().strftime("%Y-%m-%d")
    city_count = defaultdict(int)
    if not os.path.exists(STATS_LOG_PATH):
        return "Немає статистики."
    with open(STATS_LOG_PATH, "r", encoding="utf-8") as f:
        for line in f:
            date, city_from, city_to = line.strip().split(",")
            if date == today:
                city_count[city_from] += 1
                city_count[city_to] += 1
    if not city_count:
        return "Немає даних."
    sorted_cities = sorted(city_count.items(), key=lambda x: x[1], reverse=True)[:10]
    return "\n".join([f"{city}: {count} разів" for city, count in sorted_cities])
