<div dir="rtl">

# پاسخ تشریحی: فرمت‌های توالی

> دستورها در 2026-10-20 با seqkit 2.13.0 و samtools 1.20 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند. پیام‌های پیشرفت و `[INFO]` `seqkit` (که در stderr می‌آیند) برداشته شده‌اند.

---

## تمرین ۱: کیفیت رید یکم، با دست

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | head -n 4 | tail -n 1 | fold -w1 | sort | uniq -c
printf '%d\n' "'<"
```

</div>

<div dir="ltr">

```text
      2 /
      4 <
      8 B
    112 F
60
```

</div>

1. چهار نویسه: `F` (۱۱۲ بار)، `B` (۸)، `<` (۴)، `/` (۲)؛ جمع ۱۲۶ = طول رید. ✓
2. `F` = ۷۰ − ۳۳ = **Q37**؛ `B` = ۶۶ − ۳۳ = **Q33**؛ `<` = ۶۰ − ۳۳ = **Q27**؛ `/` = ۴۷ − ۳۳ = **Q14**.
3. ‏Q ≥ ۳۰: `F` و `B` = ۱۲۰ باز از ۱۲۶ = **۹۵٫۲٪**.

---

## تمرین ۲: کارت شناسایی همه‌ی فایل‌ها

<div dir="ltr">

```bash
seqkit stats *.fna *.fa *.fasta
seqkit stats -a -T fastq/minigut_sample2_R1.fastq.gz
```

</div>

1. همان جدول بخش ۴ درس. `sample.fasta` نوع **Protein** دارد (۱۴ اسیدآمینه).
2. ستون‌های پایانی برای `minigut_sample2_R1`:

<div dir="ltr">

```text
Q20(%)	Q30(%)	AvgQual	GC(%)	sum_n
98	96	27.47	40.51	26
```

</div>

(تنها پنج ستون پایانی نشان داده شده‌اند.) **Q30 = ۹۶٪** (بهتر از ۹۲٪ `minigut`) و **GC = ۴۰٫۵۱٪** (کمتر از ۴۶٫۷۹٪؛ همان عدد ماژول ۰۹ لینوکس). `sum_n` = ۲۶: این فایل روی هم ۲۶ باز `N` دارد (پخش در ۱۵ رید؛ بخش ۰۱).

---

## تمرین ۳: ریدهای Bacteroides

<div dir="ltr">

```bash
seqkit grep -r -p '^NC_006347' fastq/minigut_R1.fastq.gz -o bfragilis_R1.fq.gz
seqkit stats -T bfragilis_R1.fq.gz
```

</div>

<div dir="ltr">

```text
num_seqs	sum_len
28912	3642912
```

</div>

(تنها ستون‌های شمار و جمع طول نشان داده شده‌اند.)

1 و 2. **۲۸٬۹۱۲ رید** و ۳٬۶۴۲٬۹۱۲ باز (۲۸٬۹۱۲ × ۱۲۶). دقیقاً همان شمار `ground_truth.tsv` برای *B. fragilis*. ✓ با ۲۱٬۰۸۸ رید *E. coli* (درس)، جمع ۵۰٬۰۰۰ است.

---

## تمرین ۴: ژن‌های رشته‌ی منفی

<div dir="ltr">

```bash
samtools faidx -i ecoli_k12.fna NC_000913.3:2336793-2339420 > gyrA.fa
seqkit stats -T gyrA.fa
seqkit subseq -r 1:3 gyrA.fa | tail -n 1
seqkit subseq -r -3:-1 gyrA.fa | tail -n 1
samtools faidx -i ecoli_k12.fna NC_000913.3:3441000-3441029 | tail -n 1
```

</div>

<div dir="ltr">

```text
num_seqs	sum_len
1	2628
ATG
TAA
ATGCAGGGTTCTGTGACAGAGTTTCTAAAA
```

</div>

1. **۲٬۶۲۸ باز**، همان طول ژن gyrA (بخش ۰۱).
2. آغاز **`ATG`** (کدون آغاز) و پایان **`TAA`** (یکی از سه کدون پایان). اگر `-i` را فراموش کرده بودید، توالی با `TTA` آغاز و با `CAT` پایان می‌یافت (مکمل معکوس کدون‌های پایان و آغاز)؛ یعنی ژن وارونه بود.
3. ‏rpoA روی رشته‌ی منفی است، پس آغازش در سر **بزرگ‌تر** (۳٬۴۴۱٬۰۲۹) است و ۳۰ باز آغاز ژن، خانه‌های ۳٬۴۴۱٬۰۰۰ تا ۳٬۴۴۱٬۰۲۹ با `-i` است. کدون‌ها: `ATG CAG GGT TCT GTG ACA GAG TTT` = **M Q G S V T E F**؛ آغاز پروتئین RpoA (زیرواحد α).

**اشتباه رایج:** گرفتن ناحیه‌ی ۳٬۴۴۰٬۰۴۰ تا ۳٬۴۴۰٬۰۶۹ (۳۰ باز **کوچک‌تر**). برای ژن رشته‌ی منفی، این **پایان** ژن است، نه آغازش.

---

## تمرین ۵: جایگاه‌های BamHI، دوباره

<div dir="ltr">

```bash
seqkit locate -P -p GGATCC ecoli_k12.fna | tail -n +2 | wc -l
seqkit locate -p GGATCC ecoli_k12.fna | tail -n +2 | wc -l
```

</div>

<div dir="ltr">

```text
494
988
```

</div>

1. **۴۹۴**، دقیقاً همان عدد درست ماژول sed و tr (پس از چسباندن خط‌ها). ✓ `seqkit` خط‌ها را خودش می‌چسباند.
2. ‏**۹۸۸** = ۲ × ۴۹۴. `GGATCC` پالیندروم است (مکمل معکوسش: `GGATCC`)، پس هر جایگاه روی هر دو رشته دیده می‌شود. برای الگویی که پالیندروم نیست (مانند `ATG`)، شمار روی دو رشته در بسیاری از موارد برابر نیست.

</div>
