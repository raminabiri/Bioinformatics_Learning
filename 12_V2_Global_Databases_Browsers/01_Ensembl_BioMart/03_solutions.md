<div dir="rtl">

# پاسخ تشریحی: Ensembl و BioMart

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0، jq و Python 3، روی سرور دوره، 2026-10-27، Ensembl release 116). چند درخواست پیش از پاسخ 200 یک یا چند بار 500 یا 503 گرفتند و دوباره زده شدند.

---

## پاسخ ۱: ژن CFTR در Ensembl

<div dir="ltr">

```bash
curl -sS "$R/lookup/symbol/homo_sapiens/CFTR?expand=1;$J" > cftr.json
jq '{id, version, seq_region_name, start, end, strand, canonical_transcript}' cftr.json
jq '.Transcript | length' cftr.json
jq -r '.Transcript[].biotype' cftr.json | sort | uniq -c
jq -r '.Transcript[] | select(.is_canonical == 1) | [.id, .length, .Translation.id, .Translation.length] | @tsv' cftr.json
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
{
  "id": "ENSG00000001626",
  "version": 20,
  "seq_region_name": "7",
  "start": 117287120,
  "end": 117715971,
  "strand": 1,
  "canonical_transcript": "ENST00000003084.11"
}
45
     11 nonsense_mediated_decay
     21 protein_coding
     11 protein_coding_CDS_not_defined
      2 retained_intron
ENST00000003084	6070	ENSP00000003084	1480
```

</div>

(الف) ‏`ENSG00000001626.20`، کروموزوم ۷، از 117287120 تا 117715971، رشته‌ی **مثبت** (برخلاف NR3C1).
(ب) ‏۴۵ رونوشت: ۲۱ کدکننده، ۱۱ ‏NMD، ۱۱ بی CDS روشن و ۲ ‏**retained intron** (رونوشتی که یک اینترون را نگه داشته؛ در بسیاری از موارد پروتئین نمی‌سازد).
(ج) **۱۴۸۰** اسید آمینه، همان طول شناخته‌شده‌ی CFTR. ✅ جهش F508del (11/05) اسید آمینه‌ی ۵۰۸ همین پروتئین را برمی‌دارد.

**اشتباه رایج:** شمردن همه‌ی رونوشت‌ها به جای پروتئین‌ها. تنها ۲۱ رونوشت از ۴۵ تا پروتئین کامل می‌سازند.

---

## پاسخ ۲: رونوشت MANE هشت ژن

<div dir="ltr">

```bash
cp $P/01_Ensembl_BioMart/data/dex_mane.xml .
curl -sS -G --data-urlencode "query@dex_mane.xml" $M > mane.tsv
awk -F'\t' 'NR > 1 && $3 != ""' mane.tsv | sort
cut -f1,8 dex_ids.tsv | tail -n +2 | sort
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
CRISPLD2	ENST00000262424	NM_031476.4
DUSP1	ENST00000239223	NM_004417.4
FKBP5	ENST00000357266	NM_004117.4
KLF15	ENST00000296233	NM_014079.4
NR3C1	ENST00000394464	NM_000176.3
PER1	ENST00000317276	NM_002616.3
TSC22D3	ENST00000372383	NM_198057.3
ZBTB16	ENST00000335953	NM_006006.6

CRISPLD2	ENST00000262424.10
DUSP1	ENST00000239223.4
FKBP5	ENST00000357266.9
GILZ	-
KLF15	ENST00000296233.4
NR3C1	ENST00000394464.7
PER1	ENST00000317276.9
TSC22D3	ENST00000372383.9
ZBTB16	ENST00000335953.9
```

</div>

**تکه‌به‌تکه:** ‏`NR > 1` سرخط را کنار می‌گذارد و `$3 != ""` رونوشت‌های بی MANE را. هر ژن ده‌ها رونوشت دارد، ولی تنها **یکی** MANE Select است.

(الف) هشت جفت بالا؛ برای نمونه FKBP5: ‏`ENST00000357266` = `NM_004117.4`.
(ب) **بله.** شناسه‌ها (بی نسخه) در هر دو فهرست یکی‌اند. در انسان، Ensembl رونوشت MANE Select را canonical می‌گذارد. (‏BioMart شناسه را بی نسخه می‌دهد و REST با نسخه؛ پیش از سنجش با چشم یا `join`، نسخه را بردارید.)

---

## پاسخ ۳: ارتولوگ‌های FKBP5 در سه گونه

<div dir="ltr">

```bash
curl -sS "$R/homology/symbol/human/FKBP5?type=orthologues;target_species=mouse;target_species=danio_rerio;target_species=drosophila_melanogaster;sequence=none;$J" \
  | jq -r '.data[0].homologies[] | [.target.species, .target.id, .type, (.target.perc_id*10|round/10), (.source.perc_id*10|round/10)] | @tsv'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
mus_musculus	ENSMUSG00000024222	ortholog_one2one	87.3	87.1
drosophila_melanogaster	FBgn0013269	ortholog_one2many	13.2	10.3
danio_rerio	ENSDARG00000028396	ortholog_one2one	59.2	58.6
```

</div>

(الف) موش: یک‌به‌یک، ۸۷٪ یکسان. گورخرماهی: یک‌به‌یک، نزدیک به ۵۹٪. مگس سرکه: ‏`FBgn0013269`، ‏**one2many**، تنها ۱۰ تا ۱۳٪ یکسان. (شناسه‌ی مگس از FlyBase است، نه `ENS…`.)

(ب) ‏`one2many` یعنی «یک ژن در یک گونه، چند ژن در گونه‌ی دیگر». برای دیدن آن «چند»، پرسش را از سوی مگس بزنید. یک نکته: پرسش از سوی مگس به پایگاه مقایسه‌ی بی‌مهرگان می‌رود که انسان ندارد (پاسخ: `Could not find a GenomeDB named 'homo_sapiens'`)؛ با `compara=multi` آن را به پایگاه مهره‌داران می‌فرستیم:

<div dir="ltr">

```bash
curl -sS "$R/homology/id/drosophila_melanogaster/FBgn0013269?compara=multi;type=orthologues;target_species=homo_sapiens;sequence=none;$J" > fly_hs.json
for g in $(jq -r '.data[0].homologies[].target.id' fly_hs.json); do
  curl -sS "$R/lookup/id/$g?$J" | jq -r '[.id, .display_name] | @tsv'; sleep 1
done
curl -sS "$R/lookup/id/FBgn0013269?$J" | jq -r '[.display_name, .description] | @tsv'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ENSG00000162222	TTC9C
ENSG00000079150	FKBP7
ENSG00000105701	FKBP8
ENSG00000141756	FKBP10
ENSG00000096060	FKBP5
Fkbp39	FK506-binding protein 39kD
```

</div>

ژن مگس **Fkbp39** است و با **پنج** ژن انسانی جفت شده: FKBP5، FKBP7، FKBP8، FKBP10 و TTC9C. یعنی در دودمان مهره‌داران این خانواده با **دوبرابر شدن ژن** گسترش یافته و هر عضو راه خودش را رفته است؛ مگس یک نسخه دارد. یکسانی کم (۱۰ تا ۱۳٪) دو دلیل دارد: نزدیک به ۶۰۰ میلیون سال جدایی، و این‌که تنها **دامنه‌ی FKBP** مشترک است و بقیه‌ی دو پروتئین با هم هم‌تراز نمی‌شوند. پس «ارتولوگ» در گونه‌های دور یعنی خویشاوندی دودمانی، نه همانندی کارکرد: نتیجه‌ی آزمایش روی Fkbp39 مگس را نمی‌شود بی‌احتیاط به FKBP5 انسان برگرداند.

---

## پاسخ ۴: نام‌های قدیمی

<div dir="ltr">

```bash
for s in GILZ GR MKP-1; do
  printf "%s\t" $s
  curl -sS "$R/xrefs/symbol/homo_sapiens/$s?$J" | jq -c .
  sleep 1
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
GILZ	[{"id":"ENSG00000157514","type":"gene"}]
GR	[{"id":"ENSG00000113580","type":"gene"}]
MKP-1	[{"id":"ENSG00000120129","type":"gene"}]
```

</div>

(الف) با جدول گام ۵: ‏GILZ ← **TSC22D3**، ‏GR ← **NR3C1**، ‏MKP-1 ← **DUSP1**. هر سه همان نام‌هایی‌اند که در مقاله‌های گلوکوکورتیکوئید بیشتر می‌بینید.

(ب) چون یک نام دیگر می‌تواند به **چند** ژن برسد، یا به ژنی که شما نمی‌خواستید. این‌جا هر کدام یک پاسخ داشت، ولی نمادهای کوتاه (مانند `GR`) در گونه‌ها یا پایگاه‌های دیگر معنای دیگری دارند. در 11/01 هم `acrB[gene]` ژن gyrB را آورد. راه درست: اسکریپت نام‌های یافته‌نشده را گزارش کند (همان `NOT_FOUND`)، شما با `xrefs/symbol` بگردید و پاسخ را **با چشم** بپذیرید. اگر پاسخ بیش از یک `id` داشت، هر کدام را با `lookup/id` ببینید.

---

## پاسخ ۵: دو release، دو پاسخ

<div dir="ltr">

```bash
curl -sS -G --data-urlencode "query@dex_query.xml" https://may2025.archive.ensembl.org/biomart/martservice | sort > m114.tsv
curl -sS -G --data-urlencode "query@dex_query.xml" $M | sort > m116.tsv
diff m114.tsv m116.tsv
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
1,3c1,3
< ENSG00000096060	FKBP5	6	35573585	35728583	-1	protein_coding	2289
< ENSG00000103196	CRISPLD2	16	84819985	84920768	1	protein_coding	83716
< ENSG00000109906	ZBTB16	11	114059041	114256765	1	protein_coding	7704
---
> ENSG00000096060	FKBP5	6	35572945	35728622	-1	protein_coding	2289
> ENSG00000103196	CRISPLD2	16	84819975	84920768	1	protein_coding	83716
> ENSG00000109906	ZBTB16	11	114058335	114256765	1	protein_coding	7704
5c5
< ENSG00000120129	DUSP1	5	172768096	172771195	-1	protein_coding	1843
---
> ENSG00000120129	DUSP1	5	172766992	172771198	-1	protein_coding	1843
7c7
< ENSG00000163884	KLF15	3	126342635	126357408	-1	protein_coding	28999
---
> ENSG00000163884	KLF15	3	126342635	126357462	-1	protein_coding	28999
```

</div>

**خواندن `diff`:** ‏`1,3c1,3` یعنی «سطرهای ۱ تا ۳ فایل نخست به سطرهای ۱ تا ۳ فایل دوم تغییر (change) کرده‌اند». ‏`<` از فایل نخست (114) و `>` از فایل دوم (116) است.

(الف) **پنج** ژن از هشت: FKBP5، CRISPLD2، ZBTB16، DUSP1 و KLF15. در هر پنج، ژن در 116 **بلندتر** شده است (برای نمونه آغاز ZBTB16 ‏۷۰۶ باز عقب‌تر رفته و پایان KLF15 ‏۵۴ باز جلوتر). دلیل: رونوشت‌های تازه با کناره‌های دورتر افزوده شده‌اند، و ژن از کناره‌های همه‌ی رونوشت‌ها ساخته می‌شود (گام ۲ درس). در NR3C1 هم شناسه‌های تازه‌ای چون `ENST00000870492` و `ENST00001113889` دیدید. NR3C1، TSC22D3 و PER1 بی‌تغییر ماندند.
(ب) شناسه‌های ENSG و NCBI Gene **هیچ** تغییری نکردند. ‏stable ID ثابت است ولی مدل ژن عوض می‌شود. پس در هر گزارش و روش کار بنویسید «Ensembl release 116». مختصات بی release ناقص است.

---

## پاسخ ۶ (فکری): جفت کردن با GTEx

(الف) **بله، یک ژن‌اند.** ‏stable ID (‏`ENSG00000113580`) یکی است و تنها نسخه فرق دارد. داده‌ی GTEx v8 (و API آن به‌طور پیش‌فرض) بر پایه‌ی آنوتیشن **GENCODE v26** (همان Ensembl 88، سال ۲۰۱۷) است؛ در آن زمان مدل NR3C1 نسخه‌ی ۱۴ بود. از آن پس مدل سه بار عوض شده است (۱۴ ← ۱۷).

(ب) ستون دوم را بی نسخه کنید:

<div dir="ltr">

```bash
cut -f2 dex_ids.tsv | cut -d. -f1 | head -4
awk -F'\t' 'BEGIN{OFS="\t"} NR > 1 {split($2, a, "."); $2 = a[1]} {print}' dex_ids.tsv | head -3
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ensembl_id
ENSG00000113580
ENSG00000096060
ENSG00000157514
symbol	ensembl_id	chrom	start	end	strand	biotype	canonical_transcript	ncbi_gene_id
NR3C1	ENSG00000113580	5	143277931	143435512	-1	protein_coding	ENST00000394464.7	2908
FKBP5	ENSG00000096060	6	35572945	35728622	-1	protein_coding	ENST00000357266.9	2289
```

</div>

- دستور نخست تنها ستون را می‌دهد. دستور دوم کل جدول را با ستون بی‌نسخه نگه می‌دارد: ‏`split($2, a, ".")` شناسه را در نقطه می‌شکند و `$2 = a[1]` تکه‌ی نخست را جای ستون می‌گذارد. ‏`OFS="\t"` می‌گوید هنگام چاپ دوباره، ستون‌ها را با Tab جدا کن.

**خطر:** با برداشتن نسخه فرض می‌کنید ژن در هر دو نسخه **همان** است. برای ژن، این بیشتر درست است. ولی گاهی مدل ژن آن‌قدر عوض می‌شود که بیان اندازه‌گیری‌شده در GTEx (بر پایه‌ی رونوشت‌های v26) دقیقاً همان ناحیه‌ی 116 نیست. برای **رونوشت‌ها** (ENST) خطر بسیار بیشتر است: نسخه‌ی تازه می‌تواند اگزون دیگری داشته باشد. برای جفت کردن رونوشت‌ها، نسخه را برندارید.

---

## پاسخ ۷: ‏gyrA در Ensembl و NCBI

<div dir="ltr">

```bash
EC=escherichia_coli_str_k_12_substr_mg1655_gca_000005845
curl -sS "$R/lookup/symbol/$EC/gyrA?$J" | jq -c '{id, display_name, seq_region_name, start, end, strand, canonical_transcript}'
curl -sS "$R/sequence/id/b2231?type=protein;species=$EC;$J" | jq -r '.seq | length'
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
curl -sS "$B/esummary.fcgi?db=gene&id=946614&version=2.0" | grep -oE '<(Name|OtherAliases|ChrAccVer|ChrStart|ChrStop)>[^<]*' | head -5
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
{"id":"b2231","display_name":"gyrA","seq_region_name":"Chromosome","start":2336793,"end":2339420,"strand":-1,"canonical_transcript":"AAC75291."}
875
<Name>gyrA
<OtherAliases>b2231, ECK2223, hisW, nalA, nfxA, norA, parD
<ChrAccVer>NC_000913.3
<ChrStart>2339419
<ChrStop>2336792
```

</div>

(الف) Ensembl: ‏`b2231`، از 2336793 تا 2339420، رشته‌ی **منفی**؛ پروتئین **۸۷۵** اسید آمینه (GyrA شناخته‌شده‌ی *E. coli*).

(ب) NCBI می‌گوید `ChrStart 2339419` و `ChrStop 2336792`. دو فرق:
1. **ترتیب:** ژن روی رشته‌ی منفی است. NCBI ‏`ChrStart` را جایی می‌گذارد که رونویسی **آغاز** می‌شود، یعنی عدد بزرگ‌تر. Ensembl همیشه عدد کوچک‌تر را `start` می‌نامد و جهت را در `strand` می‌گوید.
2. **شمارش:** ‏`ChrStart`/`ChrStop` در esummary **از صفر** (0-based) شمرده می‌شوند. 2336792 + 1 = **2336793** و 2339419 + 1 = **2339420**، درست همان Ensembl (1-based). ✅

پس هر دو پایگاه همان ۲۶۲۸ باز را نشان می‌دهند (۲۳۳۹۴۲۰ − ۲۳۳۶۷۹۳ + ۱ = ۲۶۲۸ = ۸۷۵ کدون + کدون پایان). در ماژول 12/02 همین 0-based و 1-based را در UCSC هم می‌بینید.

</div>
