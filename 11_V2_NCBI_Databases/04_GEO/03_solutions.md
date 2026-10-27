<div dir="rtl">

# پاسخ تشریحی: GEO

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0، Python 3 با pandas 2.3.3، EDirect 24.0؛ روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: دستگاه (GPL)

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=gds&id=100011154&version=2.0" | grep -oE '<(Accession|title|taxon|gdsType|n_samples)>[^<]*' | head -5
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
<Accession>GPL11154
<title>Illumina HiSeq 2000 (Homo sapiens)
<taxon>Homo sapiens
<gdsType>
<n_samples>195101
```

</div>

(الف) ‏**Illumina HiSeq 2000**، انسان. در GEO هر دستگاه برای هر جاندار یک GPL جدا دارد (HiSeq 2000 برای موش GPL دیگری است).
(ب) ‏**۱۹۵٬۱۰۱** نمونه‌ی انسانی در GEO روی همین دستگاه ثبت شده است. ‏`gdsType` برای GPL تهی است، چون گونه‌ی آزمایش ویژگی GSE است، نه دستگاه.

---

## پاسخ ۲: آلبوترول

<div dir="ltr">

```bash
python3 $P/04_GEO/scripts/geo_counts.py GSE52778_series_matrix.txt.gz counts.tsv.gz Albuterol Untreated 2289 1843 | sed -n '/selected/,$p'
esummary -db gene -id 91584,286133,26112 | xtract -pattern DocumentSummary -element Id Name Description | cut -c1-80
```

</div>

‏`sed -n '/selected/,$p'` از سطری که «selected» دارد تا پایان را چاپ می‌کند (جدول نمونه‌ها را که در درس دیدید کنار می‌گذارد).

**خروجی واقعی:**

<div dir="ltr">

```
selected genes (Albuterol vs Untreated):
        mean_cpm_Untreated  mean_cpm_Albuterol  mean_log2FC  lines_up
GeneID
2289                  15.1               100.9         1.65         4
1843                  36.9               119.5         1.10         2

top 10 up among 11520 genes with control CPM >= 5:
        mean_cpm_Untreated  mean_cpm_Albuterol  mean_log2FC  lines_up
GeneID
5187                   7.3                37.5         1.88         4
12                    23.1               134.5         1.69         4
2289                  15.1               100.9         1.65         4
4128                  20.6               107.9         1.57         3
25939                 82.7               416.0         1.56         2
91584                  9.3                44.3         1.52         3
286133                 9.2                44.5         1.51         4
730                   18.0                99.8         1.42         2
26112                 22.0                80.0         1.35         4
783                    5.4                20.8         1.31         4

26112	CCDC69	coiled-coil domain containing 69
91584	PLXNA4	plexin A4
286133	SCARA5	scavenger receptor class A member 5
```

</div>

(الف) ‏FKBP5 با آلبوترول هم بالا رفت (log2FC ‏۱٫۶۵، **هر ۴** فرد) ولی بسیار کمتر از دگزامتازون (۳٫۸۴). ‏DUSP1 ‏۱٫۱۰ ولی **تنها در ۲ فرد**: میانگین را یکی دو فرد بالا برده‌اند.
(ب) بیشترین log2FC آلبوترول **۱٫۸۸** (PER1) است، در برابر **۵٫۸۸** (ZBTB16) و ۳٫۸۴ (FKBP5) برای دگزامتازون: اثر آلبوترول بر رونویسی در این سلول‌ها بسیار کمتر است. ‏`lines_up` ‏۲ یا ۳ برای چند ژن (SAMHD1، C7) یعنی اثر **ناپایدار** است. PER1 هم ژن پاسخ به cAMP است، و آلبوترول (آگونیست گیرنده‌ی β2) cAMP را بالا می‌برد؛ پس بالا رفتن PER1 زیستی معنادار است.

---

## پاسخ ۳: هر دو دارو با هم

<div dir="ltr">

```bash
python3 $P/04_GEO/scripts/geo_counts.py GSE52778_series_matrix.txt.gz counts.tsv.gz \
    Albuterol_Dexamethasone Dexamethasone 2289 5187 1843 | sed -n '/selected/,/^$/p'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
selected genes (Albuterol_Dexamethasone vs Dexamethasone):
        mean_cpm_Dexamethasone  mean_cpm_Albuterol_Dexamethasone  mean_log2FC  lines_up
GeneID
2289                     217.3                             158.3        -1.06         2
5187                      63.8                              45.4        -0.72         1
1843                     270.9                             144.1        -1.23         0
```

</div>

(الف) نه. میانگین CPM هر سه ژن در تیمار ترکیبی **کمتر** از تنها دگزامتازون است.
(ب) ولی `lines_up` برای FKBP5 ‏۲ از ۴ است: در دو فرد بالا و در دو فرد پایین رفته؛ میانگین ‏−۱٫۰۶ را یک یا دو فرد ساخته‌اند. تنها DUSP1 در هر ۴ فرد پایین آمده (`lines_up` = ۰). با ۴ فرد و بی آمار، تنها می‌توان گفت «افزودن آلبوترول پاسخ این ژن‌ها را بیشتر نکرد». این‌که کمترش کرد یا نه، پرسشی برای DESeq2 در بخش ۱۳ است.

---

## پاسخ ۴: اندازه‌ی کتابخانه

از خروجی درس: بزرگ‌ترین **GSM1275867** (‏N052611_Dex، ‏۳۹٫۱ میلیون) و کوچک‌ترین **GSM1275863** (‏N61311_Dex، ‏۱۹٫۲ میلیون).

<div dir="ltr">

```bash
awk 'BEGIN{printf "%.2f\n", 39.1/19.2}'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
2.04
```

</div>

(الف) نسبت **۲٫۰۴**.
(ب) در N052611 کتابخانه‌ی بی‌تیمار ۲۶٫۱ و کتابخانه‌ی دگزامتازون ۳۹٫۱ میلیون است (۱٫۵ برابر). با شمار خام، هر ژنی در نمونه‌ی دگزامتازون حدود ۱٫۵ برابر (log2 ≈ ‏۰٫۵۸) «بالاتر» دیده می‌شد، حتی ژنی که هیچ دگرگون نشده. برای FKBP5 که ۱۴ برابر بالا رفته فرق کوچکی است، ولی برای ژن‌هایی با اثر کم (مانند پاسخ ۳) کل نتیجه را می‌سازد.

---

## پاسخ ۵: آزمایش‌های دیگر دگزامتازون در GEO

<div dir="ltr">

```bash
for t in 'dexamethasone AND "Homo sapiens"[porgn] AND gse[ETYP]' \
         'dexamethasone AND "Homo sapiens"[porgn] AND gse[ETYP] AND "expression profiling by high throughput sequencing"[gdsType]' \
         'gds[ETYP]' 'gds[ETYP] AND dexamethasone'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=gds --data-urlencode "term=$t" \
          | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)  $t"
  sleep 0.4
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
1796  dexamethasone AND "Homo sapiens"[porgn] AND gse[ETYP]
749  dexamethasone AND "Homo sapiens"[porgn] AND gse[ETYP] AND "expression profiling by high throughput sequencing"[gdsType]
4348  gds[ETYP]
38  gds[ETYP] AND dexamethasone
```

</div>

(الف) ‏**۱۷۹۶** GSE انسانی، و **۷۴۹** تای آن‌ها RNA-seq. ‏(همه‌ی آن‌ها آزمایش دگزامتازون نیستند: «dexamethasone» در هر جای شرح جست‌وجو شد؛ بسیاری تنها آن را در محیط کشت به کار برده‌اند.)
(ب) ‏GEO روی هم تنها **۴۳۴۸** GDS دارد، و ۳۸ تا درباره‌ی دگزامتازون. در برابر صدها هزار GSE، این شمار بسیار کم است: GDS را ویراستاران GEO دستی می‌ساختند و ساختنش سال‌هاست ادامه ندارد. پس برای داده‌ی تازه همیشه با GSE کار می‌کنید.

---

## پاسخ ۶: ‏ERCC در کدام نمونه‌ها؟

<div dir="ltr">

```python
import gzip
t = e = None
for l in gzip.open('GSE52778_series_matrix.txt.gz', 'rt'):
    if l.startswith('!Sample_title'):
        t = [x.strip('"') for x in l.rstrip('\n').split('\t')[1:]]
    if 'ercc_mix' in l:
        e = [x.strip('"') for x in l.rstrip('\n').split('\t')[1:]]
for a, b in zip(t, e):
    print(a, b)
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
N61311_untreated ercc_mix: -
N61311_Dex ercc_mix: -
N61311_Alb ercc_mix: -
N61311_Alb_Dex ercc_mix: -
N052611_untreated ercc_mix: -
N052611_Dex ercc_mix: 1
N052611_Alb ercc_mix: 1
N052611_Alb_Dex ercc_mix: 1
N080611_untreated ercc_mix: -
N080611_Dex ercc_mix: -
N080611_Alb ercc_mix: -
N080611_Alb_Dex ercc_mix: -
N061011_untreated ercc_mix: 1
N061011_Dex ercc_mix: 1
N061011_Alb ercc_mix: 1
N061011_Alb_Dex ercc_mix: 1
```

</div>

(الف) **۷** نمونه: سه نمونه‌ی تیمارشده‌ی N052611 و هر چهار نمونه‌ی N061011.
(ب) **نامتوازن** است: نمونه‌ی بی‌تیمار N052611 ERCC ندارد ولی سه تیمار همان فرد دارند؛ دو فرد اصلاً ندارند. اگر نرمال‌سازی را بر پایه‌ی ERCC بسازید، برای نیمی از نمونه‌ها شدنی نیست، و در N052611 شاهد و تیمار با دو روش جدا نرمال می‌شوند: فرق روش با اثر دارو قاطی می‌شود. پس در این آزمایش ERCC را تنها برای سنجش کیفیت به کار ببرید، نه نرمال‌سازی. (ریدهای ERCC در جدول شمارش NCBI نیستند، چون NCBI تنها ژن‌های انسانی را شمرده است.)

---

## پاسخ ۷ (اندیشیدنی): گزارش یک یافته

ایرادها:
1. ‏**«p < 0.05» از کجا آمده؟** اسکریپت هیچ آزمون آماری ندارد؛ تنها میانگین log2FC است.
2. ‏**«۱۲ برابر»**: میانگین CPM از ۸۲٫۷ به ۱۱۳۲٫۶ نزدیک به ۱۳٫۷ برابر است، ولی میانگین log2FC جفتی ۳٫۶۷ است (۲^۳٫۶۷ ≈ ‏۱۲٫۷). دو عدد گوناگون از دو روش؛ باید گفت کدام است.
3. **ثبات میان افراد گفته نشده:** ‏SAMHD1 در هر ۴ فرد با دگزامتازون بالا رفت (`lines_up` = ۴)، که باید گفته شود؛ و هیچ اشاره‌ای به نرمال‌سازی (CPM) و اندازه‌ی نمونه (۴ فرد) نیست.

جمله‌ی درست: «در داده‌ی GSE52778 (شمارش‌های NCBI، ۴ فرد)، بیان SAMHD1 با دگزامتازون در هر ۴ فرد بالا رفت (میانگین log2FC جفتی بر پایه‌ی CPM ‏= ۳٫۶۷). این یک نگاه توصیفی است؛ آزمون آماری با DESeq2 در گام بعد.»

---

## برای خواندن بیشتر

- ‏Himes BE, et al. (2014). PLoS ONE 9:e99625 (جدول ژن‌های پاسخ‌دهنده). https://doi.org/10.1371/journal.pone.0099625
- راهنمای DESeq2 (داده‌ی airway، همین آزمایش): https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html
- ‏YouTube: *Use GEO2R to Analyze Data in GEO* (NLM): https://www.youtube.com/watch?v=9RyWjzSnaE0

</div>
