<div dir="rtl">

# درس ۱: پلاسمید، IS و اینتگرون؛ ژن مقاومت سوار کدام عنصر است؟

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `03_Mobile_Elements_CRISPR` · **پیش‌نیاز:** ماژول‌های [۰۱](../01_AMR_Resistance_Genes/) و [۰۲](../02_Virulence_Factors/) (AMRFinderPlus، `makeblastdb`/`blastn`)؛ قالب GenBank از بخش [02](../../02_BioLinux/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** AMRFinderPlus 4.2.7، BLAST+ 2.17.0، پایگاه PlasmidFinder (نسخه‌ی همراه ABRicate)، Python؛ MOB-suite و MobileElementFinder از مستندات · **آخرین بازبینی:** 2026-10-24

> **وضعیت:** بخش‌های ۳ تا ۶ ✅ اجرا شده‌اند و خروجی واقعی دارند. داده یک پلاسمید **واقعی** است (pEK499، ‏۱۱۷٬۵۳۶ باز، از NCBI). بخش ۷ (MOB-suite و MobileElementFinder) ✍️ تنها از مستندات است: MOB-suite نخست پایگاه‌های بزرگی دانلود می‌کند و روی سرور ما نصب نیست.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. پلاسمید، IS، ترانسپوزون، اینتگرون و جزیره‌ی ژنومی را از هم جدا کنید.
2. یک پلاسمید را با **replicon typing** (پایگاه PlasmidFinder) تایپ کنید.
3. ژن‌های مقاومت یک پلاسمید واقعی را پیدا کنید و ببینید کدام IS کنار هر کدام است.
4. ساختار یک اینتگرون کلاس ۱ را در آنوتیشن بشناسید.
5. بگویید چرا اسمبلی short-read در بسیاری از موارد پلاسمید را کامل نمی‌سازد و MOB-suite چه می‌کند.

<div dir="ltr">

```bash
conda activate amr
cd ~/amr
P=~/Bioinformatics_Learning-main/08_AMR_Virulence_Phylogeny/99_scripts_data
```

</div>

---

## ۱. داستان

در ماژول ۰۲، ‏`blaCTX-M-15` را هم در isoA و هم در isoE دیدیم. در یک بیمارستان واقعی هم همین پرسش پیش می‌آید: **آیا یک سویه پخش شده (شیوع کلونال)، یا یک پلاسمید از سویه‌ای به سویه‌ی دیگر رفته (شیوع پلاسمیدی)؟** برای پاسخ، باید بدانیم ژن روی چه چیزی سوار است. در این درس یک پلاسمید واقعی، **pEK499** را از کلون جهانی *E. coli* ‏ST131 (بریتانیا) بررسی می‌کنیم؛ پلاسمیدی که CTX-M-15 را حمل می‌کند.

---

## ۲. مفهوم به زبان ساده: عنصرهای ژنتیکی متحرک

| عنصر | اندازه | چه می‌کند | تشبیه |
| :--- | :--- | :--- | :--- |
| **پلاسمید** | چند هزار تا چند صد هزار باز | ‏DNA حلقوی جدا از کروموزوم که خودش همانندسازی می‌کند؛ برخی با **هم‌یوغی** (conjugation) به باکتری دیگر می‌روند | کامیون |
| **IS** (insertion sequence) | نزدیک به ۷۰۰ تا ۲۵۰۰ باز | تنها ژن ترانسپوزاز را دارد و خودش را در جای دیگری از DNA می‌گذارد | جرثقیل |
| **ترانسپوزون** (transposon) | چند هزار باز | ‏IS(ها) + ژن‌های بار (مانند ژن مقاومت). دو IS هم‌نوع در دو سوی یک ژن، یک «ترانسپوزون مرکب» می‌سازند | جرثقیل با بار |
| **اینتگرون** (integron) | چند هزار باز | اینتگراز (`intI`) + جایگاه `attI` + ردیفی از **کاست‌های ژنی** که می‌توانند افزوده یا جابه‌جا شوند. خودش جابه‌جا نمی‌شود؛ سوار ترانسپوزون یا پلاسمید می‌شود | قفسه‌ی ابزار |
| **جزیره‌ی ژنومی** (genomic island) | ده‌ها هزار باز | تکه‌ی بزرگی از DNA که از جای دیگری آمده، در بسیاری از موارد کنار ژن tRNA (مانند LEE ماژول ۰۲) | اتاق الحاقی |

این عنصرها **تودرتو**‌اند: یک کاست ژنی درون یک اینتگرون، اینتگرون درون یک ترانسپوزون، و ترانسپوزون روی یک پلاسمید. همین ساختار توضیح می‌دهد چرا ژن‌های مقاومت این‌قدر سریع میان باکتری‌ها پخش می‌شوند.

**پلاسمید را چگونه تایپ کنیم؟** هر پلاسمید یک **رپلیکون** (ژن‌ها و جایگاه همانندسازی، مانند `repA`) دارد. پلاسمیدهایی با رپلیکون یکسان در یک سلول با هم کنار نمی‌آیند؛ به همین دلیل آن‌ها را در **گروه‌های ناسازگاری** (Inc) دسته‌بندی می‌کنند: IncF، IncI، IncX، IncN و مانند این‌ها. **PlasmidFinder** پایگاه توالی‌های رپلیکون است.

> 📺 **فیلم:** *Mobile Genetic Elements*: https://www.youtube.com/watch?v=ZiIKpkzhuVU · ‏*IS elements*: https://www.youtube.com/watch?v=nXDt-VeKCOU · اینتگرون: *Mechanism of Emergence of Antibiotic Resistance: Integron*: https://www.youtube.com/watch?v=9aLmUhrVHWI
> 📄 **مرجع:** Partridge SR, Kwong SM, Firth N, Jensen SO (2018). *Mobile genetic elements associated with antimicrobial resistance.* Clinical Microbiology Reviews 31:e00088-17. https://doi.org/10.1128/CMR.00088-17

---

## ۳. گام ۱: دانلود pEK499 و ساختن isoF

**چرا یک پلاسمید واقعی؟** «پلاسمید»های ماژول ۰۱ و ۰۲ تکه‌های DNA تصادفی بودند؛ رپلیکون و IS نداشتند. برای این درس به ساختار واقعی نیاز داریم. ‏pEK499 را با **E-utilities** از NCBI می‌گیریم: یک بار FASTA (برای ابزارها) و یک بار GenBank (برای آنوتیشن).

<div dir="ltr">

```bash
E=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
curl -sS "$E?db=nuccore&id=EU935739.1&rettype=fasta&retmode=text" > pEK499.fna
curl -sS "$E?db=nuccore&id=EU935739.1&rettype=gb&retmode=text" > pEK499.gb
head -1 pEK499.fna
grep -v ">" pEK499.fna | tr -d '\n' | wc -c
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`efetch.fcgi` | سرویس NCBI برای گرفتن رکورد |
| ‏`db=nuccore&id=EU935739.1` | پایگاه نوکلئوتید، شماره‌ی دسترسی pEK499 |
| ‏`rettype=fasta` / `rettype=gb` | قالب خروجی |
| ‏`tr -d '\n' \| wc -c` | پایان‌خط‌ها را برمی‌دارد و بازها را می‌شمارد |

**خروجی واقعی:**

<div dir="ltr">

```
>EU935739.1 Escherichia coli strain A plasmid pEK499, complete sequence
117536
```

</div>

حالا ایزوله‌ی **isoF** را می‌سازیم: کروموزوم K-12 + این پلاسمید، هر کدام با نامی کوتاه. ‏`sed` (بخش 01/08) سطر نام را عوض می‌کند و `>>` به پایان فایل می‌افزاید:

<div dir="ltr">

```bash
sed 's/^>.*/>isoF_chromosome/' genomes/isoC.fna > genomes/isoF.fna
sed 's/^>.*/>isoF_pEK499/' pEK499.fna >> genomes/isoF.fna
grep ">" genomes/isoF.fna
```

</div>

<div dir="ltr">

```
>isoF_chromosome
>isoF_pEK499
```

</div>

---

## ۴. گام ۲: ژن‌های مقاومت پلاسمید

<div dir="ltr">

```bash
amrfinder -n genomes/isoF.fna --organism Escherichia --plus --name isoF --threads 2 -o isoF.amr.tsv
awk -F'\t' '$3=="isoF_pEK499"' isoF.amr.tsv | cut -f4,5,6,7,9,13,14,17,18 | column -t -s$'\t'
```

</div>

**خروجی واقعی** (نزدیک به ۸۲ ثانیه، ۱۸۳ مگابایت):

<div dir="ltr">

```
39864  40670  +  blaTEM          core  BETA-LACTAM                                         BLASTX    94.06   100.00
52705  53901  -  tet(A)          core  TETRACYCLINE                                        EXACTX    100.00  100.00
57401  57952  +  aac(6')-Ib-cr5  core  AMIKACIN/KANAMYCIN/QUINOLONE/TOBRAMYCIN             ALLELEX   100.00  100.00
58086  58913  +  blaOXA-1        core  CEPHALOSPORIN                                       ALLELEX   100.00  100.00
59054  59494  +  catB3           core  CHLORAMPHENICOL                                     PARTIALX  70.00   100.00
62956  63828  -  blaCTX-M-15     core  CEPHALOSPORIN                                       ALLELEX   100.00  100.00
66738  67208  +  dfrA17          core  TRIMETHOPRIM                                        EXACTX    100.00  100.00
67342  68127  +  aadA5           core  STREPTOMYCIN                                        EXACTX    100.00  100.00
68336  68680  +  qacEdelta1      core  QUATERNARY AMMONIUM                                 ALLELEX   100.00  100.00
68677  69513  +  sul1            core  SULFONAMIDE                                         EXACTX    100.00  100.00
73595  74830  -  mrx(A)          core  AZITHROMYCIN/ERYTHROMYCIN/SPIRAMYCIN/TELITHROMYCIN  EXACTX    100.00  100.00
74830  75732  -  mph(A)          core  AZITHROMYCIN/ERYTHROMYCIN/SPIRAMYCIN/TELITHROMYCIN  EXACTX    100.00  100.00
```

</div>

**توضیح خروجی:** **۱۲ ژن core روی یک پلاسمید**، همه در نیمه‌ی میانی آن (باز ۳۹٬۸۶۴ تا ۷۵٬۷۳۲). چنین ناحیه‌ای را «جزیره‌ی مقاومت چندگانه» می‌نامند. یک پلاسمید به‌تنهایی مقاومت به بتالاکتام‌ها (سه ژن)، آمینوگلیکوزیدها، کینولون‌ها (`aac(6')-Ib-cr` هر دو را تغییر می‌دهد)، تتراسایکلین، تری‌متوپریم، سولفونامید و ماکرولیدها را می‌آورد. اگر این پلاسمید به سویه‌ی دیگری برود، **همه‌ی این مقاومت‌ها را با هم** می‌برد.

دو نکته برای ماژول ۰۱: ‏`blaTEM` با `BLASTX` (پوشش ۹۴٪) و `catB3` با `PARTIALX` (۷۰٪). بخش ۶ دلیل دومی را نشان می‌دهد.

---

## ۵. گام ۳: replicon typing با پایگاه PlasmidFinder

همان روش ماژول ۰۲ (VFDB)، این بار با پایگاه رپلیکون‌ها. نسخه‌ای از پایگاه PlasmidFinder را که ABRicate نگه می‌دارد برمی‌داریم:

<div dir="ltr">

```bash
mkdir -p plasmidfinder
curl -sS -o plasmidfinder/plasmidfinder.fna \
    https://raw.githubusercontent.com/tseemann/abricate/master/db/plasmidfinder/sequences
grep -c ">" plasmidfinder/plasmidfinder.fna
makeblastdb -in plasmidfinder/plasmidfinder.fna -dbtype nucl -out plasmidfinder/plasmidfinder > /dev/null
blastn -query genomes/isoF.fna -db plasmidfinder/plasmidfinder -perc_identity 80 \
    -max_target_seqs 10000 -outfmt "6 qseqid qstart qend pident length slen stitle" -out isoF.pf.tsv
wc -l < isoF.pf.tsv
```

</div>

<div dir="ltr">

```
488
14
```

</div>

‏۴۸۸ توالی رپلیکون در پایگاه؛ ۱۴ هم‌ردیفی روی isoF. ولی بیشترشان خویشاوندهای ضعیف یک رپلیکون‌اند. ابزار رسمی PlasmidFinder به‌طور پیش‌فرض همانندی **۹۰٪** و پوشش **۶۰٪** می‌خواهد (README رسمی آن). همین را می‌گذاریم و برای هر جایگاه تنها **بهترین** هم‌ردیفی را نگه می‌داریم:

<div dir="ltr">

```bash
awk -F'\t' '$4 >= 90 && $5/$6 >= 0.6' isoF.pf.tsv \
  | sort -t$'\t' -k2,2n -k4,4nr | awk -F'\t' '!seen[$2]++' \
  | awk -F'\t' '{split($7, a, "~~~"); print $1"\t"$2"\t"$3"\t"$4"\t"$5"/"$6"\t"a[2]}'
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`$4 >= 90 && $5/$6 >= 0.6` | آستانه‌های پیش‌فرض PlasmidFinder |
| ‏`sort -k2,2n -k4,4nr` | بر پایه‌ی جای آغاز، و در هر جا بیشترین همانندی نخست |
| ‏`awk '!seen[$2]++'` | از هر جای آغاز تنها سطر نخست (بهترین) را نگه می‌دارد |
| ‏`split($7, a, "~~~")` | نام رپلیکون را از سرآیند جدا می‌کند |

**خروجی واقعی:**

<div dir="ltr">

```
isoF_pEK499	2373	2760	99.742	388/388	IncFIA_1
isoF_pEK499	2470	2760	91.065	291/295	FIA(pBK30683)_1
isoF_pEK499	43354	43614	100.000	261/261	IncFII_1
```

</div>

**توضیح خروجی:** دو جایگاه رپلیکون: **IncFIA** (باز ۲۳۷۳) و **IncFII** (باز ۴۳۳۵۴). سطر دوم (`FIA(pBK30683)`) روی **همان ناحیه‌ی** سطر نخست است (۲۴۷۰ تا ۲۷۶۰ درون ۲۳۷۳ تا ۲۷۶۰) با همانندی کمتر؛ یعنی همان رپلیکون FIA، نه رپلیکون سوم. پس pEK499 یک **پلاسمید IncF با دو رپلیکون FII و FIA** است، همان چیزی که مقاله‌ی اصلی (Woodford و همکاران، 2009) گزارش کرده است. پلاسمیدهای IncF مشهورترین حامل CTX-M-15 در *E. coli* ‏ST131‌اند.

<details>
<summary>✋ امتحان کن: همین دستور blastn را روی isoA (ماژول ۰۱) اجرا کنید. چند رپلیکون پیدا می‌شود؟ آیا این یعنی <code>isoA_pA</code> پلاسمید نیست؟</summary>

**صفر** (ما برای isoA تا isoE اجرا کردیم: همه صفر). ‏`isoA_pA` در واقع DNA تصادفی است و رپلیکون ندارد؛ پس پاسخ درست برای این داده «پلاسمید نیست» است. ولی در یک ایزوله‌ی واقعی، **نبودن رپلیکون در یک contig، دلیل کروموزومی بودن آن نیست**: اسمبلی short-read پلاسمید را به چند contig می‌شکند و رپلیکون تنها روی یکی از آن‌هاست. این مشکلی است که MOB-suite (بخش ۷) برای حلش ساخته شده.

</details>

> 📺 **فیلم:** *What Exactly Is a Plasmid*: https://www.youtube.com/watch?v=i4JEao2rQ64 · *Origin of Replication – Plasmids 101*: https://www.youtube.com/watch?v=pN4Hx11QVS4
> 📄 **مرجع:** Carattoli A, et al. (2014). *In silico detection and typing of plasmids using PlasmidFinder and plasmid multilocus sequence typing.* Antimicrobial Agents and Chemotherapy 58:3895–3903. https://doi.org/10.1128/AAC.02412-14 · PlasmidFinder: https://bitbucket.org/genomicepidemiology/plasmidfinder

---

## ۶. گام ۴: ژن مقاومت کنار کدام IS است؟

آنوتیشن GenBank پلاسمید، جای IS‌ها را در ویژگی‌های `mobile_element` دارد:

<div dir="ltr">

```bash
awk '/^     mobile_element/ {loc = $2} /mobile_element_type=/ {split($0, a, ":"); gsub(/"/, "", a[2]); print loc "\t" a[2]}' pEK499.gb
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
36287..37106	IS26
37107..38746	ISEcp1
40672..41439	IS1
56490..57309	IS26
59496..60315	IS26
63901..64720	IS26
71690..72569	IS6100
75802..76621	IS26
86629..87448	IS26
102302..103069	IS1
113193..115724	IS66
```

</div>

‏`awk` جای هر ویژگی را در `loc` نگه می‌دارد و در سطر `mobile_element_type` نام IS را (پس از `:`) چاپ می‌کند؛ `gsub` نشانه‌ی `"` را برمی‌دارد.

‏۱۱ IS، که **هفت** تای آن‌ها IS26‌اند. ‏IS26 یکی از مهم‌ترین IS‌ها در جابه‌جایی ژن‌های مقاومت در باکتری‌های گرم‌منفی است.

اسکریپت `gene_context.py` برای هر ژن core، ISهایی را که در فاصله‌ی معینی از آن‌اند فهرست می‌کند:

<div dir="ltr">

```bash
python3 $P/03_Mobile_Elements_CRISPR/scripts/gene_context.py pEK499.gb isoF.amr.tsv isoF_pEK499 2000 \
  | column -t -s$'\t'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
gene            gene_pos     element  element_pos  distance
blaTEM          39864-40670  ISEcp1   37107-38746  1118
blaTEM          39864-40670  IS1      40672-41439  2
aac(6')-Ib-cr5  57401-57952  IS26     56490-57309  92
aac(6')-Ib-cr5  57401-57952  IS26     59496-60315  1544
blaOXA-1        58086-58913  IS26     56490-57309  777
blaOXA-1        58086-58913  IS26     59496-60315  583
catB3           59054-59494  IS26     56490-57309  1745
catB3           59054-59494  IS26     59496-60315  2
blaCTX-M-15     62956-63828  IS26     63901-64720  73
mrx(A)          73595-74830  IS6100   71690-72569  1026
mrx(A)          73595-74830  IS26     75802-76621  972
mph(A)          74830-75732  IS26     75802-76621  70
```

</div>

**سه یافته‌ی واقعی:**

1. ‏**‏`catB3` بریده شده به دست IS26.** ‏`catB3` در ۵۹۴۹۴ تمام می‌شود و IS26 از ۵۹۴۹۶ آغاز می‌شود: فاصله‌ی ۲ باز. پس IS26 درست در میان ژن نشسته و ۳۰٪ پایانی آن را از بین برده است. همین دلیل `PARTIALX` با پوشش ۷۰٪ است. **یک ژن ناقص، رد پای یک رویداد جابه‌جایی است.**
2. **یک ترانسپوزون مرکب شبیه:** ‏`aac(6')-Ib-cr` ← `blaOXA-1` ← `catB3` بریده، میان **دو IS26** (۵۶۴۹۰ و ۵۹۴۹۶). دو IS هم‌نوع در دو سوی چند ژن مقاومت، ساختاری است که می‌تواند همه را با هم جابه‌جا کند.
3. ‏**‏`blaCTX-M-15` تنها ۷۳ باز از یک IS26 فاصله دارد.** ‏CTX-M-15 روی رشته‌ی منفی است، پس بالادست آن (جایی که پروموتر هست) در مختصات **بزرگ‌تر** است: همان سوی IS26. در بسیاری از پلاسمیدها CTX-M-15 کنار ISEcp1 است که پروموتر آن را فراهم می‌کند؛ در pEK499، ‏ISEcp1 در جای دیگری (۳۷۱۰۷) است و IS26 کنار CTX-M-15 نشسته.

**اینتگرون کلاس ۱:** چهار ژن `dfrA17` ← `aadA5` ← `qacEdelta1` ← `sul1` (۶۶۷۳۸ تا ۶۹۵۱۳) ساختار کلاسیک اینتگرون کلاس ۱ است: دو **کاست** (`dfrA17` و `aadA5`) و سپس بخش ثابت `3'-CS` (`qacEΔ1` + `sul1`). اینتگراز کجاست؟

<div dir="ltr">

```bash
grep -B1 '/gene="int"' pEK499.gb | grep "CDS"
```

</div>

<div dir="ltr">

```
     CDS             complement(65567..66580)
```

</div>

اینتگراز در ۶۵۵۶۷ تا ۶۶۵۸۰ است، درست پیش از `dfrA17` (۶۶۷۳۸)؛ آنوتیشن آن را «شبیه اینتگراز پلاسمید R100» می‌نامد. ترتیب کامل: **‏int ← dfrA17 ← aadA5 ← qacEΔ1 ← sul1**.

<details>
<summary>✋ امتحان کن: اگر یک باکتری تنها کاست <code>dfrA17</code> را از دست بدهد، به کدام دارو حساس می‌شود و کدام مقاومت هنوز می‌ماند؟</summary>

به **تری‌متوپریم** حساس می‌شود (Subclass `TRIMETHOPRIM`). مقاومت به استرپتومایسین (`aadA5`)، ترکیب‌های آمونیوم چهارتایی (`qacEΔ1`) و سولفونامید (`sul1`) می‌ماند؛ سولفونامید و qac در بخش ثابت اینتگرون‌اند و با کاست‌ها جابه‌جا نمی‌شوند.

</details>

> 📺 **فیلم:** *Transposons Animation – DNA transposable elements*: https://www.youtube.com/watch?v=CroyUMRpbxg
> 📄 **مرجع:** Woodford N, et al. (2009). *Complete nucleotide sequences of plasmids pEK204, pEK499, and pEK516, encoding CTX-M enzymes in three major Escherichia coli lineages from the United Kingdom, all belonging to the international O25:H4-ST131 clone.* Antimicrob Agents Chemother 53:4472–4482. https://doi.org/10.1128/AAC.00688-09 · Mazel D (2006). *Integrons: agents of bacterial evolution.* Nature Reviews Microbiology 4:608–620. https://doi.org/10.1038/nrmicro1462

---

## ‏۷. ‏MOB-suite و ابزارهای IS (از مستندات)

در یک ایزوله‌ی واقعی، آنوتیشن GenBank آماده‌ای نداریم و پلاسمید چند contig است. دو ابزار:

‏**MOB-suite** (آزمایشگاه ملی میکروب‌شناسی کانادا) دو کار اصلی دارد:

<div dir="ltr">

```bash
conda create -n mobsuite -c conda-forge -c bioconda mob_suite
conda activate mobsuite
mob_recon --infile genomes/isoF.fna --outdir mob_isoF
mob_typer --infile pEK499.fna --out_file pEK499_mobtyper.txt
```

</div>

- ‏**`mob_recon`** contigهای یک اسمبلی را به «کروموزوم» یا گروه‌های پلاسمیدی جدا نسبت می‌دهد (فایل `contig_report.txt`) و هر پلاسمید بازسازی‌شده را جدا می‌نویسد.
- ‏**`mob_typer`** برای هر پلاسمید رپلیکون، relaxase (ژن انتقال) و **پیش‌بینی جابه‌جایی‌پذیری** می‌دهد: ستون `predicted_mobility` با سه مقدار **Conjugative** (خودش منتقل می‌شود)، **Mobilizable** (با کمک پلاسمید دیگر) و **Non-mobilizable**.
- به گفته‌ی README، در نخستین اجرا `mob_init` پایگاه‌های بزرگی را از figshare دانلود و آماده می‌کند؛ این کار زمان و حافظه‌ی زیادی می‌برد. برای همین ما آن را اجرا نکردیم.

**پیش‌بینی (اجرا نشده):** برای isoF انتظار داریم `mob_recon` contig `isoF_pEK499` را یک پلاسمید IncF جدا کند؛ برای `predicted_mobility` عددی نمی‌گوییم، خودتان ببینید.

**ابزارهای IS:** ‏**ISfinder** پایگاه مرجع IS‌هاست (جست‌وجوی وب BLAST در سایت آن) و **MobileElementFinder** (مرکز اپیدمیولوژی ژنومی DTU) IS، ترانسپوزون و فاصله‌ی آن‌ها از ژن‌های مقاومت را از روی contig می‌دهد؛ یعنی کاری که ما در بخش ۶ با آنوتیشن آماده انجام دادیم.

> 📺 **فیلم:** دوره‌ی DTU در Coursera (پلاسمید و تایپ آن با ابزارهای CGE): https://www.coursera.org/learn/wgs-bacteria
> 📄 **مرجع:** Robertson J, Nash JHE (2018). *MOB-suite: software tools for clustering, reconstruction and typing of plasmids from draft assemblies.* Microbial Genomics 4:e000206. https://doi.org/10.1099/mgen.0.000206 · MOB-suite: https://github.com/phac-nml/mob-suite · ISfinder: https://isfinder.biotoul.fr · Siguier P, et al. (2006). *ISfinder: the reference centre for bacterial insertion sequences.* Nucleic Acids Research 34:D32–D36. https://doi.org/10.1093/nar/gkj014

---

## ۸. سه اشتباه رایج

1. ‏**«contig بی رپلیکون = کروموزوم».** پلاسمید در اسمبلی short-read چند تکه است؛ تنها یک تکه رپلیکون دارد.
2. **گزارش همه‌ی هم‌ردیفی‌های PlasmidFinder.** ‏۱۴ سطر برای دو رپلیکون بود. آستانه‌ی ۹۰/۶۰ را بگذارید و برای هر جایگاه بهترین را نگه دارید.
3. **نادیده گرفتن ژن ناقص.** ‏`catB3` ناقص اثر دارویی ندارد، ولی نشان می‌دهد IS26 در این ناحیه فعال بوده است.

---

## 📘 برای کنجکاوها

- اسمبلی **long-read** (Nanopore یا PacBio) در بسیاری از موارد پلاسمید را در یک contig حلقوی کامل می‌سازد، چون رید از IS‌های تکراری بلندتر است. این را در دوره‌ی جداگانه‌ی NGS و نسل سوم می‌بینید.
- ‏**pMLST** (MLST پلاسمیدی)، برای نمونه «فرمول FAB» برای IncF (مانند F2:A1:B-)، پلاسمیدهای یک گروه Inc را ریزتر تایپ می‌کند.

---

## جمع‌بندی

- عنصرهای متحرک تودرتو‌اند: کاست ← اینتگرون ← ترانسپوزون ← پلاسمید.
- ‏pEK499: پلاسمید IncFII/IncFIA با ۱۲ ژن core در یک ناحیه‌ی ۳۶ هزار بازی، با ۱۱ IS (هفت IS26) و یک اینتگرون کلاس ۱.
- ‏replicon typing = BLAST روی پایگاه PlasmidFinder با آستانه‌ی ۹۰٪ همانندی / ۶۰٪ پوشش، و بهترین هم‌ردیفی در هر جایگاه.
- فاصله‌ی ژن تا IS، رویدادهای جابه‌جایی را نشان می‌دهد (`catB3` بریده با IS26).
- در اسمبلی واقعی، MOB-suite contigها را به پلاسمید یا کروموزوم نسبت می‌دهد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
E=https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
curl -sS "$E?db=nuccore&id=ACC&rettype=fasta&retmode=text" > ACC.fna
curl -sS "$E?db=nuccore&id=ACC&rettype=gb&retmode=text"    > ACC.gb
blastn -query ASM.fna -db plasmidfinder/plasmidfinder -perc_identity 80 -max_target_seqs 10000 \
    -outfmt "6 qseqid qstart qend pident length slen stitle" -out ID.pf.tsv
awk -F'\t' '$4 >= 90 && $5/$6 >= 0.6' ID.pf.tsv | sort -t$'\t' -k2,2n -k4,4nr | awk -F'\t' '!seen[$2]++'
python3 gene_context.py PLASMID.gb ID.amr.tsv CONTIG 2000
mob_recon --infile ASM.fna --outdir mob_ID          # documented, not run here
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| عنصر ژنتیکی متحرک (MGE) | هر تکه‌ی DNA که میان جایگاه‌ها یا سلول‌ها جابه‌جا می‌شود |
| هم‌یوغی (conjugation) | انتقال پلاسمید از یک باکتری به باکتری دیگر با تماس مستقیم |
| ‏IS (insertion sequence) | کوچک‌ترین عنصر جابه‌جاشونده؛ تنها ژن ترانسپوزاز |
| ترانسپوزون مرکب | ژن(های) بار میان دو IS هم‌نوع |
| اینتگرون / کاست ژنی | سامانه‌ی اینتگراز برای گرفتن و چیدن کاست‌ها / ژنی که با یک جایگاه `attC` جابه‌جا می‌شود |
| ‏3'-CS | بخش ثابت پایانی اینتگرون کلاس ۱ (`qacEΔ1` + `sul1`) |
| رپلیکون (replicon) | ژن‌ها و جایگاه همانندسازی پلاسمید |
| گروه ناسازگاری (Inc) | دسته‌بندی پلاسمیدها بر پایه‌ی رپلیکون |
| ‏relaxase | آنزیم آغاز انتقال پلاسمید در هم‌یوغی |
| ‏E-utilities | سرویس‌های خط فرمانی NCBI برای جست‌وجو و گرفتن رکوردها |

---

## منابع

**مستند و مقاله**
- Partridge SR, et al. (2018). *Mobile genetic elements associated with antimicrobial resistance.* Clin Microbiol Rev 31:e00088-17. https://doi.org/10.1128/CMR.00088-17
- Carattoli A, et al. (2014). *In silico detection and typing of plasmids using PlasmidFinder and plasmid multilocus sequence typing.* Antimicrob Agents Chemother 58:3895–3903. https://doi.org/10.1128/AAC.02412-14
- Woodford N, et al. (2009). *Complete nucleotide sequences of plasmids pEK204, pEK499, and pEK516…* Antimicrob Agents Chemother 53:4472–4482. https://doi.org/10.1128/AAC.00688-09 · GenBank EU935739.1: https://www.ncbi.nlm.nih.gov/nuccore/EU935739.1
- Mazel D (2006). *Integrons: agents of bacterial evolution.* Nat Rev Microbiol 4:608–620. https://doi.org/10.1038/nrmicro1462
- Robertson J, Nash JHE (2018). *MOB-suite…* Microbial Genomics 4:e000206. https://doi.org/10.1099/mgen.0.000206 · https://github.com/phac-nml/mob-suite
- Siguier P, et al. (2006). *ISfinder: the reference centre for bacterial insertion sequences.* Nucleic Acids Res 34:D32–D36. https://doi.org/10.1093/nar/gkj014
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/

**کتاب**
- ‏Craig NL, Chandler M, Gellert M, Lambowitz AM, Rice PA, Sandmeyer SB (eds.) (2015). *Mobile DNA III*. ASM Press. (فصل‌های پلاسمید، IS و اینتگرون)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Whole genome sequencing of bacterial genomes – tools and applications* (DTU): https://www.coursera.org/learn/wgs-bacteria
- ‏Coursera: *Antimicrobial resistance – theory and methods* (DTU؛ انتقال افقی ژن): https://www.coursera.org/learn/antimicrobial-resistance
- ‏edX: دوره‌ای ویژه‌ی عنصرهای متحرک در edX نیافتیم؛ نزدیک‌ترین: *Microbiology* (SNHU، MicroBachelors): https://www.edx.org/learn/microbiology/southern-new-hampshire-university-microbiology
- ‏YouTube: *Mobile Genetic Elements*: https://www.youtube.com/watch?v=ZiIKpkzhuVU
- ‏YouTube: *IS elements*: https://www.youtube.com/watch?v=nXDt-VeKCOU
- ‏YouTube: *Transposons Animation*: https://www.youtube.com/watch?v=CroyUMRpbxg
- ‏YouTube: *Mechanism of Emergence of Antibiotic Resistance: Integron*: https://www.youtube.com/watch?v=9aLmUhrVHWI
- ‏YouTube: *What Exactly Is a Plasmid*: https://www.youtube.com/watch?v=i4JEao2rQ64

‏<sub>pEK499 در 2026-10-24 با E-utilities گرفته شد. پیش‌فرض‌های PlasmidFinder (۰٫۹۰ / ۰٫۶۰) از README رسمی آن، و پایگاه از مخزن ABRicate (commit `e2064df`، ‏۴۸۸ توالی). دستورهای MOB-suite از README رسمی آن. نشانی‌های فیلم از جست‌وجوی وب‌اند؛ در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
