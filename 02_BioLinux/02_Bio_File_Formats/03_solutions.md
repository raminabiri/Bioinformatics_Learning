<div dir="rtl">

# پاسخ تشریحی: فرمت‌های داده‌ی زیستی

> اجرا شده در 2026-10-13 با samtools 1.20، bcftools 1.21 و seqkit 2.13.

---

## تمرین ۱: gyrA روی رشته‌ی منفی

<div dir="ltr">

```bash
samtools faidx $G NC_000913.3:2336793-2339420 | sed -n 2p | cut -c1-10
samtools faidx -i $G NC_000913.3:2336793-2339420 | head -2
samtools faidx -i $G NC_000913.3:2336793-2339420 | grep -v '>' | tr -d '\n' | tail -c 3; echo
```

</div>

<div dir="ltr">

```text
TTATTCTTCT
>NC_000913.3:2336793-2339420/rc
ATGAGCGACCTTGCGAGAGAAATTACACCGGTCAACATTGAGGAAGAGCTGAAGAGCTCCTATCTGGATTATGCGATGTC
TAA
```

</div>

1. بدون `-i`، توالی با `TTA` شروع می‌شود، که مکمل معکوس کدون پایان `TAA` است. یعنی **انتهای ژن** را از سمت رشته‌ی مثبت می‌خوانیم.
2. با `-i`: شروع **`ATG`** (کدون آغاز) و پایان **`TAA`** (کدون پایان).
3. ژنوم مرجع همیشه به‌صورت رشته‌ی **مثبت** ذخیره می‌شود. ژنی که روی رشته‌ی منفی است باید **reverse complement** شود تا از 5' به 3' خودش خوانده شود. ترجمه‌ی توالی بدون `-i` پروتئین بی‌معنی می‌دهد. نیمی از ژن‌های *E. coli* (۲٬۲۹۰ از ۴٬۵۰۶) روی رشته‌ی منفی‌اند.

---

## تمرین ۲: کیفیت یک رید

<div dir="ltr">

```bash
awk 'NR==4' data/minigut_3reads.fastq | fold -w1 | sort | uniq -c
```

</div>

<div dir="ltr">

```text
      2 /     ← ASCII 47 − 33 = Q14
      4 <     ← ASCII 60 − 33 = Q27
      8 B     ← ASCII 66 − 33 = Q33
    112 F     ← ASCII 70 − 33 = Q37
```

</div>

1. جمع: 2 + 4 + 8 + 112 = **۱۲۶** = طول رید. ✓
2. **۲ باز** زیر Q20 (هر دو `/` با Q14).

3. <div dir="ltr">

   ```bash
   seqkit fq2fa data/minigut_3reads.fastq | head -2

   ```

   </div>

   خط کیفیت **حذف** می‌شود. این تبدیل فقط برای ابزارهایی مجاز است که کیفیت را استفاده نمی‌کنند (مثلاً BLAST یا شمارش k-mer)، و ترجیحاً **بعد از QC و پیرایش** (ماژول 06/01). برای mapping و variant calling کیفیت لازم است.

---

## تمرین ۳: tRNAها به BED

<div dir="ltr">

```bash
awk -F'\t' 'BEGIN{OFS="\t"} $3=="gene" && $9 ~ /gene_biotype=tRNA/ {
     match($9,/Name=[^;]+/); print $1, $4-1, $5, substr($9,RSTART+5,RLENGTH-5), 0, $7}' \
  ../01_Bash_Linux/data/ecoli_k12.gff > trna.bed
wc -l < trna.bed ; head -2 trna.bed
awk '{s+=$3-$2} END{print "BED total", s}' trna.bed
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/ {s+=$5-$4+1} END{print "GFF total", s}' ../01_Bash_Linux/data/ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
86
NC_000913.3	225380	225457	ileV	0	+
NC_000913.3	225499	225575	alaV	0	+
BED total 6747
GFF total 6747
```

</div>

1. **۸۶ tRNA**.
2. هر دو **۶٬۷۴۷ باز**. فرمول طول در BED `end − start` و در GFF `end − start + 1` است.
3. اگر `$4-1` را فراموش کنید، هر بازه یک باز کوتاه‌تر می‌شود (اولین باز حذف می‌شود): **۸۶ باز کمتر** (۶٬۶۶۱). برای tRNA یعنی ۱٫۳٪ کل؛ برای یک CDS یعنی از دست رفتن باز اول کدون آغاز.

---

## تمرین ۴: GenBank در برابر FASTA

<div dir="ltr">

```bash
awk '/^ORIGIN/{f=1; next} /^\/\//{f=0} f' data/rpoB.gb | tr -d ' 0-9\n' | tr a-z A-Z | md5sum
samtools faidx $G NC_000913.3:4181245-4185273 | grep -v '>' | tr -d '\n' | md5sum
python3 -c "import re; t=open('data/rpoB.gb').read(); s=re.search(r'/translation=\"([^\"]+)\"', t).group(1); s=''.join(s.split()); print(len(s), s[:20])"
```

</div>

<div dir="ltr">

```text
07be65b41d32156e9aa0110548b73ac0  -
07be65b41d32156e9aa0110548b73ac0  -
1342 MVYSYTEKKRIRKDFGKRPQ
```

</div>

1. ‏md5 **یکسان** است: دو منبع (GenBank و FASTA مرجع) دقیقاً یک توالی دارند. مقایسه‌ی md5 سریع‌ترین راه اطمینان از یکسان بودن دو توالی بزرگ است.
2. ‏`/translation` **۱۳۴۲ اسیدآمینه** دارد و با `M` شروع می‌شود. این همان طول `P0A8V2` در UniProt است (بخش 00/02).

---

## تمرین ۵: دو رکورد SAM

<div dir="ltr">

```bash
samtools flags 163 ; samtools flags 83
```

</div>

<div dir="ltr">

```text
0xa3	163	PAIRED,PROPER_PAIR,MREVERSE,READ2
0x53	83	PAIRED,PROPER_PAIR,REVERSE,READ1
```

</div>

1. هر دو **paired** و **proper pair** هستند. رکورد اول R2 روی رشته‌ی مثبت است و mate‌اش معکوس است. رکورد دوم R1 روی رشته‌ی معکوس است.
2. ‏**TLEN** مثبت برای mate با موقعیت کمتر (سمت چپ قطعه) و منفی برای mate سمت راست است. قدر مطلقش طول قطعه است (۲۷۷ و ۴۳۰).
3. ‏**MAPQ = 1** چون این ناحیه در مرجع chr21 **تکرار** شده است (۴۳٫۸٪ از ۴۰-مرها تکراری‌اند، 06/02). همترازی یکتا نیست.
4. نام رید wgsim به شکل `chr21part_<شروع>_<پایان>_...` است:
   - **رکورد دوم:** قطعه از ۹۹٬۷۶۹ تا ۱۰۰٬۱۹۸. mate‌اش (R2) در 99,769 همتراز شده (PNEXT) و خودش (R1، معکوس) در 100,073 = 100,198 − 126 + 1. **دقیقاً درست است.**
   - **رکورد اول (برای مقایسه):** قطعه‌ی واقعی از **۴۸۱٬۷۲۸** است، ولی در **۹۹٬۹۵۰** همتراز شده. فاصله 481,728 − 99,950 = **۳۸۱٬۷۷۸** است، دقیقاً همان فاصله‌ی دو نسخه‌ی قطعه‌ی تکراری که در 06/02 پیدا کردیم. Bowtie2 بین دو نسخه‌ی یکسان **یکی را تصادفی** انتخاب کرده و MAPQ = 1 دقیقاً همین را هشدار می‌دهد. این مثال واقعی معنای MAPQ پایین را نشان می‌دهد: «جای دیگری هم به همان خوبی ممکن بود».

---

## تمرین ۶: VCF در برابر حقیقت

<div dir="ltr">

```bash
bcftools view -H -v snps   data/chr21_spiked.vcf.gz | wc -l        # 87
bcftools view -H -v indels data/chr21_spiked.vcf.gz | wc -l        # 11
bcftools query -f '[%GT]\n' data/chr21_spiked.vcf.gz | sort | uniq -c
bcftools view -H -i 'QUAL>=20' data/chr21_spiked.vcf.gz | wc -l   # 62
```

</div>

<div dir="ltr">

```text
     46 0/1
     52 1/1
```

</div>

### ‏۶.۳ precision و recall

<div dir="ltr">

```bash
cut -f2 data/chr21_true_mutations.txt | sort -u > truth.pos
bcftools view -H data/chr21_spiked.vcf.gz | cut -f2 | sort -u > call.pos
bcftools view -H -i 'QUAL>=20' data/chr21_spiked.vcf.gz | cut -f2 | sort -u > call20.pos
comm -12 truth.pos call.pos | wc -l       # 84
comm -12 truth.pos call20.pos | wc -l     # 56
```

</div>

| مجموعه | فراخوانی | TP | precision | ‏recall (از ۳۸۷) |
| :--- | -: | -: | :-: | :-: |
| همه | 98 | 84 | 0.857 | 0.217 |
| QUAL ≥ 20 | 62 | 56 | 0.903 | 0.145 |

### ۶.۴ پوشش

<div dir="ltr">

```bash
samtools depth -a -r chr21part ../../06_Metagenomics/work/02_host/bam/minigut_spiked.host.bam \
  | awk '$3>0{c++} {s+=$3; n++} END{printf "mean %.2f covered %.1f%%\n", s/n, c/n*100}'
```

</div>

<div dir="ltr">

```text
mean 2.61 covered 76.5%
```

</div>

- با **میانگین عمق ۲٫۶×** فقط ۵٬۰۰۰ جفت‌رید روی ۵۰۰ کیلوباز هست، و **۲۳٫۵٪ ناحیه** (شامل ۲۰٪ N) اصلاً رید ندارد. برای فراخوانی قابل اعتماد معمولاً حداقل ۱۰ تا ۲۰ برابر عمق لازم است.
- **ژنوتیپ‌ها هم ضعیف‌اند:** در حقیقت، ۲۳۳ از ۳۴۶ SNP **ناهم‌زیگوت** هستند (کدهای IUPAC مثل `K` و `Y` در ستون ۴ فایل حقیقت). ولی ۵۲ از ۹۸ فراخوانی `1/1` (هم‌زیگوت) است. با ۱ یا ۲ رید، اگر هر دو تصادفاً آلل جایگزین را داشته باشند، فراخوانی‌گر ناهم‌زیگوت را هم‌زیگوت می‌بیند.
- **درس:** فیلتر QUAL precision را بالا برد (۰٫۸۶ ← ۰٫۹۰) ولی recall را پایین آورد. ولی محدودیت اصلی **داده** است، نه فیلتر.

### ‏۶.۵ indelها
‏VCF موقعیت indel را با **باز لنگر قبلی** می‌نویسد (POS = بازِ قبل از تغییر). ابزارهای دیگر، و احتمالاً فهرست wgsim، ممکن است موقعیت خود باز حذف/درج‌شده را بنویسند. پس تطبیق دقیق موقعیت ممکن است indel درست را با اختلاف ۱ از دست بدهد. ابزارهای ارزیابی حرفه‌ای (مثل `hap.py` یا `vcfeval`) واریانت‌ها را **نرمال‌سازی** (`bcftools norm`) و بر اساس هاپلوتایپ مقایسه می‌کنند (بخش 10/03).

</div>
