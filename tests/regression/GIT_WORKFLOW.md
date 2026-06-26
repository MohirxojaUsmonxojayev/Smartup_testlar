# SmartupAuto — Git Versiyalar Boshqaruvi

## Umumiy Tuzilma

```
main branch:
  └── Faqat TO'LIQ ISHLAYDIGAN kod
  └── Hech qachon to'g'ridan-to'g'ri o'zgartirma
  └── Faqat develop/feature branch merge qilinadi

develop branch:
  └── Asosiy ishchi branch
  └── Yangi o'zgarishlar shu yerda sinab ko'riladi

feature/xxx branch:
  └── Bitta muayyan o'zgarish uchun
  └── Tugatilgach develop ga merge qilinadi
```

---

## Branch Nomlanish Qoidasi

```bash
# Yangi funksiya:
git checkout -b feature/telegram-screenshots
git checkout -b feature/soft-assertion
git checkout -b feature/angular-locator-fix

# Xato tuzatish:
git checkout -b fix/parametry-locator
git checkout -b fix/timeout-error
git checkout -b fix/navigation-stuck

# Test qo'shish:
git checkout -b test/finansy-new-forms
git checkout -b test/sklad-forms
```

---

## Kunlik Ish Jarayoni

### Ishni Boshlash (uydan yoki ishdan)

```bash
# 1. Main dan oxirgi holatni ol
git checkout main
git pull origin main

# 2. Ishchi branchga o'tish
git checkout develop
git merge main  # main dagi o'zgarishlarni develop ga ol

# 3. Ishlash...
```

---

### O'zgarishlarni Saqlash

```bash
# Kichik o'zgarishdan keyin (har 30-60 daqiqada):
git add .
git commit -m "wip: locator muammosi tekshirilmoqda"

# Kun oxirida:
git add .
git commit -m "feat: telegram screenshot yuborish qo'shildi"
git push origin develop
```

---

### Yangi Imkoniyat Qo'shish

```bash
# 1. Develop dan yangi branch
git checkout develop
git checkout -b feature/yangi-imkoniyat

# 2. O'zgarishlarni qil va test qil

# 3. Muvaffaqiyatli bo'lsa — develop ga qaytarish:
git checkout develop
git merge feature/yangi-imkoniyat
git push origin develop

# 4. Eski branchni o'chir:
git branch -d feature/yangi-imkoniyat
git push origin --delete feature/yangi-imkoniyat
```

---

### Main Ga Merge Qilish (faqat barqaror holatda)

```bash
# SHARTLAR:
# ✅ Barcha testlar o'tdi
# ✅ Telegram xabarlari to'g'ri keldi
# ✅ Allure reportda kutilmagan xato yo'q
# ✅ 2-3 marta muvaffaqiyatli run bo'ldi

# Merge:
git checkout main
git merge develop
git push origin main
git tag -a v1.x -m "Versiya 1.x — nima qo'shildi"
git push origin --tags
```

---

### Ish/Uy Qurilmasi O'tkazish

```bash
# Ishdan ketishdan avval:
git add .
git commit -m "wip: tugallanmagan o'zgarish"
git push origin develop

# Uyga yetganda:
git pull origin develop
# Va davom etish...
```

---

## Commit Matn Qoidalari

```
Format: [tur]: [nima qilindi]

Turlar:
  feat:     yangi imkoniyat
  fix:      xato tuzatish
  test:     test o'zgartirish
  docs:     hujjat o'zgartirish
  wip:      tugallanmagan ish (push uchun)
  refactor: kod yaxshilash (funksiya o'zgarmaydi)

Misollar:
  feat: har bir soft fail uchun telegram screenshot
  fix: angular forma locator — app-mbi-report-constructor
  test: konstruktor otchetlar universal locator
  docs: testing rules va git workflow qo'shildi
  wip: finansy formalari tekshirilmoqda
```

---

## Xavfli Holatlar va Yechimlar

### Main buzildi (ilovamiz ishlamay qoldi)
```bash
git checkout main
git log --oneline -10
# Oxirgi ishlaydigan commit ni top
git revert HEAD
# Yoki:
git reset --hard <oxirgi_yaxshi_commit_hash>
git push --force origin main
```

### Noto'g'ri branchga commit qildim
```bash
git log --oneline -3  # commit hash ni ol
git checkout togri-branch
git cherry-pick <commit_hash>
git checkout notogri-branch
git reset HEAD~1
```

### Develop main dan orqada qolib ketdi
```bash
git checkout develop
git merge main
# Conflict bo'lsa — hal qil
git push origin develop
```

---

## Muhim Fayllar

`.gitignore` da quyidagilar bo'lishi SHART:
```
.env               ← Telegram token — HECH QACHON push qilma
__pycache__/
.pytest_cache/
test-results/allure-results/
test-results/allure-report/
test-results/traces/
*.log
```

---

## Hozirgi Branch Holati

| Branch | Maqsad | Holat |
|--------|--------|-------|
| main | Barqaror ishchi kod | ✅ Himoyalangan |
| develop | Asosiy ishchi branch | 🔄 Faol |
| feature/* | Yangi imkoniyatlar | 📝 Kerak bo'lganda |
| fix/* | Xato tuzatish | 🔧 Kerak bo'lganda |

---

## GitHub da Ko'rish

Repository: https://github.com/MohirxojaUsmonxojayev/Smartup_testlar

Qoidalar:
- `main` → to'g'ridan-to'g'ri push qilmang
  (ixtiyoriy: GitHub Settings → Branch Protection Rules)
- Barcha o'zgarishlar `develop` orqali o'tadi
- Tag qo'yish: har barqaror versiyada

---

## Uy Qurilmasida Boshlash

```bash
git clone https://github.com/MohirxojaUsmonxojayev/Smartup_testlar.git
cd Smartup_testlar
git checkout develop
pip install -r requirements.txt

# Test ishlatish:
python -m pytest tests/regression/test_check_forms_opening.py \
    --url https://app3.greenwhite.uz/xtrade \
    --company-code novatrade \
    --company-password greenwhite \
    --headless
```
