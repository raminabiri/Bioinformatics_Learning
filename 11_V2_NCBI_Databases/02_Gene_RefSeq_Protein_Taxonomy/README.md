<div dir="rtl">

# ماژول ۰۲: Gene، RefSeq، Protein و Taxonomy (Gene, RefSeq, Protein, IPG, CDD, Taxonomy) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `11_V2_NCBI_Databases` |
| **پیش‌نیاز** | ماژول [11/01](../01_Entrez_EDirect/) (E-utilities، EDirect، `xtract`، سرور تاریخچه) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏curl 8.20.0، EDirect 24.0، NCBI Datasets CLI 18.38.0 |
| **داده** | ‏NR3C1 انسان (Gene ID 2908؛ MANE ‏`NM_000176.3` → `NP_000167.1`، ۷۷۷ aa)؛ rpoB *E. coli* (`NP_418414.1` → `WP_000263098.1`)؛ TaxIDهای 511145، 562، 9606، 83332 |
| **منابع رایانه** | تنها درخواست وب |
| **وضعیت** | ✅ اجرا شده (2026-10-27) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. فرق GenBank و RefSeq را بگویید و پیشوندهای RefSeq (`NC_`، `NG_`، `NM_`، `NR_`، `NP_`، `XM_`، `WP_`) را بخوانید.
2. از یک ژن انسانی به رونوشت‌ها، ایزوفرم‌ها و رونوشت MANE Select برسید.
3. با IPG تکرار یک پروتئین باکتریایی را در ژنوم‌ها بسنجید و `WP_` را بشناسید.
4. دامنه‌های حفظ‌شده را از CDD و دودمان یک جاندار را از Taxonomy بگیرید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ GenBank و RefSeq، NR3C1 و MANE، NCBI Datasets، IPG، CDD و Taxonomy.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** نام ژن، accession و TaxID؛ همه‌چیز از NCBI.
- **خروجی:** `nr3c1_rna.acc`، `NM_000176.gb`، `nr3c1_prot.faa` (۲۱ ایزوفرم)؛ ورودی ماژول 11/04 (GEO، پاسخ به دگزامتازون) و 11/05 (واریانت‌ها).

</div>
