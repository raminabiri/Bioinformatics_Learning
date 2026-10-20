<div dir="rtl">

# پاسخ تشریحی: لوله و هدایت خروجی

> دستورها در 2026-10-20 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: شمار ریدهای هر چهار فایل

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | wc -l
zcat fastq/minigut_R2.fastq.gz | wc -l
zcat fastq/minigut_sample2_R1.fastq.gz | wc -l
zcat fastq/minigut_sample2_R2.fastq.gz | wc -l
```

</div>

<div dir="ltr">

```text
200000
200000
99972
99972
```

</div>

1. ‏`minigut`: R1 و R2 هر کدام **۵۰٬۰۰۰ رید**. `minigut_sample2`: هر کدام **۲۴٬۹۹۳ رید**.
2. **بله، یکسان‌اند**، و باید چنین باشد. در توالی‌یابی دوخوانه (paired-end)، هر قطعه‌ی DNA از **دو سر** خوانده می‌شود: R1 از یک سر و R2 از سر دیگر. پس هر رید R1 یک «جفت» در R2 دارد. اگر شمارشان یکی نبود، یکی از دو فایل خراب یا نیمه‌کاره است.

(نوشتن یک دستور برای هر چهار فایل با هم را در ماژول «متغیر و حلقه» یاد می‌گیرید.)

---

## تمرین ۲: رید سوم نمونه‌ی دوم

رید سوم = خط‌های ۹ تا ۱۲. پس ۱۲ خط اول را بگیر و ۴ خط آخرش را:

<div dir="ltr">

```bash
zcat fastq/minigut_sample2_R1.fastq.gz | head -n 12 | tail -n 4
```

</div>

<div dir="ltr">

```text
@CP009257.1_2_0/1
ATTTGTTTACTGCTGTGGCTGATGTGAGTGTGTTACAGGGTTAAATTCATCAAGGATGCTATGCTAAAGT…
+
FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF8FFFFFFFFFFFFFFFFFFFFFFFFFFFF8FF…
```

</div>

1. نام: `@CP009257.1_2_0/1`.
2. با `CP009257.1` آغاز می‌شود: ژنوم *Acinetobacter baumannii* AB030، که بیشترین ریدهای این نمونه را دارد.

**اشتباه رایج:** `head -n 12 | tail -n 3`، که خط نام را جا می‌اندازد. یک رید همیشه **۴** خط است.

---

## تمرین ۳: طول ریدهای نمونه‌ی دوم

<div dir="ltr">

```bash
zcat fastq/minigut_sample2_R1.fastq.gz | head -n 2 | tail -n 1 | wc -c
```

</div>

<div dir="ltr">

```text
152
```

</div>

۱۵۲ − ۱ (پایان‌خط) = **۱۵۱ باز**. ریدهای این نمونه ۲۵ باز بلندتر از `minigut` (۱۲۶) هستند؛ پس دو نمونه با تنظیمات توالی‌یابی گوناگون ساخته شده‌اند. در ماژول `awk` میانگین طول **همه‌ی** ریدها را حساب می‌کنیم، نه تنها رید یکم.

---

## تمرین ۴: یک فایل آزمایشی کوچک

<div dir="ltr">

```bash
zcat fastq/minigut_sample2_R1.fastq.gz | head -n 4000 > test_1000.fastq
wc -l test_1000.fastq
ls -lh test_1000.fastq
```

</div>

<div dir="ltr">

```text
4000 test_1000.fastq
-rw-rw-r-- 1 ubuntu ubuntu 319K Oct 20 07:02 test_1000.fastq
```

</div>

1. ۱۰۰۰ رید × ۴ خط = **۴٬۰۰۰ خط**.
2. **۴٬۰۰۰ خط** و نزدیک به **319K** (۳۱۹ کیلوبایت؛ بازشده و فشرده‌نشده). تاریخ و ساعت روی کامپیوتر شما فرق دارد.
3. دستورها روی فایل کوچک **بی‌درنگ** اجرا می‌شوند، پس اشتباه‌ها زود پیدا می‌شوند. وقتی دستور درست کار کرد، آن را روی فایل کامل (که در پروژه‌ی واقعی می‌تواند ده‌ها گیگابایت باشد) اجرا کنید.

---

## تمرین ۵: نتیجه و خطا، جدا

### بخش ۱

<div dir="ltr">

```bash
ls ecoli_k12.gff fastq missing.fa > list.txt 2> errors.txt
cat list.txt
cat errors.txt
```

</div>

<div dir="ltr">

```text
ecoli_k12.gff

fastq:
minigut_R1.fastq.gz
minigut_R2.fastq.gz
minigut_sample2_R1.fastq.gz
minigut_sample2_R2.fastq.gz
ls: cannot access 'missing.fa': No such file or directory
```

</div>

- ‏`list.txt` نتیجه را دارد: نام فایل `ecoli_k12.gff`، و چون `fastq` پوشه است، فهرست محتوای آن.
- ‏`errors.txt` تنها پیام خطا را دارد، چون `missing.fa` نیست.
- هیچ‌کدام در ترمینال چاپ نشد.

### بخش ۲

<div dir="ltr">

```bash
head -n 1 ecoli_k12.fna > headers.txt
head -n 1 host_chr21_region.fa >> headers.txt
cat headers.txt
```

</div>

<div dir="ltr">

```text
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
>chr21part
```

</div>

دستور یکم با `>` فایل را می‌سازد؛ دستور دوم باید **`>>`** باشد. اگر دوباره `>` بزنید، خط یکم پاک می‌شود و تنها `>chr21part` می‌ماند.

</div>
