<div dir="rtl">

# ماژول ۰۱: Entrez و E-utilities از خط فرمان (Entrez, E-utilities and EDirect) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `11_V2_NCBI_Databases` |
| **پیش‌نیاز** | ماژول 02/03 (نخستین `efetch` با `curl`)؛ ماژول 03/05 (`Bio.Entrez`)؛ `grep`، `cut`، `awk` و لوله (بخش ۰۱) |
| **زمان تقریبی** | ۴ ساعت (۲ درس، نزدیک به ۲٫۵ ساعت، و تمرین‌ها) |
| **ابزار** | ‏curl 8.20.0؛ EDirect 24.0 (`esearch`، `esummary`، `elink`، `efilter`، `efetch`، `xtract`)؛ Biopython 1.87 |
| **داده** | پنج ژن مقاومت *E. coli* K-12 MG1655 (TaxID 511145): ‏*rpoB*، *rpoC*، *gyrA*، *parC*، *acrB*؛ پاسخ معلوم: جای ژن روی `NC_000913.3` و طول پروتئین‌های RefSeq |
| **منابع رایانه** | سبک: تنها درخواست وب؛ کمتر از ۱۰۰ مگابایت حافظه |
| **وضعیت** | ✅ اجرا شده (2026-10-27) |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ساختار Entrez، فرق UID و accession.version، و پیوند میان پایگاه‌ها را توضیح دهید.
2. ‏`einfo`، `esearch`، `esummary`، `elink` و `efetch` را با `curl` به کار ببرید و با سرور تاریخچه به هم بچسبانید.
3. با برچسب فیلد (`[gene]`، `[preferred symbol]`، `[Organism:noexp]`) جست‌وجوی دقیق بنویسید و دام نام‌های دیگر ژن را بشناسید.
4. با EDirect و `xtract -block` یک جدول ژن درست بسازید و با `efilter` پروتئین‌های RefSeq را جدا کنید.
5. مرز سرعت را رعایت کنید و کلید API را تنها در متغیر محیطی نگه دارید.

## ترتیب مطالعه
1. ‏[01_lesson_eutils.md](01_lesson_eutils.md): درس ۱، Entrez و E-utilities با `curl`؛ سرور تاریخچه، مرز سرعت و کلید API.
2. ‏[02_lesson_edirect.md](02_lesson_edirect.md): درس ۲، EDirect، `xtract`، دام نام‌های دیگر و `elink -name`، و همان جدول با Biopython.
3. ‏[03_exercises.md](03_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
4. ‏[04_solutions.md](04_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** تنها نام ژن‌ها و TaxID؛ همه‌چیز از NCBI گرفته می‌شود.
- **خروجی:** `genes5.tsv` (جای ژن، رشته، طول)، `prot5.faa` (پنج پروتئین RefSeq)؛ ورودی ماژول 11/02 (Gene، RefSeq و Protein).
- **اسکریپت:** [gene_table.py](../99_scripts_data/01_Entrez_EDirect/scripts/gene_table.py) (Biopython؛ ایمیل از `ENTREZ_EMAIL` و کلید از `NCBI_API_KEY`).

</div>
