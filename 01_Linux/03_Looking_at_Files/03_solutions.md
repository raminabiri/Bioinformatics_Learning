<div dir="rtl">

# پاسخ تشریحی: نگاه کردن به فایل‌ها

> دستورها در 2026-10-20 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: فایل کروموزوم ۲۱

<div dir="ltr">

```bash
head -n 2 host_chr21_region.fa
wc -l host_chr21_region.fa
wc -c host_chr21_region.fa
tail -n 3 host_chr21_region.fa
```

</div>

<div dir="ltr">

```text
>chr21part
TCCCTTACCTGGGTCTGTTGTATAATGCATCTTAGCAGCTATGTAACAGT
10001 host_chr21_region.fa
510011 host_chr21_region.fa
ttgagcaacccgaatctgcggtcttgtaacaaaagaatgtggagtggtat
tgtgtaaagtgaactttaactgttcctggtaatcattatcaattatacca
ccatacattataatgtgtctcatcgccaggcttgaatgtgttgtaatcca
```

</div>

1. خط عنوان `>chr21part` است. هر خط توالی **۵۰ حرف** دارد (برخلاف ژنوم *E. coli* که ۸۰ حرف بود). هر فایل FASTA ممکن است طول خط دیگری داشته باشد.
2. **۱۰٬۰۰۱ خط** و **۵۱۰٬۰۱۱ بایت**.
3. ۵۱۰٬۰۱۱ − ۱۰٬۰۰۱ (پایان‌خط‌ها) − ۱۰ (خط عنوان `>chr21part`) = **۵۰۰٬۰۰۰ باز**. یعنی یک تکه‌ی ۵۰۰ کیلوبازی (۱۰٬۰۰۰ خط × ۵۰ حرف).
4. در ژنوم‌های انسان و بسیاری از یوکاریوت‌ها، بخش‌های **تکراری** (repeats) را با حروف کوچک می‌نویسند. به این کار **soft-masking** می‌گویند: توالی سر جایش هست، ولی ابزارها می‌توانند این بخش‌ها را جدا ببینند. تکرارها در هم‌ترازی و اسمبلی دردسرسازند؛ در بخش‌های ۰۶ و ۰۷ دوباره به آن‌ها می‌رسیم.

---

## تمرین ۲: سلامت دانلود

<div dir="ltr">

```bash
md5sum ecoli_k12.gff
tail -n 1 ecoli_k12.gff
tail -n 2 ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
837628601d3bbf74c218716d7ea2df86  ecoli_k12.gff
###
ATAAAACTGGTCGACTGGTTACAACAACGCCTGGGGCTTTTAGAGCAACGAGACACGGCAATGTTGCACCGTTTGCTGCA
TGATATTGAAAAAAATATCACCAAATAAAAAACGCCTTAGTAAGTATTTTTC
```

</div>

1. ‏md5 باید **دقیقاً** `837628601d3bbf74c218716d7ea2df86` باشد. اگر یک حرف فرق داشت، فایل با فایل درس یکی نیست.
2. ‏GFF با `###` (نشانه‌ی پایان) تمام می‌شود و FASTA با یک خط کوتاه‌تر که سر جای خودش پایان یافته است. ولی **تنها md5 مطمئن است.** فایلی که درست وسط کار قطع شده، ممکن است پایانی ظاهراً عادی داشته باشد.

---

## تمرین ۳: فشرده یا نه، و چقدر؟

<div dir="ltr">

```bash
ls -lh fastq/minigut_sample2_R1.fastq.gz
file fastq/minigut_sample2_R1.fastq.gz
```

</div>

<div dir="ltr">

```text
-rw-rw-r-- 1 ubuntu ubuntu 1.6M Oct 19 21:22 fastq/minigut_sample2_R1.fastq.gz
fastq/minigut_sample2_R1.fastq.gz: gzip compressed data, was "test_minigut_sample2_R1.fastq", last modified: Wed Mar 23 12:28:05 2022, from Unix, original size modulo 2^32 8164491
```

</div>

1. فشرده **1.6M** (نزدیک به ۱٫۶ مگابایت)؛ اصلی **۸٬۱۶۴٬۴۹۱ بایت** (نزدیک به ۸٫۲ مگابایت).
2. ۸٫۲ ÷ ۱٫۶ ≈ **۵ برابر**؛ کمی بیشتر از `minigut_R1` (نزدیک به ۴٫۳ برابر). میزان فشرده شدن به محتوا بستگی دارد: هرچه متن تکراری‌تر (برای نمونه خط‌های کیفیت با `FFFF…` فراوان)، فشرده‌سازی بهتر.

**نکته:** `modulo 2^32` یعنی برای فایل‌های بزرگ‌تر از ۴ گیگابایت این عدد درست نیست. برای فایل‌های کوچک این درس مشکلی نیست.

---

## تمرین ۴: ورق زدن و جستجو در GFF

1. نخستین خط داده نوع **`region`** دارد: کل کروموزوم، از ۱ تا ۴٬۶۴۱٬۶۵۲.
2. با `/rpoB` و Enter، نخستین رخداد در خطی از نوع **`gene`** است، با آغاز **۴٬۱۸۱٬۲۴۵** و پایان **۴٬۱۸۵٬۲۷۳**: همان جایی که در بخش ۰۰ در NCBI Gene دیدیم. (این خط ۸٬۶۱۸ام فایل است.)
3. با **`q`**.

**اشتباه رایج:** بستن پنجره‌ی ترمینال برای بیرون آمدن از `less`. لازم نیست؛ `q` کافی است.

---

## تمرین ۵: جدول پاسخ درست شبیه‌سازی

<div dir="ltr">

```bash
wc -l ground_truth.tsv
cat ground_truth.tsv
```

</div>

1. **۲۴ خط**؛ با کنار گذاشتن خط عنوان ستون‌ها، **۲۳ ردیف** داده.
2. ‏`minigut` از **دو** ژنوم ساخته شده: *Bacteroides fragilis* YCH46 (`NC_006347.1`، ۲۸٬۹۱۲ جفت رید) و *Escherichia coli* K-12 MG1655 (`NC_000913.3`، ۲۱٬۰۸۸ جفت رید). ۲۱ ردیف دیگر مال `minigut_sample2` است.
3. فایل تنها ۲۴ خط دارد و در یک نگاه دیده می‌شود. ژنوم ۵۸٬۰۲۲ خط دارد؛ `cat` همه را از ترمینال رد می‌کند و چیزی دیده نمی‌شود.

</div>
