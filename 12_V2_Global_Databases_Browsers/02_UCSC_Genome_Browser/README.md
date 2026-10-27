<div dir="rtl">

# ماژول ۰۲: مرورگر ژنوم UCSC (UCSC Genome Browser, Table Browser and liftOver) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ماژول [12/01](../01_Ensembl_BioMart/) (`dex_ids.tsv`)؛ BED و شماره‌گذاری از صفر ([02/03](../../02_BioLinux/03_Annotation_Formats/))؛ Conda ([02/01](../../02_BioLinux/01_Conda_Bioconda/))؛ F508del ([11/05](../../11_V2_NCBI_Databases/05_Variation_Clinical/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۸۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏UCSC Genome Browser (وب)، UCSC REST API، `curl` و `jq`، liftOver 502 (`envs/databases.yml`) |
| **داده** | ناحیه‌ی NR3C1 و FKBP5 در hg38؛ هشت ژن پاسخ به دگزامتازون (BED)؛ F508del در hg19 و hg38؛ سه پنجره‌ی آزمون liftOver |
| **منابع رایانه** | درخواست وب؛ liftOver چند ثانیه و کمتر از ۱۰۰ مگابایت |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ Table Browser و بارگذاری ترک خودتان ✍️ |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ترک‌ها را در مرورگر UCSC بخوانید و حالت نمایششان را عوض کنید.
2. با UCSC REST API ترک، توالی و جست‌وجو بگیرید و مختصات 0-based و 1-based را بی‌خطا جابه‌جا کنید.
3. با Table Browser (یا API) جدول، BED و اگزون‌ها را بیرون بکشید.
4. ترک خودتان را از یک جدول بسازید.
5. با liftOver مختصات را میان hg19 و hg38 جابه‌جا کنید و شکست‌های آن را بشناسید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ ترک‌ها و حالت نمایش، اسمبلی‌ها، API، Table Browser، custom track، liftOver.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** `dex_ids.tsv` از 12/01؛ [`nr3c1_regions.bed`](../99_scripts_data/02_UCSC_Genome_Browser/data/nr3c1_regions.bed) و [`lift_test_hg19.bed`](../99_scripts_data/02_UCSC_Genome_Browser/data/lift_test_hg19.bed)؛ تصویرهای درس در [`images/`](../99_scripts_data/02_UCSC_Genome_Browser/images/).
- **خروجی:** `dex_hg38.bed` و `dex_hg19.bed`، `fkbp5_exons.bed`؛ این فایل‌ها را برای ماژول‌های بعدی نگه دارید.

</div>
