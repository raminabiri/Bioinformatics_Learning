<div dir="rtl">

# درس: خانواده و دامنه‌ی پروتئین؛ InterPro، Pfam و HMMER

**بخش:** `12_V2_Global_Databases_Browsers` · **ماژول:** `04_Protein_Families_Domains` · **پیش‌نیاز:** ‏BLAST+ و CD-Search ([11/07](../../11_V2_NCBI_Databases/07_BLAST_Suite_Tools/))؛ ژن‌های مقاومت ([08/01](../../08_AMR_Virulence_Phylogeny/01_AMR_Resistance_Genes/))؛ `curl` و `jq` ([12/01](../01_Ensembl_BioMart/)) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** InterPro API (release 110.0، Pfam 38.2)، HMMER 3.4 (محیط `databases`)، BLAST+ 2.17.0؛ InterProScan و eggNOG-mapper (وب، ✍️) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده**، جز InterProScan و eggNOG-mapper که تنها وب‌اند (✍️). همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). هر جست‌وجوی HMMER کمتر از ۰٫۱ ثانیه و ۱۳ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. **دامنه**، **خانواده**، **ابرخانواده** و **clan** را از هم جدا کنید.
2. منطق **profile HMM** را به زبان ساده بگویید و بدانید چرا از BLAST حساس‌تر است.
3. با **InterPro API** دامنه‌های یک پروتئین را از Pfam و دوازده پایگاه دیگر بگیرید.
4. با **`hmmscan`** و **`hmmsearch`** دامنه‌ها را خودتان بیابید و با آستانه‌ی **GA** بسنجید.
5. بدانید **InterProScan** و **eggNOG-mapper** کی به کار می‌آیند، و چرا «دامنه‌ی X دارد» یعنی «کار X را می‌کند» نیست.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/global/m04 && cd ~/global/m04
conda activate databases
P=~/Bioinformatics_Learning-main/12_V2_Global_Databases_Browsers/99_scripts_data
bash $P/04_Protein_Families_Domains/data/download.sh      # query.faa, mini_pfam.hmm, ecoli.faa
I=https://www.ebi.ac.uk/interpro/api
```

</div>

---

## ۱. داستان

در بخش ۰۸ دو ایزوله‌ی مقاوم دیدید: `isoA` با ژن **blaCTX-M-15** و `isoB` با ژن **blaNDM-1**. هر دو آنزیم «**بتالاکتاماز**» نام دارند: حلقه‌ی بتالاکتام پنی‌سیلین‌ها و سفالوسپورین‌ها را می‌شکنند. آیا خویشاوندند؟ در 11/07 هم با CD-Search دیدید گیرنده‌ی گلوکوکورتیکوئید سه بخش دارد (GCR، ‏DBD، ‏LBD). این‌ها **دامنه**‌اند: تکه‌هایی از پروتئین که جداگانه تا می‌خورند و در پروتئین‌های بسیاری تکرار می‌شوند.

**پاسخ معلوم (Ambler 1980؛ Bush و Jacoby 2010):** بتالاکتامازها چهار رده دارند:

| رده | سازوکار | نمونه | خویشاوند |
| :---: | :--- | :--- | :--- |
| ‏**A** | سرین | ‏TEM-1، CTX-M-15، KPC-2 | پروتئین‌های متصل به پنی‌سیلین (PBP) |
| ‏**C** | سرین | ‏AmpC ‏*E. coli* | ‏PBP |
| ‏**D** | سرین | ‏OXA-48 | ‏PBP |
| ‏**B** | فلز (روی) | ‏NDM-1 | **هیچ‌کدام از بالا**؛ ساختار جدا |

یعنی سه رده‌ی سرینی از یک نیا هستند، که خودش از **PBP**‌ها، آنزیم‌های ساخت دیواره‌ی سلولی و هدف خود بتالاکتام‌ها، آمده است. رده‌ی B کار مشابهی را با ساختاری دیگر انجام می‌دهد (**هم‌گرایی**). این درس همین را از داده بیرون می‌کشد.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ چهار واژه

| واژه | معنا | نمونه |
| :--- | :--- | :--- |
| **دامنه** (domain) | تکه‌ای که جدا تا می‌خورد و کاری دارد | انگشت روی GR (۴۲۰ تا ۴۸۷) |
| **خانواده** (family) | پروتئین‌ها یا دامنه‌هایی با نیای روشن و توالی هم‌ترازشدنی | ‏Pfam ‏PF13354: بتالاکتامازهای رده‌ی A |
| **ابرخانواده** (homologous superfamily) | خانواده‌هایی با ساختار سه‌بعدی یکسان، حتی اگر توالی‌شان دیگر هم‌تراز نشود | «Beta-lactamase/transpeptidase-like» |
| ‏**clan** (در Pfam) | گروه خانواده‌های Pfam با نیای مشترک | ‏CL0013 |

### ۲.۲ از BLAST تا profile HMM

‏BLAST **دو** توالی را با هم می‌سنجد. اگر خویشاوندی دور باشد (۲۰٪ یکسانی)، نشانه زیر نویز گم می‌شود.

‏**profile** به جای یک توالی، **صدها** توالی هم‌تراز یک خانواده را خلاصه می‌کند: برای هر جایگاه، هر اسید آمینه با چه احتمالی می‌آید.

<div dir="ltr">

```text
position:        1    2    3    4    5    6
seq 1            C    L    V    C    S    D
seq 2            C    K    I    C    A    D
seq 3            C    A    V    C    G    E
seq 4            C    R    V    C    S    D
profile:         C    any  V/I  C    any  D/E
                 100% 25%  75%  100% 50%  75%
```

</div>

جایگاه ۱ و ۴ همیشه `C` است. اگر توالی تازه‌ای در این دو جا `C` داشت، امتیاز **زیادی** می‌گیرد، و اگر نداشت، **جریمه**‌ی زیادی. ولی جایگاه ۲ هر چیزی می‌تواند باشد و کمابیش بی‌اثر است. BLAST این را نمی‌داند و با همه‌ی جایگاه‌ها یکسان رفتار می‌کند.

‏**HMM** (مدل پنهان مارکوف) همان profile است، با یک افزوده: احتمال **درج** و **حذف** در هر جایگاه هم دارد (برای نمونه «این‌جا در خانواده گاهی ۵ اسید آمینه‌ی اضافه می‌آید»). ‏**HMMER** نرم‌افزار ساخت و جست‌وجوی این مدل‌هاست، و هر خانواده‌ی **Pfam** یک HMM است.

### ‏۲.۳ ‏InterPro: چتر بالای پایگاه‌ها

گروه‌های گوناگون هر کدام مدل‌های خودشان را برای خانواده‌ها ساخته‌اند. InterPro سیزده تا از آن‌ها را در بر دارد: Pfam، PROSITE (الگو و profile)، PRINTS، SMART، CDD، NCBIfam، PANTHER، PIRSF، HAMAP، SFLD، CATH-Gene3D و SUPERFAMILY. **InterPro** (EMBL-EBI) مدل‌هایی را که به یک چیز اشاره دارند در یک **مدخل InterPro** (`IPR…`) گرد می‌آورد. ‏**InterProScan** برنامه‌ای است که یک توالی تازه را با **همه**‌ی این مدل‌ها می‌سنجد. در 2026-10-27: ‏InterPro ‏۵۴٬۹۲۲ مدخل و Pfam ‏۳۰٬۱۳۴ خانواده داشت.

---

## ۳. گام ۱: ‏BLAST کجا کم می‌آورد؟

**چرا؟** پیش از HMM، ببینیم BLAST (11/07) درباره‌ی شش بتالاکتاماز چه می‌گوید.

<div dir="ltr">

```bash
grep '>' query.faa | cut -c1-60
awk '/^>/ {p = !/P04150/} p' query.faa > bla6.faa
blastp -query bla6.faa -subject bla6.faa -outfmt "6 qacc sacc pident length evalue bitscore" -evalue 10 2> /dev/null \
  | awk '{split($1, q, "|"); split($2, s, "|"); if (q[3] < s[3]) print q[3], s[3], $3, $4, $5, $6}' \
  | sort -k1,1 -k2,2 -u | column -t
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`awk '/^>/ {p = !/P04150/} p'` | هر رکوردی را چاپ کن جز GR (‏`p` در سرخط تعیین و برای سطرهای توالی نگه داشته می‌شود) |
| ‏`-subject bla6.faa` | همه در برابر همه، بی ساختن پایگاه |
| ‏`-evalue 10` | پاسخ‌های ضعیف را هم نشان بده |
| ‏`split($1, q, "\|")` | ‏`sp\|P62593\|BLAT_ECOLX` را بشکن؛ `q[3]` نام کوتاه است |
| ‏`q[3] < s[3]` | هر جفت یک بار (نه A→B و B→A) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
>sp|P62593|BLAT_ECOLX Beta-lactamase TEM OS=Escherichia coli
>sp|A0A5R8T042|BLC15_ECO25 Beta-lactamase CTX-M-15 OS=Escheri
>sp|Q9F663|BLKPC_KLEPN Carbapenem-hydrolyzing beta-lactamase
>sp|P00811|AMPC_ECOLI Beta-lactamase OS=Escherichia coli (str
>sp|Q6XEC0|BLO48_KLEPN Beta-lactamase OXA-48 OS=Klebsiella pn
>sp|C7C422|BLAN1_KLEPN Metallo-beta-lactamase type 2 OS=Klebs
>sp|P04150|GCR_HUMAN Glucocorticoid receptor OS=Homo sapiens
AMPC_ECOLI   BLAT_ECOLX   23.529  51   1.8       18.1
AMPC_ECOLI   BLC15_ECO25  34.375  32   8.9       15.8
AMPC_ECOLI   BLO48_KLEPN  28.302  53   0.55      19.6
BLAN1_KLEPN  BLC15_ECO25  40.909  22   0.063     22.3
BLAN1_KLEPN  BLKPC_KLEPN  23.810  63   0.19      20.8
BLAN1_KLEPN  BLO48_KLEPN  37.931  29   0.62      19.2
BLAT_ECOLX   BLC15_ECO25  38.550  262  3.39e-62  188
BLAT_ECOLX   BLKPC_KLEPN  44.737  228  6.07e-67  200
BLAT_ECOLX   BLO48_KLEPN  50.000  16   0.14      21.2
BLC15_ECO25  BLKPC_KLEPN  52.521  238  3.17e-89  257
BLC15_ECO25  BLO48_KLEPN  71.429  7    2.7       17.3
```

</div>

**توضیح خروجی:**
- **درون رده‌ی A** (TEM، CTX-M-15، KPC): ‏۳۹ تا ۵۳٪ یکسانی روی بیش از ۲۲۰ اسید آمینه، E از 1e-62 تا 1e-89. خویشاوندی روشن.
- **رده‌ی A در برابر C** (AmpC) یا **D** (OXA-48): تنها تکه‌های ۷ تا ۵۳ اسید آمینه‌ای با E بالای ۰٫۱. یعنی **هیچ** نشانه‌ی معناداری. (‏۷۱٪ روی ۷ اسید آمینه، تصادف است؛ 11/07.)
- ‏NDM-1 (رده‌ی B) با هیچ‌کدام: باز تنها نویز.

پس BLAST نمی‌تواند بگوید A، C و D خویشاوندند. گام ۳ نشان می‌دهد HMM می‌تواند.

---

## ۴. گام ۲: ‏InterPro API

### ۴.۱ دامنه‌های Pfam هر پروتئین

<div dir="ltr">

```bash
for a in P62593 A0A5R8T042 Q9F663 P00811 Q6XEC0 C7C422 P04150; do
  curl -sS "$I/entry/pfam/protein/uniprot/$a" \
    | jq -r --arg a $a '.results[] | [$a, .metadata.accession, .metadata.name,
        (.proteins[0].entry_protein_locations[] | .fragments[] | "\(.start)-\(.end)")] | @tsv'
  sleep 1
done
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`entry/pfam/protein/uniprot/ACC` | «مدخل‌های Pfam که روی این پروتئین UniProt می‌نشینند» |
| ‏`--arg a $a` | متغیر پوسته را به `jq` بده (در jq: `$a`) |
| ‏`entry_protein_locations[].fragments[]` | جای دامنه روی پروتئین (یک دامنه می‌تواند چند تکه باشد) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
P62593	PF13354	Beta-lactamase enzyme family	32-286
A0A5R8T042	PF13354	Beta-lactamase enzyme family	33-289
Q9F663	PF13354	Beta-lactamase enzyme family	32-286
P00811	PF00144	Beta-lactamase	29-376
Q6XEC0	PF00905	Penicillin binding protein transpeptidase domain	48-259
C7C422	PF00753	Metallo-beta-lactamase superfamily	72-250
P04150	PF00104	Ligand-binding domain of nuclear hormone receptor	558-735
P04150	PF00105	Double treble clef zinc finger, C4 type	420-487
P04150	PF02155	Glucocorticoid receptor	26-401
```

</div>

**توضیح خروجی:**
- سه پروتئین رده‌ی A یک خانواده‌اند (**PF13354**). AmpC خانواده‌ی دیگری است (PF00144).
- ‏**OXA-48 در PF00905 است: «دامنه‌ی ترانس‌پپتیداز پروتئین متصل به پنی‌سیلین».** یعنی Pfam بتالاکتاماز رده‌ی D را در همان خانواده‌ی PBPها گذاشته است.
- ‏NDM-1: «ابرخانواده‌ی متالوبتالاکتاماز» (PF00753).
- ‏GR: سه دامنه، همان سه بخش CD-Search در 11/07 (GCR ‏۲۶–۴۰۱ درست یکسان؛ DBD و LBD با مرزهای کمی دیگر، چون مدل‌ها دیگرند).

### ‏۴.۲ ‏clan: خویشاوندی دور

<div dir="ltr">

```bash
for p in PF13354 PF00144 PF00905 PF00753 PF00104 PF00105; do
  curl -sS "$I/entry/pfam/$p" | jq -r --arg p $p \
    '[$p, .metadata.name.name, (.metadata.set_info.accession // "-"), (.metadata.set_info.name // "-"), .metadata.counters.proteins] | @tsv'
  sleep 1
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
PF13354	Beta-lactamase enzyme family	CL0013	Beta-lactamase	22331
PF00144	Beta-lactamase	CL0013	Beta-lactamase	118531
PF00905	Penicillin binding protein transpeptidase domain	CL0013	Beta-lactamase	102409
PF00753	Metallo-beta-lactamase superfamily	CL0381	Metallo-HOrase	187908
PF00104	Ligand-binding domain of nuclear hormone receptor	-	-	82807
PF00105	Double treble clef zinc finger, C4 type	CL0839	Tbcl_zf	82752
```

</div>

**توضیح خروجی:**
- خانواده‌های رده‌ی **A، C و D** هر سه در **clan ‏CL0013** هستند: نیای مشترک. ✅ همان پاسخ معلوم.
- رده‌ی **B** در clan دیگری است (**CL0381**، «Metallo-hydrolase/oxidoreductase»). ✅ نیای جدا.
- ستون آخر: شمار پروتئین‌های UniProt در هر خانواده. ‏PF00753 بیش از ۱۸۷ هزار پروتئین دارد؛ بیشترشان **بتالاکتاماز نیستند** (گام ۴).
- ‏`// "-"` در jq یعنی «اگر تهی بود، `-` بنویس» (LBD در هیچ clan نیست).

### ۴.۳ همه‌ی پایگاه‌ها با هم

<div dir="ltr">

```bash
curl -sS "$I/entry/all/protein/uniprot/A0A5R8T042?page_size=100" \
  | jq -r '.results[] | [.metadata.source_database, .metadata.accession, .metadata.type, (.metadata.integrated // "-"),
           (.metadata.name | tostring | .[0:45]),
           ([.proteins[0].entry_protein_locations[]?.fragments[] | "\(.start)-\(.end)"] | join(","))] | @tsv' | sort
```

</div>

**خروجی واقعی (2026-10-27؛ CTX-M-15):**

<div dir="ltr">

```
cathgene3d	G3DSA:3.40.710.10	homologous_superfamily	IPR012338	DD-peptidase/beta-lactamase superfamily	26-291
interpro	IPR000871	family	-	Beta-lactamase, class-A	27-288
interpro	IPR012338	homologous_superfamily	-	Beta-lactamase/transpeptidase-like	26-291
interpro	IPR023650	active_site	-	Beta-lactamase, class-A active site	69-84
interpro	IPR045155	domain	-	Beta-lactamase class A, catalytic domain	33-289
interpro	IPR058131	family	-	Beta-lactamase CTX-M	1-291
ncbifam	NF033089	family	IPR058131	CTX-M family extended-spectrum class A beta-l	1-291
ncbifam	NF033103	family	-	class A beta-lactamase	36-289
panther	PTHR35333	family	IPR000871	BETA-LACTAMASE	27-288
pfam	PF13354	domain	IPR045155	Beta-lactamase enzyme family	33-289
prints	PR00118	family	IPR000871	BLACTAMASEA	36-60,67-84,109-134,145-169,171-196,207-222,224-239
prosite	PS00146	conserved_site	IPR023650	Beta-lactamase class-A active site	69-84
ssf	SSF56601	homologous_superfamily	IPR012338	beta-lactamase/transpeptidase-like	32-289
```

</div>

**خواندن خروجی:**
- ستون چهارم می‌گوید هر مدل در **کدام مدخل InterPro** گرد آمده است: PANTHER و PRINTS زیر `IPR000871` (رده‌ی A)، CATH-Gene3D و SUPERFAMILY زیر `IPR012338` (ابرخانواده‌ی ساختاری «بتالاکتاماز/ترانس‌پپتیداز»).
- **سطح‌ها از کلی به ویژه:** ابرخانواده (ساختار، ۲۶–۲۹۱) ← رده‌ی A ← CTX-M ← (NCBIfam: «CTX-M با طیف گسترده»).
- ‏**PRINTS** با هفت تکه: یک «اثر انگشت» از چند نقش کوتاه حفظ‌شده.
- ‏**PROSITE PS00146** جایگاه فعال را در **۶۹ تا ۸۴** می‌گذارد. توالی آن تکه:

<div dir="ltr">

```bash
awk '/^>/ {p = /A0A5R8T042/; next} p' query.faa | tr -d '\n' | cut -c69-84
```

</div>

<div dir="ltr">

```
FAMCSTSKVMAAAAVL
```

</div>

‏`S-T-S-K` در ۷۳ تا ۷۶: نقش **S-x-x-K** بتالاکتامازهای سرینی. سرین ۷۳ همان **سرینی** است که حلقه‌ی بتالاکتام را می‌شکند. در مقاله‌ها آن را **Ser70** می‌نامند: شماره‌گذاری **Ambler** همه‌ی آنزیم‌های رده‌ی A را روی TEM-1 هم‌تراز می‌کند. همان داستان S531 و S450 در 11/07.

✍️ **در مرورگر:** ‏https://www.ebi.ac.uk/interpro/ ← جست‌وجوی `A0A5R8T042` ← برگه‌ی **Entries** همین جدول را با نوارهای رنگی روی طول پروتئین می‌کشد. برای یک **توالی تازه** (نه در UniProt)، **Search ← By sequence** همان InterProScan است: توالی را می‌چسبانید و چند دقیقه بعد همین جدول را می‌گیرید. سرویس برنامه‌ای آن (EBI Job Dispatcher، `iprscan5`) نشانی ایمیل می‌خواهد؛ ما از سرور دوره کاری نفرستادیم.

> 📺 **فیلم:** *Exploring protein families and domains using InterPro* (EMBL-EBI): https://www.youtube.com/watch?v=lQ7cSkvURvM · *InterProScan* (EMBL-EBI): https://www.youtube.com/watch?v=EWLGFuTpUnQ
> 📄 **مرجع:** Blum M, et al. (2025). *InterPro: the protein sequence classification resource in 2025.* Nucleic Acids Res 53(D1):D444–D456. https://doi.org/10.1093/nar/gkae1082 · Jones P, et al. (2014). *InterProScan 5.* Bioinformatics 30:1236–1240. https://doi.org/10.1093/bioinformatics/btu031 · راهنمای InterPro و API: https://interpro-documentation.readthedocs.io/

---

## ۵. گام ۳: ‏HMMER؛ دامنه‌ها را خودتان بیابید

### ‏۵.۱ ‏`hmmscan`: یک پروتئین در برابر چند مدل

‏`download.sh` هفت HMM Pfam را از InterPro گرفت و با `hmmpress` آماده کرد. نخست ببینیم در آن چه هست:

<div dir="ltr">

```bash
grep -E '^(NAME|ACC|LENG|GA)' mini_pfam.hmm | paste - - - -
```

</div>

<div dir="ltr">

```
NAME  Hormone_recep	ACC   PF00104.36	LENG  213	GA    23.5 23.5;
NAME  zf-C4	ACC   PF00105.25	LENG  70	GA    21.1 18;
NAME  Beta-lactamase	ACC   PF00144.30	LENG  329	GA    27 27;
NAME  Lactamase_B	ACC   PF00753.34	LENG  196	GA    22.7 21.9;
NAME  Transpeptidase	ACC   PF00905.28	LENG  299	GA    22.1 22.1;
NAME  GCR	ACC   PF02155.21	LENG  373	GA    29.3 29.3;
NAME  Beta-lactamase2	ACC   PF13354.13	LENG  256	GA    22 22;
```

</div>

- ‏`LENG`: شمار جایگاه‌های مدل (zf-C4 ‏۷۰).
- ‏**`GA` (gathering threshold):** آستانه‌ی امتیاز (bit) که کارشناسان Pfam برای **هر** خانواده برگزیده‌اند: هر توالی بالای آن، عضو خانواده است. عدد نخست برای کل توالی و دومی برای هر دامنه.

<div dir="ltr">

```bash
hmmscan --cut_ga --domtblout scan.domtbl -o scan.txt mini_pfam.hmm query.faa
grep -v '^#' scan.domtbl | awk '{split($4, q, "|");
    printf "%-12s %-15s %-9s %8s %6s %5s-%-5s %5s-%-5s\n", q[2], $1, $2, $7, $14, $16, $17, $18, $19}'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`hmmscan` | هر **توالی** را در برابر همه‌ی **مدل‌ها** بسنج (پرسش: «این پروتئین چه دامنه‌هایی دارد؟») |
| ‏`--cut_ga` | به جای E-value، آستانه‌ی GA هر خانواده را به کار ببر (همان کار Pfam و InterPro) |
| ‏`--domtblout` | جدول یک‌سطری برای هر **دامنه** |
| ستون‌های چاپ‌شده | پروتئین، نام مدل، Pfam، ‏E-value کل توالی ($7)، امتیاز دامنه ($14)، جای روی **مدل** ($16–$17)، جای روی **پروتئین** ($18–$19) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
P62593       Beta-lactamase2 PF13354.13  2.8e-47  149.6     7-256      32-286  
P62593       Beta-lactamase  PF00144.30  1.6e-37  117.6     3-327      33-278  
A0A5R8T042   Beta-lactamase2 PF13354.13    8e-49  154.6     2-254      33-289  
A0A5R8T042   Beta-lactamase  PF00144.30  1.1e-39  124.7     4-327      40-283  
Q9F663       Beta-lactamase2 PF13354.13  1.2e-49  157.3     5-254      32-286  
Q9F663       Beta-lactamase  PF00144.30  2.8e-36  113.6     1-327      33-280  
P00811       Beta-lactamase  PF00144.30 1.3e-101  328.6     2-328      29-376  
Q6XEC0       Transpeptidase  PF00905.28  4.9e-47  149.1    18-299      48-259  
C7C422       Lactamase_B     PF00753.34  2.7e-15   44.1     3-196      72-250  
P04150       GCR             PF02155.21   8e-216  704.9     1-373      26-401  
P04150       Hormone_recep   PF00104.36  5.2e-35  108.0    11-206     558-735  
P04150       zf-C4           PF00105.25  7.8e-32   97.8     2-69      420-487
```

</div>

**توضیح خروجی:**
- جای دامنه‌ها روی پروتئین **درست** همان پاسخ InterPro است (برای نمونه CTX-M-15 ‏۳۳–۲۸۹). ✅ InterPro همین کار را با همین مدل‌ها کرده است.
- **نکته‌ی اصلی:** هر سه آنزیم رده‌ی A با مدل **رده‌ی C** (PF00144) هم امتیاز ۱۱۴ تا ۱۲۵ bit و E ‏1e-36 تا 1e-39 گرفتند، بسیار بالای GA ‏(۲۷). همان خویشاوندی که BLAST (گام ۱) با E بالای ۰٫۱ ندید! مدل صدها توالی رده‌ی C جایگاه‌های حفظ‌شده‌ی مشترک دو رده را می‌شناسد.
- چرا InterPro (بخش ۴.۱) برای رده‌ی A تنها PF13354 را نشان داد؟ چون Pfam برای خانواده‌های **یک clan** تنها **بهترین** را نگه می‌دارد (clan competition). هر دو در CL0013 هستند و PF13354 امتیاز بالاتری دارد.

### ۵.۲ مدل از درون: سیستئین‌های انگشت روی

‏`hmmlogo` برای هر جایگاه مدل، «ارتفاع» هر اسید آمینه (اطلاعات، بر حسب bit) را می‌دهد. جایگاه‌های بلندتر حفظ‌شده‌ترند. مدل zf-C4 (‏۷۰ جایگاه):

<div dir="ltr">

```bash
hmmfetch mini_pfam.hmm zf-C4 > zf.hmm
hmmlogo --height_relent_abovebg zf.hmm | awk 'NR > 2 && NF >= 21 {
    split("A C D E F G H I K L M N P Q R S T V W Y", L, " "); max = 0; s = 0;
    for (i = 2; i <= 21; i++) {s += $i; if ($i > max) {max = $i; aa = L[i-1]}}
    sub(":", "", $1); printf "%s\t%s\t%.2f\n", $1, aa, s}' > zf_cons.tsv
sort -k3,3gr zf_cons.tsv | head -10
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
20	C	2.59
23	C	2.59
39	C	2.59
3	C	2.59
45	C	2.59
55	C	2.59
58	C	2.59
63	C	2.59
6	C	2.59
14	H	1.77
```

</div>

نُه جایگاه بیشترین ارتفاع را دارند و **همه سیستئین‌اند**. هشت تای آن‌ها دو الگوی انگشت روی را می‌سازند: `C-x2-C-x13-C-x2-C` (جایگاه‌های ۳، ۶، ۲۰، ۲۳) و `C-x5-C-x9-C-x2-C` (‏۳۹، ۴۵، ۵۵، ۵۸). هر چهار سیستئین یک اتم روی را نگه می‌دارند. در هم‌ترازی `hmmscan` (فایل `scan.txt`) جایگاه k مدل روی GR باقی‌مانده‌ی 418+k است؛ پس سیستئین‌های انگشت‌ها در GR: **C421، C424، C438، C441** و **C457، C463، C473، C476**.

> 📺 **فیلم:** *How to perform HMM search online (Tutorial) using HMMER?* (XploreBio): https://www.youtube.com/watch?v=mdpM6XxxZF4
> 📄 **مرجع:** Eddy SR (2004). *What is a hidden Markov model?* Nat Biotechnol 22:1315–1316. https://doi.org/10.1038/nbt1004-1315 · Eddy SR (2011). *Accelerated Profile HMM Searches.* PLoS Comput Biol 7:e1002195. https://doi.org/10.1371/journal.pcbi.1002195 · Mistry J, et al. (2021). *Pfam: The protein families database in 2021.* Nucleic Acids Res 49:D412–D419. https://doi.org/10.1093/nar/gkaa913 · راهنمای HMMER: http://hmmer.org/documentation.html

---

## ۶. گام ۴: ‏`hmmsearch`؛ یک مدل در برابر یک پروتئوم

**چرا؟** پرسش وارونه: «در ژنوم *E. coli* K-12 کدام پروتئین‌ها عضو این خانواده‌اند؟». ‏`hmmsearch` یک **مدل** را در برابر همه‌ی **توالی‌ها** می‌سنجد.

<div dir="ltr">

```bash
grep -c '>' ecoli.faa
for name in Beta-lactamase2 Beta-lactamase Transpeptidase Lactamase_B; do
  hmmfetch mini_pfam.hmm $name > one.hmm
  echo "== $name"
  hmmsearch --cut_ga --tblout one.tbl -o /dev/null one.hmm ecoli.faa
  grep -v '^#' one.tbl | awk '{d = ""; for (i = 19; i <= NF; i++) d = d " " $i;
                               printf "%-16s %9s %6s %s\n", $1, $5, $6, substr(d, 1, 60)}'
done
```

</div>

**تکه‌به‌تکه:** ‏`hmmfetch` یک مدل را با نامش از پایگاه بیرون می‌کشد. در `--tblout` ستون ۵ ‏E-value و ستون ۶ امتیاز است، و از ستون ۱۹ به بعد توضیح پروتئین (چند واژه، پس با حلقه به هم می‌چسبانیم).

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
4300
== Beta-lactamase2
NP_415360.1        4.8e-15   53.4  D-alanyl-D-alanine carboxypeptidase DacC [Escherichia coli 
NP_416638.4          7e-11   39.7  peptidoglycan DD-endopeptidase PbpG [Escherichia coli str. 
NP_416514.4        4.4e-10   37.1  D-alanyl-D-alanine carboxypeptidase DacD [Escherichia coli 
NP_415165.1        9.5e-10   36.0  D-alanyl-D-alanine carboxypeptidase DacA [Escherichia coli 
NP_417649.1        1.3e-07   29.0  peptidoglycan DD-endopeptidase DacB [Escherichia coli str. 
== Beta-lactamase
NP_418574.1        8.3e-99  328.8  beta-lactamase [Escherichia coli str. K-12 substr. MG1655]
NP_416925.2        7.6e-70  233.6  penicillin binding protein 4B [Escherichia coli str. K-12 s
NP_414910.1        1.6e-68  229.3  peptidoglycan DD-carboxypeptidase/peptidoglycan DD-endopept
== Transpeptidase
NP_414626.1        2.9e-88  293.9  peptidoglycan DD-transpeptidase FtsI [Escherichia coli str.
NP_415168.1        1.3e-81  272.1  peptidoglycan DD-transpeptidase MrdA [Escherichia coli str.
NP_417855.4          2e-26   90.9  peptidoglycan glycosyltransferase/peptidoglycan DD-transpep
YP_010051172.1     3.2e-25   86.9  PBP-1Bgamma [Escherichia coli str. K-12 substr. MG1655]
NP_414691.1        3.6e-25   86.7  peptidoglycan glycosyltransferase/peptidoglycan DD-transpep
NP_417014.1        4.9e-13   46.9  peptidoglycan glycosyltransferase PbpC [Escherichia coli st
== Lactamase_B
NP_415447.1        3.6e-42  142.5  hydroxyacylglutathione hydrolase GloC [Escherichia coli str
NP_418507.2        8.4e-28   95.6  linear primary-alkylsulfatase [Escherichia coli str. K-12 s
NP_414748.1        5.5e-27   92.9  hydroxyacylglutathione hydrolase GloB [Escherichia coli str
NP_415433.4        3.5e-24   83.8  metallo-beta-lactamase superfamily inner membrane protein Y
NP_417190.1        6.3e-15   53.6  anaerobic nitric oxide reductase flavorubredoxin [Escherichia coli
NP_416771.4        3.6e-08   31.5  ribonuclease BN [Escherichia coli str. K-12 substr. MG1655]
```

</div>

**توضیح خروجی (این مهم‌ترین بخش درس است):**
- ‏*E. coli* K-12 سویه‌ی آزمایشگاهی است و **هیچ** بتالاکتاماز رده‌ی A یا D ندارد. با این حال مدل رده‌ی A پنج پروتئین و مدل رده‌ی D شش پروتئین یافت: همه **PBP**، آنزیم‌های ساخت دیواره‌ی سلولی (DacA/B/C/D، FtsI یا PBP3، MrdA یا PBP2، و MrcA و MrcB یا PBP1A و PBP1B). یعنی همان **هدف‌های** پنی‌سیلین. ✅ پاسخ معلوم: بتالاکتامازهای سرینی از PBPها آمده‌اند.
- مدل رده‌ی C سه پروتئین یافت: **AmpC** (`NP_418574.1`، تنها بتالاکتاماز کروموزومی *E. coli*) و دو PBP دیگر (PBP4B و AmpH).
- مدل متالوبتالاکتاماز شش پروتئین یافت و **هیچ‌کدام** بتالاکتاماز نیست: گلیوکسالاز II ‏(GloB، GloC)، آلکیل‌سولفاتاز، فلاورابردوکسین و ریبونوکلئاز BN. همه هیدرولاز یا اکسیدوردوکتازهای فلزی‌اند، با همان تاخوردگی و کارهای بسیار گوناگون.

**درس:** «دامنه‌ی بتالاکتاماز دارد» ≠ «بتالاکتاماز است». نام خانواده از نخستین عضو شناخته‌شده آمده، نه از کار همه‌ی اعضا. برای پیش‌بینی **کار** باید خانواده‌ی **ویژه**‌تر (NCBIfam: «CTX-M family»، گام ۲)، ارتولوگ‌ها (گام ۵) یا آزمایش را دید. ابزار AMRFinderPlus در 08/01 برای همین مدل‌های **ویژه‌ی** ژن‌های مقاومت با آستانه‌های سخت دارد.

---

## ۷. گام ۵: ‏eggNOG-mapper (✍️)

**چرا؟** InterPro می‌گوید «چه دامنه‌ای». ‏**eggNOG-mapper** می‌پرسد «نزدیک‌ترین **ارتولوگ** شناخته‌شده کیست؟» و آنوتیشن آن را منتقل می‌کند: نام ژن، دسته‌ی **COG**، **KO** ‏KEGG (12/05)، اصطلاح‌های **GO** (12/05) و EC. چون از ارتولوگ‌ها (نه پارالوگ‌ها) منتقل می‌کند، برای پیش‌بینی کار از «تنها دامنه» دقیق‌تر است: PBP4B را «PBP» می‌نامد، نه «بتالاکتاماز».

✍️ **گام‌ها (از راهنمای eggNOG-mapper؛ پایگاه آن نزدیک به ۵۰ گیگابایت است و روی سرور دوره اجرا نشد):**
1. ‏http://eggnog-mapper.embl.de ← فایل FASTA پروتئین‌ها را بارگذاری کنید و نشانی ایمیل خود را بدهید.
2. ‏*Taxonomic scope* را **Bacteria** (یا خودکار) بگذارید.
3. چند دقیقه تا چند ساعت بعد، پیوند نتیجه می‌آید. فایل `*.emapper.annotations` یک سطر برای هر پروتئین دارد، با ستون‌هایی چون `seed_ortholog`، `evalue`، `COG_category`، `Description`، `Preferred_name`، `GOs`، `EC`، `KEGG_ko`، `KEGG_Pathway` و `PFAMs`.
4. همین ابزار روی Galaxy هم هست (آموزش GTN در منابع).

> 📺 **فیلم:** برای eggNOG-mapper فیلم آموزشی رسمی یا معتبری نیافتیم؛ آموزش نوشتاری Galaxy: https://training.galaxyproject.org/training-material/topics/genome-annotation/tutorials/functional/tutorial.html
> 📄 **مرجع:** Cantalapiedra CP, et al. (2021). *eggNOG-mapper v2.* Mol Biol Evol 38:5825–5829. https://doi.org/10.1093/molbev/msab293 · Hernández-Plaza A, et al. (2023). *eggNOG 6.0.* Nucleic Acids Res 51:D389–D394. https://doi.org/10.1093/nar/gkac1022

---

## ۸. سه اشتباه رایج

1. **دامنه = کار.** پنج PBP با مدل بتالاکتاماز رده‌ی A و شش آنزیم گوناگون با مدل متالوبتالاکتاماز (گام ۴). پیش از گفتن «این ژن مقاومت است»، خانواده‌ی ویژه، ارتولوگ و جایگاه فعال را ببینید.
2. ‏**E-value به جای GA، یا نادیده گرفتن هم‌پوشانی.** بی `--cut_ga`، ‏`hmmscan` پاسخ‌های بسیار ضعیف را هم می‌دهد؛ با آن، همان آستانه‌ی کارشناسان Pfam. و یک تکه می‌تواند به چند خانواده‌ی یک clan بخورد (رده‌ی A با PF13354 و PF00144): بهترین را برگزینید، نه هر دو را دو دامنه بشمارید.
3. **شماره‌گذاری دیگر.** سرین فعال CTX-M-15 در UniProt ‏Ser73 و در مقاله‌ها Ser70 (Ambler) است؛ جای دامنه روی **مدل** (ستون‌های ۱۶–۱۷) با جای روی **پروتئین** (۱۸–۱۹) یکی نیست. همیشه بگویید کدام شماره.

---

## 📘 برای کنجکاوها

- **همه‌ی Pfam روی رایانه‌ی خودتان:** ‏`Pfam-A.hmm.gz` (‏۴۱۸ مگابایت فشرده، 2026-01-22؛ https://ftp.ebi.ac.uk/pub/databases/Pfam/current_release/) را بگیرید، `hmmpress` کنید و `hmmscan --cut_ga` بزنید. برای چند هزار پروتئین چند دقیقه طول می‌کشد.
- ‏**‏`phmmer` و `jackhmmer`:** ‏`phmmer` یک توالی را (مانند BLAST) با همان آمار HMMER می‌جوید؛ `jackhmmer` چند دور تکرار می‌کند و هر بار از پاسخ‌ها مدل تازه می‌سازد (مانند PSI-BLAST). با `hmmbuild` از هر هم‌ترازی چندگانه (08/04) هم مدل خودتان را می‌سازید.
- ‏**‏InterProScan روی رایانه‌ی خودتان:** نسخه‌ی ۵ (و ۶ تازه) با همه‌ی پایگاه‌ها چند ده گیگابایت است؛ برای ژنوم‌های کامل در خط لوله (بخش ۲۰).

---

## جمع‌بندی

- دامنه ← خانواده ← ابرخانواده و clan: از ویژه به کلی.
- ‏profile HMM جایگاه‌های حفظ‌شده را سنگین‌تر می‌سنجد و خویشاوندی دوری را می‌بیند که BLAST نمی‌بیند (رده‌ی A با مدل رده‌ی C: ‏E ‏1e-39 در برابر BLAST ‏E > 0.1).
- ‏InterPro مدل‌های سیزده پایگاه را در مدخل‌های `IPR` گرد می‌آورد؛ API آن جای دامنه‌ها را می‌دهد. بتالاکتامازهای A، C و D در clan ‏CL0013، رده‌ی B در CL0381.
- ‏`hmmscan` (توالی در برابر مدل‌ها) و `hmmsearch` (مدل در برابر پروتئوم)، با `--cut_ga`.
- عضویت در خانواده کار را نمی‌گوید: مدل‌های بتالاکتاماز در *E. coli* K-12 بیشتر PBP و آنزیم‌های دیگر یافتند. ‏eggNOG-mapper با ارتولوگ‌ها کار را دقیق‌تر پیش‌بینی می‌کند.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
I=https://www.ebi.ac.uk/interpro/api
curl -sS "$I/entry/pfam/protein/uniprot/ACC"                 # Pfam domains of a UniProt protein (+ positions)
curl -sS "$I/entry/all/protein/uniprot/ACC?page_size=100"    # all member databases
curl -sS "$I/entry/pfam/PFxxxxx"                             # family info, clan (set_info), counts
curl -sS "$I/entry/pfam/PFxxxxx?annotation=hmm" | gunzip > PFxxxxx.hmm
hmmpress db.hmm                                              # prepare HMM database for hmmscan
hmmscan --cut_ga --domtblout out.domtbl db.hmm proteins.faa  # domains of each protein
hmmfetch db.hmm NAME > one.hmm                               # one model by name
hmmsearch --cut_ga --tblout out.tbl one.hmm proteome.faa     # family members in a proteome
hmmlogo --height_relent_abovebg one.hmm                      # conservation per model position
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| دامنه (domain) | تکه‌ای از پروتئین که جدا تا می‌خورد و در پروتئین‌های بسیاری تکرار می‌شود |
| خانواده / ابرخانواده | گروه با نیای روشن و توالی هم‌ترازشدنی / با ساختار یکسان و نیای دورتر |
| ‏clan | گروه خانواده‌های Pfam با نیای مشترک |
| ‏profile | خلاصه‌ی جایگاه‌به‌جایگاه یک هم‌ترازی چندگانه |
| ‏HMM (مدل پنهان مارکوف) | ‏profile با احتمال درج و حذف در هر جایگاه |
| ‏GA (gathering threshold) | آستانه‌ی امتیاز هر خانواده‌ی Pfam برای عضویت |
| ‏bit score | امتیاز هم‌ترازی، ناوابسته به اندازه‌ی پایگاه |
| ‏InterPro / مدخل IPR | چتر پایگاه‌های خانواده / یک مدخل که مدل‌های هم‌معنا را گرد می‌آورد |
| ‏InterProScan | برنامه‌ی سنجش یک توالی با همه‌ی مدل‌های InterPro |
| ‏PBP | پروتئین متصل به پنی‌سیلین؛ آنزیم ساخت دیواره و هدف بتالاکتام‌ها |
| رده‌بندی Ambler | چهار رده‌ی A، B، C، D بتالاکتامازها بر پایه‌ی توالی |
| ارتولوگ / پارالوگ | همتا در گونه‌ی دیگر (از گونه‌زایی) / همتا در همان ژنوم (از دوبرابر شدن ژن) |
| ‏COG | گروه‌های ارتولوگ با دسته‌های کارکردی (حرف‌های A تا Z) |
| هم‌گرایی | رسیدن دو دودمان جدا به یک کار، با ساختار دیگر |

---

## منابع

**مقاله و مستند**
- ‏Blum M, et al. (2025). *InterPro: the protein sequence classification resource in 2025.* Nucleic Acids Res 53(D1):D444–D456. https://doi.org/10.1093/nar/gkae1082
- ‏Mistry J, et al. (2021). *Pfam: The protein families database in 2021.* Nucleic Acids Res 49:D412–D419. https://doi.org/10.1093/nar/gkaa913
- ‏Jones P, et al. (2014). *InterProScan 5: genome-scale protein function classification.* Bioinformatics 30:1236–1240. https://doi.org/10.1093/bioinformatics/btu031
- ‏Eddy SR (2004). *What is a hidden Markov model?* Nat Biotechnol 22:1315–1316. https://doi.org/10.1038/nbt1004-1315
- ‏Eddy SR (2011). *Accelerated Profile HMM Searches.* PLoS Comput Biol 7:e1002195. https://doi.org/10.1371/journal.pcbi.1002195
- ‏Cantalapiedra CP, et al. (2021). *eggNOG-mapper v2.* Mol Biol Evol 38:5825–5829. https://doi.org/10.1093/molbev/msab293
- ‏Hernández-Plaza A, et al. (2023). *eggNOG 6.0: enabling comparative genomics across 12 535 organisms.* Nucleic Acids Res 51:D389–D394. https://doi.org/10.1093/nar/gkac1022
- ‏Ambler RP (1980). *The structure of β-lactamases.* Philos Trans R Soc Lond B 289:321–331. https://doi.org/10.1098/rstb.1980.0049
- ‏Bush K, Jacoby GA (2010). *Updated Functional Classification of β-Lactamases.* Antimicrob Agents Chemother 54:969–976. https://doi.org/10.1128/AAC.01009-09
- راهنماها: InterPro ‏https://www.ebi.ac.uk/interpro/ · HMMER ‏http://hmmer.org/documentation.html · eggNOG-mapper ‏https://github.com/eggnogdb/eggnog-mapper/wiki

**کتاب**
- ‏Durbin R, Eddy SR, Krogh A, Mitchison G (1998). *Biological Sequence Analysis: Probabilistic Models of Proteins and Nucleic Acids.* Cambridge University Press. (فصل ۵: profile HMMها)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۱۲: پروتئین‌ها، دامنه‌ها و InterPro)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioinformatics Methods I* (University of Toronto؛ BLAST و هم‌ترازی): https://www.coursera.org/learn/bioinformatics-methods-1
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Exploring protein families and domains using InterPro* (EMBL-EBI): https://www.youtube.com/watch?v=lQ7cSkvURvM
- ‏YouTube: *Understanding InterPro families, domains and functions* (EMBL-EBI): https://www.youtube.com/watch?v=YWQdfr4QFLI
- ‏YouTube: *InterProScan* (EMBL-EBI): https://www.youtube.com/watch?v=EWLGFuTpUnQ

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند (InterPro API ‏release 110.0، Pfam 38.2؛ HMMER 3.4؛ BLAST+ 2.17.0). فرستادن کار به InterProScan و eggNOG-mapper ایمیل می‌خواهد و از سرور دوره انجام نشد (✍️). DOIها با Crossref وارسی شدند؛ فیلم‌ها با noembed. شماره‌ی فصل کتاب‌های Durbin و Pevsner در وارسی پایانی با فهرست کتاب سنجیده شود.</sub>

</div>
