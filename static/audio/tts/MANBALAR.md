# O'zbekcha savol ovozlari

Savol matnlari Bilimbo bazasidagi `ovoz_matn` (bo'sh bo'lsa `matn`) maydonidan,
qo'shimcha audio esa `audio_matn` maydonidan olinadi. Hayvonlarning haqiqiy
ovoz fayllari bu generatsiyaga kirmaydi.

- Xizmat: Microsoft Edge onlayn text-to-speech.
- Kutubxona: [edge-tts](https://github.com/rany2/edge-tts), 7.3.1.
- Asosiy ovoz: `uz-UZ-MadinaNeural`; namunalar uchun `uz-UZ-SardorNeural` ham.
- Til: o'zbekcha (lotin yozuvi).
- Tezlik: `-10%`; ovoz balandligi va tembri o'zgartirilmagan.
- Format: MP3. Matn, ovoz va tezlik xeshi fayl nomiga kiradi.
- `SAVOLLAR.json`: oxirgi generatsiyadagi savollar, tayyorlangan matnlar va yo'llar.
- `namunalar.html`: uchta savolni ikkala ovozda tinglash sahifasi.

Ovozlar ushbu buyruq bilan qayta yaratiladi:

```bash
python manage.py generate_question_audio
```

Microsoft o'zbekcha ovozlari haqida:
[Azure Speech language support](https://learn.microsoft.com/azure/cognitive-services/speech-service/language-support?tabs=tts).
`edge-tts` norasmiy kutubxona. Rasmiy xizmatga o'tilganda tayyor MP3 ijrosi
o'zgarmaydi; faqat fayllarni yaratadigan funksiya almashtiriladi.
