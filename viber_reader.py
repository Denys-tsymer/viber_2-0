import os
import time
import threading
import pytesseract
from PIL import Image
from settings import TESSERACT_PATH, OCR_LANGUAGES, CITY_DATABASE_PATH
from telegram_sender import send_to_telegram
from debug_logger import add_debug, update_stats
from rapidfuzz import fuzz

pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

def delete_file_later(filepath, delay=60):
    def delayed():
        time.sleep(delay)
        try:
            os.remove(filepath)
        except:
            pass
    threading.Thread(target=delayed, daemon=True).start()

def load_city_database():
    cities = {}
    for root, dirs, files in os.walk(CITY_DATABASE_PATH):
        for file in files:
            if file.endswith(".txt"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    for line in f:
                        parts = line.strip().split("—")
                        if len(parts) >= 2:
                            name = parts[0].strip()
                            cities[name.lower()] = {
                                "original": name,
                                "ukrainian": parts[1].strip(),
                                "zip": parts[2].strip() if len(parts) > 2 else "",
                            }
    return cities

def extract_blocks(text):
    return [block.strip() for block in text.split("\n") if len(block.strip()) > 5]

def classify(text):
    text = text.lower()
    if any(word in text for word in ["пасажир", "пас", "людина", "місце"]):
        return "👤 Пасажир"
    elif any(word in text for word in ["посилка", "пакунок", "кг", "док", "передача"]):
        return "📦 Посилка"
    elif any(word in text for word in ["дит", "немовля", "малюк"]):
        return "👶 Дитина"
    elif any(word in text for word in ["тварин", "кіт", "пес", "собака"]):
        return "🐾 Тварина"
    return "❓ Невідомо"

def find_cities(text, db, threshold=80):
    found = []
    for word in text.split():
        word = word.strip(",.!?-_").lower()
        for city in db:
            score = fuzz.ratio(word, city)
            if score >= threshold:
                found.append((city, db[city]))
                add_debug(f"🎯 Збіг: {word} ≈ {city} ({score}%)")
    return found

def generate_map_link(city_name):
    return f"https://www.google.com/maps/search/{city_name.replace(' ', '+')}"

def process_image(image_path):
    try:
        add_debug(f"📷 Обробка зображення: {image_path}")
        image = Image.open(image_path)
        ocr_text = pytesseract.image_to_string(image, lang=OCR_LANGUAGES)
        add_debug('📄 OCR TEXT:\n' + ocr_text)

        blocks = extract_blocks(ocr_text)
        db = load_city_database()

        for block in blocks:
            found = find_cities(block, db)
            if len(found) >= 2:
                city1, data1 = found[0]
                city2, data2 = found[1]
                category = classify(block)
                update_stats(data1["ukrainian"])
                update_stats(data2["ukrainian"])

                bolded = block
                for city in (city1, city2):
                    bolded = bolded.replace(city, f"<b>{city}</b>")

                msg = f"""<b>🔎 Виявлено маршрут</b>
📄 <i>{bolded}</i>

📍 {data1["original"]} — {data1["ukrainian"]} ➡ {data2["original"]} — {data2["ukrainian"]}
🔖 Категорія: {category}
🏷 Індекси: {data1["zip"]} ➡ {data2["zip"]}
🌍 Мапа: {generate_map_link(data1["original"])} ➡ {generate_map_link(data2["original"])}
"""

                asyncio.run(send_to_telegram(msg.strip(), image_path))
                add_debug(f"📨 Надіслано повідомлення: {data1['ukrainian']} ➡ {data2['ukrainian']}")
                break
            else:
                add_debug("⚠️ Недостатньо міст у блоці")

        delete_file_later(image_path)
    except Exception as e:
        add_debug(f"❌ Помилка при обробці: {e}")