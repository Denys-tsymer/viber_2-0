def classify_message(text):
    # Простий фільтр за ключовими словами
    if 'пасажир' in text.lower():
        return 'passenger'
    elif 'посилка' in text.lower():
        return 'parcel'
    elif 'діти' in text.lower():
        return 'children'
    elif 'тварини' in text.lower():
        return 'animals'
    elif 'адреса' in text.lower():
        return 'address'
    else:
        return 'unknown'
