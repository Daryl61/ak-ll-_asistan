from asisstant import get_gemini_response , detect_intent
from database import create_connection, add_note, add_event, get_notes, get_events

create_connection()

print("Hoşgeldin abi")
print("Komutlar: not ekle | notları göster | etkinlik ekle | etkinlikleri göster | sohbet et | çıkış")

while True:
    command = input("EMİR VER: ").strip().lower()

    if command == "not ekle":
        content = input("Not içeriği: ").strip()
        add_note(content)
        print("Not eklendi.")

    elif command == "notları göster":
        notes = get_notes()
        if notes:
            print("Notlar:")
            for content, created_at in notes:
                print(f"- {content} (oluşturulma tarihi: {created_at})")
        else:
            print("Not bulunamadı.")

    elif command == "etkinlik ekle":
        event = input("Etkinlik adı: ").strip()
        event_date = input("Etkinlik tarihi: ").strip()
        add_event(event, event_date)
        print("Etkinlik eklendi.")

    elif command == "etkinlikleri göster":
        events = get_events()
        if events:
            print("Etkinlikler:")
            for event, event_date in events:
                print(f"- {event} (tarih: {event_date})")
        else:
            print("Etkinlik bulunamadı.")

    elif command == "sohbet et":
        mesaj = input("Kullanıcı Sorusu: ").strip()
        intent = detect_intent(mesaj)
        if intent == "not_ozet":
            notes = get_notes()
            if not notes:
                print("Not bulunamadı.")
                continue

            all_notes_text = "\n".join([f"- {note[0]}" for note in notes])
            prompt = f"Bu notları özetle:\n{all_notes_text}"
            summary = get_gemini_response(prompt)

            print("Not özeti:")
            print(summary)

        elif intent == "etkinlik_goster":
            events = get_events()
            if not events:
                print("Henüz etkinlik yok.")
                continue

            all_events_text = "\n".join([f"- {e[0]} ({e[1]})" for e in events])
            prompt = f"Aşağıdaki etkinlikleri özetler misin?\n{all_events_text}"
            summary = get_gemini_response(prompt)

            print("Etkinlik özeti:")
            print(summary)

        else:
            response = get_gemini_response(mesaj)
            print("Asistan:", response)

    elif command == "çıkış":
        print("Çıkılıyor...")
        break

    else:
        print("Geçersiz komut girdin.")