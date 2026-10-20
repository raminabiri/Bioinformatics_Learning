<div dir="rtl">

# پاسخ تشریحی: ستون‌ها و شمردن با cut، sort و uniq

> دستورها در 2026-10-20 با GNU coreutils و GNU grep 3.11 (locale `en_US.UTF-8`) در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: الگوی طلایی، اول با چشم

<div dir="ltr">

```bash
grep -v '^#' ecoli_k12.gff | head -n 20 > small20.gff
cut -f3 small20.gff
cut -f3 small20.gff | sort | uniq -c
cut -f3 small20.gff | uniq -c | wc -l
```

</div>

<div dir="ltr">

```text
      9 CDS
     10 gene
      1 region
20
```

</div>

1 و 2. **۱ region، ۱۰ gene، ۹ CDS.** با چشم: یک region و پس از آن gene و CDS یکی در میان؛ خط بیستم یک gene است که CDS‌اش در خط بیست‌ویکم مانده است.
3. **۲۰ ردیف**، همه با شمار ۱. `uniq -c` تنها همانندهای **کنار هم** را یکی می‌کند، و این‌جا هیچ دو خط همانندی کنار هم نیستند. (`wc -l` در پایان لوله ردیف‌ها را شمرد.)

---

## تمرین ۲: نمای کلی ژنوم

<div dir="ltr">

```bash
grep -v '^#' ecoli_k12.gff | cut -f3 | sort | uniq -c | sort -rn
```

</div>

1. **۱۱ نوع** (۱۱ ردیف خروجی؛ فهرست کامل در بخش ۶ درس). برای این‌که مستقیم بشمارید: `… | sort | uniq -c | wc -l`.
2. **۵۰** عنصر ژنتیکی متحرک. این‌ها در بسیاری از موارد توالی‌های درج‌شونده (IS) هستند؛ در بخش ۰۸ دوره به آن‌ها می‌پردازیم.

---

## تمرین ۳: CDSها و tRNAها روی کدام رشته‌اند؟

<div dir="ltr">

```bash
grep -P '\tCDS\t' ecoli_k12.gff | cut -f7 | sort | uniq -c
grep -P '\ttRNA\t' ecoli_k12.gff | cut -f7 | sort | uniq -c
```

</div>

<div dir="ltr">

```text
   2118 +
   2222 -
     49 +
     37 -
```

</div>

1. ‏CDS: **۲٬۱۱۸** روی + و **۲٬۲۲۲** روی −؛ جمع ۴٬۳۴۰ = شمار CDSها. ✓
2. ‏tRNA: **۴۹** روی + و **۳۷** روی −؛ جمع ۸۶. ✓

---

## تمرین ۴: پرریدترین و کم‌ریدترین ژنوم‌های نمونه‌ی دوم

<div dir="ltr">

```bash
grep minigut_sample2 ground_truth.tsv | sort -k2,2nr | head -n 3 | cut -f2,4
grep minigut_sample2 ground_truth.tsv | sort -k2,2n | head -n 3 | cut -f2,4
cut -f1 ground_truth.tsv | sort | uniq -c
```

</div>

<div dir="ltr">

```text
16154	Acinetobacter baumannii strain AB030
1178	Pseudomonas aeruginosa PAO1
965	Staphylococcus epidermidis ATCC 12228
24	Lactobacillus gasseri ATCC 33323 = JCM 1131
69	Streptococcus pneumoniae R6
113	Streptococcus agalactiae 2603V/R
      2 minigut
     21 minigut_sample2
      1 sample
```

</div>

1. بیشترین: *Acinetobacter baumannii* (۱۶٬۱۵۴)، *Pseudomonas aeruginosa* (۱٬۱۷۸)، *Staphylococcus epidermidis* (۹۶۵).
2. کمترین: *Lactobacillus gasseri* (۲۴)، *Streptococcus pneumoniae* (۶۹)، *Streptococcus agalactiae* (۱۱۳).
3. **۲۱ ژنوم.** (`sample` همان خط عنوان ستون‌هاست.) این نمونه بسیار **نابرابر** است: یک باکتری نزدیک به دوسوم ریدها را دارد و برخی تنها چند ده رید. در متاژنومیکس (بخش ۰۶) خواهید دید که پیدا کردن گونه‌های کم‌فراوان، چالش اصلی است.

**اشتباه رایج:** `sort -k2,2r` بی `n`. ترتیب متنی می‌شود و `965` بالای `16154` می‌افتد.

---

## تمرین ۵: گونه‌های ژن

<div dir="ltr">

```bash
grep -o -E 'gene_biotype=[a-zA-Z_]+' ecoli_k12.gff | sort | uniq -c | sort -rn
```

</div>

<div dir="ltr">

```text
   4290 gene_biotype=protein_coding
    145 gene_biotype=pseudogene
    107 gene_biotype=ncRNA
     86 gene_biotype=tRNA
     22 gene_biotype=rRNA
      1 gene_biotype=other
```

</div>

1. شش گونه: پروتئین‌ساز ۴٬۲۹۰، کاذب ۱۴۵، ncRNA ۱۰۷، tRNA ۸۶، rRNA ۲۲، و یکی «دیگر».
2. جمع: ۴٬۲۹۰ + ۱۴۵ + ۱۰۷ + ۸۶ + ۲۲ + ۱ = **۴٬۶۵۱**، یعنی ۱۴۵ تا بیشتر از ۴٬۵۰۶ ژن. چرا؟ `gene_biotype=` هم در خط‌های `gene` هست و هم در خط‌های `pseudogene` (۱۴۵ خط؛ تمرین ۲). ژن‌های کاذب نوع جداگانه‌ی `pseudogene` در ستون ۳ دارند، پس در شمار `gene` نیامدند. **۴٬۵۰۶ + ۱۴۵ = ۴٬۶۵۱** ✓. همین عدد ۴٬۶۵۱ را NCBI به‌عنوان «شمار کل ژن‌ها» گزارش می‌کند؛ پس «شمار ژن» به تعریف بستگی دارد.

</div>
