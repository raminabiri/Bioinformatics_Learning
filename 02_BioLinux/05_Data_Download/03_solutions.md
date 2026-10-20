<div dir="rtl">

# پاسخ تشریحی: دریافت داده با دستور

> دستورها در **2026-10-12** با NCBI Datasets CLI 18.38.0 اجرا شده‌اند. عددهایی که با زمان تغییر می‌کنند، تاریخ دارند.

---

## تمرین ۱: سفر gyrA با یک دستور

خروجی (2026-10-12):

<div dir="ltr">

```text
== 3. NCBI Gene
GeneID=946614  symbol=gyrA  locus_tag=b2231  DNA gyrase subunit A
== 4. UniProtKB (reviewed / Swiss-Prot)
Entry	Length	Protein names	EC number
P0AES4	875	DNA gyrase subunit A (EC 5.6.2.2)	5.6.2.2
== 5. KEGG (via UniProt cross-reference)
ENTRY       b2231             CDS       T00007
ORTHOLOGY   K02469  DNA gyrase subunit A [EC:5.6.2.2]
== 6. AlphaFold DB
model=AF-P0AES4-F1  mean_pLDDT=87.38
== 7. PDB (experimental structures that contain this UniProt sequence)
entries=19  first: 1AB4, 1X75, 1ZI0, 3NUH, 4TMA
== 8. PubMed (literature)
PubMed hits for "gyrA AND fluoroquinolone resistance": 2848
```

</div>

1. **بله، یکی‌اند:** Gene ID 946614، UniProt P0AES4، طول ۸۷۵. با دستور به همان چیزی رسیدیم که در مرورگر دیدیم، ولی در چند ثانیه.
2. **۱۹ ساختار** در برابر ۳۹۱ برای RpoB. یک دلیل: RpoB بخشی از آنزیم بزرگ RNA پلیمراز است و هر ساختاری از کل این آنزیم (با DNA، RNA، فاکتورها و داروها) زنجیره‌ی RpoB را هم دارد. دلیل دیگر: بسیاری از ساختارهای gyrase از گونه‌های دیگر (مانند *Staphylococcus aureus* یا *Mycobacterium tuberculosis*) هستند و در این شمارش که تنها `P0AES4` را می‌جوید، نمی‌آیند.
3. **نه.** gyrA در KEGG در هیچ نقشه‌ی مسیری (PATHWAY) نیست. پیامد: در بخش ۰۶، اگر کار ژن‌های میکروبیوم را تنها در سطح «مسیر» خلاصه کنید، ژن‌هایی مانند gyrA، و بسیاری از ژن‌های مقاومت، از دید شما پنهان می‌مانند.

---

## تمرین ۲: ژنوم مرجع را دانلود کنید و بکاوید

<div dir="ltr">

```bash
datasets download genome accession GCF_000005845.2 --include genome,protein,gff3 --filename ecoli_k12.zip
unzip -o ecoli_k12.zip
grep -c '>' ncbi_dataset/data/GCF_000005845.2/protein.faa
awk -F'\t' '$3=="gene" && $9 ~ /Name=rpoB;/ {print $1, $4, $5, $7, $5-$4+1}' ncbi_dataset/data/GCF_000005845.2/genomic.gff
```

</div>

<div dir="ltr">

```text
4300
NC_000913.3 4181245 4185273 + 4029
```

</div>

2. **۴٬۳۰۰ پروتئین.**
3. آغاز **۴٬۱۸۱٬۲۴۵**، پایان **۴٬۱۸۵٬۲۷۳**، رشته‌ی **+**. همان چیزی است که در NCBI Gene دیدیم.
4. ۴٬۰۲۹ نوکلئوتید = ۱٬۳۴۳ کدون = ۱٬۳۴۲ اسیدآمینه + یک کدون پایان. ✓

**اشتباه رایج:** فراموش کردن `+1`. همچنین نوشتن `Name=rpoB` بی `;`: در آن صورت ژن‌هایی مانند `rpoBC` (اگر بود) هم پیدا می‌شدند. `;` پایان نام را نشان می‌دهد.

---

## تمرین ۳: هزار رید از ENA، بی‌دانلود کامل

<div dir="ltr">

```bash
curl -s https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz | zcat | head -n 4000 > ERR688359_head.fastq
wc -l ERR688359_head.fastq
awk 'NR%4==2 {print length($0)}' ERR688359_head.fastq | sort -n | uniq -c | sort -rn | head -3
awk 'NR%4==2 {print length($0)}' ERR688359_head.fastq | sort -n | sed -n '1p;$p'
```

</div>

<div dir="ltr">

```text
4000 ERR688359_head.fastq
    794 96
     20 95
     12 94
30
96
```

</div>

1. فایل **۴٬۰۰۰ خط** دارد، یعنی ۱٬۰۰۰ رید.
2. کوتاه‌ترین **۳۰** و بلندترین **۹۶** باز است. طول ۹۶ از همه بیشتر آمده است: ۷۹۴ رید از ۱٬۰۰۰ (۷۹٫۴٪).
3. دستگاه همه‌ی ریدها را با یک طول می‌خواند. پس این ریدها **پیش از ثبت در بایگانی پیرایش (trim) شده‌اند**: بخش‌های کم‌کیفیت انتهای برخی ریدها بریده شده است. پیامد: اگر شما روی این داده کنترل کیفیت کنید، داده‌ی «خام» را نمی‌سنجید، و این را باید در گزارش بنویسید. پیرایش را در بخش ۰۶ یاد می‌گیرید.

---

## تمرین ۴ (چالشی): خلاصه‌ی نمونه‌به‌نمونه

<div dir="ltr">

```bash
bash ../scripts/project_summary.sh PRJEB7774 > PRJEB7774_samples.tsv
head -3 PRJEB7774_samples.tsv
tail -n +2 PRJEB7774_samples.tsv | cut -f2 | sort | uniq -c
tail -n +2 PRJEB7774_samples.tsv | sort -t$'\t' -k4,4n | sed -n '1p;$p'
```

</div>

خروجی (2026-10-12):

<div dir="ltr">

```text
sample	n_runs	layouts	total_reads
SAMEA3136623	2	PAIRED,SINGLE	19967424
SAMEA3136624	2	SINGLE,PAIRED	26034931
    156 2
SAMEA3136709	2	SINGLE,PAIRED	16312237
SAMEA3136692	2	SINGLE,PAIRED	40653767
```

</div>

1. **۱۵۶ نمونه، هر کدام ۲ اجرا** (یکی SINGLE و یکی PAIRED). با [تمرین ۴ ماژول پایگاه‌های داده](../../00_Orientation/02_Biological_Databases/02_exercises.md) جور است.
2. کمترین: `SAMEA3136709` (۱۶٫۳ میلیون)؛ بیشترین: `SAMEA3136692` (۴۰٫۷ میلیون).
3. **ایراد:** در اجرای PAIRED، `read_count` شمار **جفت‌ها**ست، پس شمار ریدها دو برابر آن است. جمع آن با شمار ریدهای SINGLE، جمع دو یکای گوناگون است، مانند جمع زدن «شمار جفت کفش» با «شمار تک کفش». افزون بر این، این دو اجرا از دو کتابخانه‌ی جداگانه با طول رید گوناگون‌اند و نباید بی‌اندیشه با هم یکی شوند. برای سنجش عمق نمونه‌ها، ستون `base_count` (شمار کل بازها) یا تنها اجرای PAIRED بهتر است.

**نکته درباره‌ی اسکریپت:** ENA ستون `run_accession` را همیشه نخست می‌گذارد، هر ترتیبی که در `fields=` خواسته باشید. برای همین اسکریپت ستون‌ها را **با نام** پیدا می‌کند، نه با شماره.

</div>
