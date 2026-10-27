<div dir="rtl">

# پاسخ تشریحی: BLAST+ و ابزارهای کنارش

همه‌ی خروجی‌ها واقعی‌اند (BLAST+ 2.17.0، Biopython 1.87؛ روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: یک تکه‌ی ناشناخته

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=nuccore&id=NC_000913.3&rettype=fasta&retmode=text&seq_start=3164001&seq_stop=3165000" > mystery.fna
blastx -query mystery.fna -db prot5 -evalue 1e-5 -outfmt "6 sseqid pident length qstart qend sstart send qframe evalue bitscore"
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ref|NP_417491.1|	100.000	332	998	3	326	657	-3	0.0	675
ref|NP_416734.1|	26.316	380	995	9	330	706	-3	2.04e-27	103
```

</div>

(الف) ‏**`blastx`**: پرسش نوکلئوتید، پایگاه پروتئین. برخورد اصلی **ParC** (`NP_417491.1`)، **۱۰۰٪** همانندی روی ۳۳۲ اسید آمینه (جایگاه‌های ۳۲۶ تا ۶۵۷ پروتئین)، در چارچوب **−3**: ژن روی رشته‌ی منفی است (درس 11/01: parC ‏3165972→3163714). ‏`qstart` (۹۹۸) بزرگ‌تر از `qend` (۳) است، چون هم‌ترازی روی رشته‌ی مقابل خوانده شده.
(ب) **GyrA** (`NP_416734.1`)، ۲۶٪ روی ۳۸۰ اسید آمینه با E-value ‏۲ × ۱۰^−۲۷^. همانندی کم است ولی هم‌ترازی **بلند** است و E-value بسیار کوچک؛ پس شباهت واقعی است: ParC (توپوایزومراز IV) و GyrA (ژیراز) از یک ژن نیایی آمده‌اند (هم‌خانواده؛ تمرین ۳). برای پروتئین، ۲۵ تا ۳۰٪ همانندی روی بیش از ۱۰۰ اسید آمینه در بسیاری از موارد هم‌تباری (homology) را نشان می‌دهد.

---

## پاسخ ۲: ‏GyrA سل و جایگاه‌های مقاومت به کینولون

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=protein&id=NP_214520.1&rettype=fasta&retmode=text" > mtb_gyrA.faa
head -1 mtb_gyrA.faa
blastp -query mtb_gyrA.faa -db prot5 -outfmt "6 sseqid pident length qstart qend sstart send evalue bitscore qcovs" | head -4
blastp -query mtb_gyrA.faa -db prot5 -max_hsps 1 -max_target_seqs 1 -outfmt "6 qstart sstart qseq sseq" > gyr_hsp.tsv 2>/dev/null
python3 $P/07_BLAST_Suite_Tools/scripts/map_positions.py gyr_hsp.tsv 90 91 94
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
>NP_214520.1 DNA gyrase subunit A [Mycobacterium tuberculosis H37Rv]
ref|NP_416734.1|	44.807	857	15	834	8	857	0.0	733	98
ref|NP_417491.1|	34.732	691	13	687	3	659	1.64e-125	385	95
ref|NP_417491.1|	19.474	190	621	806	499	674	0.003	30.0	95
ref|NP_417491.1|	31.429	35	565	599	641	674	0.25	23.9	95
query A90  <->  subject S83
query S91  <->  subject A84
query D94  <->  subject D87
```

</div>

(الف) ‏GyrA *E. coli* (`NP_416734.1`): ‏۴۵٪ همانندی در **یک** HSP بلند (۸۵۷ اسید آمینه)، پوشش ۹۸٪. (‏`2>/dev/null` هشدار «Examining 5 or more matches» را پنهان می‌کند.)
(ب) ‏**A90 ↔ S83**، S91 ↔ A84 و **D94 ↔ D87**. جهش‌های مقاومت به کینولون در *E. coli* بیشتر در S83 و D87 (S83L، D87N؛ بخش ۰۸) و در سل در A90 و D94 (A90V، D94G) است: همان دو جایگاه، با دو شماره‌گذاری. این ناحیه **QRDR** (Quinolone Resistance-Determining Region) نام دارد. در جایگاه نخست سل آلانین دارد و *E. coli* سرین؛ پس «S83L» در سل هم‌ارز ندارد و جهش سل در همان جا A90V است.

---

## پاسخ ۳: هم‌خانواده‌ها (paralog)

(الف) از خروجی پاسخ ۲: ‏GyrA سل با ParC *E. coli* ‏**۳۵٪** همانند است روی ۶۹۱ اسید آمینه (E-value ‏۱۰^−۱۲۵^)، با پوشش ۹۵٪.
(ب) ‏GyrA و ParC در هر ژنوم باکتری هر دو هستند و به هم شبیه‌اند. اگر ژنوم تازه‌ای تنها یکی را داشته باشد یا یکی ناقص اسمبل شده باشد، بهترین برخورد BLAST ممکن است **هم‌خانواده‌ی نادرست** را نشان دهد و ژن را نادرست نام‌گذاری کنید. راه درست: برخورد را با **هر دو** هم‌خانواده بسنجید (این‌جا ۴۵٪ در برابر ۳۵٪، bit score ‏۷۳۳ در برابر ۳۸۵)، و از **BLAST دوسویه** (reciprocal best hit) کار بکشید: اگر A بهترین برخورد B است و B هم بهترین برخورد A، احتمالاً **هم‌ارز** (ortholog) هستند.

---

## پاسخ ۴: سر ۳′ آغازگر

<div dir="ltr">

```bash
awk '$1=="rpoB_F1406" && $6==20 && $3>=15' pr.tsv
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
rpoB_F1406	20	20	0	1	20	4182650	4182669	plus	3.06e-05
rpoB_F1406	20	15	1	6	20	3232256	3232270	plus	7.2
rpoB_F1406	20	18	2	3	20	4625160	4625143	minus	28
```

</div>

(الف) جز خود هدف، **دو** برخورد ناقص که سر ۳′ (باز ۲۰) را می‌پوشانند: ۱۵ باز با ۱ جفت‌نشدگی در ۳٬۲۳۲٬۲۵۶، و ۱۸ باز با ۲ جفت‌نشدگی در ۴٬۶۲۵٬۱۴۳ (رشته‌ی منفی). هیچ‌کدام کامل نیستند و آغازگر R در کنارشان نیست، پس فراورده‌ی PCR ناخواسته‌ای از آن‌ها انتظار نمی‌رود؛ ولی در دمای اتصال پایین ممکن است آغازگر را «بدزدند».
(ب) ‏DNA پلیمراز تنها از **سر ۳′** آغازگر می‌سازد. اگر ۱۵ باز ۳′ جفت شوند، پلیمراز آغاز می‌کند هرچند ۵′ آزاد باشد. اگر تنها ۵′ جفت شود و ۳′ آزاد بماند، پلیمراز جایی برای آغاز ندارد. به همین علت Primer-BLAST جفت‌نشدگی‌های نزدیک ۳′ را سخت‌تر می‌شمارد.

---

## پاسخ ۵: ‏ORF در تکه‌ای از ژن روی رشته‌ی منفی

<div dir="ltr">

```bash
python3 $P/07_BLAST_Suite_Tools/scripts/six_frames.py mystery.fna
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
NC_000913.3:3164001-3165000: 1000 bp
frame +1: longest ORF 30 aa  MVTGSDGSMSCS...
frame +2: no ORF >= 30 aa
frame +3: longest ORF 191 aa  MAFSAAYPAHLR...
frame -1: no ORF >= 30 aa
frame -2: longest ORF 41 aa  MAGVPPRYRAPP...
frame -3: longest ORF 327 aa  MIGLDGRPAVKN...
```

</div>

(الف) چارچوب **−3** با **۳۲۷** اسید آمینه: همان چارچوب `blastx` (پاسخ ۱). چارچوب +3 یک ORF سایه‌ی ۱۹۱ اسید آمینه‌ای دارد (همان پدیده‌ی گام ۶ درس).
(ب) تکه‌ی ۱۰۰۰ بازی **از میانه‌ی** ژن parC است: آغاز واقعی پروتئین (۷۵۲ اسید آمینه) بیرون از این تکه است. اسکریپت ORF را از نخستین `M` پس از یک کُدون پایان یا آغاز تکه می‌گیرد، که یک **متیونین درونی** است (`blastx` پوشش را از جایگاه ۳۲۶ پروتئین نشان داد). درس: ORFfinder روی تکه‌های ناقص، ORF ناقص می‌دهد؛ ORFfinder وب گزینه‌ی «ignore nested ORFs» و آغاز با «any sense codon» برای همین دارد.

---

## پاسخ ۶: E-value را پیش‌بینی کنید

(الف) پیش‌بینی: ده برابر، یعنی ‏**۵٫۸۹ × ۱۰^−۹۱^**.

<div dir="ltr">

```bash
blastp -query mtb_rpoB.faa -db prot5 -dbsize 10000000000 -outfmt '6 sseqid length evalue bitscore' | awk '$1~/418414/ && $2==311'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
ref|NP_418414.1|	311	5.89e-91	328
```

</div>

درست همان. ‏E = m × n × 2^−S^ (m طول پرسش، n اندازه‌ی پایگاه، S bit score): با ۱۰ برابر شدن n، E هم ۱۰ برابر می‌شود.
(ب) ‏bit score همان **۳۲۸** می‌ماند.

---

## پاسخ ۷ (اندیشیدنی): گزارش یک برخورد

برخورد ۷۱٪ با RpoC در گام ۱ تنها **۱۴** اسید آمینه است، با E-value ‏**۰٫۱۷** و پوشش ۱۱٪: یعنی انتظار داریم چنین برخوردی را از **شانس** هم ببینیم. این هیچ چیزی درباره‌ی کارکرد پروتئین نمی‌گوید. همراه درصد همانندی باید گزارش کند: **طول هم‌ترازی**، **پوشش پرسش** (`qcovs`)، **E-value** (با نام و اندازه‌ی پایگاه) و **bit score**؛ و برای نام‌گذاری کارکرد، پوشش بالا (بیش از ۷۰٪) و E-value بسیار کوچک (کمتر از ۱۰^−۱۰^) و ترجیحاً دامنه‌های حفظ‌شده (CD-Search) را هم بسنجد.

---

## برای خواندن بیشتر

- ‏Korf I, Yandell M, Bedell J (2003). *BLAST.* O'Reilly. (آمار Karlin–Altschul و E-value)
- ‏Jin DJ, Gross CA (1988). J Mol Biol 202:45–58 (RRDR در *E. coli*). https://doi.org/10.1016/0022-2836(88)90517-7
- ‏YouTube: *How to run a local Blast against a custom database* (BioBam): https://www.youtube.com/watch?v=ujCEp9ZwcJw

</div>
