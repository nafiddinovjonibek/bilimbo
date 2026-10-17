# O'zbekcha savol ovozlari

Savol matnlari Bilimbo bazasidagi `ovoz_matn` (bo'sh bo'lsa `matn`) maydonidan,
qo'shimcha audio esa `audio_matn` maydonidan olinadi. Hayvonlarning haqiqiy
ovoz fayllari bu generatsiyaga kirmaydi.

- Xizmat: Microsoft Edge onlayn text-to-speech.
- Kutubxona: [edge-tts](https://github.com/rany2/edge-tts), 7.3.1.
- Mavjud savol yozuvlari: `uz-UZ-MadinaNeural`; namunalar uchun `uz-UZ-SardorNeural` ham.
- Tanlangan asosiy ovoz: Narakeet `odina`. Uning savol audiolari API kaliti
  sozlangach yaratiladi; tayyor bo'lguncha Madina yozuvlari ijro etiladi.
- Til: o'zbekcha (lotin yozuvi).
- Tezlik: `-10%`; ovoz balandligi va tembri o'zgartirilmagan.
- Format: MP3. Matn, ovoz va tezlik xeshi fayl nomiga kiradi.
- `SAVOLLAR.json`: oxirgi generatsiyadagi savollar, tayyorlangan matnlar va yo'llar.
- `namunalar.html`: savollarni turli ovozlarda tinglash va xizmatlarning
  tayyor demo ovozlari bilan tanishish sahifasi.
- `QOSHIMCHA_NAMUNALAR.json`: qo'shimcha namunalar, matn turi va manba URL lari.

## Narakeet demo ovozlari

Dilnoza, Odina, Gulnora, Zulfiya va Shavkat yozuvlari
[Narakeet ovozlar katalogi](https://www.narakeet.com/languages/#group-Uzbek) dagi
ochiq demo MP3 manzillaridan ijro etiladi. Fayllar loyihaga ko'chirilmagan.
Bu namunalarda xizmatning demo matni o'qiladi, Bilimbo savollari emas.
Yangi savolni Narakeet orqali yaratish joriy tarmoqdan xizmatning network
reputation controls tekshiruvi sabab bloklandi; bu cheklov chetlab o'tilmadi.

Odina uchun rasmiy API integratsiyasi `home/narakeet.py` da. MP3 lar
`audio/tts/odina/` ga yoziladi, `voice=odina` va `voice-speed=1.00`
parametrlari ishlatiladi. API kaliti `.env` dagi `NARAKEET_API_KEY` orqali
olinadi. [Rasmiy API hujjati](https://www.narakeet.com/docs/automating/text-to-speech-api/).
Namuna sahifasida Odina "Tanlangan ovoz" deb belgilangan.

## Boshqa xizmatlarning sinov holati

[VoiceLab o'zbekcha sinov sahifasi](https://voicelab.uz/text-to-speech/uzbek)
Bilimbo savoli bilan tekshirildi. `language=uz` so'rovi HTTP 200 va
`audio/wav` qaytardi, lekin audio tanasi 0 bayt bo'lgani uchun namuna
qo'shilmadi. ElevenLabs uchun muhitda API kaliti sozlanmagan.
Bu xizmatlar nomidan audio o'rniga boshqa xizmat yozuvlari berilmagan.

Ovozlar ushbu buyruq bilan qayta yaratiladi:

```bash
python manage.py generate_question_audio
```

Microsoft o'zbekcha ovozlari haqida:
[Azure Speech language support](https://learn.microsoft.com/azure/cognitive-services/speech-service/language-support?tabs=tts).
`edge-tts` norasmiy kutubxona. Rasmiy xizmatga o'tilganda tayyor MP3 ijrosi
o'zgarmaydi; faqat fayllarni yaratadigan funksiya almashtiriladi.
