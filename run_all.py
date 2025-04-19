import subprocess

if __name__ == "__main__":
    # Запускає main.py та telegram_bot.py одночасно
    subprocess.Popen(["python", "main.py"])
    subprocess.Popen(["python", "telegram_bot.py"])