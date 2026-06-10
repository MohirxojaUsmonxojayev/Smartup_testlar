## Loyiha Xususiyatlari

### Company View
- Company viewda `Безопасность`/Security tab ichida `Политика лицензирования` radio/switch control bor; company setup runida `--create-company --disable-license-policy` berilsa off qilinadi.
- `Политика лицензирования` control view tabning o'zida interaktiv `smt-switch` sifatida turadi (`id="licensing_policy_enabled"`, `role="switch"`). Uni off qilish uchun global `Изменить` tugmasini bosmaslik kerak, chunki u oddiy `company_edit` formaga olib kiradi va tablar yo'qoladi.
- Policy off qilingan runlarda setup zanjiri `Buy License` va `Attach License` qadamlari real license flowga kirmaydi; policy yoqiq bo'lsa yangi company uchun `Активация для лицензии` precondition emas.
- Company setup runida `Безопасность`/Security tabdagi `Ограничение количества одновременных сеансов` segmenti doim `Отключено` qilinadi; aks holda keyingi group/user loginlarda `Активные сеансы`/`concurrent_session_list` blokeri chiqadi.

### Company Add
Tags: company, setup, locator, wait
- `Создать` bosilgandan keyin `Компания (создание)` headeri `#companyForm` mount bo'lishidan oldin ko'rinishi mumkin; required fieldlarni to'ldirishdan oldin `#companyForm` va kamida bitta `smt-control` ko'rinishini kutish kerak.
- `Шаблоны` card ichidagi `Маркировка` inputidan `UZ Marking` optioni tanlanadi; company setupda `План счетов=UZ COA`, `Банки=UZ BANK`, `Маркировка=UZ Marking` shablonlari majburiy.
