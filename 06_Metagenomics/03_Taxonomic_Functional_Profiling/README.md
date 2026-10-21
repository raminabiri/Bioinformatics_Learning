<div dir="rtl">

# ماژول ۰۳: پروفایل تاکسونومیک (Kraken2 و Bracken) و معرفی پروفایل عملکردی

| | |
| :--- | :--- |
| **بخش** | `06_Metagenomics` |
| **پیش‌نیاز** | ماژول [برداشتن میزبان](../02_Host_Removal_Alignment/) (ریدهای پاک)؛ [پایتون](../../03_Python/)؛ [Bray–Curtis در vegan](../../04_R_Packages/03_Bioc_Examples/) |
| **زمان تقریبی** | ۵ ساعت (۲ درس × ۱ ساعت + ۳ ساعت تمرین) |
| **ابزار** | ‏Kraken2 2.17.1، Bracken 3.0.1؛ MetaPhlAn 4 و HUMAnN 3 تنها معرفی (اجرا نشده)؛ محیط [`envs/metagenomics.yml`](../../envs/metagenomics.yml) |
| **داده** | ‏`~/meta/host/clean/` + `ground_truth_species.tsv` + **پایگاه داده‌ی تمرینی** (کمابیش ۱۳۰ مگابایت دانلود) |
| **وضعیت** | ✅ قالب تازه (2026-10-21)؛ خروجی‌های Kraken2/Bracken از اجرای 2026-10-13؛ بخش MetaPhlAn/HUMAnN ✍️ تنها نوشته‌شده |

> ⚠️ **پایگاه داده‌ی این ماژول تنها برای تمرین است** (۴۵ ژنوم، ۲۶۳ مگابایت). برای کار پژوهشی پایگاه کامل لازم است، برای نمونه Kraken2 Standard (۷۹٫۶ گیگابایت) یا PlusPF (۸۴٫۸ گیگابایت) از https://benlangmead.github.io/aws-indexes/k2.

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. منطق k-mer و LCA در Kraken2 و پخش دوباره‌ی ریدها در Bracken را بگویید، و فرقش را با رویکرد ژن نشانگر (MetaPhlAn).
2. خروجی‌های `.kraken`، `.kreport` و `.bracken` را بخوانید.
3. یک پروفایل را با ترکیب واقعی بسنجید (درستی، بازیابی، Bray–Curtis).
4. اثر `--confidence`، آستانه‌ی فراوانی و سطح تاکسونومی را بیازمایید و انتخابتان را توجیه کنید.
5. محدودیت‌های بنیادی را بشناسید: گونه‌ی غایب از پایگاه، گروه‌های گونه‌ای، رید در برابر سلول.

## ترتیب مطالعه
1. ‏[01_lesson_kraken.md](01_lesson_kraken.md): چه کسانی در نمونه‌اند؟ Kraken2 و Bracken.
2. ‏[02_lesson_evaluation.md](02_lesson_evaluation.md): پروفایل چقدر درست است؟ و معرفی پروفایل عملکردی.
3. ‏[03_exercises.md](03_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.
5. اسکریپت‌ها و فهرست ژنوم‌های پایگاه: [99_scripts_data/03_Taxonomic_Functional_Profiling](../99_scripts_data/03_Taxonomic_Functional_Profiling/) (`build_practice_db.sh`، `run_profile.sh`، `evaluate_profile.py`، `check.sh`).

## ورودی و خروجی

<div dir="ltr">

```text
~/meta/
├── host/clean/                 input (module 02)
├── ground_truth_species.tsv    known composition (copied in lesson 1)
└── profile/
    ├── kraken2_practice_db/    practice database (hash.k2d + Bracken models)
    ├── kraken/                 <sample>_c<conf>.kraken / .kreport / .log
    └── bracken/                <sample>_c<conf>.bracken / .breport / .log
```

</div>

</div>
