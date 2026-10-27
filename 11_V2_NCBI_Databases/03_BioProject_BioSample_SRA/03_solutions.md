<div dir="rtl">

# پاسخ تشریحی: BioProject، BioSample و SRA

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0 و SRA Toolkit 3.4.1، روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: بزرگ‌ترین run

<div dir="ltr">

```bash
sort -t, -k8,8nr runinfo.csv | head -2 | cut -d, -f1,4,7,8,16,26
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ERR688549,39170675,188,5701,PAIRED,SAMEA3136692
ERR688638,36858391,184,5431,PAIRED,SAMEA3136768
```

</div>

(الف) ‏`ERR688549`: ‏۳۹٫۲ میلیون جفت‌رید، **۵۷۰۱** مگابایت. سرستون (`Run,…`) این بار در پایان فهرست است، چون `nr` آن را (که عدد نیست) صفر می‌گیرد؛ پس `grep -v '^Run'` لازم نیست.
(ب) ‏۵۷۰۱ ÷ ۳۲ ≈ **۱۷۸** برابر. برای آزمودن گردش کار کوچک‌ترین (`ERR710417`، ۳۲ مگابایت) یا `ERR688359` (۹۶ مگابایت، با پاسخ معلوم از ENA)؛ تنها پس از درست کار کردن گردش کار به runهای بزرگ بروید.

---

## پاسخ ۲: نمونه‌های پروژه در یک نگاه

<div dir="ltr">

```bash
WE=$(grep -o '<WebEnv>[^<]*' hs.xml | cut -d'>' -f2)
curl -sS "$B/elink.fcgi?dbfrom=sra&db=biosample&query_key=1&WebEnv=$WE&cmd=neighbor_history" > hl.xml
grep -oE '<(LinkName|QueryKey)>[^<]*' hl.xml; sleep 0.4
WE2=$(grep -o '<WebEnv>[^<]*' hl.xml | cut -d'>' -f2); QK=$(grep -o '<QueryKey>[^<]*' hl.xml | cut -d'>' -f2)
curl -sS "$B/efetch.fcgi?db=biosample&query_key=$QK&WebEnv=$WE2" > all_bs.xml
grep -oE 'attribute_name="geographic location \(country and/or sea\)"[^>]*>[^<]*' all_bs.xml | sed 's/.*>//' | sort | uniq -c
grep -oE '<Title>[^<]*' all_bs.xml | sort | uniq -c | sort -rn
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`dbfrom=sra&db=biosample` | از ۳۱۲ run به نمونه‌هایشان؛ دو run یک نمونه یک BioSample می‌دهند |
| ‏`\(` و `\)` | پرانتز در `grep -E` معنای ویژه دارد؛ برای پرانتز واقعی در نام ویژگی، پیشش `\` |
| ‏`sed 's/.*>//'` | هر چه تا آخرین `>` هست را بردار؛ تنها مقدار بماند |

**خروجی واقعی:**

<div dir="ltr">

```
<LinkName>sra_biosample
<QueryKey>2
    156 Austria
     63 <Title>Stool sample from controls
     47 <Title>Stool sample from advanced adenoma
     46 <Title>Stool sample from carcinoma
```

</div>

(الف) هر **۱۵۶** نمونه از **اتریش**‌اند (مختصات نمونه‌ی درس، 47.80 و 13.04، در شهر زالتسبورگ است). یافته‌های این پروژه را بی آزمودن نمی‌توان به جمعیت‌های دیگر گسترش داد.
(ب) ‏۶۳ شاهد + ۴۷ آدنوم پیشرفته + ۴۶ سرطان = **۱۵۶**، برابر با شمار BioSampleهای runinfo. ‏`QueryKey` این بار **۲** است، چون همان WebEnv فهرست شماره‌ی ۱ (runها) را از پیش داشت.

---

## پاسخ ۳: run جفت، بی دانلود

<div dir="ltr">

```bash
mkdir -p ex3 && cd ex3
fastq-dump -X 3 --split-files ERR688506
ls -la
head -2 ERR688506_1.fastq | cut -c1-80
head -2 ERR688506_2.fastq | cut -c1-80
cd ..
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
Read 3 spots for ERR688506
Written 3 spots for ERR688506
-rw-rw-r-- 1 ubuntu ubuntu  748 Oct 27 14:35 ERR688506_1.fastq
-rw-rw-r-- 1 ubuntu ubuntu  844 Oct 27 14:35 ERR688506_2.fastq
@ERR688506.1 FCD1R36ACXX:8:1101:1395:1997#CGAATCAT length=46
CGCGGCGCCGCGGAAAGATACGCTAAACAAGCCCGAACGCAAGCCC
@ERR688506.1 FCD1R36ACXX:8:1101:1395:1997#CGAATCAT length=46
GGCGCGCATCGACGGCACACCTCACCGGGTTCATGGCCAAGGAGAG
```

</div>

(الف) **دو** فایل: هر spot جفت دو رید دارد؛ `--split-files` رید نخست را در `_1` و رید دوم را در `_2` می‌گذارد. سه spot = سه رید در هر فایل.
(ب) نام spot یکی است (`ERR688506.1`) و نام اصلی دستگاه هم (`FCD1R36ACXX:8:1101:1395:1997`: سلول جریان، lane، کاشی و مختصات x و y خوشه). دو رید از **یک خوشه** روی سلول جریان آمده‌اند، از دو سر یک تکه‌ی DNA. ابزارهای هم‌ردیفی (بخش ۰۶) جفت‌ها را با **ترتیب یکسان** در دو فایل می‌شناسند؛ هرگز یکی از دو فایل را جدا پالایش یا مرتب نکنید.

---

## پاسخ ۴: حجم FASTQ را پیش‌بینی کنید

از درس: FASTQ ‏`ERR688359` = ‏۳۶۴٬۴۷۶٬۸۴۶ بایت؛ ستون `bases` = ‏۱۰۲٬۸۷۴٬۴۱۲.

<div dir="ltr">

```bash
awk 'BEGIN{b=364476846/102874412; printf "bytes per base: %.2f\n", b; printf "ERR688506 FASTQ: %.1f GB\n", 6094123641*b/1e9}'
df -h . | tail -1
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
bytes per base: 3.54
ERR688506 FASTQ: 21.6 GB
/dev/nvme1n1p2  937G  678G  212G  77% /
```

</div>

(الف) ‏**۳٫۵۴** بایت برای هر باز: یک بایت برای خود باز، یک بایت برای کیفیتش، و بقیه برای دو سرخط (که در نسخه‌ی NCBI در سطر `+` تکرار می‌شود) و نویسه‌های پایان سطر. ریدهای کوتاه‌تر سهم سرخط را بالاتر می‌برند.
(ب) نزدیک به **۲۱٫۶ گیگابایت** برای یک نمونه، در برابر ۴٫۶ گیگابایت SRA. سرور دوره ۲۱۲ گیگابایت جای خالی دارد: کمتر از ۱۰ نمونه‌ی جفت بازشده. پس FASTQها را پس از ساختن `gzip` کنید، یا ابزار بعدی را مستقیم روی لوله (`fastq-dump -Z`) بگذارید.

---

## پاسخ ۵: سنجش با ENA

<div dir="ltr">

```bash
curl -s https://ftp.sra.ebi.ac.uk/vol1/fastq/ERR688/ERR688359/ERR688359.fastq.gz | zcat 2>/dev/null | head -4 > ena_first.fq
cat ena_first.fq
[ "$(sed -n 2p ena_first.fq)" = "$(sed -n 2p ERR688359.fastq)" ] && echo SAME-SEQ
[ "$(sed -n 4p ena_first.fq)" = "$(sed -n 4p ERR688359.fastq)" ] && echo SAME-QUAL
```

</div>

‏`head -4` پس از چهار سطر لوله را می‌بندد و `curl` دیگر دانلود نمی‌کند؛ `2>/dev/null` پیام `zcat` درباره‌ی بسته شدن لوله را پنهان می‌کند.

**خروجی واقعی:**

<div dir="ltr">

```
@ERR688359.1 FCD1R36ACXX:8:1101:13034:1994#TGAATCAT/1
AGAAGAACGCGATCTTAACTTCACTCTGAACAAGAACGGAGAAATATTACGTTTTAAAATCACCAACTGCCCCCTCGCAGACCTCAAATATGCCAA
+
DFEFHGGHDGIHGIIIJJJJJIIIJJIIIJJIJIJJJIGIIGIGGHIGIJJ@EHFHHHFFFEF>CBDACCDBDBDDDDDDBDBDDCCCADEDDDDD
SAME-SEQ
SAME-QUAL
```

</div>

(الف) بله، توالی و کیفیت **یکسان‌اند** (و شمار ریدها هم، گام ۵ درس).
(ب) ‏ENA: ‏`/1` در پایان سرخط و سطر `+` تهی. NCBI: ‏`length=96` و سرخط تکراری پس از `+`. بیشتر ابزارها (fastp، FastQC، هم‌ردیف‌کننده‌ها) سرخط را تنها نام می‌دانند و فرقی نمی‌بینند؛ ولی ابزارهای قدیمی که جفت‌ها را با `/1` و `/2` می‌شناسند، یا اسکریپت‌هایی که سطر `+` را تهی می‌پندارند، ممکن است بشکنند. درس: **پیش از ادغام داده از دو منبع، سرخط‌ها را ببینید.**

---

## پاسخ ۶ (حسابی): کل پروژه

<div dir="ltr">

```bash
awk 'BEGIN{s=595177e6/280e3; printf "download: %.1f days\n", s/86400; printf "FASTQ: %.1f TB\n", 595177e6*3.6/1e12}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
download: 24.6 days
FASTQ: 2.1 TB
```

</div>

(الف) نزدیک به **۲۵ روز** دانلود پیوسته.
(ب) نزدیک به **۲٫۱ ترابایت** FASTQ بازشده (۳٫۶ برابر حجم SRA، مانند `ERR688359`)، ده برابر جای خالی سرور. پس یا محاسبه را در ابر نزدیک به داده انجام دهید، یا تنها زیرمجموعه‌ای از نمونه‌ها را بگیرید، یا هر نمونه را پس از تحلیل پاک کنید.

---

## پاسخ ۷ (اندیشیدنی): برنامه‌ی کار

1. **فراداده:** همه‌ی BioSampleها را بگیرید (پاسخ ۲) و جدولی از `BioSample`، گروه (Title)، و runهای هر نمونه (ستون ۲۶ runinfo) بسازید؛ ۶۳ شاهد و ۴۶ سرطان.
2. **حجم و جا:** با runinfo حجم این ۱۰۹ نمونه را جمع بزنید، با سرعت دانلود و `df -h` بسنجید (پاسخ‌های ۴ و ۶)، و دو نمونه‌ی کوچک را برای آزمون گردش کار برگزینید.
3. **آزمون گردش کار:** همه‌ی گام‌ها (دانلود، `vdb-validate`، `fasterq-dump`، کنترل کیفیت با fastp از بخش ۰۶، شمارش ریدها) را روی آن دو نمونه اجرا کنید، سپس تنها گام‌های سنگین را روی بقیه (بخش ۲۰: Snakemake/Nextflow).

‏**runهای SINGLE را نگه دارید**، ولی جدا: آن‌ها ریدهای همان نمونه‌اند که جفتشان دور ریخته شده؛ دور ریختنشان اطلاعات را کم می‌کند و چون برای همه‌ی نمونه‌ها هست، سوگیری میان گروه‌ها نمی‌سازد. ابزارهای متاژنوم (بخش ۱۸) ریدهای جفت و تک را با هم می‌پذیرند.

---

## برای خواندن بیشتر

- ‏Feng Q, et al. (2015). *Gut microbiome development along the colorectal adenoma–carcinoma sequence.* Nat Commun 6:6528. https://doi.org/10.1038/ncomms7528
- ‏SRA Toolkit wiki، بخش «fasterq-dump»: https://github.com/ncbi/sra-tools/wiki
- ‏YouTube: *NCBI's Sequence Read Archive: Downloading sequences* (Dranalytics): https://www.youtube.com/watch?v=evlIjjlIUBA

</div>
