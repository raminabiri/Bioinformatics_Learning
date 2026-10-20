<div dir="rtl">

# پاسخ تشریحی: ویرایش متن با tr و sed

> دستورها در 2026-10-20 با GNU sed، GNU coreutils، GNU grep 3.11 و mawk 1.3.4 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: کالبدشکافی تکه‌ی کروموزوم ۲۱

<div dir="ltr">

```bash
grep -v '^>' host_chr21_region.fa | tr -d '\n' | wc -c
grep -v '^>' host_chr21_region.fa | tr -cd 'Nn' | wc -c
grep -v '^>' host_chr21_region.fa | tr -cd 'acgt' | wc -c
grep -v '^>' host_chr21_region.fa | tr -cd 'ACGTacgt' | wc -c
grep -v '^>' host_chr21_region.fa | tr -cd 'GCgc' | wc -c
echo "160215 400000" | awk '{print $1/$2*100}'
```

</div>

<div dir="ltr">

```text
500000
100000
268185
400000
160215
40.0538
```

</div>

1. **۵۰۰٬۰۰۰ باز** (همان عددی که در ماژول ۰۳ با حساب `wc -c` به دست آوردیم).
2. ‏**۱۰۰٬۰۰۰ N**، یعنی **۲۰٪**. این تکه از ژنوم مرجع انسان بخش‌هایی دارد که توالی‌شان شناخته نیست (در بسیاری از موارد نزدیک سانترومر).
3. **۲۶۸٬۱۸۵** باز با حروف کوچک، از **۴۰۰٬۰۰۰** باز شناخته‌شده: **۶۷٪**. بیشترِ این تکه **تکراری** است؛ در ژنوم انسان بیش از نیمی از کل ژنوم را تکرارها می‌سازند.
4. ‏GC = ۱۶۰٬۲۱۵ ÷ ۴۰۰٬۰۰۰ = **۴۰٫۰۵٪**. اگر بر ۵۰۰٬۰۰۰ تقسیم کنید، ۳۲٪ می‌گیرید که **نادرست** است: N یعنی «نمی‌دانیم چه بازی است»، پس نباید در هیچ سوی کسر بیاید.

**اشتباه رایج:** `tr -cd 'GC'` (تنها حروف بزرگ). در این فایل بیش از نیمی از G و Cها کوچک‌اند و گم می‌شوند.

---

## تمرین ۲: جایگاه‌های BamHI

<div dir="ltr">

```bash
grep -c 'GGATCC' ecoli_k12.fna
grep -v '^>' ecoli_k12.fna | grep -o 'GGATCC' | wc -l
grep -v '^>' ecoli_k12.fna | tr -d '\n' | grep -o 'GGATCC' | wc -l
```

</div>

<div dir="ltr">

```text
465
467
494
```

</div>

1. ۴۶۵ خط دارای `GGATCC`؛ ۴۶۷ رخداد خط‌به‌خط؛ **۴۹۴** رخداد واقعی.
2. ۴۹۴ − ۴۶۷ = **۲۷ جایگاه** روی مرز خط‌ها بودند و بی‌صدا گم شده بودند.

---

## تمرین ۳: مکمل معکوس

<div dir="ltr">

```bash
echo 'ATGAGCGACCTTGCGAGAGAAATTACACCG' | tr 'ACGTacgt' 'TGCAtgca' | rev
echo 'ATGAGCGACCTTGCGAGAGAAATTACACCG' | tr 'ACGTacgt' 'TGCAtgca' | rev | tr 'ACGTacgt' 'TGCAtgca' | rev
```

</div>

<div dir="ltr">

```text
CGGTGTAATTTCTCTCGCAAGGTCGCTCAT
ATGAGCGACCTTGCGAGAGAAATTACACCG
```

</div>

1. ‏`CGGTGTAATTTCTCTCGCAAGGTCGCTCAT`. توجه کنید که با `CAT` پایان می‌یابد: مکمل معکوسِ کدون آغاز `ATG`. چون gyrA روی رشته‌ی **منفی** است، در فایل ژنوم (که رشته‌ی مثبت را نگه می‌دارد) آغاز این ژن به شکل همین `…CAT` دیده می‌شود.
2. **همان توالی آغازین.** مکملِ مکمل خود باز است (A→T→A) و معکوسِ معکوس همان ترتیب اول. این یک وارسی ساده است که دستور مکمل معکوس را درست نوشته‌اید.

---

## تمرین ۴: TSV به CSV

<div dir="ltr">

```bash
sed 's/\t/,/g' ground_truth.tsv > ground_truth.csv
wc -l ground_truth.csv
cut -d',' -f4 ground_truth.csv | head -n 3
sed 's/^minigut_sample2/sample2/' ground_truth.tsv | cut -f1 | sort | uniq -c
```

</div>

<div dir="ltr">

```text
24 ground_truth.csv
organism
Bacteroides fragilis YCH46
Escherichia coli K-12 MG1655
      2 minigut
      1 sample
     21 sample2
```

</div>

1. **۲۴ خط**، همان شمار خط‌های TSV؛ تنها جداکننده عوض شده است.
2. ‏`organism` (عنوان ستون)، سپس نام دو باکتری نمونه‌ی `minigut`. چون جداکننده اکنون ویرگول است، `cut` باید `-d','` بگیرد.
3. ۲ ردیف `minigut`، ۲۱ ردیف `sample2`، و ۱ خط عنوان (`sample`). `^` لازم است: بی آن، `minigut_sample2` در هر جای خط عوض می‌شد.

**اشتباه رایج:** فراموش کردن `g` در `s/\t/,/g`. تنها Tab یکم هر خط ویرگول می‌شود و فایل نیمه‌CSV می‌ماند.

---

## تمرین ۵: sed به جای ابزارهای پیشین

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | sed -n '5,8p'
sed '/^#/d' ecoli_k12.gff | wc -l
```

</div>

<div dir="ltr">

```text
@NC_006347.1_1/1
CGCAAAGCCAGCTTCGCGAATTGATCCGCCAGAGTTTCAATCATCCTTCCATTTATGTATGGGGGCTTCACAATGAAGTA…
+
BBBBBFFFFFFFFFFFFFFFFFFFFFFFFFFFF/FFFFFFFFFFFFFFFFFFBFFBFFFF/FFFFFFFFFFFFFFFFFF/…
9523
```

</div>

1. **یکی است**: همان رید `@NC_006347.1_1/1` که در ماژول ۰۴ با `head -n 8 | tail -n 4` گرفتیم.
2. **۹٬۵۲۳** خط؛ دقیقاً همان `grep -v -c '^#'`. ✓

در لینوکس برای یک کار در بسیاری از موارد چند راه هست. هر کدام را که روشن‌تر می‌فهمید به کار ببرید؛ ولی روش‌های دیگر را هم بشناسید، چون در اسکریپت‌های دیگران می‌بینید.

</div>
