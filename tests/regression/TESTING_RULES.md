> ⚠️ **BU HUJJATNI HAR SESSIYA BOSHIDA O'QI.**
> Bu loyihada test fayllari 2000+ qator bo'lishi mumkin.
> Faylga ishlov berishdan oldin pastdagi "TOKEN TEJASH QOIDALARI" bo'limiga rioya qil.

# SmartupAuto — Test Yozish Qoidalari va Xatoliklar

## Ushbu hujjat haqida

Bu fayl test yozishda qilingan **real xatoliklar** asosida tuzilgan.
Har bir yangi test yoki o'zgartirish qilishdan avval o'qilishi **SHART**.

---

## ⚡ TOKEN TEJASH QOIDALARI

### Katta faylda ko'p o'xshash o'zgarish kerak bo'lsa:
1. Avval faylni TO'LIQ o'qima
2. `grep -n` bilan o'zgaradigan qatorlarni top
3. Python skript yoz (`re` / regex orqali) — skript faylni dasturiy o'zgartirsin
4. Skriptni ishga tushir
5. Natijani `grep -c` bilan tasdiqlа
6. Faqat 1-2 ta namuna qadamni `Read(offset, limit)` bilan tekshir

### Kichik o'zgarish kerak bo'lsa (1-10 qator):
1. `Edit` (str_replace) ishlatilsin — `Write` (create_file) EMAS
2. Faqat o'zgaradigan qismni o'qish yetarli

### Fayl holatini tekshirish kerak bo'lsa:
1. `wc -l` bilan qator sonini bil
2. `grep -n` bilan kerakli joyni top
3. `Read(offset=X, limit=Y)` bilan FAQAT shu joyni ko'r
4. Butun faylni o'qish — oxirgi chora

### Taqiqlanadi:
- 100+ ta bir xil pattern bo'lsa, ularni birma-bir qo'lda yozish
- Har edit dan keyin butun faylni qayta o'qish
- `Write` orqali mavjud katta faylni qayta yaratish (`Edit` yetarli bo'lsa)
- 2000+ qatorli faylni `Read` (limit ko'rsatmasdan) bilan to'liq ochish

---

## ❌ QILISH MUMKIN BO'LMAGAN ISHLAR

### 1. Murakkab fallback locator qo'shish

**XATO:**
```python
def check_element_visible(page, locator, text):
    try:
        expect(page.locator(locator)).to_contain_text(text)
    except:
        expect(page.locator("button, tab, span, a")
              .filter(has_text=text)).to_be_visible()
```

**NIMA YOMON:** Test soatlab ishlaydi — ko'p elementlarni birma-bir qidiradi.
Har bir muvaffaqiyatsiz qadam 30–120 soniya kutadi, 200+ qadamda bu
soatlarga aylanadi.

**TO'G'RI:**
```python
expect(page.locator("b-page")).to_contain_text("Параметры")
```

Agar element topilmasa — bu **TEST XATOSI emas, TIZIM XATOSI**.
Soft assertion bilan yoz va davom et.

---

### 2. Faqat `AssertionError` ushlash

**XATO:**
```python
except AssertionError:
    soft.check(False, "...")
```

**NIMA YOMON:** Playwright `TimeoutError`, `NavigationError` va boshqa
xatolar ushlanmaydi — test to'xtab qoladi va qolgan 200+ qadam tekshirilmaydi.

**TO'G'RI:**
```python
except Exception as e:
    soft.check(False,
        f"❌ [Bo'lim] Forma — element topilmadi | {type(e).__name__}")
```

---

### 3. Barcha formalar bir xil deb taxmin qilish

**XATO:** Bir formada Angular locator ishladi deb barcha o'xshash
formalarga ham `app-mbi-report-constructor` qo'llash.

**NIMA YOMON:** Tizimda eski (`b-page`) va yangi Angular
(`app-mbi-report-constructor`) formalar **ARALASH** mavjud.
Ba'zi "Конструктор отчетов" formalari hali eski tizimda.

**TO'G'RI — UNIVERSAL LOCATOR:**
```python
page.wait_for_load_state("domcontentloaded", timeout=10000)
angular = page.locator("app-mbi-report-constructor")
if angular.count() > 0:
    expect(angular).to_contain_text("Параметры", timeout=10000)
else:
    expect(page.locator("b-page")).to_contain_text("Параметры", timeout=10000)
```

---

### 4. Locatorni taxmin qilish

**XATO:** `"Параметры"` button ko'rinishida bo'lishi mumkin deb
`get_by_role("button")` ishlatish.

**TO'G'RI:** Avval codegen bilan tekshir:
```bash
python -m playwright codegen https://app3.greenwhite.uz/xtrade
```

Faqat codegen ko'rsatgan locatorni ishlatish. Taxmin qilma — isbotla.

---

## ✅ DOIM QILINADIGAN ISHLAR

### 1. Yangi locator qo'shishdan avval

- Codegen bilan real sahifada tekshir
- `debug_*.py` fayl yozib DOM ni ko'r
- Taxmin qilma — isbotla

### 2. Har bir `expect()` try/except ga o'ralgan bo'lsin

```python
try:
    expect(page.locator("b-page")).to_contain_text("Создать")
except Exception as e:
    soft.check(False,
        f"❌ [Главное] Организации — 'Создать' topilmadi | {type(e).__name__}")
```

### 3. Angular forma aniqlash

Quyidagi belgilar Angular formani ko'rsatadi:
- URL da `/a2/` mavjud
- `app-*` locator ishlaydi
- `b-page` locator `count() == 0`

Tekshirish:
```python
print(page.locator("app-mbi-report-constructor").count())  # > 0 = Angular
print(page.locator("b-page").count())                      # > 0 = eski
```

### 4. Navigatsiya xatosi bo'lganda

Angular formadan chiqishda `link` emas `button` ishlatilishi kerak:
```python
# Eski forma sahifasidan:
page.get_by_role("link", name="Продажа").click()

# Angular forma sahifasidan (commercial_dashboard va hokazo):
page.get_by_role("button", name="Продажа").click()
```

**Yoki ishonchli usul** — `goto(_home_url)` bilan bosh sahifaga qayt:
```python
try:
    page.goto(_home_url, wait_until="domcontentloaded", timeout=8000)
except Exception:
    pass
```

### 5. Test vaqtini nazorat qilish

| Holat | Vaqt | Baho |
|-------|------|------|
| 1 ta qadam | < 30 soniya | Normal |
| To'liq 219 qadam | 5–10 daqiqa | Normal |
| To'liq 219 qadam | 10–20 daqiqa | Locator muammosi bor |
| To'liq 219 qadam | 30+ daqiqa | Jiddiy muammo — to'xtat va tahlil qil |

---

## 📋 YANGI TEST YOZISH CHECKLIST

Har bir yangi forma uchun:

- [ ] Codegen bilan locator aniqlandi
- [ ] Angular yoki eski forma ekanini tekshirdim
- [ ] `expect()` `try/except` ga o'ralgan
- [ ] `except Exception as e` ishlatilgan (`AssertionError` emas)
- [ ] Xato xabari qisqa va aniq: `"❌ [Bo'lim] Forma | XatoTuri"`
- [ ] Soft assertion oxirida `assert_all()` chaqiriladi
- [ ] Timeout 30 soniyadan oshmasin

---

## 🏗️ TIZIM ARXITEKTURASI

### Locator xaritasi

| Forma turi | Locator | Misol sahifalar |
|------------|---------|-----------------|
| Eski forma | `b-page` | Организации, Пользователи, Параметры |
| Angular konstruktor | `app-mbi-report-constructor` | Конструктор отчетов (ba'zilari) |
| Grid forma | `b-grid` | Шаги визита, Объекты |
| Heading forma | `[role="heading"]` | Визиты, Архив визитов |
| Forma elementi | `form` | Настройки интеграции |
| Maxsus selektor | `#anor288-button-add` | Alohida hollar |
| Dropdown | `smt-dropdown-button` | Экспорт tugmasi |

### Aralash tizim haqida

SmartupAuto hali migratsiya jarayonida — ba'zi modullar Angular ga
o'tgan, qolganlar hali eski `b-page` arxitekturasida. Shuning uchun:

- "Конструктор отчетов" bo'limida ham eski, ham Angular formalar bor
- Har doim `angular.count() > 0` bilan tekshirish kerak
- URL dagi `/a2/` Angular sahifani bildiradi

---

## 🔄 MUAMMO CHIQSA NIMA QILISH

1. **Test qaysi qadamda to'xtadi?** → Allure report da ko'r (`allure serve test-results/allure-results`)
2. **Element sahifada bormi?** → Brauzerda ko'r (`--headed` flag bilan ishga tushir)
3. **Locator to'g'rimi?** → Codegen bilan tekshir
4. **Angular yoki eski forma?** → URL da `/a2/` bormi?
5. **Hali ham ishlamaydi?** → `debug_form.py` yoz, DOM ni chiqar:
   ```python
   print(page.content())  # Butun HTML
   print(page.locator("app-mbi-report-constructor").count())
   print(page.locator("b-page").count())
   ```

---

## 📝 SESSIYADA ANIQLANGAN XATOLIKLAR TARIXI

| # | Xato | Sabab | Yechim |
|---|------|-------|--------|
| 1 | Test 30–50 daqiqa ishladi | `check_element_visible()` ko'p fallback locator qidirdi | `to_contain_text()` bilan almashtirish |
| 2 | `TimeoutError` da test to'xtadi | `except AssertionError` faqat assert xatolarini ushladi | `except Exception as e` |
| 3 | 12 Angular forma xato berdi | Barcha Конструктор formalari Angular deb taxmin qilindi | Universal `angular.count() > 0` pattern |
| 4 | Angular forma dan keyingi navigatsiya to'xtadi | Angular formada menyu `link` emas `button` | `goto(_home_url)` bilan qaytish |

**Natija:** 32 daqiqa → 8 daqiqa, 219 qadamning 217 tasi muvaffaqiyatli.
