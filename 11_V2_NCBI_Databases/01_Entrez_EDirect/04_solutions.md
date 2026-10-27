<div dir="rtl">

# پاسخ تشریحی: Entrez، E-utilities و EDirect

همه‌ی خروجی‌ها واقعی‌اند (curl 8.20.0، EDirect 24.0 و Biopython 1.87، روی سرور دوره، 2026-10-27). شمار مقاله‌ها و رکوردها هر روز کمی بالا می‌رود؛ شناسه‌ها و مختصات نه.

---

## پاسخ ۱: فیلدهای پایگاه Gene

<div dir="ltr">

```bash
grep -B1 -A1 -iE '<FullName>(Preferred Symbol|Gene Name|Organism)' einfo_gene.xml
grep -A2 '<Name>PFN</Name>' einfo_gene.xml
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-iE '<FullName>(A\|B\|C)'` | یکی از سه نام کامل، بی توجه به بزرگی و کوچکی حرف |
| ‏`-B1 -A1` | یک سطر پیش (نام کوتاه) و یک سطر پس (شرح) را هم نشان بده |

**خروجی واقعی:**

<div dir="ltr">

```
			<Name>ORGN</Name>
			<FullName>Organism</FullName>
			<Description>scientific and common names of organism</Description>
--
			<Name>GENE</Name>
			<FullName>Gene Name</FullName>
			<Description>Symbol or symbols of the gene</Description>
--
			<Name>PREF</Name>
			<FullName>Preferred Symbol</FullName>
			<Description>Preferred symbol of the gene</Description>
			<Name>PFN</Name>
			<FullName>Protein Full Name</FullName>
			<Description>Protein full name</Description>
```

</div>

(الف) ‏`ORGN`، `GENE` و `PREF`. شرح `GENE` («Symbol **or symbols**») از پیش می‌گوید نام‌های دیگر را هم می‌جوید؛ همان دام acrB/gyrB درس ۲.
(ب) ‏`PFN` یعنی **Protein Full Name**، نه «preferred». نام‌های کوتاه از یک پایگاه به پایگاه دیگر هم فرق دارند. ‏`rpoB[PFN]` خطا نمی‌دهد، تنها نتیجه‌ی دیگری می‌دهد؛ پس پیش از نوشتن یک برچسب کوتاه آن را در einfo بسنجید، یا نام کامل (`[preferred symbol]`) بنویسید.

---

## پاسخ ۲: gyrA با و بی برچسب

<div dir="ltr">

```bash
for t in 'gyrA' 'gyrA[gene]' 'gyrA[preferred symbol]'; do
  n=$(curl -sS -G "$B/esearch.fcgi" --data-urlencode "db=gene" \
        --data-urlencode "term=$t AND txid511145[Organism:noexp]" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)
  echo "$t: $n"; sleep 0.4
done
esearch -db gene -query "gyrA AND txid511145[Organism:noexp]" | esummary \
  | xtract -pattern DocumentSummary -element Id Name Description | cut -c1-90
```

</div>

حلقه‌ی `for` سه بار همان دستور را با سه پرسش اجرا می‌کند؛ `$t` هر بار یکی از آن‌هاست و تنها برچسب فرق دارد.

**خروجی واقعی:**

<div dir="ltr">

```
gyrA: 7
gyrA[gene]: 1
gyrA[preferred symbol]: 1
946614	gyrA	DNA gyrase subunit A
948211	gyrB	DNA gyrase subunit B
945108	acrB	multidrug efflux pump RND permease AcrB
945112	acrA	multidrug efflux pump membrane fusion lipoprotein AcrA
947686	rpsO	30S ribosomal subunit protein S15
947499	parC	DNA topoisomerase IV subunit A
6106750	NEWENTRY	Record to support submission of GeneRIFs for a gene not in Gene (Escheric
```

</div>

(الف) بی برچسب **۷**، با `[gene]` و با `[preferred symbol]` هر دو **۱** (`946614`). برای gyrA این دو برچسب یکی‌اند، چون هیچ ژن دیگری «gyrA» را نام دیگر خود ندارد؛ برای acrB نه (درس ۲).
(ب) بی برچسب، «gyrA» در **همه‌ی فیلدها** جست‌وجو شد، از جمله خلاصه‌ی متنی و GeneRIFها. ‏gyrB، parC، acrA و acrB در کار و مقاله‌ها با gyrA پیوند دارند (هدف کینولون‌ها و پمپ برون‌ریز)؛ rpsO احتمالاً از راه یک مقاله یا نوشته‌ی مشترک آمده است. ‏**`NEWENTRY`** ژن واقعی نیست: شرحش می‌گوید رکوردی است برای ثبت GeneRIF درباره‌ی ژنی که هنوز رکورد Gene ندارد. پرسش بی برچسب این‌گونه «زباله» را هم می‌آورد.

---

## پاسخ ۳: ژن parC از ژنوم

(الف) ‏`ChrStart` (3165972) بزرگ‌تر از `ChrStop` (3163714) است، پس **رشته‌ی منفی**. با افزودن یک به هر دو: GenBank ‏`complement(3163715..3165973)`.

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text&seq_start=3163715&seq_stop=3165973&strand=2" > parC.fna
head -1 parC.fna
grep -v '>' parC.fna | tr -d '\n' | wc -c
grep -v '>' parC.fna | tr -d '\n' | cut -c1-12
grep -v '>' parC.fna | tr -d '\n' | tail -c 3; echo
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`seq_start` / `seq_stop` | همیشه عدد کوچک‌تر / بزرگ‌تر، حتی برای رشته‌ی منفی |
| ‏`strand=2` | رشته‌ی مکمل وارونه را بده (۱ = رشته‌ی مثبت) |
| ‏`tail -c 3` | سه نویسه‌ی پایانی |

**خروجی واقعی:**

<div dir="ltr">

```
>NC_000913.3:c3165973-3163715 Escherichia coli str. K-12 substr. MG1655, complete genome
2259
ATGAGCGATATG
TAA
```

</div>

(ب) **۲۲۵۹** باز، آغاز با **ATG** و پایان با **TAA**: یک ژن کامل، با طولی بخش‌پذیر بر ۳ (۲۲۵۹ = ۷۵۳ × ۳ = ۷۵۲ اسید آمینه + کُدون پایان؛ همان ۷۵۲ درس ۲). ‏`c` در سرخط یعنی complement. اگر یک را نمی‌افزودید (`seq_start=3163714&seq_stop=3165972`)، همه‌ی توالی یک باز جابه‌جا می‌شد: آغاز دیگر ATG نبود و ترجمه بی‌معنا می‌شد.

---

## پاسخ ۴: مقاله‌ها و GeneRIF

<div dir="ltr">

```bash
for ln in gene_pubmed gene_pubmed_rif; do
  echo "$ln $(curl -sS "$B/elink.fcgi?dbfrom=gene&db=pubmed&id=946614&linkname=$ln" | grep -c '<Id>')"
  sleep 0.4
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
gene_pubmed 203
gene_pubmed_rif 21
```

</div>

(الف) با کم کردن شناسه‌ی ژن آغاز: **۲۰۲** مقاله (همان عدد درس ۲، گام ۶) و **۲۰** مقاله‌ی GeneRIF.
(ب) ‏**GeneRIF** (Gene Reference Into Function) یک جمله‌ی کوتاه درباره‌ی **کارکرد** ژن است که یک کارشناس یا پژوهشگر از یک مقاله برداشته و به رکورد Gene افزوده است. ‏`gene_pubmed` همه‌ی مقاله‌های پیوندی را دارد (از جمله مقاله‌هایی که تنها توالی را ثبت کرده‌اند)؛ ‏`gene_pubmed_rif` تنها آن‌هایی که چیزی درباره‌ی کارکرد گفته‌اند. برای rpoB همین دو عدد ۳۵۰ و ۱۷ است. برای یک مرور ادبیات، GeneRIFها نقطه‌ی آغاز خوبی‌اند.

---

## پاسخ ۵: زنجیر سرور تاریخچه برای پنج ژن

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode "db=gene" --data-urlencode "usehistory=y" \
  --data-urlencode "term=(rpoB[preferred symbol] OR rpoC[preferred symbol] OR gyrA[preferred symbol] OR parC[preferred symbol] OR acrB[preferred symbol]) AND txid511145[Organism:noexp]" > h.xml
WE=$(grep -o '<WebEnv>[^<]*' h.xml | cut -d'>' -f2); grep -oE '<Count>[^<]*' h.xml | head -1; sleep 0.4
curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&linkname=gene_protein_refseq&cmd=neighbor_history&query_key=1&WebEnv=$WE" | grep -oE '<QueryKey>[^<]*'; sleep 0.4
curl -sS "$B/efetch.fcgi?db=protein&query_key=2&WebEnv=$WE&rettype=fasta&retmode=text" > five.faa
awk '/^>/{if(h)print h, n; h=$1; n=0; next}{n+=length($0)} END{print h, n}' five.faa
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
<Count>5
<QueryKey>2
>NP_418415.1 1407
>NP_418414.1 1342
>NP_417491.1 752
>NP_416734.1 875
>NP_414995.1 1049
```

</div>

(الف) همان پنج پروتئین و همان طول‌های درس ۲ (گام ۵): ‏rpoC ‏۱۴۰۷، rpoB ‏۱۳۴۲، parC ‏۷۵۲، gyrA ‏۸۷۵ و acrB ‏۱۰۴۹.
(ب) این‌جا خودتان پارامتر `linkname` را مستقیم به `elink.fcgi` دادید و سرور NCBI آن را به کار برد. در EDirect 24.0، دستور `elink` وقتی برگه را از لوله می‌گیرد `-name` را به درخواست نمی‌رساند. این را از بیرون دیدیم (۱۳ = ۱۳)، نه از درون کد. درس کلی: **هر ابزار میانی (EDirect، Biopython، …) ممکن است رفتار API را اندکی دگرگون کند؛ با یک پاسخ معلوم بسنجید.**

---

## پاسخ ۶: زیرسویه‌های K-12

<div dir="ltr">

```bash
python3 $P/01_Entrez_EDirect/scripts/gene_table.py "rpoB[gene] AND Escherichia coli K-12[orgn]"
esearch -db gene -query "rpoB[gene] AND Escherichia coli K-12[orgn]" | esummary \
  | xtract -pattern DocumentSummary -element Id Name -block Organism -element ScientificName TaxID
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
# query: rpoB[gene] AND Escherichia coli K-12[orgn]
# hits: 6
id	symbol	chr_acc	start	stop	strand	length
948488	rpoB	NC_000913.3	4181244	4185272	+	4029
14968024	rpoB	NC_020518.1	3610457	3614485	+	4029
12934478	rpoB	NC_007779.1	3455435	3451407	-	4029
7952368	rpoB	NC_012759.1	4068947	4072975	+	4029
7436037	rpoB	-	-	-	-	-
6058462	rpoB	NC_010473.1	4278963	4282991	+	4029

948488	rpoB	Escherichia coli str. K-12 substr. MG1655	511145
14968024	rpoB	Escherichia coli str. K-12 substr. MDS42	1110693
12934478	rpoB	Escherichia coli str. K-12 substr. W3110	316407
7952368	rpoB	Escherichia coli BW2952	595496
7436037	rpoB	Escherichia coli str. K-12 substr. W3110	316407
6058462	rpoB	Escherichia coli str. K-12 substr. DH10B	316385
```

</div>

(الف) ‏MG1655، MDS42، W3110 (دو بار)، BW2952 و DH10B. ‏**W3110** دو رکورد دارد: `12934478` با مختصات روی `NC_007779.1`، و `7436037` **بی** `GenomicInfo` (خط تیره‌ها). رکورد دوم امروز در Gene جای ژنومی ندارد (به هیچ اسمبلی کنونی وصل نیست)؛ برای جدول مختصات به کار نمی‌آید. اسکریپت این حالت را با `if not doc["GenomicInfo"]` گرفت؛ بی آن، `[0]` روی یک فهرست تهی خطای `IndexError` می‌داد.
(ب) در **W3110** (`3455435 > 3451407`، رشته‌ی منفی). طول همان **۴۰۲۹** است؛ ژن دگرگون نشده، **جهت** آن در کروموزوم برگشته است. ‏W3110 نسبت به MG1655 یک **وارونگی** بزرگ کروموزومی دارد که rpoB درون آن است. درس: مختصات و رشته‌ی یک ژن ویژگی **یک اسمبلی** است، نه خود ژن؛ همیشه `ChrAccVer` را کنار مختصات بنویسید. جای rpoB در MDS42 هم فرق دارد (۳٫۶ میلیون به جای ۴٫۱۸)، چون MDS42 سویه‌ای است که بخش‌های بزرگی از ژنومش برداشته شده.

---

## پاسخ ۷ (اندیشیدنی): یک کلاس، یک نشانی IP

(الف) ‏NCBI بی کلید هر **نشانی IP** را به ۳ درخواست در ثانیه می‌بندد، نه هر هنرجو را. ‏۲۰ × ۵۰ = ۱۰۰۰ درخواست در چند ثانیه، پس بیشتر آن‌ها با `{"error":"API rate limit exceeded",…}` رد می‌شوند (درس ۱، گام ۷: از ۱۲ درخواست هم‌زمان ۹ تا رد شد). کسی متوجه نمی‌شود چون پاسخ رد شده خطای `curl` نمی‌سازد؛ اسکریپت یک فایل کوچک با یک سطر JSON می‌گیرد و اگر خروجی را نسنجد، با سطرهای تهی جلو می‌رود و جدول **ناقص** می‌سازد. اگر این بار سنگین تکرار شود، NCBI ممکن است آن IP را برای مدتی ببندد.
(ب) سه دگرگونی:
1. **یک درخواست برای همه:** ۵۰ UID را با ویرگول در یک `esummary` بفرستید (`id=1,2,3,…`)، یا سرور تاریخچه را به کار ببرید؛ همان کار `gene_table.py` و EDirect. ‏۵۰ درخواست به ۱ می‌رسد.
2. **کلید API برای هر هنرجو** (در `NCBI_API_KEY`، نه در اسکریپت) و **درنگ** (`sleep 0.34` بی کلید، `sleep 0.1` با کلید) میان درخواست‌ها.
3. **سنجش خروجی:** پس از هر پاسخ دنبال `"error"` یا `<ERROR>` بگردید، شمار رکوردها را (`grep -c '^>'` یا `Count`) با شمار خواسته‌شده بسنجید، و در صورت خطا پس از چند ثانیه دوباره بکوشید. ‏EDirect و Biopython بخشی از این کار را خودشان می‌کنند.

---

## برای خواندن بیشتر

- ‏Kans J. *Entrez Direct* (نمونه‌های بیشتر لوله و `xtract`): https://www.ncbi.nlm.nih.gov/books/NBK179288/
- ‏Sayers E. *The E-utilities In-Depth*، فهرست همه‌ی پارامترها: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- ‏Brown GR, et al. (2015). *Gene: a gene-centered information resource at NCBI.* Nucleic Acids Res 43:D36–D42 (بخش GeneRIF). https://doi.org/10.1093/nar/gku1055
- ‏YouTube: *E-Utilities Introduction* (NLM): https://www.youtube.com/watch?v=BCG-M5k-gvE

</div>
