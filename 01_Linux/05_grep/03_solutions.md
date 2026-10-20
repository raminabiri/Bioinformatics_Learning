<div dir="rtl">

# پاسخ تشریحی: جستجو با grep

> دستورها در 2026-10-20 با GNU grep 3.11 (grep پیش‌فرض Ubuntu 24.04) در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: gyrA کجاست؟

<div dir="ltr">

```bash
grep -c 'gyrA' ecoli_k12.gff
grep -n 'Name=gyrA;' ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
2
4858:NC_000913.3	RefSeq	gene	2336793	2339420	.	-	.	ID=gene-b2231;…
```

</div>

1. **۲ خط** (ژن و CDS آن).
2. خط **۴٬۸۵۸**. آغاز **۲٬۳۳۶٬۷۹۳**، پایان **۲٬۳۳۹٬۴۲۰**، رشته‌ی **منفی** (`-`). خط CDS نام دیگری (`Name=NP_…`) دارد، پس الگوی `Name=gyrA;` تنها خط ژن را می‌یابد.

**اشتباه رایج:** الگوی `'gyrA'` بی `Name=` و `;`. این‌جا تنها دو خط می‌یابد، ولی برای ژن‌هایی مانند `rpo` (ماژول، بخش ۳) بسیاری خط‌های ناخواسته هم می‌آیند.

---

## تمرین ۲: چند ژن از هر نوع؟

<div dir="ltr">

```bash
grep -c -P '\tgene\t' ecoli_k12.gff
grep -c -P '\tCDS\t' ecoli_k12.gff
grep -P '\tgene\t' ecoli_k12.gff | grep -c 'gene_biotype=rRNA'
grep -P '\tgene\t' ecoli_k12.gff | grep -c 'gene_biotype=protein_coding'
```

</div>

<div dir="ltr">

```text
4506
4340
22
4290
```

</div>

1. **۴٬۵۰۶** ژن و **۴٬۳۴۰** CDS.
2. **۲۲** ژن rRNA (هفت اپرون × ۳، به‌اضافه‌ی یک 5S اضافه).
3. **۴٬۲۹۰** ژن پروتئین‌ساز، ولی **۴٬۳۴۰** CDS: ۵۰ CDS بیشتر. چرا؟ دو دلیل دارد. یکم، ژن‌های کاذب (`pseudogene`) هم خط CDS دارند: ۳۷ خط CDS از آنِ ژن‌های کاذب است. دوم، برخی ژن‌ها **چند** خط CDS دارند. برای نمونه *dnaX* (`gene-b0470`) سه خط CDS دارد، چون با لغزش ریبوزوم دو پروتئین با طول‌های گوناگون می‌سازد. **«شمار ژن» به این بستگی دارد که چه چیزی را می‌شمارید.** در ماژول ۰۶ این را دقیق‌تر بررسی می‌کنید.

---

## تمرین ۳: خط‌های توالی

<div dir="ltr">

```bash
grep -v -c '^>' ecoli_k12.fna
```

</div>

<div dir="ltr">

```text
58021
```

</div>

1. **۵۸٬۰۲۱** خط توالی.
2. **بله**: ۵۸٬۰۲۱ + ۱ خط عنوان = ۵۸٬۰۲۲ = `wc -l`. ✓

---

## تمرین ۴: ریدهای هر باکتری

<div dir="ltr">

```bash
zcat fastq/minigut_R1.fastq.gz | grep -c '^@NC_000913.3'
zcat fastq/minigut_R1.fastq.gz | grep -c '^@NC_006347.1'
zcat fastq/minigut_sample2_R1.fastq.gz | grep -c '^@NC_002516.2'
```

</div>

<div dir="ltr">

```text
21088
28912
1178
```

</div>

1. ‏*E. coli* **۲۱٬۰۸۸** و *B. fragilis* **۲۸٬۹۱۲** رید. جمع: ۲۱٬۰۸۸ + ۲۸٬۹۱۲ = **۵۰٬۰۰۰** = شمار کل ریدها. ✓ پس این نمونه تنها از همین دو باکتری ساخته شده است.
2. ‏*P. aeruginosa* **۱٬۱۷۸** رید؛ دقیقاً همان عدد `ground_truth.tsv`. ✓

**چرا `^` لازم است؟** `^@` تنها خط‌های **نام** را می‌گیرد. بی آن، اگر رشته‌ی `NC_000913.3` جای دیگری در فایل بیاید، شمرده می‌شود. (در این داده چنین نیست، ولی `^` عادت خوبی است.)

---

## تمرین ۵: خانواده‌ی ژن‌های thr

<div dir="ltr">

```bash
grep -P '\tgene\t' ecoli_k12.gff | grep -o -E 'Name=thr[A-Z]+;'
grep -P '\tgene\t' ecoli_k12.gff | grep 'gene_biotype=tRNA' | grep -o -E 'Name=thr[A-Z]+;'
```

</div>

<div dir="ltr">

```text
Name=thrL;
Name=thrA;
Name=thrB;
Name=thrC;
Name=thrW;
Name=thrS;
Name=thrV;
Name=thrP;
Name=thrU;
Name=thrT;
Name=thrW;
Name=thrV;
Name=thrU;
Name=thrT;
```

</div>

1. **۱۰ ژن**: thrL، thrA، thrB، thrC (اپرون ساخت ترئونین)، thrS (آنزیم ترئونیل-tRNA سنتتاز)، thrP، و چهار ژن tRNA.
2. چهار ژن tRNA: **thrW، thrV، thrU، thrT**. این‌ها tRNAهای ترئونین‌اند. نام‌گذاری *E. coli* برای ژن‌های tRNA همین است: سه حرف آمینواسید + یک حرف.

**نکته:** `grep` میانی (`gene_biotype=tRNA`) تنها خط‌هایی را نگه داشت که هم ژن‌اند و هم tRNA؛ سپس `-o` نام‌ها را بیرون کشید. لوله‌ی سه‌تایی یعنی سه صافی پشت سر هم.

</div>
