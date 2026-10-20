<div dir="rtl">

# پاسخ تشریحی: فرمت‌های آنوتیشن

> دستورها در 2026-10-20 با mawk 1.3.4، GNU grep 3.11، curl و seqkit 2.13.0 اجرا شدند. پیام‌های `[INFO]` `seqkit` برداشته شده‌اند.

---

## تمرین ۱: GFF کوچک rpoB

<div dir="ltr">

```bash
{ grep '^##' $G/ecoli_k12.gff | head -n 3; awk -F'\t' '$4<=4185273 && $5>=4181245' $G/ecoli_k12.gff; } > my_rpoB.gff3
diff my_rpoB.gff3 rpoB.gff3
```

</div>

1. ‏`diff` **هیچ خروجی‌ای** نداد: دو فایل یکسان‌اند. فایل آماده‌ی دوره هم با همین دستور ساخته شده بود.
2. ژن: `ID=gene-b3987`. CDS: `ID=cds-NP_418414.1;Parent=gene-b3987`. پس **ژن پدر است** و CDS فرزند آن. `b3987` همان locus tag rpoB است، و `NP_418414.1` شناسه‌ی پروتئین RefSeq (بخش ۰۰).

---

## تمرین ۲: BED برای gyrA

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" && $9 ~ /Name=gyrA;/ {print $1, $4-1, $5, "gyrA", 0, $7}' $G/ecoli_k12.gff > gyrA.bed
cat gyrA.bed
seqkit subseq --bed gyrA.bed $G/ecoli_k12.fna | seqkit fx2tab -n -l
seqkit subseq --bed gyrA.bed $G/ecoli_k12.fna | seqkit subseq -r 1:3 | tail -n 1
```

</div>

<div dir="ltr">

```text
NC_000913.3	2336792	2339420	gyrA	0	-
NC_000913.3_2336793-2339420:- gyrA	2628
ATG
```

</div>

1 و 2. طول **۲٬۶۲۸** و آغاز **`ATG`**.
3. ستون ۶ BED `-` است و `seqkit subseq` برای رشته‌ی منفی **خودش مکمل معکوس** را برمی‌گرداند (`:-` در نام خروجی). پس توالی، خود ژن است، از کدون آغاز. این همان کاری است که در ماژول پیشین با `samtools faidx -i` کردیم.

---

## تمرین ۳: کوتاه‌ترین ژن‌ها

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" {print $1, $4-1, $5, ".", 0, $7}' $G/ecoli_k12.gff > genes.bed
cut -f6 genes.bed | sort | uniq -c
awk '{print $3-$2, $1, $2, $3, $6}' genes.bed | sort -n | head -n 3
grep -P '\tgene\t' $G/ecoli_k12.gff | grep -P '\t1079120\t'
```

</div>

<div dir="ltr">

```text
   2216 +
   2290 -
27 NC_000913.3 1079119 1079146 +
27 NC_000913.3 3737176 3737203 -
30 NC_000913.3 2483728 2483758 +
NC_000913.3	RefSeq	gene	1079120	1079146	.	+	.	ID=…;Name=ymdG;…
```

</div>

1. **۲٬۲۱۶** روی + و **۲٬۲۹۰** روی −؛ همان عددهای بخش ۰۱.
2. دو ژن **۲۷ بازی**: یکی روی + از مرز ۱٬۰۷۹٬۱۱۹ (BED) و یکی روی − از مرز ۳٬۷۳۷٬۱۷۶.
3. آغاز GFF = آغاز BED + ۱: ۱٬۰۷۹٬۱۲۰ و ۳٬۷۳۷٬۱۷۷. جستجو در GFF: **ymdG** و **baxL**. ۲۷ باز = ۹ کدون = **۸ اسیدآمینه** + یک کدون پایان. چنین پروتئین‌های بسیار کوچکی را بیشتر با پروتئومیکس کشف کرده‌اند؛ در بخش ۰۷ (آنوتیشن) خواهید دید که برنامه‌های پیش‌بینی ژن آن‌ها را در بسیاری از موارد نمی‌یابند.

---

## تمرین ۴: GenBank ژن gyrA

<div dir="ltr">

```bash
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=gbwithparts&retmode=text&seq_start=2336793&seq_stop=2339420&strand=2" > gyrA.gb
grep '^LOCUS\|/product\|/protein_id' gyrA.gb
grep -A 1 '^ORIGIN' gyrA.gb | tail -n 1
```

</div>

<div dir="ltr">

```text
LOCUS       NC_000913               2628 bp    DNA     linear   CON 02-SEP-2026
                     /product="DNA gyrase subunit A"
                     /protein_id="NP_416734.1"
        1 atgagcgacc ttgcgagaga aattacaccg gtcaacattg aggaagagct gaagagctcc
```

</div>

1. فایل ۲۳۷ خط دارد.
2. طول **۲٬۶۲۸ bp**؛ پروتئین **DNA gyrase subunit A**؛ شناسه **NP_416734.1**.
3. ‏`atgagcgacc ttgcgagaga aattacaccg…`: دقیقاً همان `ATGAGCGACCTTGCGAGAGAAATTACACCG` ماژول پیشین (با حروف کوچک و گروه‌های ۱۰تایی، به شیوه‌ی GenBank). ✓ با `strand=2`، NCBI خودش مکمل معکوس را داد.

(تاریخ در خط `LOCUS` تاریخ آخرین به‌روزرسانی رکورد است و ممکن است برای شما فرق کند.)

---

## تمرین ۵: تبدیل دستی

1. ‏GFF: آغاز = ۱۸۹ + ۱ = **۱۹۰**، پایان = **۲۵۵**.
2. `NC_000913.3:190-255`.
3. ‏BED: ۲۵۵ − ۱۸۹ = **۶۶**. GFF: ۲۵۵ − ۱۹۰ + ۱ = **۶۶**. ✓ هر دو یکی‌اند، چون هر شیوه فرمول طول خودش را دارد.

**اشتباه رایج:** `NC_000913.3:189-255`. این ۶۷ باز می‌دهد و یک باز پیش از ژن را هم می‌آورد.

</div>
