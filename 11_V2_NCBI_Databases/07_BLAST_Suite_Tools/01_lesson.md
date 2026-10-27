<div dir="rtl">

# درس: BLAST+ و ابزارهای کنارش؛ از جهش سل تا آغازگر PCR

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `07_BLAST_Suite_Tools` · **پیش‌نیاز:** ماژول [00/03](../../00_Orientation/03_Web_Tools/) (BLAST چه می‌کند)؛ ماژول [08/03](../../08_AMR_Virulence_Phylogeny/03_Mobile_Elements_CRISPR/) (`makeblastdb` و `blastn`)؛ ماژول [09/01](../../09_Structural_Bioinformatics/01_Protein_Structure/) (دو شماره‌گذاری rpoB)؛ ماژول‌های [11/01](../01_Entrez_EDirect/) و [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) · **زمان:** حدود ۱۰۰ دقیقه · **ابزار:** BLAST+ 2.17.0 (`makeblastdb`، `blastp`، `tblastn`، `blastn`، `-remote`)، Biopython 1.87، CD-Search (API)؛ Primer-BLAST و ORFfinder (✍️ وب) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده**، جز صفحه‌های وب Primer-BLAST و ORFfinder (✍️؛ همان کار با BLAST+ و Biopython روی سرور انجام شد). همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). هر جست‌وجوی محلی زیر ۰٫۲ ثانیه و ۷۵ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. برای هر پرسش، برنامه‌ی درست BLAST را برگزینید (`blastn`، `blastp`، `blastx`، `tblastn`، `tblastx`).
2. ‏**E-value**، **bit score**، درصد همانندی و **پوشش** را درست بخوانید و بدانید E-value به اندازه‌ی پایگاه وابسته است.
3. با یک هم‌ترازی BLAST، شماره‌ی جایگاه‌ها را از یک گونه به گونه‌ی دیگر ببرید (S450 سل ↔ S531 *E. coli*).
4. با `tblastn` یک ژن را در ژنوم بیابید و با `blastn-short` ویژگی آغازگرهای PCR را بسنجید.
5. ‏BLAST راه دور، ORF و دامنه‌های حفظ‌شده (CD-Search) را به کار ببرید.

**پیش از آغاز:** داده‌ی این درس از ماژول‌های پیشین است:

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m07 && cd ~/ncbi/m07
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
P=~/Bioinformatics_Learning-main/11_V2_NCBI_Databases/99_scripts_data
cp ~/ncbi/m01/prot5.faa .                                   # five E. coli resistance proteins (11/01)
curl -sS "$B/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text" > ecoli.fna
curl -sS "$B/efetch.fcgi?db=protein&id=NP_215181.1&rettype=fasta&retmode=text" > mtb_rpoB.faa
ls -la ecoli.fna; head -1 mtb_rpoB.faa
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
-rw-rw-r-- 1 ubuntu ubuntu 4708035 Oct 27 15:03 ecoli.fna
>NP_215181.1 DNA-directed RNA polymerase subunit beta [Mycobacterium tuberculosis H37Rv]
```

</div>

---

## ۱. داستان

در ماژول 09/01 جدولی دیدید: S531 در *E. coli* همان S450 در *M. tuberculosis* است. ولی این جدول از کجا آمد؟ کسی دو پروتئین را **هم‌تراز** کرده است. در این درس خودتان همین کار را می‌کنید و همان پاسخ را می‌گیرید. سپس همان پرسش‌های آزمایشگاه را می‌پرسیم: «ژن rpoB کجای ژنوم است؟»، «برای PCR ناحیه‌ی مقاومت، کدام آغازگرها تنها همین یک جا را می‌گیرند؟»، و «این پروتئین چه دامنه‌هایی دارد؟». ‏BLAST+ ابزار همه‌ی این پرسش‌هاست.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ پنج برنامه

| برنامه | پرسش (query) | پایگاه (database) | نمونه |
| :--- | :--- | :--- | :--- |
| ‏`blastn` | نوکلئوتید | نوکلئوتید | یک ژن در یک ژنوم؛ آغازگر (`-task blastn-short`) |
| ‏`blastp` | پروتئین | پروتئین | پروتئین سل در برابر پروتئین‌های *E. coli* |
| ‏`blastx` | نوکلئوتید (ترجمه در ۶ چارچوب) | پروتئین | یک contig ناشناخته: «چه پروتئینی را کد می‌کند؟» |
| ‏`tblastn` | پروتئین | نوکلئوتید (ترجمه در ۶ چارچوب) | یک پروتئین را در ژنومی بی annotation بیابید |
| ‏`tblastx` | نوکلئوتید (ترجمه) | نوکلئوتید (ترجمه) | دو ژنوم دور؛ کند |

**قاعده:** برای گونه‌های **دور**، در سطح **پروتئین** بسنجید: کد ژنتیکی تکراری است و جهش‌های خاموش DNA را زودتر از پروتئین دگرگون می‌کنند.

### ۲.۲ چهار عدد هر برخورد (hit)

| عدد | معنا | وابسته به |
| :--- | :--- | :--- |
| ‏**bit score** | نمره‌ی هم‌ترازی، نرمال‌شده | تنها خود هم‌ترازی |
| ‏**E-value** | شمار برخوردهایی با این نمره که **از شانس** در پایگاهی به این اندازه انتظار داریم | نمره **و اندازه‌ی پایگاه** |
| ‏**pident** | درصد همانندی | تنها بخش هم‌ترازشده |
| ‏**qcovs** | درصد پرسش که پوشیده شده | همه‌ی HSPها روی هم |

هر برخورد ممکن است چند **HSP** (High-scoring Segment Pair، تکه‌ی هم‌تراز) داشته باشد.

> 📺 **فیلم:** *How to run a local Blast against a custom database* (BioBam Bioinformatics): https://www.youtube.com/watch?v=ujCEp9ZwcJw
> 📄 **مرجع:** Altschul SF, et al. (1990). *Basic local alignment search tool.* J Mol Biol 215:403–410. https://doi.org/10.1016/S0022-2836(05)80360-2 · Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421

---

## ۳. گام ۱: پایگاه محلی و `blastp`

<div dir="ltr">

```bash
makeblastdb -in ecoli.fna -dbtype nucl -out ecoli -parse_seqids 2>&1 | grep added
makeblastdb -in prot5.faa -dbtype prot -out prot5 -parse_seqids 2>&1 | grep added
/usr/bin/time -f "time=%es maxRSS=%MKB" blastp -query mtb_rpoB.faa -db prot5 \
  -outfmt "6 qseqid sseqid pident length qlen slen qstart qend sstart send evalue bitscore qcovs"
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-parse_seqids` | شناسه‌ی هر توالی (`NC_000913.3`) را نگه دار تا در خروجی و `blastdbcmd` به کار آید |
| ‏`-outfmt "6 …"` | جدول Tab‌دار با ستون‌هایی که خودتان نام می‌برید |
| ‏`qlen`، `slen` | طول پرسش و طول هدف |
| ‏`qcovs` | پوشش پرسش با همه‌ی HSPهای همان هدف |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Adding sequences from FASTA; added 1 sequences in 0.0940011 seconds.
Adding sequences from FASTA; added 5 sequences in 0.0542581 seconds.
NP_215181.1	ref|NP_418414.1|	58.278	604	1172	1342	255	850	350	937	0.0	706	93
NP_215181.1	ref|NP_418414.1|	54.662	311	1172	1342	853	1131	1040	1339	3.20e-97	328	93
NP_215181.1	ref|NP_418414.1|	40.708	226	1172	1342	32	246	12	224	1.01e-46	172	93
NP_215181.1	ref|NP_418415.1|	71.429	14	1172	1407	687	700	1201	1214	0.17	25.0	11
NP_215181.1	ref|NP_418415.1|	27.068	133	1172	1407	759	875	1130	1250	0.30	24.3	11
NP_215181.1	ref|NP_418415.1|	28.571	28	1172	1407	794	821	1350	1377	6.0	20.0	11
NP_215181.1	ref|NP_414995.1|	45.455	22	1172	1049	950	971	706	727	0.52	23.5	5
NP_215181.1	ref|NP_414995.1|	26.000	50	1172	1049	854	888	577	626	7.2	19.6	5
NP_215181.1	ref|NP_417491.1|	50.000	12	1172	752	226	237	498	509	1.5	21.9	3
NP_215181.1	ref|NP_417491.1|	42.105	19	1172	752	892	910	654	672	9.1	19.2	3
time=0.10s maxRSS=69528KB
```

</div>

**توضیح خروجی:**
- **سه HSP** روی rpoB *E. coli* (`NP_418414.1`): ‏۵۸٪، ۵۵٪ و ۴۱٪ همانندی، E-value صفر تا ۱۰^−۴۶^، روی هم ۹۳٪ پرسش را می‌پوشانند. چرا سه تکه و نه یکی؟ پروتئین *E. coli* ‏۱۷۰ اسید آمینه بلندتر است (۱۳۴۲ در برابر ۱۱۷۲): میان تکه‌ها **درج‌هایی** دارد که در سل نیست (برای نمونه میان جایگاه ۹۳۷ و ۱۰۴۰ پروتئین *E. coli*). ‏BLAST هم‌ترازی را در جای درج‌های بزرگ می‌شکند.
- بقیه‌ی برخوردها (rpoC، acrB، parC) **ساختگی**‌اند: E-value بین ۰٫۱۷ و ۹٫۱، یعنی انتظار داریم چنین برخوردی از **شانس** هم پیدا شود. یکی ۷۱٪ همانندی دارد، ولی تنها روی **۱۴** اسید آمینه: درصد همانندی بالا روی هم‌ترازی کوتاه معنایی ندارد.
- قاعده‌ی سرانگشتی برای پروتئین: E-value کمتر از ۱۰^−۵^ و پوشش بالای ۵۰ تا ۷۰٪.

---

## ۴. گام ۲: بردن شماره‌ها از سل به *E. coli*

**چرا؟** این همان جدول 09/01 است. اسکریپت [map_positions.py](../99_scripts_data/07_BLAST_Suite_Tools/scripts/map_positions.py) هم‌ترازی را باز می‌خواند و برای هر جایگاه پرسش، جایگاه هم‌تراز هدف را می‌گوید:

<div dir="ltr">

```bash
blastp -query mtb_rpoB.faa -db prot5 -max_hsps 1 -max_target_seqs 1 -outfmt "6 qstart sstart qseq sseq" > hsp.tsv
python3 $P/07_BLAST_Suite_Tools/scripts/map_positions.py hsp.tsv 435 445 450 452
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-max_hsps 1 -max_target_seqs 1` | تنها بهترین تکه با بهترین هدف (HSP نخست بالا) |
| ‏`qseq`، `sseq` | خود دو رشته‌ی هم‌تراز، با `-` در جای شکاف |
| در اسکریپت | از `qstart` و `sstart` آغاز کن و روی دو رشته پیش برو؛ شکاف شمارنده‌ی همان رشته را بالا نمی‌برد |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Warning: [blastp] Examining 5 or more matches is recommended
query D435  <->  subject D516
query H445  <->  subject H526
query S450  <->  subject S531
query L452  <->  subject L533
```

</div>

**پاسخ معلوم برقرار است:** ‏D435 ↔ D516، H445 ↔ H526، S450 ↔ S531؛ درست جدول 09/01. فاصله‌ی ۸۱ اسید آمینه همان درج‌های آغاز پروتئین *E. coli* است. هشدار `Examining 5 or more matches` می‌گوید `-max_target_seqs 1` ممکن است بهترین برخورد واقعی را از دست بدهد (BLAST پیش از پایان، فهرست را کوتاه می‌کند)؛ این‌جا تنها یک rpoB در پایگاه هست، پس خطری ندارد.

---

## ۵. گام ۳: ‏`tblastn`؛ ژن در ژنوم، بی annotation

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" tblastn -query mtb_rpoB.faa -db ecoli -evalue 1e-10 \
  -outfmt "6 sseqid pident length qstart qend sstart send sframe evalue bitscore"
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
ref|NC_000913.3|	58.278	604	255	850	4182292	4184055	1	0.0	662
ref|NC_000913.3|	54.662	311	853	1131	4184362	4185261	1	1.94e-93	328
ref|NC_000913.3|	40.708	226	32	246	4181278	4181916	1	8.22e-44	172
time=0.13s maxRSS=75232KB
```

</div>

**توضیح خروجی:**
- همان سه تکه، این بار روی **ژنوم**: از 4181278 تا 4185261، در **چارچوب +1** (`sframe`). مختصات ژن rpoB از 11/01: ‏4181245..4185273. پس `tblastn` ژن را درست یافت، بی آنکه annotation ژنوم را بداند. این راه یافتن یک ژن در ژنوم تازه‌ای است که هنوز annotation ندارد (بخش ۰۷).
- ‏E-value و bit score کمی با `blastp` فرق دارند: پایگاه این بار ۴٫۶ میلیون باز در ۶ چارچوب است، نه ۵ پروتئین.

---

## ۶. گام ۴: E-value به اندازه‌ی پایگاه وابسته است

**چرا؟** E-value «شمار برخوردهای شانسی **در پایگاهی به این اندازه**» است. همان هم‌ترازی را با اندازه‌های گوناگون پایگاه بسنجیم (`-dbsize` اندازه را وانمود می‌کند):

<div dir="ltr">

```bash
for d in 0 1000000000 100000000000; do
  o=""; [ $d -gt 0 ] && o="-dbsize $d"
  echo "dbsize=$d: $(blastp -query mtb_rpoB.faa -db prot5 $o -outfmt '6 sseqid length pident evalue bitscore' \
      | awk '$1~/418414/ && $2==311 {print $4, $5} $1~/418415/ && $2==14 {print "rpoC 14aa:", $4, $5}' | paste -sd' ')"
done
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`o=""; [ $d -gt 0 ] && o="-dbsize $d"` | در نوبت نخست گزینه را نگذار (اندازه‌ی واقعی پایگاه) |
| ‏`awk '$1~/418414/ && $2==311'` | تنها HSP دوم rpoB (۳۱۱ اسید آمینه) |
| ‏`$2==14` | همان برخورد ساختگی ۱۴ اسید آمینه‌ای rpoC |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
dbsize=0: 3.20e-97 328 rpoC 14aa: 0.17 25.0
dbsize=1000000000: 5.89e-92 328
dbsize=100000000000: 5.89e-90 328
```

</div>

**توضیح خروجی:**
- ‏**bit score** همیشه **۳۲۸** است: هم‌ترازی همان است.
- ‏**E-value** با بزرگ شدن پایگاه **بالا** می‌رود (۱۰^−۹۷^ → ۱۰^−۹۰^): در پایگاه بزرگ‌تر، شانس پیدا کردن چنین برخوردی بیشتر است.
- برخورد ساختگی rpoC در پایگاه‌های بزرگ‌تر **ناپدید** شد: E-valueاش از آستانه‌ی پیش‌فرض (۱۰) گذشت.
- **درس:** E-value دو جست‌وجو روی دو پایگاه گوناگون را با هم نسنجید؛ bit score را بسنجید.

> 📄 **مرجع:** راهنمای BLAST (E-value، bit score، `outfmt`): https://blast.ncbi.nlm.nih.gov/doc/blast-help/

---

## ۷. گام ۵: سنجش آغازگرهای PCR

**چرا؟** برای تعیین توالی ناحیه‌ی مقاومت (RRDR، کُدون‌های ۵۰۷ تا ۵۳۳) در ایزوله‌های بالینی، باید آن را با PCR تکثیر کرد. آغازگر خوب: ۱۸ تا ۲۵ باز، GC نزدیک به ۵۰ تا ۶۰٪، Tm دو آغازگر نزدیک هم، و **تنها یک** جای اتصال در ژنوم.

نخست نامزدها را با Biopython (بخش ۰۳) بسنجیم. ‏`ec_rpoB.fna` ژن rpoB است (11/01: ‏4181245..4185273):

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text&seq_start=4181245&seq_stop=4185273" > ec_rpoB.fna
python3 - <<'EOF'
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqUtils import MeltingTemp as mt, gc_fraction
g = str(next(SeqIO.parse('ec_rpoB.fna', 'fasta')).seq)
f = g[1405:1425]                                   # forward: gene bases 1406-1425
r = str(Seq(g[1750:1770]).reverse_complement())    # reverse: gene bases 1751-1770
for name, p in (('rpoB_F1406', f), ('rpoB_R1770', r)):
    print(name, p, round(mt.Tm_NN(p), 1), round(gc_fraction(p) * 100))
print('amplicon:', 1770 - 1406 + 1, 'bp; codons', (1406 - 1) // 3 + 1, 'to', 1770 // 3)
EOF
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
rpoB_F1406 TACGTGTAGAGCGTGCGGTG 56.9 60
rpoB_R1770 CGGAGTCTCAAGGAAGCCGT 56.1 60
amplicon: 365 bp; codons 469 to 590
```

</div>

‏Tm ‏۵۶٫۹ و ۵۶٫۱ (نزدیک هم)، GC ‏۶۰٪، فراورده‌ی ۳۶۵ بازی که کُدون‌های ۴۶۹ تا ۵۹۰، یعنی همه‌ی RRDR، را در بر دارد. ‏`Tm_NN` دمای ذوب را با مدل «nearest-neighbor» برآورد می‌کند.

حالا **ویژگی** (specificity): آیا هر آغازگر تنها یک جا در ژنوم را می‌گیرد؟ یک آغازگر بد ۱۲ بازی هم برای سنجش می‌گذاریم:

<div dir="ltr">

```bash
printf ">rpoB_F1406\nTACGTGTAGAGCGTGCGGTG\n>rpoB_R1770\nCGGAGTCTCAAGGAAGCCGT\n>bad_12mer\nGCTGGCGCTGGC\n" > primers.fa
blastn -task blastn-short -query primers.fa -db ecoli -evalue 1000 \
  -outfmt "6 qseqid qlen length mismatch qstart qend sstart send sstrand evalue" > pr.tsv
awk '$2==$3 && $4==0 {c[$1]++} END{for(k in c) print k, c[k]}' pr.tsv | sort
awk '$1!="bad_12mer" && $2==$3 && $4==0' pr.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-task blastn-short` | تنظیم‌های ویژه‌ی توالی‌های کوتاه‌تر از ۳۰ باز (word size کوچک) |
| ‏`-evalue 1000` | برخوردهای ضعیف را هم نشان بده؛ برای آغازگر هر جای اتصال مهم است |
| ‏`$2==$3 && $4==0` | هم‌ترازی به **همه‌ی طول** آغازگر (`length` = `qlen`) و **بی جفت‌نشدگی** |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
bad_12mer 46
rpoB_F1406 1
rpoB_R1770 1
rpoB_F1406	20	20	0	1	20	4182650	4182669	plus	3.06e-05
rpoB_R1770	20	20	0	1	20	4183014	4182995	minus	3.06e-05
```

</div>

**توضیح خروجی:**
- هر آغازگر rpoB **یک** جای کامل دارد: F روی رشته‌ی **مثبت** از ۴۱۸۲۶۵۰، R روی رشته‌ی **منفی** تا ۴۱۸۳۰۱۴. فراورده: ‏۴۱۸۳۰۱۴ − ۴۱۸۲۶۵۰ + ۱ = **۳۶۵** باز؛ همان پیش‌بینی. (۴۱۸۱۲۴۵ + ۱۴۰۶ − ۱ = ۴۱۸۲۶۵۰.)
- آغازگر بد ۱۲ بازی **۴۶** جای کامل دارد: در PCR ده‌ها فراورده‌ی ناخواسته می‌سازد. آغازگر کوتاه و پر GC در ژنوم GC‌دار *E. coli* بارها تکرار می‌شود.
- برخوردهای ناقص (۱۲ از ۲۰ باز) هم در `pr.tsv` هستند (بیش از هزار برای هر آغازگر با `-evalue 1000`)؛ آن‌هایی مهم‌اند که **سر ۳′** آغازگر را می‌پوشانند، چون پلیمراز از سر ۳′ می‌سازد. تمرین ۴.

### ‏۷.۱ ‏Primer-BLAST ✍️ (از مستندات)

‏**Primer-BLAST** (https://www.ncbi.nlm.nih.gov/tools/primer-blast/) همین دو گام را با هم می‌کند: با **Primer3** آغازگر می‌سازد و با BLAST ویژگی‌اش را روی پایگاهی که برمی‌گزینید (مانند ژنوم *E. coli* با TaxID 562) می‌سنجد. گام‌ها: ‏`NC_000913.3` و بازه‌ی ۴۱۸۲۶۰۰ تا ۴۱۸۳۱۰۰ را در «PCR Template» بدهید؛ در «Primer Pair Specificity Checking Parameters» جاندار را *Escherichia coli* (taxid:562) بگذارید؛ «Get Primers». این ابزار API رسمی ندارد، پس در اسکریپت از همان BLAST+ بالا کار بکشید.

> 📺 **فیلم:** *How to Design Specific PCR Primers Using Primer-BLAST* (Roshan Ali Academy): https://www.youtube.com/watch?v=P2ctzK2ZbHY · *qPCR primer design with NCBI Primer-BLAST* (Bio-Lab): https://www.youtube.com/watch?v=D94a0H3G8JI
> 📄 **مرجع:** Ye J, et al. (2012). *Primer-BLAST: a tool to design target-specific primers for polymerase chain reaction.* BMC Bioinformatics 13:134. https://doi.org/10.1186/1471-2105-13-134 · Untergasser A, et al. (2012). *Primer3—new capabilities and interfaces.* Nucleic Acids Res 40:e115. https://doi.org/10.1093/nar/gks596

---

## ۸. گام ۶: ORF؛ چارچوب خواندن درست

**چرا؟** ‏`tblastn` گفت ژن در چارچوب +1 است. بی BLAST، می‌شد بلندترین **ORF** (چارچوب خواندن باز: از ATG تا کُدون پایان) را در شش چارچوب جست. ‏ORFfinder در وب NCBI (https://www.ncbi.nlm.nih.gov/orffinder/) همین را می‌کند (✍️)؛ اسکریپت [six_frames.py](../99_scripts_data/07_BLAST_Suite_Tools/scripts/six_frames.py) ساده‌ترین شکل آن است:

<div dir="ltr">

```bash
python3 $P/07_BLAST_Suite_Tools/scripts/six_frames.py ec_rpoB.fna
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
NC_000913.3:4181245-4185273: 4029 bp
frame +1: longest ORF 1342 aa  MVYSYTEKKRIR...
frame +2: longest ORF 69 aa  MVTTSKTPSSYP...
frame +3: no ORF >= 30 aa
frame -1: longest ORF 962 aa  MVAVHDVFIHLG...
frame -2: longest ORF 77 aa  MYSTGTSISLTS...
frame -3: longest ORF 34 aa  MHGWRHRVPGTG...
```

</div>

**توضیح خروجی:**
- چارچوب **+1**: ‏**۱۳۴۲** اسید آمینه با آغاز `MVYSYTEKKRIR`، درست همان `NP_418414.1` (11/01).
- **شگفتی:** چارچوب **−1** (رشته‌ی مقابل) یک ORF ‏**۹۶۲** اسید آمینه‌ای دارد! این یک **ORF سایه** (shadow ORF) است: در ژن‌های GC‌دار، رشته‌ی مقابل کمتر کُدون پایان دارد (کُدون‌های پایان AT‌دارند)، پس ORFهای بلند ساختگی پدید می‌آیند. هیچ پروتئینی از آن ساخته نمی‌شود.
- **درس:** طول ORF به‌تنهایی ژن بودن را ثابت نمی‌کند؛ ابزارهای annotation (Prokka/Bakta، بخش ۰۷) شباهت به پروتئین‌های شناخته‌شده و الگوی کُدون را هم می‌سنجند.

---

## ۹. گام ۷: دامنه‌ها با CD-Search

**چرا؟** در 11/02 نام سه دامنه‌ی گیرنده‌ی گلوکوکورتیکوئید را از CDD گرفتیم، ولی نه **جای** آن‌ها را. ‏CD-Search (همان BLAST در برابر مدل‌های CDD، با `rpsblast`) جای دامنه‌ها را می‌دهد. پایگاه CDD برای `rpsblast` محلی چند گیگابایت است؛ پس از API دسته‌ای NCBI کار می‌کشیم:

<div dir="ltr">

```bash
U=https://www.ncbi.nlm.nih.gov/Structure/bwrpsb/bwrpsb.cgi
curl -sS -X POST "$U" -d "queries=NP_000167.1&queries=NP_418414.1&db=cdd&smode=auto&useid1=true&compbasedadj=1&filter=true&evalue=0.01&tdata=hits" > cds_submit.txt
head -4 cds_submit.txt
ID=$(grep -oE 'QM3-[A-Za-z0-9_-]+' cds_submit.txt | head -1)
until curl -sS "$U?cdsid=$ID&tdata=hits" > cds_hits.txt && grep -q '^#status	0' cds_hits.txt; do sleep 5; done
grep -E '^Q#' cds_hits.txt | cut -f1-9
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-X POST … -d "queries=…"` | کار را بفرست؛ هر `queries=` یک پروتئین (accession یا توالی) |
| ‏`cdsid` | شماره‌ی کار، مانند WebEnv در E-utilities |
| ‏`until … do sleep 5; done` | هر ۵ ثانیه بپرس تا `#status 0` (پایان) بیاید |
| ‏`tdata=hits` | خروجی جدولی برخوردها |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
#Batch CD-search tool	NIH/NLM/NCBI
#cdsid	QM3-qcdsearch-EE0C2BEACA43DBF-25CF5CDC664FA70
#datatype	hitsConcise Results
#status	3	msg	Job is still running
Q#1 - NP_000167.1	specific	426625	26	401	0	681.987	pfam02155	GCR
Q#1 - NP_000167.1	specific	132761	531	777	0	536.438	cd07076	NR_LBD_GR
Q#1 - NP_000167.1	specific	143546	417	494	4.34812e-56	186.19	cd07172	NR_DBD_GR_PR
Q#2 - NP_418414.1	specific	234749	1	1342	0	2281.56	PRK00405	rpoB
Q#2 - NP_418414.1	superfamily	469606	972	1029	0.000244436	40.9845	cl00082	HMG-box_SF superfamily
```

</div>

**توضیح خروجی:**
- گیرنده‌ی گلوکوکورتیکوئید (۷۷۷ اسید آمینه): بخش آغازی **GCR** ‏۲۶ تا ۴۰۱، **DBD** ‏۴۱۷ تا ۴۹۴ (۷۸ اسید آمینه، دو انگشت روی) و **LBD** ‏۵۳۱ تا ۷۷۷ (تا پایان پروتئین). حالا روشن است چرا GRβ (‏۷۴۲، 11/02) دگزامتازون نمی‌گیرد: پایان پروتئینش، یعنی بخشی از **LBD**، فرق دارد.
- ‏rpoB: یک مدل تمام‌قد (PRK00405، ۱ تا ۱۳۴۲)، همان یافته‌ی 11/02؛ و یک برخورد **ضعیف** با ابرخانواده‌ی HMG-box (E-value ‏۲٫۴ × ۱۰^−۴^، ۵۸ اسید آمینه). ‏HMG-box دامنه‌ی اتصال به DNA در پروتئین‌های **یوکاریوتی** است؛ این برخورد احتمالاً یک شباهت دور یا شانسی است. برخوردهای ضعیف را با زیست‌شناسی پروتئین بسنجید.

> 📺 **فیلم:** *Gene Conserved Domains* (Abnova): https://www.youtube.com/watch?v=UX7amIyT3xw
> 📄 **مرجع:** Marchler-Bauer A, Bryant SH (2004). *CD-Search: protein domain annotations on the fly.* Nucleic Acids Res 32:W327–W331. https://doi.org/10.1093/nar/gkh454 · راهنمای CDD: https://www.ncbi.nlm.nih.gov/Structure/cdd/cdd_help.shtml

---

## ۱۰. گام ۸: BLAST راه دور

**چرا؟** پایگاه‌های بزرگ NCBI (nr، Swiss-Prot، core_nt) را نمی‌شود روی لپ‌تاپ نگه داشت. ‏`-remote` همان دستور BLAST+ را روی سرورهای NCBI اجرا می‌کند. ناحیه‌ی RRDR پروتئین سل (جایگاه‌های ۴۲۶ تا ۴۵۲) را در برابر Swiss-Prot بفرستیم:

<div dir="ltr">

```bash
python3 -c "
from Bio import SeqIO
s = str(next(SeqIO.parse('mtb_rpoB.faa', 'fasta')).seq)
open('rrdr.faa', 'w').write('>Mtb_RpoB_426-452\n' + s[425:452] + '\n'); print(s[425:452], len(s[425:452]))"
/usr/bin/time -f "time=%es maxRSS=%MKB" timeout 900 blastp -remote -db swissprot -query rrdr.faa -max_target_seqs 10 \
  -outfmt "6 sseqid pident length qcovs evalue bitscore sscinames" > remote.tsv 2> remote.err; echo rc=$?
wc -l < remote.tsv
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
GTSQLSQFMDQNNPLSGLTHKRRLSAL 27
rc=124
0
```

</div>

**نتیجه‌ی واقعی:** پس از **۱۵ دقیقه** (`timeout 900`) هیچ پاسخی نیامد (`rc=124` = زمان تمام شد). ‏`-remote` کار را در **صف** سرورهای NCBI می‌گذارد و تا پایان می‌ایستد؛ زمان صف به بار سرور بستگی دارد، نه به اندازه‌ی پرسش. برای دیدن آنچه در پشت `-remote` رخ می‌دهد، همان را با **URL API** BLAST فرستادیم:

<div dir="ltr">

```bash
U=https://blast.ncbi.nlm.nih.gov/Blast.cgi
curl -sS -X POST "$U" --data-urlencode "CMD=Put" --data-urlencode "PROGRAM=blastp" --data-urlencode "DATABASE=swissprot" \
     --data-urlencode "QUERY=GTSQLSQFMDQNNPLSGLTHKRRLSAL" --data-urlencode "HITLIST_SIZE=10" > put.html
grep -oE 'RID = [A-Z0-9]+|RTOE = [0-9]+' put.html
R=$(grep -oE 'RID = [A-Z0-9]+' put.html | awk '{print $3}')
curl -sS "$U?CMD=Get&FORMAT_OBJECT=SearchInfo&RID=$R" | grep -oE 'Status=[A-Z]+'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
RID = E13YYMUD014
RTOE = 2
Status=WAITING
```

</div>

**توضیح خروجی:**
- ‏**RID** (Request ID) شماره‌ی کار در صف است، مانند `cdsid` در CD-Search (گام ۷) و WebEnv در E-utilities. ‏**RTOE** برآورد زمان پایان به ثانیه است: ۲.
- ولی وضعیت (`Status`) بیش از **۲۵ دقیقه** `WAITING` ماند. ما نخست هر ۳۰ ثانیه پرسیدیم، که **بیش از اندازه** است (پایین را ببینید)؛ سپس هر ۶۵ ثانیه. وقتی `READY` شد، نتیجه با `CMD=Get&FORMAT_TYPE=Tabular&RID=…` گرفته می‌شود.
- **درس:** BLAST راه دور برای چند جست‌وجوی گاه‌به‌گاه است، نه برای گردش کار. NCBI می‌خواهد بیش از یک درخواست در ۱۰ ثانیه و بیش از یک بار در دقیقه برای پرسیدن وضعیت یک RID نفرستید. برای کار جدی، پایگاه را دانلود کنید (`update_blastdb.pl --decompress swissprot`) یا BLAST را در ابر اجرا کنید (ElasticBLAST).

> 📺 **فیلم:** *How to run a local Blast against a custom database* (BioBam Bioinformatics): https://www.youtube.com/watch?v=ujCEp9ZwcJw
> 📄 **مرجع:** ‏BLAST URL API (Put/Get، RID): https://blast.ncbi.nlm.nih.gov/doc/blast-help/developerinfo.html · راهنمای BLAST: https://blast.ncbi.nlm.nih.gov/doc/blast-help/

---

## ۱۱. سه اشتباه رایج

1. **درصد همانندی بی طول.** ‏۷۱٪ روی ۱۴ اسید آمینه (rpoC، گام ۱) ساختگی است و ۴۱٪ روی ۲۲۶ اسید آمینه (rpoB) واقعی. همیشه `length`، `qcovs` و E-value را کنار هم ببینید.
2. **سنجیدن E-value میان دو پایگاه.** همان هم‌ترازی در پایگاه ۱۰۰ برابر بزرگ‌تر، E-value ‏۱۰۰ برابر بزرگ‌تر دارد (گام ۴). برای مقایسه bit score.
3. ‏**‏`blastn` معمولی برای آغازگر.** تنظیم پیش‌فرض (`megablast`، word size ‏۲۸) برای توالی ۲۰ بازی هیچ برخوردی نمی‌یابد؛ `-task blastn-short` لازم است.

---

## 📘 برای کنجکاوها

- ‏**`-max_target_seqs`** فیلتر پس از جست‌وجو نیست؛ BLAST در میانه‌ی کار فهرست را کوتاه می‌کند و ممکن است بهترین برخورد را از دست بدهد (هشدار گام ۲). برای کاهش خروجی، بهتر است با `-evalue` یا پس از جست‌وجو با `sort | head` پالایش کنید.
- ‏**پایگاه‌های آماده‌ی NCBI** (`swissprot`، `refseq_protein`، `core_nt`) را با `update_blastdb.pl` می‌توان گرفت؛ `core_nt` صدها گیگابایت است.
- ‏**ClusteredNR:** در وب NCBI برای blastp گزینه‌ی nr **خوشه‌بندی‌شده** هم هست: هر خوشه‌ی پروتئین‌های نزدیک یک نماینده دارد، پس نتیجه‌ها گوناگون‌ترند و تکرار کمتر (مانند IPG در 11/02).

---

## جمع‌بندی

- ‏blastp: ‏RpoB سل در برابر *E. coli*: سه HSP، ۴۱ تا ۵۸٪ همانندی، پوشش ۹۳٪؛ برخوردهای دیگر با E-value بالای ۰٫۱ ساختگی‌اند.
- ‏`map_positions.py`: ‏S450 ↔ S531، H445 ↔ H526، D435 ↔ D516 (پاسخ معلوم 09/01).
- ‏tblastn: rpoB در 4181278..4185261، چارچوب +1، بی annotation.
- ‏E-value با اندازه‌ی پایگاه بالا می‌رود؛ bit score نه.
- آغازگرهای F1406/R1770: هر کدام یک جای کامل؛ فراورده‌ی ۳۶۵ بازی RRDR. آغازگر بد ۱۲ بازی: ۴۶ جا.
- ‏ORF: ‏۱۳۴۲ اسید آمینه در +1، و یک ORF سایه‌ی ۹۶۲ در −1.
- ‏CD-Search: جای سه دامنه‌ی GR (GCR، DBD ‏۴۱۷–۴۹۴، LBD ‏۵۳۱–۷۷۷).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
makeblastdb -in seqs.fa -dbtype nucl|prot -out DB -parse_seqids
blastp|blastn|tblastn -query Q -db DB -evalue 1e-5 -outfmt "6 qseqid sseqid pident length qstart qend sstart send evalue bitscore qcovs"
blastp … -max_hsps 1 -max_target_seqs 1 -outfmt "6 qstart sstart qseq sseq" > hsp.tsv; python3 map_positions.py hsp.tsv POS…
blastn -task blastn-short -query primers.fa -db GENOME -evalue 1000 -outfmt "6 qseqid qlen length mismatch sstart send sstrand"
python3 six_frames.py gene.fna
curl -X POST …/bwrpsb.cgi -d "queries=ACC&db=cdd&tdata=hits"; then poll ?cdsid=ID
blastp -remote -db swissprot -query Q.faa
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏HSP | یک تکه‌ی هم‌تراز با نمره‌ی بالا میان پرسش و هدف |
| ‏bit score | نمره‌ی نرمال‌شده‌ی هم‌ترازی، ناوابسته به پایگاه |
| ‏E-value | شمار برخوردهای شانسی با همین نمره، در پایگاهی به همین اندازه |
| پوشش (coverage) | درصد پرسش که در هم‌ترازی آمده است |
| درج (insertion) | تکه‌ای که در یک توالی هست و در دیگری نیست |
| چارچوب خواندن (frame) | یکی از سه راه خواندن کُدون‌ها روی هر رشته |
| ‏ORF | تکه‌ای از ATG تا کُدون پایان، بی کُدون پایان در میانه |
| ‏ORF سایه | ‏ORF بلند ساختگی روی رشته‌ی مقابل یک ژن |
| آغازگر (primer) | ‏DNA کوتاهی که PCR از آن آغاز می‌شود |
| ‏Tm | دمایی که نیمی از آغازگرها از DNA جدا می‌شوند |
| ویژگی (specificity) | گرفتن تنها یک جای هدف |
| ‏RRDR | ناحیه‌ی تعیین‌کننده‌ی مقاومت به ریفامپیسین در rpoB |

---

## منابع

**مقاله و مستند**
- ‏Altschul SF, et al. (1990). *Basic local alignment search tool.* J Mol Biol 215:403–410. https://doi.org/10.1016/S0022-2836(05)80360-2
- ‏Camacho C, et al. (2009). *BLAST+: architecture and applications.* BMC Bioinformatics 10:421. https://doi.org/10.1186/1471-2105-10-421
- ‏Ye J, et al. (2012). *Primer-BLAST.* BMC Bioinformatics 13:134. https://doi.org/10.1186/1471-2105-13-134
- ‏Untergasser A, et al. (2012). *Primer3—new capabilities and interfaces.* Nucleic Acids Res 40:e115. https://doi.org/10.1093/nar/gks596
- ‏Marchler-Bauer A, Bryant SH (2004). *CD-Search.* Nucleic Acids Res 32:W327–W331. https://doi.org/10.1093/nar/gkh454
- ‏Jin DJ, Gross CA (1988). *Mapping and sequencing of mutations in the Escherichia coli rpoB gene that lead to rifampicin resistance.* J Mol Biol 202:45–58. https://doi.org/10.1016/0022-2836(88)90517-7 (RRDR)
- راهنمای BLAST: https://blast.ncbi.nlm.nih.gov/doc/blast-help/ · Primer-BLAST: https://www.ncbi.nlm.nih.gov/tools/primer-blast/ · ORFfinder: https://www.ncbi.nlm.nih.gov/orffinder/

**کتاب**
- ‏Korf I, Yandell M, Bedell J (2003). *BLAST.* O'Reilly. (فصل‌های آمار E-value و ماتریس‌های نمره)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل‌های ۳ تا ۵: هم‌ترازی دوتایی و BLAST)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioinformatics Methods I* (University of Toronto؛ BLAST و هم‌ترازی): https://www.coursera.org/learn/bioinformatics-methods-1
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *How to run a local Blast against a custom database* (BioBam Bioinformatics): https://www.youtube.com/watch?v=ujCEp9ZwcJw
- ‏YouTube: *How to Design Specific PCR Primers Using Primer-BLAST* (Roshan Ali Academy): https://www.youtube.com/watch?v=P2ctzK2ZbHY
- ‏YouTube: *qPCR primer design with NCBI Primer-BLAST* (Bio-Lab): https://www.youtube.com/watch?v=D94a0H3G8JI

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند؛ Primer-BLAST و ORFfinder وب‌اند (✍️). DOIها با doi.org، صفحه‌ها با درخواست مستقیم وارسی شدند؛ فیلم‌ها با noembed.</sub>

</div>
