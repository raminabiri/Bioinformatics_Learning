<div dir="rtl">

# پاسخ تشریحی: مرورگر ژنوم UCSC

همه‌ی خروجی‌ها واقعی‌اند (UCSC API، liftOver 502 و Ensembl REST، روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: رونوشت MANE ژن FKBP5

<div dir="ltr">

```bash
grep FKBP5 dex_hg38.bed
curl -sS "$U/getData/track?genome=hg38;track=mane;chrom=chr6;start=35572944;end=35728622" > fkbp5_mane.json
jq -c '.mane[] | {name, geneName2, strand, chromStart, chromEnd, thickStart, thickEnd, blockCount}' fkbp5_mane.json
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
chr6	35572944	35728622	FKBP5	0	-
{"name":"ENST00000357266.9","geneName2":"FKBP5","strand":"-","chromStart":35573589,"chromEnd":35688915,"thickStart":35575834,"thickEnd":35642824,"blockCount":11}
```

</div>

(الف) ‏`ENST00000357266.9`، رشته‌ی منفی، از 35573589 تا 35688915 (0-based)، CDS از 35575834 تا 35642824، **۱۱** اگزون.

(ب) ‏1-based: ‏35573589 + 1 = **35573590**. با Ensembl:

<div dir="ltr">

```bash
curl -sS "https://rest.ensembl.org/lookup/id/ENST00000357266?content-type=application/json" | jq -c '{id, start, end, length, strand}'
```

</div>

<div dir="ltr">

```
{"id":"ENST00000357266","start":35573590,"end":35688915,"length":3750,"strand":-1}
```

</div>

یکسان. ✅ (‏`length` ‏۳۷۵۰ را در تمرین ۲ به کار می‌بریم.) یادداشت: رونوشت MANE تا 35688915 می‌رود، ولی **ژن** FKBP5 در `dex_hg38.bed` تا 35728622؛ رونوشت‌های دیگری ۴۰ کیلوباز دورتر آغاز می‌شوند.

---

## پاسخ ۲: اگزون‌ها به BED

<div dir="ltr">

```bash
jq -c '.mane[0] | {chromStart, chromStarts, blockSizes}' fkbp5_mane.json
jq -r '.mane[0] | [.chrom, .chromStart, .chromStarts, .blockSizes, .strand] | @tsv' fkbp5_mane.json \
 | awk -F'\t' 'BEGIN {OFS = "\t"} {n = split($3, st, ","); split($4, sz, ",");
     for (i = 1; i < n; i++) { e = ($5 == "-") ? n - i : i; print $1, $2 + st[i], $2 + st[i] + sz[i], "exon" e, 0, $5 } }' > fkbp5_exons.bed
cat fkbp5_exons.bed
awk '{s += $3 - $2} END {print "exon bases:", s}' fkbp5_exons.bed
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`n = split($3, st, ",")` | رشته‌ی `0,3404,…,` را در `,` بشکن و در آرایه‌ی `st` بگذار؛ `n` شمار تکه‌ها (۱۲؛ چون `,` پایانی یک تکه‌ی تهی می‌سازد) |
| ‏`for (i = 1; i < n; i++)` | تکه‌های ۱ تا ۱۱، بی تکه‌ی تهی پایانی |
| ‏`$2 + st[i]` | ‏`chromStarts` نسبی است؛ آن را با `chromStart` جمع کن |
| ‏`e = ($5 == "-") ? n - i : i` | روی رشته‌ی منفی شماره‌ی اگزون را وارونه کن |
| ‏`s += $3 - $2` | درازای هر اگزون را جمع بزن |

**خروجی واقعی:**

<div dir="ltr">

```
{"chromStart":35573589,"chromStarts":"0,3404,6446,13444,17540,23658,45506,46542,63424,69130,115214,","blockSizes":"2353,240,186,84,91,157,115,143,145,124,112,"}
chr6	35573589	35575942	exon11	0	-
chr6	35576993	35577233	exon10	0	-
chr6	35580035	35580221	exon9	0	-
chr6	35587033	35587117	exon8	0	-
chr6	35591129	35591220	exon7	0	-
chr6	35597247	35597404	exon6	0	-
chr6	35619095	35619210	exon5	0	-
chr6	35620131	35620274	exon4	0	-
chr6	35637013	35637158	exon3	0	-
chr6	35642719	35642843	exon2	0	-
chr6	35688803	35688915	exon1	0	-
exon bases: 3750
```

</div>

(الف) اگزون ۱: ‏`chr6 35688803 35688915` (۱۱۲ باز، سر بزرگ). اگزون ۱۱: ‏`chr6 35573589 35575942` (۲۳۵۳ باز؛ بیشترش 3′ UTR).
(ب) ‏**۳۷۵۰** باز = درازای mRNA بالغ (بی اینترون)، درست همان `length` ‏Ensembl در تمرین ۱. ✅ ژن ۱۱۵ کیلوباز است و mRNA تنها ۳٫۷ کیلوباز: بیش از ۹۶٪ رونوشت اولیه اینترون است.
(ج) کدون آغاز در `thickEnd` ‏(35642824) است و این عدد در **اگزون ۲** (35642719 تا 35642843) می‌افتد. پس اگزون ۱ **همه‌اش 5′ UTR** است و ترجمه از اگزون ۲ آغاز می‌شود.

**اشتباه رایج:** شماره‌گذاری اگزون از چپ به راست روی رشته‌ی منفی. اگزون «۱» همیشه سر **5′** رونوشت است.

---

## پاسخ ۳: کدون آغاز و پایان FKBP5

<div dir="ltr">

```bash
ts=$(jq -r '.mane[0].thickStart' fkbp5_mane.json); te=$(jq -r '.mane[0].thickEnd' fkbp5_mane.json)
echo "thick $ts $te"
curl -sS "$U/getData/sequence?genome=hg38;chrom=chr6;start=$((te - 3));end=$te" | jq -r .dna | rev | tr ACGT TGCA
curl -sS "$U/getData/sequence?genome=hg38;chrom=chr6;start=$ts;end=$((ts + 3))" | jq -r .dna | rev | tr ACGT TGCA
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
thick 35575834 35642824
ATG
TGA
```

</div>

‏`$((te - 3))` حساب عددی پوسته است (01/09). آغاز **ATG** و پایان **TGA**. ✅ هر دو تنها پس از مکمل وارونه دیده می‌شوند، چون API رشته‌ی مثبت را می‌دهد.

---

## پاسخ ۴: هشت ژن، دو اسمبلی

<div dir="ltr">

```bash
paste <(awk '{print $4, $3 - $2}' dex_hg38.bed) <(awk '{print $4, $3 - $2}' dex_hg19.bed)
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ZBTB16 198431	ZBTB16 198431
CRISPLD2 100794	CRISPLD2 100794
PER1 16040	PER1 16040
KLF15 14828	KLF15 14828
NR3C1 157582	NR3C1 157582
DUSP1 4207	DUSP1 4207
FKBP5 155678	FKBP5 155678
TSC22D3 64122	TSC22D3 64122
```

</div>

‏`<( … )` خروجی یک دستور را چون یک فایل به دستور دیگر می‌دهد، تا `paste` دو جدول را کنار هم بگذارد.

(الف) **هیچ** فرقی نیست. درون این ژن‌ها توالی میان دو اسمبلی عوض نشده است؛ تنها جایشان روی کروموزوم.
(ب) ‏143277930 − 142657495 = **۶۲۰٬۴۳۵** باز. نه، با ۳۵۹٬۹۴۶ ‏F508del یکی نیست، چون CFTR روی کروموزوم **دیگری** (۷) است. جابه‌جایی میان دو اسمبلی برای هر ناحیه جداست: هر جا که در hg38 شکافی پر یا تکه‌ای افزوده شد، شماره‌های پس از آن جابه‌جا شدند. پس **نمی‌توان** یک عدد ثابت را به همه‌ی کروموزوم افزود؛ کار liftOver همین است.

---

## پاسخ ۵: سه ناحیه‌ی دشوار

<div dir="ltr">

```bash
liftOver $P/02_UCSC_Genome_Browser/data/lift_test_hg19.bed hg19ToHg38.over.chain.gz lt.bed lt_un.txt
cat lt.bed; echo "-- unmapped"; cat lt_un.txt
liftOver -minMatch=0.5 $P/02_UCSC_Genome_Browser/data/lift_test_hg19.bed hg19ToHg38.over.chain.gz lt5.bed lt5_un.txt 2> /dev/null
cat lt5.bed; echo "-- unmapped"; cat lt5_un.txt
curl -sS "$U/getData/sequence?genome=hg19;chrom=chr1;start=6793;end=7793" | jq -r .dna | tr -d 'N' | wc -c
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
Reading liftover chains
Mapping coordinates
chr4_GL000008v2_random	13832	14832	w190_moved
-- unmapped
#Deleted in new
chr1	6793	7793	w18_gap
#Split in new
chr1	148683284	148684284	w210_split
chr4_GL000008v2_random	13832	14832	w190_moved
chr1	144333723	144334385	w210_split
-- unmapped
#Deleted in new
chr1	6793	7793	w18_gap
0
```

</div>

(الف)
- ‏**w18_gap:** ‏Deleted. توالی hg19 آن **صفر** باز غیر `N` دارد: ۱۰ کیلوباز نخست کروموزوم ۱ در hg19 شکاف است (تلومر). چیزی برای جابه‌جایی نیست.
- ‏**w190_moved:** جابه‌جا شد، ولی به `chr4_GL000008v2_random`. در hg19 این توالی کنار سانترومر کروموزوم ۱ گذاشته شده بود؛ در hg38 روی تکه‌ای است که به کروموزوم ۴ نسبت داده شده ولی جای دقیقش روشن نیست. پاسخ «درست» است، ولی اگر تنها کروموزوم‌های اصلی را نگه دارید، از دست می‌رود.
- ‏**w210_split:** ‏Split. بازه در hg38 تکه‌تکه شده است و با minMatch ‏۰٫۹۵ پذیرفته نمی‌شود.

(ب) با `-minMatch=0.5` پنجره‌ی split به `chr1:144333723-144334385` رفت: **۶۶۲** باز از ۱۰۰۰. یعنی تنها تکه‌ی بزرگ‌تر جابه‌جا شد و ۳۳۸ باز دیگر جای دیگری‌اند یا نیستند. برای یک **SNP** درون آن تکه پذیرفتنی است؛ برای یک **ناحیه** (پیک، اگزون) نه، چون بازه‌ی hg38 دیگر همان ناحیه‌ی hg19 نیست. بهتر است پنجره را **کوچک‌تر** کنید (برای نمونه، تنها نقطه‌ی میانی پیک را جابه‌جا کنید) تا minMatch را پایین بیاورید.

---

## پاسخ ۶ (فکری): ‏chain نادرست

(الف) liftOver تنها می‌پرسد «آیا این بازه در اسمبلی مبدأ chain هم‌ترازی دارد؟». مختصات hg38 هم بیشترشان در hg19 جای «معناداری» دارند، چون دو اسمبلی بیشتر یکسان‌اند و تنها شماره‌ها کمی جابه‌جا شده‌اند. پس liftOver آن‌ها را بی‌خطا به جای **نادرست** می‌برد. در درس همین را دیدیم: هر هشت ژن hg38 با chain ‏hg19ToHg38 «جابه‌جا» شدند و NR3C1 ‏۶۲۰ کیلوباز دورتر افتاد، بی هیچ سطر unmapped.

(ب) دو راه:
1. **یک نقطه‌ی شناخته‌شده:** اگر فایل ژن یا واریانت شناخته‌شده‌ای دارد (برای نمونه F508del یا NR3C1)، مختصاتش را با پاسخ معلوم دو اسمبلی بسنجید: `grep NR3C1 peaks.bed`. آغاز 143277930 یعنی hg38، و 142657495 یعنی hg19.
2. **توالی:** چند سطر را با `getData/sequence` در **هر دو** اسمبلی بگیرید و با توالی‌ای که همکار گزارش کرده (یا با الگوی مورد انتظار، مانند موتیف پیک) بسنجید. در اسمبلی درست توالی جور است. ترک‌های `chr` بی‌همتا هم نشانه‌اند: `chrUn_…v1` و `_alt` با این نام‌ها تنها در hg38 هستند.

---

## پاسخ ۷: ‏CFTR در دو اسمبلی

<div dir="ltr">

```bash
for g in hg19 hg38; do
  printf "%s\t" $g
  curl -sS "$U/search?search=CFTR&genome=$g" \
    | jq -r '.positionMatches[] | select(.trackName == "ncbiRefSeqCurated") | [(.matches | length), .matches[0].position] | @tsv'
done
echo $((117542521 - 117182575))
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
hg19	2	chr7:117182575-117204730
hg38	3	chr7:117542521-117564676
359946
```

</div>

(الف) نخستین پاسخ ترک RefSeq در hg19 از 117182575 و در hg38 از 117542521 آغاز می‌شود: **۳۵۹٬۹۴۶** باز، درست همان فاصله‌ی F508del. در این ناحیه‌ی کوچک (چند ده کیلوباز) هیچ تغییری میان دو اسمبلی نبوده، پس همه‌ی بازها همان اندازه جابه‌جا شده‌اند. (نخستین پاسخ هر دو یک رونوشت کوتاه است، نه کل ژن؛ برای مقایسه همین بس است چون از یک رکورد است.)

(ب) ✍️ ابزار **View ← In Other Genomes (Convert)** برای `chr7:117559580-117559602` ‏(hg38) در hg19 ناحیه‌ی **`chr7:117199634-117199656`** را می‌دهد. ما همین را با liftOver سنجیدیم:

<div dir="ltr">

```bash
printf "chr7\t117559579\t117559602\tregion\n" > r.bed
liftOver r.bed hg38ToHg19.over.chain.gz r19.bed r_un.txt 2> /dev/null; cat r19.bed
```

</div>

<div dir="ltr">

```
chr7	117199633	117199656	region
```

</div>

‏117199633 (0-based) = 117199634 (1-based): همان ناحیه‌ی تصویر hg19 درس. ✅ ابزار Convert همان chainهای liftOver را به کار می‌برد.

</div>
