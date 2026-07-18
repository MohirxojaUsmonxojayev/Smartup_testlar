# 🚀 Smartup Test Automation Framework

> **Enterprise-grade Selenium Test Automation Framework with Flow Pattern, Advanced Logging, Qase.io Integration & Email Reporting**

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-green)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.x-orange)](https://pytest.org/)
[![Qase.io](https://img.shields.io/badge/Qase.io-Integrated-purple)](https://qase.io/)
[![Allure](https://img.shields.io/badge/Allure-Report-red)](https://docs.qameta.io/allure/)
[![Framework](https://img.shields.io/badge/Framework-Flow%20Based%20POM-purple)](https://github.com)

---

## 📑 Mundarija

- [Kirish](#-kirish)
- [Asosiy Xususiyatlar](#-asosiy-xususiyatlar)
- [Arxitektura](#-arxitektura)
- [O'rnatish](#-ornatish)
- [Environment Configuration](#-environment-configuration)
- [Tez Boshlash](#-tez-boshlash)
- [Logging Tizimi](#-logging-tizimi)
- [UI Loaders Mexanizmi](#-ui-loaders-mexanizmi)
- [Exception Handling](#-exception-handling)
- [Flow Pattern](#-flow-pattern)
- [Page Object Model](#-page-object-model)
- [Auth Flow](#-auth-flow)
- [Qase.io Integration](#-qaseio-integration)
- [Email Reporting](#-email-reporting)
- [Screen Recording](#-screen-recording)
- [Testlarni Ishga Tushirish](#-testlarni-ishga-tushirish)
- [Allure Report](#-allure-report)
- [Best Practices](#-best-practices)
- [Troubleshooting](#-troubleshooting)
- [FAQ](#-faq)

---

## 🎯 Kirish

**Smartup Test Automation Framework** - bu professional enterprise darajadagi test automation framework bo'lib, quyidagi texnologiyalar va integratsiyalar asosida qurilgan:

### 🛠️ Texnologiyalar

- **Selenium WebDriver 4.x** - Brauzer avtomatizatsiyasi
- **Pytest 7.x** - Test runner va fixture management
- **Allure Report** - Vizual test hisobotlar
- **Qase.io** - Test case management va tracking
- **OpenCV & FFmpeg** - Screen recording (video)
- **SMTP** - Email reporting
- **Colorama** - Rangli console logs

### 🎭 Kimlar uchun?

- ✅ QA Automation Engineers (Junior → Senior)
- ✅ SDET (Software Development Engineer in Test)
- ✅ Test Automation Architects
- ✅ Enterprise loyihalarda ishlovchilar
- ✅ CI/CD pipeline larida test automation qo'llaydiganlar

---

## ⭐ Asosiy Xususiyatlar

### 🔥 Core Features

| Xususiyat | Tavsif | Status |
|-----------|--------|--------|
| 🎯 **Flow-based Pattern** | Biznes jarayonlarni qayta ishlatish va minimal kod takrorlash | ✅ Production |
| 🔍 **Caller Chain Tracking** | Xatoliklarni aniq topish uchun to'liq call stack | ✅ Production |
| ⏱️ **Automatic Timing** | Har bir metodning bajarilish vaqtini avtomatik yozish | ✅ Production |
| 🎨 **Colored Logging** | Console da rangli va o'qilishi oson loglar | ✅ Production |
| 🌐 **UI Loaders Handler** | Angular, React, jQuery async operatsiyalarni avtomatik kutish | ✅ Production |
| 📸 **Auto Screenshots** | Xatolik vaqtida avtomatik screenshot olish | ✅ Production |
| 🎥 **Screen Recording** | FFmpeg/OpenCV orqali video yozish | ✅ Production |
| 🔄 **Smart Retry** | Stale element, scroll va boshqa xatolarni avtomatik retry qilish | ✅ Production |
| 📊 **Soft Assertions** | Bir nechta assertionlarni yig'ish va oxirida ko'rsatish | ✅ Production |
| 📧 **Email Reports** | Test natijalarini avtomatik email orqali yuborish | ✅ Production |
| 🔗 **Qase.io Integration** | Test case management va tracking | ✅ Production |
| 📈 **Allure Reports** | Professional vizual hisobotlar | ✅ Production |
| 🧪 **Data-driven Tests** | Bir test funksiyasi - ko'p test scenariylari | ✅ Production |
| 🔐 **Auth Flow** | Centralized login/logout management | ✅ Production |
| ♻️ **Test Retry** | Muvaffaqiyatsiz testlarni avtomatik retry | ✅ Production |

---

## 🏗️ Arxitektura

### Loyiha Strukturasi

```
Smartup_testlar/
│
├── pages/                                # Page Object Model
│   ├── core/
│   │   └── md/
│   │       ├── base_page.py              # ⭐ Asosiy Page class
│   │       └── login_page.py             # Login page
│   └── anor/
│       └── mdeal/
│           └── order/
│               ├── order_add_main.py
│               ├── order_add_product.py
│               └── order_add_final.py
│
├── flows/                                # ⭐ Flow functions (biznes logika)
│   ├── auth_flow.py                      # ⭐ Login/logout flows
│   └── order_flows/
│       └── order_add_flow.py             # main_flow, product_flow, final_flow
│
├── tests/                                # Test files
│   └── ui/
│       ├── test_order/
│       │   ├── test_order.py             # ⭐ 80+ testlar
│       │   └── test_order_edit.py
│       └── test_reference/
│           └── test_legal_person.py      # ⭐ Qase.io misoli
│
├── utils/                                # ⭐ Utility modules
│   ├── logger.py                         # Logging configuration
│   ├── log_helpers.py                    # Caller chain tracking
│   ├── ui_loaders.py                     # ⭐ UI async handlers
│   ├── exception.py                      # Custom exceptions
│   ├── assertions.py                     # Assertion helpers
│   ├── email.py                          # ⭐ Email reporting
│   ├── screen_recorder.py                # ⭐ Video recording
│   └── env_reader.py                     # Environment config
│
├── logs/                                 # Log files (auto-generated)
├── screenshot_dir/                       # Screenshots (auto-generated)
├── artifacts/videos/                     # ⭐ Video recordings (auto-generated)
├── allure-results/                       # ⭐ Allure raw data
├── .env                                  # ⭐ Environment variables
├── pytest.ini                            # ⭐ Pytest configuration
├── conftest.py                           # ⭐ Pytest fixtures & hooks
└── README.md                             # Bu fayl
```

---

## 🛠️ O'rnatish

### 1. Requirements

**System Requirements:**
- Python 3.8+
- Chrome/Firefox browser
- ChromeDriver (automatic via webdriver-manager)
- FFmpeg (optional, video encoding uchun)

**FFmpeg O'rnatish (ixtiyoriy, lekin tavsiya etiladi):**

```bash
# Windows (Chocolatey)
choco install ffmpeg

# Ubuntu/Debian
sudo apt update
sudo apt install ffmpeg

# macOS (Homebrew)
brew install ffmpeg

# Tekshirish
ffmpeg -version
```

### 2. Virtual Environment Yaratish

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Dependencies O'rnatish

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```txt
# Core
selenium==4.15.0
pytest==7.4.3
webdriver-manager==4.0.1

# Logging & Colors
colorama==0.4.6

# Reporting
allure-pytest==2.13.2
qase-pytest==6.1.5

# Video Recording
opencv-python==4.8.1.78
numpy==1.24.3

# Utils
python-dotenv==1.0.0
```

### 4. Environment Configuration

`.env` fayl yaratish (root directory da):

```env
# ==================== BASE CONFIGURATION ====================
# Base URL
URL=https://smartup.online

# Company credentials
EMAIL_COMPANY=admin@head
PASSWORD_COMPANY=greenwhite
CODE_INPUT=autotest

# User credentials
PASSWORD_USER=123456789

# ==================== TIMEOUT SETTINGS ====================
DEFAULT_TIMEOUT=30
PAGE_LOAD_TIMEOUT=120

# ==================== QASE.IO CONFIGURATION ====================
QASE_MODE=testops
QASE_TESTOPS_PROJECT=RP
QASE_TESTOPS_API_TOKEN=your_qase_api_token_here
QASE_TESTOPS_RUN_TITLE=Automation tests

# ==================== EMAIL CONFIGURATION ====================
# Gmail SMTP settings
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password_here
EMAIL_RECIPIENTS=qa_team@company.com,manager@company.com
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# ==================== FEATURE FLAGS ====================
ENABLE_VIDEO_RECORDING=true
ENABLE_EMAIL_REPORTS=true
ENABLE_QASE_REPORTING=true
```

---

## 🔐 Environment Configuration

### Gmail App Password Yaratish

Email reporting ishlashi uchun Gmail App Password kerak:

1. Google Account ga kiring: https://myaccount.google.com/
2. **Security** bo'limiga o'ting
3. **2-Step Verification** ni yoqing (agar yoqilmagan bo'lsa)
4. **App passwords** ga o'ting
5. **Select app** → **Other** → **"Smartup Tests"** deb nom bering
6. **Generate** tugmasini bosing
7. 16 belgili parolni `.env` fayldagi `EMAIL_PASSWORD` ga kiriting

### Qase.io API Token Olish

1. Qase.io ga kiring: https://app.qase.io/
2. **Settings** → **API Tokens**
3. **Create new token** tugmasini bosing
4. Token ni copy qiling
5. `.env` fayldagi `QASE_TESTOPS_API_TOKEN` ga kiriting

---

## 🚀 Tez Boshlash

### Birinchi Test Yozish

**1. Page Object yaratish:**

```python
# pages/example_page.py
from selenium.webdriver.common.by import By
from pages.core.md.base_page import BasePage

class ExamplePage(BasePage):
    # Locators
    username_input = (By.ID, "username")
    password_input = (By.ID, "password")
    login_button = (By.XPATH, "//button[@type='submit']")
    
    def wait_for_page_load(self):
        """Sahifa ochilishini kutish"""
        self.wait_for_element_visible(self.login_button)
        self.logger.info("✅ Login page yuklandi")
    
    def input_credentials(self, username, password):
        """Login ma'lumotlarini kiritish"""
        self.input_text(self.username_input, username)
        self.input_text(self.password_input, password)
    
    def click_login(self):
        """Login tugmasini bosish"""
        self.click(self.login_button)
```

**2. Flow funksiya yaratish:**

```python
# flows/login_flow.py
from pages.example_page import ExamplePage

def login_flow(driver, username, password):
    """Login jarayoni"""
    page = ExamplePage(driver)
    page.wait_for_page_load()
    page.input_credentials(username, password)
    page.click_login()
    return True
```

**3. Qase.io bilan test yozish:**

```python
# tests/test_login.py
import pytest
from qase.pytest import qase
from flows.login_flow import login_flow

@qase.id(100)  # ⭐ Qase.io test case ID
@qase.title("Successful Login Test")
@pytest.mark.regression
def test_successful_login(driver, test_data):
    """
    Muvaffaqiyatli login testi
    
    Preconditions:
        - User mavjud bo'lishi kerak
        - Login page ochiq bo'lishi kerak
    
    Checklist:
    1. Login page ochilgani tekshiriladi
    2. Username va password kiritiladi
    3. Login tugmasi bosiladi
    4. Dashboard sahifasi ochilgani tekshiriladi
    """
    data = test_data["data"]
    
    # Flow ishlatish
    result = login_flow(
        driver=driver,
        username=data["username"],
        password=data["password"]
    )
    
    # Assertion
    assert result is True
    assert "dashboard" in driver.current_url
```

**4. Testni ishga tushirish:**

```bash
# Bitta test
pytest tests/test_login.py::test_successful_login -v

# Barcha testlar
pytest -m regression
```

---

## 🔍 Logging Tizimi

### Arxitektura

Logging tizimi 3 qismdan iborat:

1. **logger.py** - Logging configuration va rangli output
2. **log_helpers.py** - Caller chain tracking va timing
3. **base_page.py** - Log integration

### Caller Chain Tracking

**Nima?**
- Metodlar chaqirilish zanjirini avtomatik kuzatish
- Format: `PageName → method1 → method2 → current`

**Qanday ishlaydi?**

```python
# test dan chaqiriladi
order_page.click_save_button()
    ↓
# Page metodida
def click_save_button(self):
    self.click(self.save_button)  # ← Bu yerda log
        ↓
# BasePage metodida
def click(self, locator):
    self.logger.debug(f"{self._get_caller_chain()}: {locator}")
    # Log: OrderPage → click_save_button → click: (By.XPATH, '...')
```

### Log Levels va Ranglari

| Level | Rang | Qachon ishlatiladi | Misol |
|-------|------|-------------------|-------|
| 🟢 INFO | Green | Muvaffaqiyatli actionlar | `⏺ Click SUCCESS: button` |
| 🟡 WARNING | Yellow | Retry yoki ogohlantirishlar | `Element stale, qayta urinish (1/3)` |
| 🔴 ERROR | Red | Xatolar | `Element topilmadi: locator` |
| ⚫ DEBUG | Gray | Texnik detallar | `OrderPage → click → _click` |

### Automatic Timing

Har bir metod avtomatik timing bilan loglanadi:

```python
# Log output
🔽==================== start: click - click_save_button ====================🔽
⏺ Click SUCCESS: (By.XPATH, '//button[@id="save"]')
🔼==================== end: click - click_save_button (2.5s) ====================🔼
```

### Log Fayllar

Har bir test uchun alohida log fayl:

```
logs/
├── test_add_order_2025_10_30.log
├── test_edit_order_2025_10_30.log
└── test_delete_order_2025_10_30.log
```

**Log fayl tarkibi:**

```log
2025-10-30 15:30:45 - [INFO] - test_add_order - ✅ Order Main page yuklandi
2025-10-30 15:30:45 - [DEBUG] - test_add_order - OrderAddMain → click_rooms_input → click: (By.XPATH, '//div[@id="rooms"]')
2025-10-30 15:30:47 - [WARNING] - test_add_order - Element stale, qayta urinish (1/3)
2025-10-30 15:30:48 - [INFO] - test_add_order - ⏺ Click SUCCESS: (By.XPATH, '//div[@id="rooms"]')
2025-10-30 15:30:48 - [INFO] - test_add_order - ✅ Order Product page yuklandi
```

---

## 🌐 UI Loaders Mexanizmi

### Muammo

Modern web ilovalar (Angular, React, jQuery) async operatsiyalar ishlatadi:
- ❌ Element DOM da bor, lekin loading overlay ostida
- ❌ Button bosiladi, lekin HTTP so'rov tugamagan
- ❌ Spinner ko'rinadi, lekin element clickable emas

### Yechim: UILoaders Class

`UILoaders` avtomatik ravishda quyidagilarni kutadi:

#### 1. Async Operations (JavaScript)

```javascript
// Kutilayotgan operatsiyalar:
- jQuery.active          // jQuery AJAX
- Angular $http          // Angular HTTP requests
- XMLHttpRequest         // Vanilla JS XHR
- window.fetch           // Modern Fetch API
```

#### 2. Block UI Overlays

```css
/* Kutilayotgan elementlar: */
div.block-ui-overlay
div.block-ui-message-container
.cs-backdrop.open
body.block-ui-active
```

#### 3. Spinners

```css
/* Kutilayotgan spinnerlar: */
img[src*='loading.svg']
img[src*='loading.gif']
div.spinner
```

### Configuration

```python
# base_page.py
self._loaders = UILoaders(
    driver=self.driver,
    logger=self.logger,
    page_load_timeout=120,              # Maksimal kutish vaqti
    block_ui_absence_window=0.5,        # Block UI barqarorlik vaqti
    overlay_selectors=[                 # Qo'shimcha overlay selectorlar
        "div.custom-overlay",
        ".my-loading-screen"
    ],
    spinner_selectors=[                 # Qo'shimcha spinner selectorlar
        ".my-spinner",
        "img[alt='loading']"
    ]
)
```

---

## ⚠️ Exception Handling

### Custom Exception Hierarchy

```python
ElementInteractionError              # Base exception
├── ElementNotFoundError            # Element DOM da yo'q
├── ElementVisibilityError          # Element ko'rinmaydi
├── ElementNotClickableError        # Element clickable emas
├── ElementStaleError               # Element stale bo'ldi
├── ScrollError                     # Scroll xatosi
├── LoaderTimeoutError              # Loader timeout
├── JavaScriptError                 # JavaScript xatosi
└── ElementTimeoutError             # Umumiy timeout
```

### Context-Rich Errors

Har bir exception quyidagi ma'lumotlarni o'z ichiga oladi:

```python
{
    "message": "Element topilmadi",
    "locator": "(By.XPATH, '//button[@id=\"save\"]')",
    "page": "OrderAddFinal",
    "url": "https://smartup.online/order/add",
    "caller": "OrderPage → click_save_button → click",
    "step": "click:attempt1",
    "original_error": "NoSuchElementException"
}
```

### Smart Retry Mechanism

**3 marta avtomatik retry:**

```python
def wait_for_element_visible(self, locator):
    for attempt in range(3):
        try:
            element = self.wait_for_element(locator, wait_type="presence")
            self._scroll_to_element(element, locator)
            element = self.wait_for_element(locator, wait_type="visibility")
            return element
            
        except (ElementStaleError, ScrollError, JavaScriptError) as e:
            self.logger.warning(f"{e.message}, qayta urinish ({attempt + 1}/3)")
            time.sleep(1)
            continue
    
    # 3 ta urinishdan keyin xato
    raise ElementVisibilityError("Element barcha usullar bilan ko'rilmadi")
```

---

## 🎭 Flow Pattern

### Nima?

Flow pattern - bu biznes jarayonlarni alohida funktsiyalarga ajratish va ularni qayta ishlatish mexanizmi.

### Flow Funksiya Strukturasi

```python
def main_flow(driver, **kwargs):
    """
    Order Main page flow
    
    Args:
        driver: WebDriver instance
        **kwargs:
            - room_name (str): Xona nomi
            - robot_name (str): Robot nomi
            - client_name (str): Client nomi
            - get_deal_time (bool): Deal time ni olish
    
    Returns:
        dict: Olingan ma'lumotlar
    """
    # 1. Page obyektini yaratish
    main_page = OrderAddMain(driver)
    main_page.wait_for_page_load()
    
    # 2. Return uchun dict
    result = {}
    
    # 3. Conditional actions
    if kwargs.get("room_name"):
        main_page.select_room(kwargs.get("room_name"))
    
    if kwargs.get("robot_name"):
        main_page.select_robot(kwargs.get("robot_name"))
    
    if kwargs.get("client_name"):
        main_page.select_client(kwargs.get("client_name"))
    
    # 4. Ma'lumot olish (agar kerak bo'lsa)
    if kwargs.get("get_deal_time"):
        result["deal_time"] = main_page.get_deal_time()
    
    # 5. Keyingi qadamga o'tish
    main_page.click_next()
    
    return result
```

---

## 🔐 Auth Flow

### Login/Logout Management

Framework da centralized authentication management mavjud:

**auth_flow.py strukturasi:**

```python
# flows/auth_flow.py

def login(driver, email, password):
    """Asosiy login funksiyasi"""
    login_page = LoginPage(driver)
    login_page.wait_for_page_load()
    login_page.fill_form(email, password)
    login_page.click_button()

def dashboard(driver, dashboard_check, change_password_check, filial_name, url):
    """Dashboard navigation va setup"""
    dashboard_page = DashboardPage(driver)
    
    if dashboard_check:
        dashboard_page.element_visible_dashboard()
    
    if change_password_check:
        dashboard_page.element_visible_change_password()
    
    if filial_name:
        dashboard_page.find_filial(filial_name)
    
    if url:
        base_page = BasePage(driver)
        base_page.switch_window(direction="prepare")
        cut_url = base_page.cut_url()
        base_page.switch_window(direction="new", url=cut_url + url)

def login_admin(driver, test_data, **kwargs):
    """Admin sifatida login"""
    data = test_data["data"]
    email = kwargs.get("email", data["email"])
    password = kwargs.get("password", data["password"])
    
    login(driver, email, password)
    
    dashboard_check = kwargs.get("dashboard_check", True)
    change_password_check = kwargs.get("change_password_check", False)
    filial_name = kwargs.get("filial_name", data["Administration_name"])
    url = kwargs.get("url", 'trade/intro/dashboard')
    
    dashboard(driver, dashboard_check, change_password_check, filial_name, url)

def login_user(driver, test_data, **kwargs):
    """Oddiy user sifatida login"""
    data = test_data["data"]
    email = kwargs.get("email", data["email_user"])
    password = kwargs.get("password", data["password_user"])
    
    login(driver, email, password)
    
    dashboard_check = kwargs.get("dashboard_check", True)
    change_password_check = kwargs.get("change_password_check", False)
    filial_name = kwargs.get("filial_name", data["filial_name"])
    url = kwargs.get("url", 'trade/intro/dashboard')
    
    dashboard(driver, dashboard_check, change_password_check, filial_name, url)

def logout(driver):
    """Logout funksiyasi"""
    login_page = LoginPage(driver)
    login_page.click_navbar_button()
    login_page.click_logout_button()
```

### Qanday Ishlatish?

```python
# Test da
import pytest
from flows.auth_flow import login_admin, login_user, logout

def test_admin_action(driver, test_data):
    # Admin sifatida login
    login_admin(driver, test_data, url='anor/mr/person/legal_person_list')
    
    # Test actions...
    
    # Logout
    logout(driver)

def test_user_action(driver, test_data):
    # User sifatida login
    login_user(driver, test_data, url='trade/tdeal/order/order_list')
    
    # Test actions...
```

---

## 🔗 Qase.io Integration

### Nima?

Qase.io - bu test case management va tracking platformasi. Bizning framework Qase.io bilan to'liq integratsiya qilingan.

### Konfiguratsiya

**1. .env faylda:**

```env
QASE_MODE=testops
QASE_TESTOPS_PROJECT=RP
QASE_TESTOPS_API_TOKEN=your_api_token_here
QASE_TESTOPS_RUN_TITLE=Automation tests
```

**2. pytest.ini da:**

```ini
[pytest]
addopts = --qase-mode=testops
```

### Testlarda Ishlatish

```python
import pytest
from qase.pytest import qase

@qase.id(164)  # ⭐ Qase.io test case ID
@qase.title("Add Legal Person")
@pytest.mark.regression
def test_add_legal_person(driver, test_data, soft_assertions):
    """
    Legal Person qo'shish va tekshirish.
    
    Preconditions:
        - Admin sifatida login bo'lishi kerak
        - Legal Person list sahifasi ochiq bo'lishi kerak
    
    Checklist:
    1. Admin login qilinadi
    2. Legal Person list sahifasi ochilgani tekshiriladi
    3. Add tugmasi bosiladi
    4. Add formasi ochilgani tekshiriladi
    5. Maydonlar to'ldiriladi
    6. Save tugmasi bosiladi va Yes tasdiqlanadi
    7. Ro'yxatda Code orqali qidiriladi
    8. Yozuv topiladi
    9. View tugmasi bosiladi
    10. Qiymatlar tekshiriladi
    """
    # Test kodlari...
```

### Qase.io Features

| Feature | Tavsif | Ishlatish |
|---------|--------|-----------|
| **Test Case ID** | Qase.io dagi test case bilan bog'lash | `@qase.id(164)` |
| **Test Title** | Test nomini belgilash | `@qase.title("Add Legal Person")` |
| **Automatic Reporting** | Test natijalarini avtomatik yuborish | Auto |
| **Test Steps** | Docstring da yozilgan checklist | Auto parse |
| **Screenshots** | Xato vaqtidagi screenshotlar | Auto attach |
| **Execution Time** | Test davomiyligi | Auto record |

### Testlarni Qase.io bilan ishga tushirish

```bash
# Qase.io ga natijalarni yuborish
pytest -m regression --qase-mode=testops

# Qase.io ga yubormasdan (local run)
pytest -m regression --qase-mode=off
```

---

## 📧 Email Reporting

### Nima?

Test natijalarini avtomatik email orqali yuborish tizimi.

### Konfiguratsiya

**utils/email.py:**

```python
# Email settings
EMAIL_SENDER = 'your_email@gmail.com'
EMAIL_PASSWORD = 'your_app_password'  # Gmail App Password
EMAIL_RECIPIENTS = ['qa_team@company.com', 'manager@company.com']
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
```

### Email Format

Email quyidagi ma'lumotlarni o'z ichiga oladi:

```
==========================================
✅/❌ TEST NATIJALARI
==========================================

📊 UMUMIY STATISTIKA:
──────────────────────────────────────────
Jami testlar:              100
✅ Muvaffaqiyatli:         95
❌ Muvaffaqiyatsiz:        3
⭕ O'tkazib yuborilgan:   2
⚠️  Xatolar:               0
📈 Muvaffaqiyat darajasi:  95.0%
⏱️  Umumiy davomiylik:     1234.56 sekund

==========================================
📋 TEST TAFSILOTLARI:
==========================================

❌ MUVAFFAQIYATSIZ TESTLAR:
──────────────────────────────────────────
1. test_order.py::test_add_order_with_consignment
   ⏱️ Davomiylik: 45.23s
   ⚠️ Xato: ElementNotFoundError: Element topilmadi...

✅ MUVAFFAQIYATLI TESTLAR:
──────────────────────────────────────────
1. test_order.py::test_edit_order (⏱️ 32.15s)
2. test_order.py::test_delete_order (⏱️ 28.45s)
...

==========================================
📅 Sana: 2025-10-30 15:45:23
==========================================
```

### Qanday Ishlaydi?

**conftest.py da avtomatik:**

```python
# conftest.py

def pytest_sessionfinish(session, exitstatus):
    """Test sessiyasi tugaganda email yuborish"""
    # Natijalarni hisoblash
    passed_count = len(test_results['passed'])
    failed_count = len(test_results['failed'])
    
    # Email subject
    status = "✅ PASSED" if failed_count == 0 else "❌ FAILED"
    subject = f"{status} - Automation Test Natijalari"
    
    # Email body
    body = format_test_results(
        passed=passed_count,
        failed=failed_count,
        skipped=skipped_count,
        errors=errors_count,
        total_duration=total_duration,
        test_details=test_results
    )
    
    # Email yuborish
    send_email_report(subject, body)
```

### Email ni O'chirish/Yoqish

**.env faylda:**

```env
ENABLE_EMAIL_REPORTS=true  # yoki false
```

---

## 🎥 Screen Recording

### Nima?

Test jarayonini video ga yozish (FFmpeg yoki OpenCV orqali).

### Features

| Feature | Tavsif |
|---------|--------|
| **FFmpeg Support** | H.264 MP4 yoki VP9 WebM encoding |
| **OpenCV Fallback** | FFmpeg bo'lmasa OpenCV ishlatadi |
| **Allure Integration** | Videoni avtomatik Allure ga qo'shish |
| **Overlay Information** | Video ustiga vaqt, URL, test nomi |
| **Configurable FPS** | 8-30 FPS (default: 8) |
| **Auto Size Detection** | Browser o'lchamiga avtomatik moslashish |

### Qanday Ishlatish?

**conftest.py da:**

```python
from utils.screen_recorder import ScreenRecorder

@pytest.fixture
def recorder(request, driver):
    """Screen recorder fixture"""
    test_name = request.node.name
    
    rec = ScreenRecorder(
        driver=driver,
        filename=f"{test_name}_{{ts}}.mp4",
        output_dir="artifacts/videos",
        fps=8.0,
        prefer="h264",  # h264, vp9, yoki opencv
        draw_info=True,  # Overlay yozish
        attach_to_allure=True,
        test_name=test_name
    )
    
    rec.start()
    yield rec
    rec.stop()

# Test da ishlatish
def test_with_video(driver, recorder):
    # Video avtomatik yoziladi
    driver.get("https://example.com")
    # ...
    # Video avtomatik to'xtatiladi va Allure ga qo'shiladi
```

### Video Formats

| Format | Codec | Browser Support | File Size | Quality |
|--------|-------|----------------|-----------|---------|
| **MP4 (H.264)** | libx264 | ✅ Excellent | Medium | High |
| **WebM (VP9)** | libvpx-vp9 | ✅ Good | Small | High |
| **MP4 (mp4v)** | OpenCV | ⚠️ Limited | Large | Medium |

**Tavsiya:** H.264 MP4 (FFmpeg bilan)

### Configuration

```python
# Screen recording sozlamalari
rec = ScreenRecorder(
    driver=driver,
    fps=8.0,                    # Frames per second
    size="auto",                # yoki (1920, 1080)
    prefer="h264",              # h264, vp9, opencv
    draw_info=True,             # Overlay ma'lumot
    attach_to_allure=True,      # Allure ga qo'shish
    keep_on_success=True        # Muvaffaqiyatli testda ham saqlash
)
```

---

## 🧪 Testlarni Ishga Tushirish

### Basic Commands

```bash
# Barcha testlarni ishga tushirish
pytest

# Ma'lum bir test faylini ishga tushirish
pytest tests/ui/test_order/test_order.py

# Ma'lum bir testni ishga tushirish
pytest tests/ui/test_order/test_order.py::test_add_order_with_consignment_demo

# Verbose rejimda
pytest -v

# Quiet rejimda
pytest -q --no-header --no-summary

# Parallel ishga tushirish (4 ta worker)
pytest -n 4
```

### Markers

**pytest.ini da e'lon qilingan markerlar:**

```ini
[pytest]
markers =
    api: Api test case marker
    qase: Qase test case marker
    integration_report: Integration test cases
    regression: Regression test cases
    user_setup: User setup test cases
    order_group_A: Order-A test cases
    order_group_B: Order-B test cases
    order_group_C: Order-C test cases
```

**Ishlatish:**

```bash
# Regression testlar
pytest -m regression

# Order group A testlar
pytest -m order_group_A

# Markerlarni kombinatsiya qilish
pytest -m "regression and not slow"

# Bir nechta markerlar
pytest -m "order_group_A or order_group_B"
```

### Pytest Options

```bash
# Headless rejimda
pytest --headless

# Birinchi xato da to'xtash
pytest -x

# Maksimal 5 ta xato
pytest --maxfail=5

# Oxirgi muvaffaqiyatsiz testni qayta ishga tushirish
pytest --lf

# Muvaffaqiyatsiz testlarni birinchi ishga tushirish
pytest --ff

# Retry (muvaffaqiyatsiz testlarni qayta urinish)
pytest --reruns=2 --reruns-delay=5
```

### Advanced Commands

```bash
# Allure + Qase.io + Email
pytest -m regression --alluredir=allure-results --qase-mode=testops

# Video recording bilan
pytest -m regression --record-video

# Specific test with all features
pytest tests/ui/test_order/test_order.py::test_add_order \
  -v \
  --alluredir=allure-results \
  --qase-mode=testops \
  --record-video \
  --reruns=1
```

### Test Runner (80+ testlar ketma-ket)

```bash
# Barcha testlarni ketma-ket ishga tushirish
pytest tests/ui/test_ui_test_runner.py -v

# Qisqa output bilan
pytest tests/ui/test_ui_test_runner.py -q --no-header --no-summary
```

---

## 📈 Allure Report

### Allure Nima?

Allure - bu professional test reporting framework.

### Ishga Tushirish

**1. Testlarni ishga tushirish va natijalarni yig'ish:**

```bash
pytest -m regression --alluredir=allure-results
```

**2. Allure report generatsiya qilish:**

```bash
# Report generatsiya va ochish
allure serve allure-results

# Faqat generatsiya
allure generate allure-results -o allure-report --clean

# Generatsiya qilingan reportni ochish
allure open allure-report
```

### Allure Features

| Feature | Tavsif |
|---------|--------|
| 📊 **Overview** | Test statistika va trend |
| 📋 **Suites** | Test suite lar bo'yicha guruhlash |
| 📈 **Graphs** | Vizual grafiklar |
| ⏱️ **Timeline** | Test execution timeline |
| 🔍 **Behaviors** | BDD style feature lar |
| 📦 **Packages** | Package structure |
| 📸 **Attachments** | Screenshot va videolar |
| 📝 **Test Body** | Test kodlari va loglar |

### Allure ga Ma'lumot Qo'shish

```python
import allure

@allure.feature("Order Management")
@allure.story("Create Order")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_order(driver):
    with allure.step("Open order page"):
        driver.get("https://example.com/orders")
    
    with allure.step("Fill order form"):
        # ...
        allure.attach(
            driver.get_screenshot_as_png(),
            name="Order Form",
            attachment_type=allure.attachment_type.PNG
        )
    
    with allure.step("Submit order"):
        # ...
```

### Allure Environment

**allure-results/environment.properties:**

```properties
Browser=Chrome
Browser.Version=120.0
OS=Windows 10
Base.URL=https://smartup.online
Test.Environment=Production
```

---

## 💡 Best Practices

### 1. Logging

#### ✅ DO

```python
# Informative log messages
self.logger.info("✅ Order created successfully")
self.logger.debug(f"Clicking element: {locator}")
self.logger.warning("Element stale, retrying...")
self.logger.error("Failed to create order")

# Caller chain ishlatish
self.logger.debug(f"{self._get_caller_chain()}: {locator}")
```

#### ❌ DON'T

```python
# Print ishlatmang
print("Order created")  # ❌

# Bo'sh log
self.logger.info("")  # ❌

# Detail yo'q
self.logger.info("Error")  # ❌
```

### 2. Locators

#### ✅ DO

```python
# ID ishlatish (eng yaxshi)
username_input = (By.ID, "username")

# CSS selector
username_input = (By.CSS_SELECTOR, "input[name='username']")

# Relative XPath
username_input = (By.XPATH, "//input[@name='username']")
```

#### ❌ DON'T

```python
# Absolute XPath ishlatmang
username_input = (By.XPATH, "/html/body/div[1]/div[2]/form/input[1]")  # ❌

# Text content ga bog'lanmang (o'zgarishi mumkin)
button = (By.XPATH, "//button[text()='Сохранить']")  # ❌
```

### 3. Waits

#### ✅ DO

```python
# Explicit wait ishlatish
self.wait_for_element_visible(locator)

# Custom timeout
self.wait_for_element_visible(locator, timeout=60)

# UI Loaders avtomatik
self._wait_for_all_loaders()
```

#### ❌ DON'T

```python
# time.sleep ishlatmang (antipattern)
import time
time.sleep(5)  # ❌
```

### 4. Assertions

#### ✅ DO

```python
# Descriptive message
assert order_id is not None, "Order ID bo'sh bo'lmasligi kerak"

# Soft assertions
soft_assertions.assert_equals(actual, expected, "Order status")
soft_assertions.assert_all()
```

#### ❌ DON'T

```python
# Message yo'q
assert order_id is not None  # ❌

# Multiple hard assertions (birinchi xato da to'xtaydi)
assert status == "Draft"
assert amount == 1000
assert client == "Test Client"
```

### 5. Test Data

#### ✅ DO

```python
# Fixture dan foydalanish
def test_order(driver, test_data):
    data = test_data["data"]
    client_name = data["client_name"]

# Environment variables
from utils.env_reader import get_env
base_url = get_env("URL")
```

#### ❌ DON'T

```python
# Hardcoded data
def test_order(driver):
    client_name = "Test Client"  # ❌
    base_url = "https://test.com"  # ❌
```

### 6. Qase.io

#### ✅ DO

```python
# ID va Title qo'shish
@qase.id(164)
@qase.title("Add Legal Person")
def test_add_legal_person(...):
    """
    Batafsil docstring:
    
    Preconditions:
        - ...
    
    Checklist:
    1. Step 1
    2. Step 2
    ...
    """
```

#### ❌ DON'T

```python
# ID yo'q
def test_add_legal_person(...):  # ❌
    pass

# Docstring yo'q
@qase.id(164)
def test_add_legal_person(...):  # ❌
    pass
```

---

## 🔧 Troubleshooting

### Keng tarqalgan muammolar

#### 1. Element topilmadi

**Xato:**
```
ElementNotFoundError: Element topilmadi | locator=XPATH=//button[@id="save"]
```

**Yechim:**
- ✅ Locator to'g'riligini tekshiring
- ✅ Element sahifada borligini tekshiring
- ✅ Timeout ni oshiring
- ✅ Wait_for_element_visible ishlatganingizni tekshiring

#### 2. Qase.io ga yuborilmayapti

**Muammo:**
Test natijalar Qase.io ga yuklanmayapti

**Yechim:**

1. API token to'g'riligini tekshiring:
```bash
# .env faylda
QASE_TESTOPS_API_TOKEN=your_actual_token
```

2. Qase mode ni tekshiring:
```bash
pytest -m regression --qase-mode=testops
```

3. Project ID to'g'riligini tekshiring:
```env
QASE_TESTOPS_PROJECT=RP  # Sizning project code ingiz
```

#### 3. Email yuborilmayapti

**Muammo:**
Test natijalar email ga kelmayapti

**Yechim:**

1. Gmail App Password yaratilganligini tekshiring
2. 2-Factor Authentication yoqilganligini tekshiring
3. Email settings ni tekshiring:
```python
# utils/email.py
EMAIL_SENDER = 'correct_email@gmail.com'
EMAIL_PASSWORD = '16_digit_app_password'  # Oddiy parol EMAS!
EMAIL_RECIPIENTS = ['recipient@example.com']
```

4. SMTP port ochiqligini tekshiring:
```bash
telnet smtp.gmail.com 587
```

#### 4. Video yozilmayapti

**Muammo:**
Screen recording ishlamayapti

**Yechim:**

1. FFmpeg o'rnatilganligini tekshiring:
```bash
ffmpeg -version
```

2. OpenCV o'rnatilganligini tekshiring:
```bash
pip install opencv-python
```

3. Recorder fixture ishlatilganligini tekshiring:
```python
def test_with_video(driver, recorder):  # ← recorder fixture
    # Test code
```

#### 5. Allure report ochilmayapti

**Muammo:**
`allure serve` ishlamayapti

**Yechim:**

1. Allure o'rnatilganligini tekshiring:
```bash
allure --version
```

2. Allure o'rnatish:
```bash
# Windows (Scoop)
scoop install allure

# Mac
brew install allure

# Linux
sudo apt-add-repository ppa:qameta/allure
sudo apt-get update
sudo apt-get install allure
```

3. Java o'rnatilganligini tekshiring (Allure Java kerak):
```bash
java -version
```

---

## ❓ FAQ

### Q1: Flow va Page Object farqi nima?

**A:** 
- **Page Object** - sahifadagi elementlar va ular bilan oddiy actionlar
- **Flow** - biznes jarayonlar (bir nechta page actionlarni birlashtirib)

```python
# Page Object
class OrderPage(BasePage):
    def select_room(self, name):
        # Oddiy action
        pass

# Flow
def main_flow(driver, **kwargs):
    # Biznes jarayon (ko'p actionlar)
    page.select_room(kwargs.get("room"))
    page.select_robot(kwargs.get("robot"))
    page.click_next()
```

### Q2: Qase.io nima uchun kerak?

**A:** 
- ✅ Test case larni boshqarish (test management)
- ✅ Test natijalarini tracking qilish
- ✅ Test coverage ko'rish
- ✅ Requirements bilan bog'lash
- ✅ Team collaboration

### Q3: Email reporting o'chirib qo'yish mumkinmi?

**A:** Ha, `.env` faylda:

```env
ENABLE_EMAIL_REPORTS=false
```

Yoki `conftest.py` da `pytest_sessionfinish` funksiyasini comment out qiling.

### Q4: Video yozish testlarni sekinlashtiradimi?

**A:** 
- ⚠️ Ha, 10-15% sekinroq
- ✅ Lekin debug uchun juda foydali
- ✅ Faqat muhim testlarda ishlatish tavsiya etiladi

### Q5: UI Loaders har doim kerakmi?

**A:** 
- ✅ Angular/React/jQuery app lar uchun - **HA**
- ❌ Oddiy static HTML uchun - **YO'Q** (o'chirish mumkin)

```python
# O'chirish
def click(self, locator):
    # self._wait_for_all_loaders()  # ← Comment out
    element = self.wait_for_element(locator)
```

### Q6: Parallel testlar ishlayaptimi?

**A:** Ha, lekin ehtiyotlik bilan:

```bash
# pytest-xdist o'rnatish
pip install pytest-xdist

# Parallel ishga tushirish
pytest -n 4
```

**Diqqat:** 
- Testlar bir-biriga bog'liq bo'lmasligi kerak
- Har bir test o'z ma'lumotlarini yaratishi kerak

### Q7: login_admin va login_user farqi nima?

**A:**

- **login_admin** - Admin credentials bilan login
- **login_user** - Oddiy user credentials bilan login

```python
# Admin login
login_admin(driver, test_data, url='admin/settings')

# User login
login_user(driver, test_data, url='user/dashboard')
```

### Q8: FFmpeg nima uchun tavsiya etiladi?

**A:**

FFmpeg ishlatsangiz:
- ✅ Kichikroq fayl hajmi (H.264)
- ✅ Yaxshiroq sifat
- ✅ Browser da to'g'ridan-to'g'ri ochiladi
- ✅ Allure da to'g'ri render qilinadi

OpenCV (fallback):
- ❌ Kattaroq fayl hajmi
- ❌ Browser compatibility issues
- ⚠️ Fallback variant

### Q9: Testlar qancha vaqt davom etadi?

**A:**

Bizning 80+ testlar:
- ⏱️ Sequential: ~2-3 soat
- ⏱️ Parallel (n=4): ~45-60 daqiqa

### Q10: Framework ni boshqa loyihaga ko'chirish mumkinmi?

**A:** Ha, oson:

1. ✅ Copy qilish: `pages/core/`, `utils/`, `conftest.py`
2. ✅ O'zgartirish: `.env`, `test_data`
3. ✅ Yangi page lar yozish
4. ✅ Yangi flow lar yozish
5. ✅ Qase.io project o'zgartirish

---

## 📜 License

Bu loyiha MIT license ostida tarqatiladi.

```
MIT License

Copyright (c) 2025 Smartup QA Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction...
```

---

## 👥 Muallif

**Smartup Automation QA Team**

- 👨‍💻 Lead QA Engineer: Turg'unov Jasur
- 📧 Email: tjasur224@gmail.com
- 💬 Telegram: @JasurTurgunov01
- 🌐 Website: https://smartup.online/

---

## 📊 Statistika

- **Total Lines of Code:** ~15,000+
- **Test Cases:** 80+
- **Page Objects:** 30+
- **Flow Functions:** 20+
- **Utility Functions:** 50+
- **Documentation:** 10,000+ words

---

## ⚡ Quick Links

| Link | Description |
|------|-------------|
| [Installation](#-ornatish) | O'rnatish bo'yicha to'liq guide |
| [Quick Start](#-tez-boshlash) | Birinchi test yozish |
| [Logging](#-logging-tizimi) | Logging system tavsifi |
| [Flow Pattern](#-flow-pattern) | Flow pattern guide |
| [Qase.io](#-qaseio-integration) | Qase.io integration |
| [Email Reports](#-email-reporting) | Email reporting setup |
| [Allure](#-allure-report) | Allure report generation |
| [FAQ](#-faq) | Ko'p so'raladigan savollar |

---

<div align="center">
Made with ❤️ by Smartup QA Team

<br/>

**Last Updated:** 2025-10-30

</div>
