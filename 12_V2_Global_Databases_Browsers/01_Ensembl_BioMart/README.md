<div dir="rtl">

# ماژول ۰۱: Ensembl و BioMart (Ensembl, BioMart and REST API) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ماژول‌های [11/02](../../11_V2_NCBI_Databases/02_Gene_RefSeq_Protein_Taxonomy/) (RefSeq، MANE) و [11/04](../../11_V2_NCBI_Databases/04_GEO/) (ژن‌های پاسخ به دگزامتازون)؛ `curl` و `jq` ([02/05](../../02_BioLinux/05_Data_Download/))؛ پایتون تا [03/02](../../03_Python/02_Python_Lists_Loops/) (دیکشنری) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏curl 8.20.0، jq، Python 3 با requests 2.34.2؛ Ensembl REST و BioMart (release 116) |
| **داده** | هشت ژن پاسخ به دگزامتازون (NR3C1، FKBP5، TSC22D3، ZBTB16، PER1، DUSP1، KLF15، CRISPLD2)؛ CFTR؛ rpoB و gyrA *E. coli* K-12 |
| **منابع رایانه** | تنها درخواست وب؛ اسکریپت ۳۴ مگابایت حافظه |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ گام‌های مرورگر وب ✍️ |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. شناسه‌های Ensembl (ENSG/ENST/ENSP و نسخه) را بخوانید و با RefSeq، NCBI Gene و UniProt جفت کنید.
2. با Ensembl REST و `curl` ژن، رونوشت‌ها، رونوشت canonical و MANE، توالی و ارتولوگ‌ها را بگیرید.
3. با BioMart (مرورگر و XML) جدول ویژگی ژن‌ها بسازید.
4. با `requests` در پایتون از REST بپرسید و پاسخ‌های 429/500/503 را مدیریت کنید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ شناسه‌ها، release و سایت تازه، REST (lookup، xrefs، sequence، homology، POST)، BioMart، اسکریپت پایتون، Ensembl Bacteria.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** نماد ژن‌ها؛ پرسش‌های XML در [`99_scripts_data/01_Ensembl_BioMart/data/`](../99_scripts_data/01_Ensembl_BioMart/data/)؛ اسکریپت [`ens_ids.py`](../99_scripts_data/01_Ensembl_BioMart/scripts/ens_ids.py).
- **خروجی:** `dex_ids.tsv` (نماد ← ENSG، رونوشت canonical، NCBI Gene ID)؛ ورودی ماژول‌های 12/02 (مختصات در UCSC)، 12/05 (GO و مسیرها) و 12/06 (بیان در بافت‌ها).

## یادداشت
‏release 116 آخرین release سایت قدیمی Ensembl است. www.ensembl.org اکنون سایت تازه را باز می‌کند و BioMart در jun2026.archive.ensembl.org مانده است. سرور REST همان rest.ensembl.org است.

</div>
