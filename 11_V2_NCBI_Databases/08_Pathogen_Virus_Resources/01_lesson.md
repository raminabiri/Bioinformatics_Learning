<div dir="rtl">

# درس: Pathogen Detection، MicroBIGG-E و NCBI Virus؛ مقاومت و ویروس‌ها در مقیاس جهانی

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `08_Pathogen_Virus_Resources` · **پیش‌نیاز:** ماژول [08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/) (AMRFinderPlus، blaCTX-M-15)؛ ماژول [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) (NCBI Datasets)؛ ماژول [11/07](../07_BLAST_Suite_Tools/) (gyrA S83/D87)؛ Python (بخش ۰۳) · **زمان:** حدود ۹۰ دقیقه (به‌اضافه‌ی زمان دانلود) · **ابزار:** curl 8.20.0، Python 3، NCBI Datasets CLI 18.38.0؛ Isolates Browser و MicroBIGG-E (✍️ وب) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده**، جز صفحه‌های وب Isolates Browser و MicroBIGG-E (✍️؛ همان داده از FTP گرفته و روی سرور تحلیل شد). همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). فایل اصلی ۵۵۳ مگابایت است و دانلودش ۲۶ دقیقه طول کشید؛ اسکریپت آن را سطر به سطر می‌خواند (۲۷۲ مگابایت حافظه).

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید **NCBI Pathogen Detection** چه می‌کند: هر ژنوم باکتری بیماری‌زای تازه را با AMRFinderPlus می‌سنجد و در **خوشه‌های SNP** می‌گذارد.
2. فایل‌های FTP این سامانه (فراداده و ژن‌های AMR، فهرست خوشه‌ها) را بشناسید و پیش از دانلود حجمشان را بسنجید.
3. یک ژن مقاومت (**blaCTX-M-15**) را در صدها هزار ایزوله بشمارید: کشور، دهه، همراهان و خوشه‌ها؛ همان پرسشی که **MicroBIGG-E** در وب پاسخ می‌دهد.
4. با **NCBI Datasets** ژنوم‌های یک ویروس (ویروس تب خونریزی‌دهنده‌ی کریمه-کنگو) را جدول کنید و یک ژنوم را بگیرید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m08 && cd ~/ncbi/m08
P=~/Bioinformatics_Learning-main/11_V2_NCBI_Databases/99_scripts_data
F=https://ftp.ncbi.nlm.nih.gov/pathogen/Results/Escherichia_coli_Shigella/latest_snps
df -h .
```

</div>

---

## ۱. داستان

در ماژول 08/01 با AMRFinderPlus در **یک** ژنوم *E. coli* ژن **blaCTX-M-15** را یافتید: بتالاکتامازی با طیف گسترده (ESBL) که سفالوسپورین‌های نسل سوم را بی‌اثر می‌کند. پرسش بعدی هر پژوهشگر سلامت عمومی: «این ژن در جهان چقدر شایع است؟ کجا؟ همراه چه ژن‌های دیگری؟ آیا ایزوله‌های بیمارستان ما به ایزوله‌های کشورهای دیگر نزدیک‌اند؟» ‏NCBI همین کار را هر روز برای **همه‌ی** ژنوم‌های عمومی چند ده گونه‌ی بیماری‌زا انجام می‌دهد و نتیجه را آزاد می‌گذارد. در این درس آن را از FTP می‌گیریم و خودمان می‌شماریم. بخش دوم درس همین را برای **ویروس‌ها** با NCBI Virus و Datasets نشان می‌دهد.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏Pathogen Detection در سه گام

1. **گردآوری:** هر ژنوم یا run عمومی از گونه‌های برگزیده (*E. coli/Shigella*، *Salmonella*، *Klebsiella*، … بیش از ۵۰ گروه) که به SRA یا GenBank می‌رسد.
2. ‏**AMRFinderPlus:** ژن‌های مقاومت، تنش و بیماری‌زایی، و **جهش‌های نقطه‌ای** (مانند `gyrA_S83L=POINT`)؛ همان ابزار 08/01.
3. **خوشه‌بندی:** ژنوم‌هایی که کمتر از چند ده SNP با هم فاصله دارند در یک **خوشه‌ی SNP** (`PDS…`) می‌روند و درخت دارند. دو ایزوله در یک خوشه = احتمال **یک منشأ** (یک شیوع، یک زنجیره‌ی انتقال).

| شناسه | معنا | نمونه |
| :--- | :--- | :--- |
| ‏`PDG` | یک «گروه» (یک گونه یا گروه گونه‌ها) و نسخه‌ی تحلیل آن | ‏`PDG000000004.6392` (*E. coli/Shigella*، نسخه‌ی ۶۳۹۲) |
| ‏`PDT` | یک ایزوله (target) | ‏`PDT000002365.3` |
| ‏`PDS` | یک خوشه‌ی SNP | ‏`PDS000267218.12` |

**تشبیه:** هر ایزوله یک شناسنامه‌ی مقاومت (فهرست ژن‌ها) و یک «خانواده» (خوشه‌ی SNP) دارد؛ Pathogen Detection دفتر ثبت جهانی هر دو است.

### ‏۲.۲ ‏MicroBIGG-E و Isolates Browser

- ‏**Isolates Browser** (https://www.ncbi.nlm.nih.gov/pathogens/isolates/): جدول وب همه‌ی ایزوله‌ها، با جست‌وجو، فیلتر و دانلود (✍️ وب).
- ‏**MicroBIGG-E** (https://www.ncbi.nlm.nih.gov/pathogens/microbigge/): یک سطر برای **هر ژن یافته‌شده** در هر ایزوله، با جای ژن روی contig. برای پرسش «همه‌ی blaCTX-M-15ها» ساخته شده (✍️ وب).
- هر دو همان داده‌ی FTP را نشان می‌دهند که ما در این درس می‌گیریم.

> 📺 **فیلم:** *Introducing the NCBI Pathogen Detection Isolates Browser* (National Library of Medicine): https://www.youtube.com/watch?v=T8HluuzOb5c · *NCBI Minute: Accessing NCBI AMR Pathogen Data in the Cloud* (NLM): https://www.youtube.com/watch?v=j4dzFOo2FmI
> 📄 **مرجع:** Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence.* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0 · راهنمای Pathogen Detection: https://www.ncbi.nlm.nih.gov/pathogens/pathogens_help/

---

## ۳. گام ۱: پیش از دانلود، بسنجید

**چرا؟** این فایل‌ها بزرگ‌اند و هر روز به‌روز می‌شوند. نخست فهرست پوشه را ببینید:

<div dir="ltr">

```bash
curl -sS $F/AMR/ | sed 's/<[^>]*>/ /g' | grep PDG
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
 PDG000000004.6392.amr.metadata.tsv                        2026-10-27 05:12  527M
 PDG000000004.6392.amr.metadata.xml                        2026-10-27 05:06  4.4G
```

</div>

**توضیح خروجی:**
- ‏`PDG000000004.6392`: گروه *E. coli/Shigella*، **نسخه‌ی ۶۳۹۲** تحلیل؛ همان روز ساخته شده است. ‏`latest_snps` همیشه به تازه‌ترین نسخه اشاره می‌کند؛ برای تکرارپذیری، **شماره‌ی نسخه** را در گزارش بنویسید.
- فایل TSV ‏**۵۲۷ مگابایت** و همان داده در XML ‏۴٫۴ گیگابایت. TSV را برمی‌داریم.
- پوشه‌ی `Metadata/` همین ستون‌ها را بی ستون‌های AMR دارد؛ `Clusters/` فهرست خوشه‌ها (۲۱ مگابایت) و فاصله‌های SNP (۱۶ گیگابایت)؛ `SNP_trees/` درخت هر خوشه.

---

## ۴. گام ۲: دانلود و ستون‌ها

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" curl -sS -o ecoli.amr.metadata.tsv \
  -w 'size=%{size_download} speed=%{speed_download}\n' $F/AMR/PDG000000004.6392.amr.metadata.tsv
curl -sS -o clusters.tsv $F/Clusters/PDG000000004.6392.reference_target.cluster_list.tsv
head -1 ecoli.amr.metadata.tsv | tr '\t' '\n' | nl | sed -n '22p;25p;33p;36p;43p;50p;57p;58p'
awk -F'\t' 'NR==2 {print $43; print $25; print $36; print $58}' ecoli.amr.metadata.tsv
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
size=552542417 speed=360671
time=1532.05s maxRSS=12024KB
    22	collection_date
    25	geo_loc_name
    33	scientific_name
    36	species_taxid
    43	target_acc
    50	computed_types
    57	AST_phenotypes
    58	AMR_genotypes
PDT000002365.3
USA
562
"acrF,blaEC,mdtM"
```

</div>

**توضیح خروجی:**
- ‏۵۵۳ مگابایت در **۲۶ دقیقه** (۳۶۰ کیلوبایت در ثانیه از سرور ما)، ولی تنها **۱۲ مگابایت** حافظه: `curl` داده را مستقیم در دیسک می‌نویسد.
- فایل **۶۷ ستون** دارد؛ مهم‌ها: تاریخ و کشور، `species_taxid` (۵۶۲ = *E. coli*)، `target_acc` (‏`PDT…`، پل به فهرست خوشه‌ها)، و **`AMR_genotypes`**: همه‌ی ژن‌ها و جهش‌های AMRFinderPlus با ویرگول، درون `"…"`.
- ‏`blaEC` بتالاکتاماز **کروموزومی** همه‌ی *E. coli*‌هاست (AmpC ذاتی)، نه ژن اکتسابی؛ `acrF` و `mdtM` هم پمپ‌های ذاتی‌اند. پس «ژن AMR دارد» همیشه به معنای «مقاوم است» نیست.
- ستون `scientific_name` نام **سویه** را دارد (برای نمونه `Escherichia coli O104:H4 str. TY-2482`)؛ برای شمردن گونه‌ها از `species_taxid` کار بکشید.

---

## ۵. گام ۳: ‏blaCTX-M-15 در ۵۹۲ هزار ایزوله

**چرا با پایتون و نه pandas؟** ‏`pd.read_csv` این فایل را یک‌جا در حافظه می‌برد (چند گیگابایت). اسکریپت [amr_summary.py](../99_scripts_data/08_Pathogen_Virus_Resources/scripts/amr_summary.py) فایل را **سطر به سطر** با `csv.DictReader` می‌خواند و تنها شمارنده‌ها را نگه می‌دارد:

<div dir="ltr">

```python
    for r in rows:
        total += 1
        species[r["species_taxid"]] += 1
        genotypes = r["AMR_genotypes"].strip('"').split(",")
        if gene in genotypes:
            ...
            carriers.append((r["target_acc"], country, year, set(genotypes)))
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`csv.DictReader(…, delimiter="\t")` | هر سطر یک دیکشنری با نام ستون‌ها |
| ‏`.strip('"').split(",")` | فهرست ژن‌ها؛ `gene in genotypes` برابری **کامل** است (blaCTX-M-15 با blaCTX-M-150 یکی نمی‌شود) |
| ‏`Counter` | شمارنده‌ی کشور، دهه و ژن‌های همراه |

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" python3 $P/08_Pathogen_Virus_Resources/scripts/amr_summary.py \
    ecoli.amr.metadata.tsv blaCTX-M-15 clusters.tsv
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
isolates: 591810
top species_taxid: 562 520620, 624 34827, 623 32057, 621 1500
with blaCTX-M-15: 77220 (13.0%)

top countries:
  NULL	13740
  USA	11883
  United Kingdom	7816
  Netherlands	3144
  Malawi	2841
  France	2523
  Bangladesh	2489
  Australia	2206
  Iran	50

by decade: 1900s 17, 1980s 2, 1990s 1, 2000s 977, 2010s 26000, 2020s 29837 | no usable year: 20386

most frequent companions of blaCTX-M-15:
  blaEC	96.9%
  acrF	83.2%
  mdtM	74.3%
  gyrA_S83L=POINT	67.3%
  parC_S80I=POINT	59.1%
  gyrA_D87N=POINT	53.5%
  mph(A)	51.7%
  mrx(A)	51.2%
  sul1	50.8%
  sul2	49.7%

carriers in a SNP cluster: 59835 of 77220
largest clusters: PDS000204584.658 2798, PDS000273111.23 1805, PDS000225708.42 1220
time=4.32s maxRSS=272480KB
```

</div>

**توضیح خروجی:**
- ‏**۵۹۱٬۸۱۰** ایزوله: ‏۵۲۰ هزار *E. coli* (562) و بقیه *Shigella* (624 = *S. sonnei*، 623 = *S. flexneri*، 621 = *S. boydii*). ‏۴٫۳ ثانیه و ۲۷۲ مگابایت حافظه برای ۵۵۳ مگابایت داده.
- ‏**۱۳٪** (۷۷٬۲۲۰) blaCTX-M-15 دارند: پرشمارترین ESBL جهان.
- کشورها: **بی کشور** (`NULL`) بیشترین است، سپس آمریکا و بریتانیا. ایران **۵۰**. این‌ها شمار **ژنوم‌های ثبت‌شده**‌اند، نه شیوع در جمعیت (اشتباه رایج ۳).
- دهه‌ها: بیشتر از ۲۰۱۰ به این سو؛ ۲۰٬۳۸۶ ایزوله سال درستی ندارند (`missing`، `NULL` یا عدد نادرست). ‏۱۷ ایزوله‌ی «۱۹۰۰ها» احتمالاً تاریخ‌های نادرست یا نمونه‌های بایگانی‌اند؛ بی وارسی تفسیرشان نکنید.
- **همراهان:** ‏`gyrA_S83L` (۶۷٪)، `parC_S80I` (۵۹٪) و `gyrA_D87N` (۵۴٪): بیشتر حاملان CTX-M-15 به **فلوروکینولون‌ها** هم مقاوم‌اند. این همان جهش‌های 11/07 (S83 و D87) است. ترکیب ESBL و مقاومت به کینولون ویژگی شناخته‌شده‌ی دودمان پرخطر **ST131** است (برای سنجیدن، نوع MLST هر ایزوله لازم است که در این جدول نیست).
- **خوشه‌ها:** ‏۷۷٫۵٪ حاملان در یک خوشه‌ی SNP‌اند؛ بزرگ‌ترین خوشه ۲۷۹۸ حامل دارد. یعنی گسترش CTX-M-15 بیشتر **کلونی** است (یک دودمان باکتری پخش می‌شود)، نه تنها جابه‌جایی پلاسمید.

> 📺 **فیلم:** *Using the NCBI Pathogen Detection Pipeline as Part of the Epi Work Flow* (Integrated Food Safety Centers of Excellence): https://www.youtube.com/watch?v=8JkitjkNwYk
> 📄 **مرجع:** Nicolas-Chanoine MH, Bertrand X, Madec JY (2014). *Escherichia coli ST131, an intriguing clonal group.* Clin Microbiol Rev 27:543–574. https://doi.org/10.1128/CMR.00125-13

---

## ۶. گام ۴: خوشه‌های SNP

<div dir="ltr">

```bash
cut -f1 clusters.tsv | tail -n +2 | sort | uniq -c | awk '{print $1}' > csizes.txt
wc -l < csizes.txt
sort -n csizes.txt | awk '{a[NR]=$1} END{print "min", a[1], "median", a[int((NR+1)/2)], "max", a[NR]}'
awk '$1==2' csizes.txt | wc -l
tail -n +2 clusters.tsv | wc -l
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`cut -f1 … \| sort \| uniq -c` | برای هر خوشه (ستون ۱، `PDS…`) شمار ایزوله‌ها |
| ‏`awk '{a[NR]=$1} END{…}'` | اندازه‌ها را (مرتب‌شده) در آرایه بریز؛ نخستین، میانه و آخرین |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
59827
min 2 median 2 max 6277
34383
382716
```

</div>

**توضیح خروجی:**
- ‏**۵۹٬۸۲۷** خوشه؛ میانه‌ی اندازه **۲**، و **۳۴٬۳۸۳** خوشه (۵۷٪) تنها دو ایزوله دارند. بزرگ‌ترین ۶۲۷۷ ایزوله دارد.
- ‏۳۸۲٬۷۱۶ ایزوله در خوشه‌اند: **۶۵٪** همه. بقیه هیچ ایزوله‌ی نزدیکی ندارند.
- خوشه‌ی دوتایی یعنی دو ژنوم بسیار نزدیک: گاهی یک **شیوع** (دو بیمار، یک منبع)، گاهی دو نمونه از **یک بیمار** یا یک آزمایشگاه. پیش از نتیجه‌گیری اپیدمیولوژیک، فراداده (کشور، تاریخ، منبع) را ببینید؛ موضوع دوره‌ی جدای اپیدمیولوژی ژنومیک.

---

## ۷. گام ۵: ‏NCBI Virus و Datasets

**چرا؟** برای ویروس‌ها NCBI یک درگاه جدا دارد: **NCBI Virus** (https://www.ncbi.nlm.nih.gov/labs/virus/vssi/، ✍️ وب). همان داده با **NCBI Datasets** (11/02) از خط فرمان در دسترس است. نخست یک پاسخ معلوم: ژنوم مرجع SARS-CoV-2.

<div dir="ltr">

```bash
datasets summary virus genome accession NC_045512.2 --as-json-lines \
  | dataformat tsv virus-genome --fields accession,virus-name,virus-tax-id,length,completeness,host-name,isolate-collection-date,geo-location
datasets download virus genome accession NC_045512.2 --filename sars2.zip
unzip -o -q sars2.zip -d sars2
grep -v '>' sars2/ncbi_dataset/data/genomic.fna | tr -d '\n' | wc -c
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Accession	Virus Name	Virus Taxonomic ID	Length	Completeness	Host Name	Isolate Collection date	Geographic Location
NC_045512.2	Severe acute respiratory syndrome coronavirus 2	2697049	29903	COMPLETE	Homo sapiens	2019-12	China
29903
```

</div>

‏**۲۹٬۹۰۳** باز؛ همان طول شناخته‌شده‌ی ژنوم مرجع ووهان (دسامبر ۲۰۱۹).

حالا یک ویروس نزدیک‌تر به ما: **ویروس تب خونریزی‌دهنده‌ی کریمه-کنگو** (CCHFV)، که در ایران بومی است. ژنومش سه بخش (segment) دارد: **S**، **M** و **L**.

<div dir="ltr">

```bash
datasets summary virus genome taxon "Crimean-Congo hemorrhagic fever virus" --as-json-lines > cchfv.jsonl
wc -l < cchfv.jsonl
dataformat tsv virus-genome --inputfile cchfv.jsonl \
  --fields accession,completeness,length,geo-location,isolate-collection-date,virus-tax-id,segment > cchfv.tsv
cut -f2 cchfv.tsv | sort | uniq -c
cut -f7 cchfv.tsv | sort | uniq -c | sort -rn | head -5
cut -f4 cchfv.tsv | sort | uniq -c | sort -rn | head -8
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
5471
    396 COMPLETE
      1 Completeness
   5075 PARTIAL
   1835 S
   1499 M
   1338 L
    782 
     15 S-RNA segment
   2128 Russia
    665 Turkey
    264 Pakistan
    186 China
    177 Kosovo
    177 Iran
    136 South Africa
    100 
```

</div>

**توضیح خروجی:**
- ‏**۵۴۷۱** رکورد، تنها **۳۹۶** کامل (۷٪)؛ بیشتر تکه‌هایی از یک بخش‌اند، برای تشخیص یا تعیین ژنوتیپ.
- بخش‌ها: S بیش از همه (۱۸۳۵؛ هدف رایج تشخیص). ‏۷۸۲ رکورد **بی نام بخش** و ۱۵ با نوشتار دیگر («S-RNA segment»): فراداده‌ی ویروس هم مانند باکتری یکدست نیست؛ پیش از شمردن، نوشتارها را یکی کنید.
- کشورها: روسیه (۲۱۲۸) و ترکیه (۶۶۵) در صدر؛ **ایران ۱۷۷**.

> 📺 **فیلم:** *NCBI virus: download viral genomes in FASTA format* (OmicsLogic): https://www.youtube.com/watch?v=Uw5lP3vFSNY
> 📄 **مرجع:** Hatcher EL, et al. (2017). *Virus Variation Resource – improved response to emergent viral outbreaks.* Nucleic Acids Res 45(D1):D482–D490. https://doi.org/10.1093/nar/gkw1065 · Brister JR, et al. (2015). *NCBI Viral Genomes Resource.* Nucleic Acids Res 43(D1):D571–D577. https://doi.org/10.1093/nar/gku1207 · مستندات Datasets: https://www.ncbi.nlm.nih.gov/datasets/docs/v2/

---

## ۸. سه اشتباه رایج

1. **دانلود XML به جای TSV، یا دانلود بی سنجش.** ‏۴٫۴ گیگابایت در برابر ۵۲۷ مگابایت؛ و `SNP_distances.tsv` ‏۱۶ گیگابایت است. نخست فهرست پوشه.
2. ‏**‏`pd.read_csv` روی فایل نیم‌گیگابایتی.** سطر به سطر بخوانید (`csv`)، یا تنها ستون‌های لازم را (`usecols`) و در تکه‌ها (`chunksize`).
3. **شمار ژنوم = شیوع.** آمریکا ۱۱٬۸۸۳ ژنوم CTX-M-15 دارد چون **بیشتر توالی‌یابی می‌کند** (برنامه‌های پایش ملی)، نه لزوماً چون CTX-M-15 در آن شایع‌تر است. داده‌ی عمومی نمونه‌ی **تصادفی** نیست.

---

## 📘 برای کنجکاوها

- ‏**ابر:** همه‌ی داده‌ی Pathogen Detection و MicroBIGG-E در Google BigQuery هم هست؛ یک پرسش SQL همین شمارش‌ها را بی دانلود ۵۰۰ مگابایت می‌دهد (فیلم NCBI Minute بالا).
- ‏**`computed_types`:** برای برخی گروه‌ها (مانند *Salmonella* و *E. coli*) نوع سرمی پیش‌بینی‌شده؛ و `AST_phenotypes` نتیجه‌ی آزمون حساسیت آزمایشگاهی، اگر ثبت‌کننده داده باشد. سنجیدن ژنوتیپ با فنوتیپ یکی از کاربردهای مهم این جدول است.
- ‏**درخت هر خوشه** در `SNP_trees/PDS….tar.gz` با قالب Newick است و با ابزارهای ماژول 08/04 (ggtree) خوانده می‌شود.

---

## جمع‌بندی

- ‏Pathogen Detection: هر ژنوم عمومی ← AMRFinderPlus ← خوشه‌ی SNP. نسخه‌ی تحلیل (`PDG…6392`) را گزارش کنید.
- ‏*E. coli/Shigella*: ‏۵۹۱٬۸۱۰ ایزوله؛ blaCTX-M-15 در ۱۳٪، بیشتر با gyrA_S83L و parC_S80I؛ ۷۷٫۵٪ حاملان در خوشه‌ها. ایران: ۵۰ حامل.
- خوشه‌ها: ‏۵۹٬۸۲۷، میانه ۲، بیشینه ۶۲۷۷؛ ۶۵٪ ایزوله‌ها در خوشه‌اند.
- ویروس‌ها با Datasets: SARS-CoV-2 مرجع ۲۹٬۹۰۳ باز؛ CCHFV ‏۵۴۷۱ رکورد، ۳۹۶ کامل، ایران ۱۷۷.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
F=https://ftp.ncbi.nlm.nih.gov/pathogen/Results/GROUP/latest_snps
curl -sS $F/AMR/ | sed 's/<[^>]*>/ /g' | grep PDG                 # sizes first
curl -sS -o amr.tsv $F/AMR/PDGxxx.amr.metadata.tsv
curl -sS -o clusters.tsv $F/Clusters/PDGxxx.reference_target.cluster_list.tsv
python3 amr_summary.py amr.tsv GENE clusters.tsv
datasets summary virus genome taxon "VIRUS NAME" --as-json-lines | dataformat tsv virus-genome --fields accession,completeness,segment,geo-location
datasets download virus genome accession ACC --filename v.zip
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏Pathogen Detection | سامانه‌ی NCBI برای سنجش AMR و خوشه‌بندی ژنوم‌های بیماری‌زا |
| ‏PDG / PDT / PDS | گروه و نسخه‌ی تحلیل / ایزوله / خوشه‌ی SNP |
| خوشه‌ی SNP | ژنوم‌هایی که تنها چند SNP با هم فاصله دارند |
| ‏MicroBIGG-E | جدول همه‌ی ژن‌های AMR، تنش و بیماری‌زایی یافته‌شده در همه‌ی ایزوله‌ها |
| ‏ESBL | بتالاکتامازی که سفالوسپورین‌های طیف گسترده را می‌شکند |
| ژن ذاتی (intrinsic) | ژنی که در همه‌ی افراد یک گونه هست (مانند blaEC در *E. coli*) |
| گسترش کلونی | پخش یک دودمان باکتری با ژن‌هایش |
| ‏ST131 | دودمان پرخطر جهانی *E. coli* با ESBL و مقاومت به کینولون |
| بخش ژنوم (segment) | یکی از چند مولکول RNA جدا در ژنوم برخی ویروس‌ها |
| سوگیری نمونه‌گیری | نماینده نبودن داده برای جمعیت، به علت شیوه‌ی گردآوری |

---

## منابع

**مقاله و مستند**
- ‏Feldgarden M, et al. (2021). *AMRFinderPlus and the Reference Gene Catalog facilitate examination of the genomic links among antimicrobial resistance, stress response, and virulence.* Scientific Reports 11:12728. https://doi.org/10.1038/s41598-021-91456-0
- ‏Nicolas-Chanoine MH, Bertrand X, Madec JY (2014). *Escherichia coli ST131, an intriguing clonal group.* Clin Microbiol Rev 27:543–574. https://doi.org/10.1128/CMR.00125-13
- ‏Hatcher EL, et al. (2017). *Virus Variation Resource – improved response to emergent viral outbreaks.* Nucleic Acids Res 45(D1):D482–D490. https://doi.org/10.1093/nar/gkw1065
- ‏Brister JR, et al. (2015). *NCBI Viral Genomes Resource.* Nucleic Acids Res 43(D1):D571–D577. https://doi.org/10.1093/nar/gku1207
- ‏O'Leary NA, et al. (2024). *Exploring and retrieving sequence and metadata for species across the tree of life with NCBI Datasets.* Scientific Data 11. https://doi.org/10.1038/s41597-024-03571-y
- ‏Pathogen Detection: https://www.ncbi.nlm.nih.gov/pathogens/ · راهنما: https://www.ncbi.nlm.nih.gov/pathogens/pathogens_help/ · MicroBIGG-E: https://www.ncbi.nlm.nih.gov/pathogens/microbigge/ · NCBI Virus: https://www.ncbi.nlm.nih.gov/labs/virus/vssi/

**کتاب**
- ‏Walsh C, Wencewicz T (2016). *Antibiotics: Challenges, Mechanisms, Opportunities.* ASM Press. (فصل‌های بتالاکتامازها و مقاومت به کینولون)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل‌های ژنوم باکتری‌ها و ویروس‌ها)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Whole genome sequencing of bacterial genomes - tools and applications* (Technical University of Denmark): https://www.coursera.org/learn/wgs-bacteria
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Introducing the NCBI Pathogen Detection Isolates Browser* (National Library of Medicine): https://www.youtube.com/watch?v=T8HluuzOb5c
- ‏YouTube: *NCBI Minute: Accessing NCBI AMR Pathogen Data in the Cloud* (National Library of Medicine): https://www.youtube.com/watch?v=j4dzFOo2FmI
- ‏YouTube: *Using the NCBI Pathogen Detection Pipeline as Part of the Epi Work Flow*: https://www.youtube.com/watch?v=8JkitjkNwYk
- ‏YouTube: *NCBI virus: download viral genomes in FASTA format* (OmicsLogic): https://www.youtube.com/watch?v=Uw5lP3vFSNY

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند؛ Isolates Browser، MicroBIGG-E و NCBI Virus وب‌اند (✍️) و همان داده از FTP و Datasets گرفته شد. DOIها با doi.org و صفحه‌ها با درخواست مستقیم وارسی شدند؛ فیلم‌ها با noembed.</sub>

</div>
