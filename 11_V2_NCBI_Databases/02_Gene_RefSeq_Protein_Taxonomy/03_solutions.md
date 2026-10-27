<div dir="rtl">

# پاسخ تشریحی: Gene، RefSeq، Protein، IPG، CDD و Taxonomy

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0 و EDirect 24.0، روی سرور دوره، 2026-10-27). شمار رکوردهای IPG هر هفته بالا می‌رود.

---

## پاسخ ۱: پیشوندها را بخوانید

(الف) ‏`NC_` کروموزوم (RefSeq)؛ `NG_` ناحیه‌ی ژنومی یک ژن (RefSeqGene)؛ `NR_` ‏RNA ناکدکننده‌ی بازبینی‌شده (RefSeq)؛ `AAC76961` دو حرف و شش رقم، بی `_`: **GenBank**؛ `WP_` پروتئین ناوابسته به ژنوم (RefSeq).

<div dir="ltr">

```bash
for a in NC_000005.10 NG_009062.1 NR_157096.2; do
  curl -sS "$B/esummary.fcgi?db=nuccore&id=$a&version=2.0" | grep -oE '<(Caption|Title|Slen|MolType)>[^<]*' \
    | sed 's/<[A-Za-z]*>//' | paste -sd'|' | cut -c1-140; sleep 0.4
done
for a in AAC76961.1 WP_000263098.1; do
  curl -sS "$B/esummary.fcgi?db=protein&id=$a&version=2.0" | grep -oE '<(Caption|Title|Slen)>[^<]*' \
    | sed 's/<[A-Za-z]*>//' | paste -sd'|' | cut -c1-140; sleep 0.4
done
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`version=2.0` | قالب تازه‌ی esummary: هر فیلد یک برچسب جدا (`<Title>`)، نه `<Item Name="Title">` |
| ‏`sed 's/<[A-Za-z]*>//'` | برچسب آغازین را بردار، مقدار بماند |
| ‏`paste -sd'\|'` | همه‌ی سطرها را با `\|` در یک سطر بچسبان |

**خروجی واقعی:**

<div dir="ltr">

```
NC_000005|Homo sapiens chromosome 5, GRCh38.p14 Primary Assembly|181538259|dna
NG_009062|Homo sapiens nuclear receptor subfamily 3 group C member 1 (NR3C1), RefSeqGene on chromosome 5|164582|dna
NR_157096|Homo sapiens nuclear receptor subfamily 3 group C member 1 (NR3C1), transcript variant 15, non-coding RNA|5212|rna
AAC76961|RNA polymerase subunit beta [Escherichia coli str. K-12 substr. MG1655]|1342
WP_000263098|MULTISPECIES: DNA-directed RNA polymerase subunit beta [Pseudomonadati]|1342
```

</div>

(ب) کروموزوم ۵: ‏۱۸۱٬۵۳۸٬۲۵۹ باز. ‏RefSeqGene: ‏۱۶۴٬۵۸۲ باز (ناحیه‌ی ژن، ۱۵۷٬۵۸۲ باز در درس، به‌اضافه‌ی چند هزار باز پیرامون). ‏`NR_157096.2`: ‏۵۲۱۲ باز و **non-coding RNA**: این رونوشت چارچوب خواندنی کامل ندارد (برای نمونه یک اگزون جایگزین کُدون پایان زودرس می‌آورد)، پس NCBI برایش پروتئین ثبت نکرده است. دو پروتئین rpoB هر دو ۱۳۴۲ اسید آمینه‌اند: یکی رکورد GenBank ثبت‌کننده‌ی ژنوم، دیگری `WP_` همه‌ی ژنوم‌ها؛ «MULTISPECIES» در عنوان `WP_` همین را می‌گوید.

---

## پاسخ ۲: ایزوفرم‌های گیرنده‌ی گلوکوکورتیکوئید

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&id=2908&linkname=gene_protein_refseq&cmd=neighbor_history" > hp.xml
WE=$(grep -o '<WebEnv>[^<]*' hp.xml | cut -d'>' -f2); sleep 0.4
curl -sS "$B/efetch.fcgi?db=protein&query_key=1&WebEnv=$WE&rettype=fasta&retmode=text" > nr3c1_prot.faa
awk '/^>/{if(h)print n"\t"h; h=$0; n=0; next}{n+=length($0)} END{print n"\t"h}' nr3c1_prot.faa \
  | sort -k1,1nr | cut -d' ' -f1,4- | sed 's/ \[Homo sapiens\]//' | cut -c1-70 > iso.txt
cat iso.txt
cut -f1 iso.txt | sort | uniq -c | sort -k2,2nr
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`print n"\t"h` | طول را **پیش** از سرخط بنویس، تا مرتب کردن ساده باشد |
| ‏`sort -k1,1nr` | ستون نخست، عددی (`n`)، از بزرگ به کوچک (`r`) |
| ‏`cut -d' ' -f1,4-` | از سرخط واژه‌ی نخست (طول و accession) و واژه‌ی چهارم به بعد (`isoform …`) را نگه دار؛ «glucocorticoid receptor» کنار می‌رود |

**خروجی واقعی (بخشی از `iso.txt` و شمارش طول‌ها):**

<div dir="ltr">

```
778	>NP_001019265.1 isoform gamma
778	>NP_001351112.1 isoform gamma
778	>NP_001351113.1 isoform gamma
778	>NP_001351114.1 isoform gamma
777	>NP_000167.1 isoform alpha
…            (seven more isoform alpha, 777)
751	>NP_001191187.1 isoform alpha-B
742	>NP_001018661.1 isoform beta
692	>NP_001191188.1 isoform alpha-C1
688	>NP_001191189.1 isoform alpha-C2
680	>NP_001191190.1 isoform alpha-C3
676	>NP_001191194.1 isoform GR-P
462	>NP_001191191.1 isoform alpha-D1
447	>NP_001191192.1 isoform alpha-D2
442	>NP_001191193.1 isoform alpha-D3
      4 778
      8 777
      1 751
      1 742
      1 692
      1 688
      1 680
      1 676
      1 462
      1 447
      1 442
```

</div>

(الف) ‏**۱۱** نام ایزوفرم: gamma، alpha، alpha-B، beta، alpha-C1 تا C3، GR-P و alpha-D1 تا D3. بلندترین **GRγ** (۷۷۸، یک اسید آمینه بیشتر از GRα، از یک جایگاه پیرایش جایگزین) و کوتاه‌ترین **GRα-D3** (۴۴۲). ایزوفرم‌های C و D از **آغازگاه‌های ترجمه‌ی پایین‌دست** روی همان mRNA می‌آیند و بخشی از دامنه‌ی آغازی را ندارند.
(ب) ‏**۸** ‏`NP_` با ۷۷۷ اسید آمینه، همه GRα. رونوشت‌هایشان تنها در بخش‌های ترجمه‌نشده (**UTR**) فرق دارند و CDS یکی است؛ در NR3C1 این فرق بیشتر از **اگزون‌های نخست جایگزین** است که هر کدام از یک پیش‌بر جدا آغاز می‌شوند. پس هر رونوشت یک `NP_` جدا دارد، هرچند توالی پروتئین‌ها یکسان است. این همان چیزی است که IPG در باکتری‌ها گروه می‌کند.
(ج) ‏GRβ ‏**۷۴۲** اسید آمینه است: پایان آن از یک اگزون جایگزین (9β) می‌آید و LBD کامل ندارد، پس دگزامتازون را نمی‌گیرد.

---

## پاسخ ۳: IPG برای gyrA

<div dir="ltr">

```bash
id=$(curl -sS "$B/esearch.fcgi?db=ipg&term=NP_416734.1" | grep -o '<Id>[^<]*' | head -1 | cut -d'>' -f2); sleep 0.4
curl -sS "$B/esummary.fcgi?db=ipg&id=$id" \
  | grep -oE '<(Accession|ProteinCount|Slen|Organism|TaxIdCount|SpeciesCount|GeneraCount|AssemblyCount)>[^<]*' \
  | sed 's/<//; s/>/=/' | paste -sd' '
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ProteinCount=177667 Accession=WP_001281242.1 Slen=875 Organism=Bacteria TaxIdCount=1242 SpeciesCount=99 GeneraCount=5 AssemblyCount=193973
```

</div>

(الف) ‏`WP_001281242.1` (۸۷۵ اسید آمینه)؛ ‏۱۷۷٬۶۶۷ رکورد، ۹۹ گونه، ۵ جنس، ۱۹۳٬۹۷۳ اسمبلی.
(ب) ‏rpoB: ‏۴۰۲ هزار رکورد و ۴۰۹ گونه؛ gyrA کمتر از نیمی از آن. چند علت با هم: gyrA کمتر از rpoB حفظ‌شده است، پس سویه‌ها و گونه‌های نزدیک زودتر یک اسید آمینه فرق پیدا می‌کنند و به گروه IPG دیگری می‌روند. افزون بر این، بسیاری از ایزوله‌های بالینی تعیین توالی‌شده **جهش مقاومت به کینولون** در gyrA دارند (مانند S83L و D87N، بخش ۰۸). هر جهش یعنی یک توالی دیگر و یک گروه IPG دیگر. پس این گروه بیشتر سویه‌های **حساس** را در بر دارد.

---

## پاسخ ۴: باکتری سل در Taxonomy

<div dir="ltr">

```bash
efetch -db taxonomy -id 83332,9606 -format xml \
  | xtract -pattern Taxon -element TaxId ScientificName Rank -block LineageEx -sep ' > ' -element ScientificName | cut -c1-260
esearch -db taxonomy -query "Mycobacterium tuberculosis[scientific name]" | efetch -format uid
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
9606	Homo sapiens	species	cellular organisms > Eukaryota > Opisthokonta > Metazoa > Eumetazoa > Bilateria > Deuterostomia > Chordata > Craniata > Vertebrata > Gnathostomata > Teleostomi > Euteleostomi > Sarcopterygii > Dipnotetrapodomorpha > Tetrapoda > Amniot
83332	Mycobacterium tuberculosis H37Rv	strain	cellular organisms > Bacteria > Bacillati > Actinomycetota > Actinomycetes > Mycobacteriales > Mycobacteriaceae > Mycobacterium > Mycobacterium tuberculosis complex > Mycobacterium tuberculosis
1773
```

</div>

(الف) ‏H37Rv رده‌ی **strain** دارد ولی MG1655 ‏**no rank**. رده‌ی `strain` را NCBI تنها برای برخی سویه‌های پرکاربرد گذاشته است. پس برای یافتن «همه‌ی سویه‌ها» به `Rank` تکیه نکنید؛ با `[Organism]` (explode) زیر TaxID گونه بجویید. (دودمان انسان را `cut` بریده است.)
(ب) ‏TaxID گونه **1773**. میان جنس *Mycobacterium* و گونه یک گروه **Mycobacterium tuberculosis complex** هست؛ این گروه چند گونه‌ی بسیار نزدیک (مانند *M. bovis*) را در بر دارد. جستجوی `txid1773[Organism]` *M. bovis* را نمی‌آورد، ولی `Mycobacterium tuberculosis complex[Organism]` می‌آورد.

---

## پاسخ ۵: دامنه‌های rpoB و gyrA

<div dir="ltr">

```bash
w=$(curl -sS "$B/esearch.fcgi?db=protein&term=WP_001281242.1" | grep -o '<Id>[^<]*' | head -1 | cut -d'>' -f2); echo $w; sleep 0.4
for u in 446185243 $w; do
  ids=$(curl -sS "$B/elink.fcgi?dbfrom=protein&db=cdd&id=$u&linkname=protein_cdd_specific_2" \
        | grep -o '<Id>[^<]*' | cut -d'>' -f2 | tail -n +2 | paste -sd,); sleep 0.4
  curl -sS "$B/esummary.fcgi?db=cdd&id=$ids&version=2.0" | grep -oE '<(Accession|Title)>[^<]*' | sed 's/<[A-Za-z]*>//' | paste - -
  sleep 0.4
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
447203986
PRK00405	rpoB
PRK05560	PRK05560
```

</div>

(الف) ‏rpoB ← **PRK00405** و gyrA ← **PRK05560**.
(ب) ‏`PRK` مدلی است که از یک **خوشه‌ی پروتئینی** (protein cluster) کامل ساخته شده، یعنی همه‌ی طول پروتئین را یک‌جا می‌پوشاند، نه یک دامنه را. برای پروتئین‌های باکتریایی بسیار حفظ‌شده، چنین مدل تمام‌قدی «ویژه‌ترین» برخورد است و `protein_cdd_specific_2` تنها آن را می‌دهد. برای دیدن دامنه‌های جدا (مانند دامنه‌های β در rpoB) CD-Search را با خود توالی بزنید و «Full results» را برگزینید. عنوان PRK05560 تنها خود شناسه است؛ همین نشان می‌دهد همه‌ی رکوردهای CDD به یک اندازه شرح ندارند.

---

## پاسخ ۶: ژنی با `XM_`

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=nuccore&id=2909&linkname=gene_nuccore_refseqrna&cmd=neighbor_history" > h2.xml
WE=$(grep -o '<WebEnv>[^<]*' h2.xml | cut -d'>' -f2); sleep 0.4
curl -sS "$B/efetch.fcgi?db=nuccore&query_key=1&WebEnv=$WE&rettype=acc" | cut -c1-3 | sort | uniq -c
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
      1 NM_
      2 XM_
      2 XR_
```

</div>

(الف) ‏۱ ‏`NM_`، ‏۲ ‏`XM_` و ۲ ‏`XR_`.
(ب) همان `NM_` (و اگر MANE Select است، که برای ژنی با یک `NM_` به احتمال زیاد همان است؛ با `KEYWORDS` در رکورد GenBank بسنجید). ‏`XM_`/`XR_` را **برنامه‌ی پیش‌بینی ژن** (Gnomon) از روی ژنوم و داده‌ی RNA-seq ساخته است و کسی آن را بازبینی نکرده؛ ممکن است با به‌روزرسانی بعدی حذف یا دگرگون شود، و آزمایشگاه‌های بالینی آن را نمی‌پذیرند.

---

## پاسخ ۷ (اندیشیدنی): کدام شناسه را بنویسیم؟

(الف) یک: `AAC76961` **بی نسخه** است و یک رکورد **GenBank** است؛ بهتر است `NP_418414.1` (RefSeq، با نسخه) را بنویسد و برای نام‌گذاری جهش، شماره‌گذاری را هم بگوید (*E. coli* یا *M. tuberculosis*؛ ماژول 09/01). دو: `NR3C1` نام ژن است، نه شناسه‌ی توالی؛ این ژن ۲۲ رونوشت و ۱۱ ایزوفرم دارد (پاسخ ۲) و خواننده نمی‌داند کدام.
(ب) «توالی پروتئین RpoB از `NP_418414.1` (RefSeq، *E. coli* K-12 MG1655) گرفته شد و جهش‌ها با شماره‌گذاری *E. coli* نام برده شدند. توالی گیرنده‌ی گلوکوکورتیکوئید از رونوشت MANE Select ‏`NM_000176.3` / `NP_000167.1` (GRα) گرفته شد (دسترسی 2026-10-27).»

---

## برای خواندن بیشتر

- ‏Oakley RH, Cidlowski JA (2013). *The biology of the glucocorticoid receptor: new signaling mechanisms in health and disease.* J Allergy Clin Immunol 132:1033–1044. https://doi.org/10.1016/j.jaci.2013.09.007 (ایزوفرم‌های GR)
- ‏Morales J, et al. (2022). Nature 604:310–315 (MANE). https://doi.org/10.1038/s41586-022-04558-8
- ‏YouTube: *RefSeq and NCBI Gene* (ClinGen Resource): https://www.youtube.com/watch?v=1ndnACFDpmc

</div>
