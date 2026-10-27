<div dir="rtl">

# ماژول ۰۴: خانواده و دامنه‌ی پروتئین (InterPro, Pfam and HMMER) — نسخه‌ی ۲

| | |
| :--- | :--- |
| **بخش** | `12_V2_Global_Databases_Browsers` |
| **پیش‌نیاز** | ‏BLAST+ و CD-Search ([11/07](../../11_V2_NCBI_Databases/07_BLAST_Suite_Tools/))؛ ژن‌های مقاومت ([08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/))؛ `curl` و `jq` ([12/01](../01_Ensembl_BioMart/)) |
| **زمان تقریبی** | ۳ ساعت (یک درس، نزدیک به ۹۰ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏InterPro API (release 110.0، Pfam 38.2)، HMMER 3.4 (`envs/databases.yml`)، BLAST+ 2.17.0؛ InterProScan و eggNOG-mapper (وب، ✍️) |
| **داده** | شش بتالاکتاماز از چهار رده‌ی Ambler (TEM-1، CTX-M-15، KPC-2، AmpC، OXA-48، NDM-1) و گیرنده‌ی گلوکوکورتیکوئید (P04150)؛ پروتئوم *E. coli* K-12 (۴۳۰۰ پروتئین)؛ هفت HMM ‏Pfam |
| **منابع رایانه** | دانلود نزدیک به ۲ مگابایت؛ هر جست‌وجوی HMMER کمتر از ۰٫۱ ثانیه و ۱۳ مگابایت |
| **وضعیت** | ✅ اجرا شده (2026-10-27)؛ InterProScan و eggNOG-mapper ✍️ |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. دامنه، خانواده، ابرخانواده و clan را از هم جدا کنید و منطق profile HMM را بگویید.
2. دامنه‌های یک پروتئین را از InterPro (Pfam و دوازده پایگاه دیگر) بگیرید.
3. با `hmmscan` و `hmmsearch` و آستانه‌ی GA دامنه‌ها و اعضای یک خانواده را بیابید.
4. نشان دهید چرا «دامنه‌ی X دارد» یعنی «کار X را می‌کند» نیست، و eggNOG-mapper چه می‌افزاید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس؛ BLAST و حدهایش، InterPro و clan، hmmscan، hmmlogo، hmmsearch روی پروتئوم، eggNOG-mapper.
2. ‏[02_exercises.md](02_exercises.md): ۷ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** [`download.sh`](../99_scripts_data/04_Protein_Families_Domains/data/download.sh) (‏UniProt، InterPro، NCBI).
- **خروجی:** `scan.domtbl` (دامنه‌های هر پروتئین)، جدول‌های `hmmsearch`؛ دامنه‌ها و خانواده‌ها در ماژول 12/05 (GO و KEGG) به کار می‌آیند.

</div>
