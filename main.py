import time
import os
from datetime import datetime
from viber_reader import process_image
import mss
from PIL import Image

# Папка для скріншотів
SCREENSHOT_FOLDER = "ocr/screenshots/"
os.makedirs(SCREENSHOT_FOLDER, exist_ok=True)
os.makedirs(os.path.join(SCREENSHOT_FOLDER, 'processed'), exist_ok=True)

def capture_screen():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = sct.grab(monitor)
        img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        path = os.path.join(SCREENSHOT_FOLDER, filename)
        img.save(path)
        return path

def delete_old_processed_files():
    now = time.time()
    processed_dir = os.path.join(SCREENSHOT_FOLDER, 'processed')
    for file in os.listdir(processed_dir):
        full_path = os.path.join(processed_dir, file)
        if os.path.isfile(full_path) and now - os.path.getmtime(full_path) > 60:
            os.remove(full_path)
            print(f"🗑 Видалено старий файл: {file}")

def main():
    print("✅ Бот запущено. Автоматичне зчитування з екрана кожні 10 секунд.")
    while True:
        try:
            screenshot_path = capture_screen()
            print(f"📷 Знято скріншот: {os.path.basename(screenshot_path)}")
            process_image(screenshot_path)
            processed_path = os.path.join(SCREENSHOT_FOLDER, 'processed', os.path.basename(screenshot_path))
            os.rename(screenshot_path, processed_path)
            print("✅ Оброблено.")
            delete_old_processed_files()
        except Exception as e:
            print(f"❌ Помилка: {e}")
        time.sleep(10)

if __name__ == "__main__":
    main()