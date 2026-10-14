# Topshiriq rasmlari

Yangilangan kontent: 150 ta asosiy topshiriq va kvestlar ichidagi 29 ta mavjud bosqich.
Savol turlari, savol va variantlar soni saqlangan.

## Illyustratsiyalar

Savol sahnalari, hayvonlar, kasblar, buyumlar, fasllar va yashash muhitlari
`image_gen.imagegen` ichki vositasi bilan har biri alohida qayta yaratilgan.
Rasmlar bir xil bolalar kitobi uslubida tayyorlangan. Variantlarning foni shaffof;
bir xil mazmundagi kartochkalarda uslub javobni oshkor qilmaydi.

Har bir rasmning yakuniy prompti va shaffoflik talabi `GENERATSIYA.json` faylida.
Joriy kontent WebP rasmlardan foydalanadi. WebP yuqori sifatda kodlangan: tasvir o'lchami va alfa kanali aynan saqlangan.
Rang sifati tekshiriladi; yetarli sifat chiqmasa, yo'qotishsiz kodlash qo'llanadi.
Eski PNG fayllar avvalgi migratsiyalar va kontentni qaytarish uchun saqlangan.

## Aniq ta'lim tasvirlari

Sanoq to'plamlari, shakllar, ranglar, soyalar, naqshlar, robot yo'llari, tajriba
panellari, konstruktor namunalari va bo'laklari SVG sifatida qayta yaratilgan.
His-tuyg'u yuzlari bitta qolipdan olingan: yuzning tuzilishi saqlanib, ifodasi
almashadi. Soya tasvirlari rangli buyumning aynan o'sha alfa shaklidan olinadi.

`generate_diagrams.py` ham namuna rasmini, ham uning bo'laklarini bitta ta'rifdan
hosil qiladi. Mavjud o'yin maydoni 100:70 nisbatda; uyalar koordinatalari shu
nisbatga moslangan. Shu sababli kvadrat va doiralar maydonda cho'zilmaydi.
Bo'yash chizmalarida har bir faol qism `data-soha`, namuna talab qiladigan
ranglar esa `data-togri` bilan belgilanadi.

Qayta yaratish:

```powershell
env\Scripts\python.exe static/images/topshiriq/generate_diagrams.py
```

Bu buyruq rasmlarni va 0022 migratsiyasidagi rasm yo'llarini yangilaydi.
Amaldagi bazaga qayta qo'llash kerak bo'lsa, migratsiyani odatdagi Django
migratsiya tartibida boshqaring; skript savol yoki variant yaratmaydi.
