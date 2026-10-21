<div dir="rtl">

# درس ۱: چه کسانی در نمونه‌اند؟ Kraken2 و Bracken

**بخش:** `06_Metagenomics` · **ماژول:** `03_Taxonomic_Functional_Profiling` · **پیش‌نیاز:** ماژول [برداشتن میزبان](../02_Host_Removal_Alignment/)؛ [NCBI Taxonomy و datasets](../../02_BioLinux/05_Data_Download/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** Kraken2 2.17.1، Bracken 3.0.1 · **خروجی‌ها از اجرای:** 2026-10-13

---

> ## ⚠️ پایگاه داده‌ی این درس تنها برای تمرین است
> تا درس روی هر لپ‌تاپی و با اینترنت کند اجرا شود، یک **پایگاه داده‌ی تمرینی کوچک** از ۴۵ ژنوم (۲۶۳ مگابایت) می‌سازیم. این پایگاه تنها برای **فهم منطق ابزار و سنجیدن گونه‌های خطا** مناسب است.
>
> **برای کار پژوهشی، پایگاه داده‌ی کامل لازم است**؛ برای نمونه مجموعه‌های رسمی Kraken2 در https://benlangmead.github.io/aws-indexes/k2 (نسخه‌ی 2026-06-26):
>
> | مجموعه | حجم دانلود | حجم شاخص | محتوا |
> | :--- | ---: | ---: | :--- |
> ‏| Standard | 79.6 GB | 103.1 GB | RefSeq: باکتری، آرکی، ویروس، انسان، وکتورها |
> ‏| Standard-16 / Standard-8 | 11.2 / 5.5 GB | 14.9 / 7.5 GB | همان، فشرده‌شده برای ۱۶ یا ۸ گیگابایت حافظه (کمی کم‌دقت‌تر) |
> ‏| PlusPF | 84.8 GB | 109.9 GB | ‏Standard + پروتوزوآ و قارچ‌ها |
>
> عددهایی که با پایگاه تمرینی می‌گیرید (درصدها، شمار گونه‌های ساختگی) **به داده‌ی واقعی تعمیم‌پذیر نیست**؛ تنها گونه‌ی خطاها و منطق تفسیر تعمیم‌پذیر است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. منطق Kraken2 را بگویید: k-mer، و «نزدیک‌ترین نیای مشترک» (LCA).
2. یک پایگاه داده‌ی کوچک Kraken2 بسازید و ریدهای جفتی را طبقه‌بندی کنید.
3. سه خروجی Kraken2 را بخوانید: گزارش صفحه، `.kraken` (یک خط برای هر رید) و `.kreport` (یک خط برای هر تاکسون).
4. با Bracken فراوانی سطح گونه را برآورد کنید و بدانید چرا لازم است.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate metagenomics
cd ~/meta
C=~/Bioinformatics_Learning-main/06_Metagenomics/99_scripts_data
S=$C/03_Taxonomic_Functional_Profiling/scripts
cp $C/data/ground_truth_species.tsv .
ls host/clean
```

</div>

در `host/clean/` باید ریدهای پاک دو نمونه باشند (ماژول ۰۲).

---

## ۱. داستان

پرسش اصلی بسیاری از پروژه‌های میکروبیوم: **«چه کسانی، و به چه نسبتی، در نمونه هستند؟»** این را *پروفایل تاکسونومیک* می‌نامند. پاسخ ساده به نظر می‌رسد ولی سه سرچشمه‌ی خطای جدی دارد:

1. **پایگاه داده:** ابزار تنها چیزی را می‌شناسد که در پایگاه هست. گونه‌ی غایب یا گم می‌شود یا به نزدیک‌ترین خویشاوندش نسبت داده می‌شود.
2. **همانندی گونه‌ها:** ریدهای کوتاه از نواحی حفاظت‌شده، میان چند گونه مشترک‌اند.
3. **تعریف فراوانی:** «درصد ریدها» با «درصد سلول‌ها» یکی نیست (اندازه‌ی ژنوم‌ها فرق دارد).

برتری داده‌ی این دوره: **پاسخ درست را داریم** (`ground_truth_species.tsv`). پس هر سه گونه خطا را می‌شود **اندازه گرفت**، نه حدس زد. این درس ابزار را اجرا می‌کند؛ درس ۲ آن را می‌سنجد.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏k-mer: واژه‌های ۳۵ حرفی

یک k-mer هر تکه‌ی پیوسته‌ی k بازی از یک توالی است. رید ۱۲۶ بازی، 126 − 35 + 1 = **۹۲** تا ۳۵-مر دارد. Kraken2 برای **هر** ۳۵-مر در پایگاه یادداشت کرده است که در ژنوم کدام تاکسون‌ها دیده می‌شود.

### ‏۲.۲ ‏LCA: «نزدیک‌ترین نیای مشترک»

اگر یک k-mer تنها در *E. coli* باشد، برچسبش *E. coli* است. اگر هم در *E. coli* و هم در *Shigella* باشد، برچسبش **نزدیک‌ترین گره‌ی مشترک** آن‌ها در درخت تاکسونومی است: خانواده‌ی Enterobacteriaceae.

<div dir="ltr">

```text
                Enterobacteriaceae (543)        <- LCA of E. coli and Shigella
                 /                   \
        Escherichia (561)        Shigella (620)
           /        \                  \
   E. coli (562)  E. fergusonii    S. sonnei (624)
```

</div>

سپس برای هر رید، Kraken2 برچسب‌های همه‌ی k-merهایش را روی درخت می‌گذارد و **پربارترین مسیر ریشه تا برگ** را برمی‌گزیند. اگر k-merها میان دو شاخه تقسیم شده باشند، رید در گره‌ی بالاتر (LCA) می‌ماند.

### ۲.۳ چرا Bracken؟

ریدی که میان *E. coli* و *Shigella* مشترک است، در Kraken2 در سطح خانواده می‌ماند و **به هیچ گونه‌ای شمرده نمی‌شود**. پس شمار سطح گونه‌ی Kraken2 کمتر از واقعیت است. **Bracken** با یک مدل آماری (بر پایه‌ی اینکه ریدهای هر ژنوم در بسیاری از موارد در کدام سطح می‌مانند) این ریدها را **میان گونه‌ها پخش می‌کند**. این مدل به **طول رید** وابسته است، پس برای هر طول رید جدا ساخته می‌شود.

---

## ۳. گام ۱: ساختن پایگاه داده‌ی تمرینی (یک بار)

> این گام **کمابیش ۱۳۰ مگابایت** دانلود دارد (۴۵ ژنوم + تاکسونومی NCBI). اگر اینترنتتان کند است، آن را زمانی اجرا کنید که فرصت دارید.

<div dir="ltr">

```bash
bash $S/build_practice_db.sh
```

</div>

اسکریپت پنج کار می‌کند:

| گام اسکریپت | ابزار | کار |
| :--- | :--- | :--- |
| ۱ | ‏`datasets` (بخش ۰۲) | دانلود ۴۵ ژنوم فهرست [`practice_db_genomes.tsv`](../99_scripts_data/03_Taxonomic_Functional_Profiling/data/practice_db_genomes.tsv) |
| ۲ | ‏`curl` | دانلود درخت تاکسونومی NCBI (`nodes.dmp`، `names.dmp`) |
| ۳ | ‏`awk` | سرآیند هر توالی را `>kraken:taxid|817|…` می‌کند تا Kraken2 بداند هر ژنوم از کدام تاکسون است |
| ۴ | ‏`kraken2-build` | ساختن جدول k-mer ← LCA (`hash.k2d`) |
| ۵ | ‏`bracken-build` | ساختن مدل Bracken برای دو طول رید داده‌ی ما (۱۲۵ و ۱۵۰) |

پایگاه **عمداً همانند دنیای واقعی** طراحی شده است:
- **۲۱ گونه‌ی درون نمونه‌ها**، ولی با **سویه‌ای دیگر** جز سویه‌ای که ریدها از آن شبیه‌سازی شده‌اند (برای نمونه *E. coli* سویه‌ی ST540، نه K-12). در نمونه‌ی واقعی هم سویه‌ی شما کمابیش هرگز عیناً در پایگاه نیست.
- **۲۴ گونه‌ی خویشاوند نزدیک** (*decoy*): *Shigella sonnei/flexneri* و *Escherichia fergusonii* کنار *E. coli*، *Acinetobacter pittii* کنار *A. baumannii*، *Phocaeicola dorei* کنار *Bacteroides*، …
- ‏***Candida albicans* (قارچ) عمداً کنار گذاشته شده**، با آنکه ۳٫۵٪ ریدهای `minigut_sample2` از آن است.

خروجی ساختن در 2026-10-13: ۹۲ توالی، ۱۶۹٫۳ مگاباز، `hash.k2d` به اندازه‌ی ۲۶۳ مگابایت، ساختن در ۱۸ ثانیه. پایگاه در `profile/kraken2_practice_db/` است.

---

## ۴. گام ۲: طبقه‌بندی با Kraken2

<div dir="ltr">

```bash
mkdir -p profile/kraken
kraken2 --db profile/kraken2_practice_db --threads 4 --paired \
        --report profile/kraken/minigut_c0.kreport \
        --output profile/kraken/minigut_c0.kraken \
        host/clean/minigut_R1.fastq.gz host/clean/minigut_R2.fastq.gz
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `--db` | پوشه‌ی پایگاه داده | ‏Kraken2 پایگاه پیش‌فرض را می‌جوید و با خطا می‌ایستد |
| ② `--threads 4` | چهار هسته | کندتر |
| ③ `--paired` | دو فایل پشت سر هم، **یک جفت**اند؛ k-merهای دو رید با هم داوری می‌شوند | هر فایل جداگانه طبقه‌بندی و شمرده می‌شود |
| ④ `--report` | گزارش خلاصه، یک خط برای هر تاکسون (`.kreport`) | تنها خروجی رید به رید |
| ⑤ `--output` | خروجی رید به رید (`.kraken`) | در stdout چاپ می‌شود (ده‌ها هزار خط روی صفحه) |
| ⑥ دو فایل FASTQ | ‏R1 و R2 | — |

نام فایل‌ها `_c0` دارند، چون `--confidence` پیش‌فرض صفر است (درس ۲ آن را عوض می‌کند).

گزارش صفحه (در stderr):

<div dir="ltr">

```text
Loading database information... done.
49845 sequences (12.55 Mbp) processed in 0.198s (15142.2 Kseq/m, 3811.19 Mbp/m).
  47428 sequences classified (95.15%)
  2417 sequences unclassified (4.85%)
```

</div>

- ‏`49845 sequences`: با `--paired`، هر **جفت** یک «sequence» است.
- ‏**۹۵٫۱۵٪ طبقه‌بندی شد**، ‏۴٫۸۵٪ نه. چرا ریدی از *E. coli* یا *B. fragilis* بی‌برچسب بماند، با آنکه هر دو گونه در پایگاه‌اند؟ پاسخ: سویه‌ی پایگاه با سویه‌ی نمونه فرق دارد (تمرین ۱).
- ۰٫۲ ثانیه: پایگاه کوچک است. با پایگاه Standard، بارگذاری خود پایگاه در حافظه چند دقیقه طول می‌کشد.

---

## ۵. گام ۳: خروجی رید به رید (`.kraken`)

<div dir="ltr">

```bash
head -n 3 profile/kraken/minigut_c0.kraken
```

</div>

<div dir="ltr">

```text
C	NC_006347.1_0	817	126|126	817:71 816:21 |:| 817:13 0:11 817:1 0:21 817:46
C	NC_006347.1_1	817	126|126	817:92 |:| 817:25 0:46 817:21
C	NC_006347.1_2	817	126|126	817:92 |:| 817:92
```

</div>

| ستون | نمونه | معنی |
| :---: | :--- | :--- |
| ۱ | `C` | طبقه‌بندی‌شده (*Classified*)؛ `U` = نشده |
| ۲ | `NC_006347.1_0` | نام رید |
| ۳ | `817` | شناسه‌ی تاکسون برگزیده (taxid؛ 817 = *Bacteroides fragilis*) |
| ۴ | `126\|126` | طول R1 و R2 |
| ۵ | `817:71 816:21 \|:\| …` | برچسب k-merها، پشت سر هم: «۷۱ k-mer با برچسب 817، سپس ۲۱ با 816 (جنس *Bacteroides*)»؛ `\|:\|` مرز R1 و R2؛ `0` = k-mer در پایگاه نیست |

رید نخست: ۷۱ + ۲۱ = ۹۲ k-mer در R1 (همان عدد بخش ۲.۱). ۲۱ k-mer تنها تا سطح جنس را می‌گویند، ولی گونه را رد نمی‌کنند، پس رید به گونه رسید.

چون نام هر رید مبدأ **واقعی‌اش** را دارد، می‌توانیم ببینیم ریدهای *E. coli* (`NC_000913`) کجا رفتند. ستون ۲ با نام، ستون ۳ با taxid برگزیده:

<div dir="ltr">

```bash
awk -F'\t' '$2 ~ /^NC_000913/ {print $3}' profile/kraken/minigut_c0.kraken | sort | uniq -c | sort -rn | head -n 8
```

</div>

<div dir="ltr">

```text
   8981 562
   4909 543
   2241 624
   1672 623
   1312 620
    770 564
    765 0
    300 561
```

</div>

با درخت بخش ۲.۲:

| مقصد ریدهای *E. coli* | taxid | جفت | ٪ از ۲۱٬۰۱۸ |
| :--- | :-: | ---: | ---: |
| ‏*E. coli* (گونه) | 562 | 8,981 | 42.7 |
| ‏Enterobacteriaceae (خانواده؛ LCA) | 543 | 4,909 | 23.4 |
| *Shigella sonnei* | 624 | 2,241 | 10.7 |
| *Shigella flexneri* | 623 | 1,672 | 8.0 |
| ‏*Shigella* (جنس) | 620 | 1,312 | 6.2 |
| *E. fergusonii* | 564 | 770 | 3.7 |
| طبقه‌بندی‌نشده | 0 | 765 | 3.6 |
| ‏*Escherichia* (جنس) | 561 | 300 | 1.4 |

**تنها ۴۳٪ ریدهای *E. coli* به *E. coli* رسیدند.** کمابیش ۲۵٪ به *Shigella* رفتند. این خطای ابزار نیست، **واقعیت زیستی** است: *Shigella* از دید فیلوژنی چند دودمان **درون** گونه‌ی *E. coli* است (Pupo و همکاران، ۲۰۰۰) و تنها به دلایل بالینی و تاریخی نام جنس جدا دارد. نواحی‌ای از ژنوم K-12 که در *E. coli* پایگاه (ST540) نیست ولی در *Shigella* هست، به *Shigella* می‌رسند. **درس:** در سطح گونه، مرزهای تاکسونومی همیشه با مرزهای ژنومی یکی نیستند.

<details>
<summary>✋ امتحان کن: ۴۹۰۹ ریدی که در Enterobacteriaceae ماندند، چرا به هیچ جنسی نرسیدند؟</summary>

‏k-merهایشان هم در *Escherichia* و هم در *Shigella* (یا دیگر اعضای خانواده) بود؛ هیچ شاخه‌ی پایین‌تری همه‌ی آن‌ها را نداشت، پس رید در LCA ماند. این‌ها همان ریدهایی‌اند که Bracken (گام ۵) میان گونه‌ها پخش می‌کند.

</details>

---

## ۶. گام ۴: گزارش تاکسون به تاکسون (`.kreport`)

<div dir="ltr">

```bash
head -n 12 profile/kraken/minigut_c0.kreport
```

</div>

<div dir="ltr">

```text
  4.85	2417	2417	U	0	unclassified
 95.15	47428	0	R	1	root
 95.15	47428	0	R1	131567	  cellular organisms
 95.15	47428	0	D	2	    Bacteria
 95.15	47428	0	K	3379134	      Pseudomonadati
 54.52	27175	0	K1	1783270	        FCB group
 54.52	27175	0	K2	68336	          Bacteroidota/Chlorobiota group
 54.52	27175	0	P	976	            Bacteroidota
 54.52	27175	0	C	200643	              Bacteroidia
 54.52	27175	0	O	171549	                Bacteroidales
 54.52	27175	28	F	815	                  Bacteroidaceae
 51.41	25627	6	G	816	                    Bacteroides
```

</div>

| ستون | نمونه | معنی |
| :---: | :--- | :--- |
| ۱ | `54.52` | درصد ریدهای نمونه در این **شاخه** (خودش + همه‌ی زیرشاخه‌ها) |
| ۲ | `27175` | شمار ریدهای شاخه |
| ۳ | `28` | ریدهایی که **دقیقاً** در همین گره ماندند (LCA) |
| ۴ | `F` | رتبه: U، R (ریشه)، D (قلمرو)، K، P (شاخه)، C (رده)، O (راسته)، F (خانواده)، G (جنس)، S (گونه)؛ `K1`، `G1`… گره‌های میان‌رتبه |
| ۵ | `815` | ‏taxid |
| ۶ | `Bacteroidaceae` | نام؛ **فاصله‌های آغاز** عمق درخت را نشان می‌دهند |

سطرهای خانواده‌ی Enterobacteriaceae (awk با `$6 ~`، یعنی «ستون ۶ این الگو را دارد»):

<div dir="ltr">

```bash
awk -F'\t' '$6 ~ /Escherichia|Shigella|Enterobacteriaceae/' profile/kraken/minigut_c0.kreport
```

</div>

<div dir="ltr">

```text
 40.63	20253	4909	F	543	              Enterobacteriaceae
 20.16	10051	300	G	561	                Escherichia
 18.02	8981	8981	S	562	                  Escherichia coli
  1.54	770	770	S	564	                  Escherichia fergusonii
 10.48	5225	1312	G	620	                Shigella
  4.50	2241	2241	S	624	                  Shigella sonnei
  3.35	1672	1672	S	623	                  Shigella flexneri
```

</div>

همان عددهای جدول گام ۳، این بار از دید پایگاه. ستون ۲ = جمع ستون ۳ خودش و زیرشاخه‌ها: *Escherichia* ‏10051 = 300 + 8981 + 770.

---

## ۷. گام ۵: فراوانی گونه‌ها با Bracken

<div dir="ltr">

```bash
mkdir -p profile/bracken
bracken -d profile/kraken2_practice_db -i profile/kraken/minigut_c0.kreport \
        -o profile/bracken/minigut_c0.bracken -w profile/bracken/minigut_c0.breport \
        -r 125 -l S -t 10
```

</div>

| بخش | چیست | بی آن چه می‌شود |
| :--- | :--- | :--- |
| ① `-d` | همان پایگاه Kraken2 (مدل Bracken درون آن است) | — |
| ② `-i` | ‏`.kreport` ‏Kraken2 | — |
| ③ `-o` | جدول فراوانی (`.bracken`) | — |
| ④ `-w` | یک `.kreport` تازه با عددهای Bracken | تنها جدول |
| ⑤ `-r 125` | طول رید؛ باید با یکی از مدل‌های ساخته‌شده بخواند (۱۲۵ برای `minigut`، ۱۵۰ برای `minigut_sample2`) | ‏Bracken مدل ۱۰۰ را می‌جوید و چون ساخته نشده، می‌ایستد |
| ⑥ `-l S` | سطح گونه (*Species*)؛ `G` = جنس | ‏`S` پیش‌فرض است |
| ⑦ `-t 10` | گونه‌هایی با کمتر از ۱۰ رید کنار گذاشته شوند | پیش‌فرض ۱۰ |

گزارش Bracken (بخش میانی):

<div dir="ltr">

```text
BRACKEN SUMMARY (Kraken report: profile/kraken/minigut_c0.kreport)
    >>> Threshold: 10 
    >>> Number of species in sample: 10 
	  >> Number of species with reads > threshold: 9 
	  >> Number of species with reads < threshold: 1 
    >>> Total reads in sample: 49845
	  >> Total reads kept at species level (reads > threshold): 40853
	  >> Total reads discarded (species reads < threshold): 3
	  >> Reads distributed: 6572
	  >> Reads not distributed (eg. no species above threshold): 0
	  >> Unclassified reads: 2417
```

</div>

- ‏۴۰٬۸۵۳ رید از پیش در سطح گونه بودند؛ **۶٬۵۷۲ رید** از سطح‌های بالاتر میان گونه‌ها پخش شدند.
- یک گونه کمتر از ۱۰ رید داشت (۳ رید) و کنار رفت.

<div dir="ltr">

```bash
cut -f 1,4,5,6,7 profile/bracken/minigut_c0.bracken
```

</div>

<div dir="ltr">

```text
name	kraken_assigned_reads	added_reads	new_est_reads	fraction_total_reads
Bacteroides fragilis	25605	31	25636	0.54056
Bacteroides thetaiotaomicron	13	0	13	0.00027
Phocaeicola dorei	1503	19	1522	0.03209
Escherichia coli	8981	3940	12921	0.27245
Escherichia fergusonii	770	25	795	0.01676
Shigella sonnei	2241	1601	3842	0.08101
Shigella flexneri	1672	952	2624	0.05533
Klebsiella pneumoniae	38	0	38	0.00080
Salmonella enterica	30	0	30	0.00063
```

</div>

| ستون | معنی |
| :--- | :--- |
| `kraken_assigned_reads` | آنچه Kraken2 مستقیم به گونه داد |
| `added_reads` | آنچه Bracken از سطح‌های بالاتر افزود |
| `new_est_reads` | جمع دو ستون پیش |
| `fraction_total_reads` | سهم از ریدهای **طبقه‌بندی‌شده** (ریدهای `U` شمرده نمی‌شوند) |

‏*E. coli* با Bracken از ۸۹۸۱ به ۱۲٬۹۲۱ رید رسید (۲۷٪)؛ ولی پاسخ درست ۴۲٪ است. و **۹ گونه** گزارش شده، در نمونه‌ای که تنها **۲ گونه** دارد. درس ۲ این خطاها را می‌سنجد و راه کاستنشان را می‌آزماید.

---

## ۸. گام ۶: هر دو نمونه با یک اسکریپت

<div dir="ltr">

```bash
bash $S/run_profile.sh
```

</div>

<div dir="ltr">

```text
== minigut (confidence 0, Bracken -r 125): 47428 sequences classified (95.15%)
== minigut_sample2 (confidence 0, Bracken -r 150): 21364 sequences classified (85.50%)
```

</div>

اسکریپت طول رید هر نمونه را از ۱۰۰۰ رید نخستش برآورد می‌کند و `-r` را خودش برمی‌گزیند. نمونه‌ی ۲ تنها ۸۵٫۵٪ طبقه‌بندی شد؛ درس ۲ می‌گوید ۱۴٫۵٪ دیگر چه هستند.

---

## ۹. سه اشتباه رایج

**۱. گزارش بی نام و نسخه‌ی پایگاه.** همان ریدها با دو نسخه‌ی پایگاه دو پروفایل گوناگون می‌دهند. در Methods بنویسید: نام پایگاه، تاریخ نسخه، و اگر خودتان ساختید، فهرست ژنوم‌ها.

‏**۲. ‏`-r` نادرست در Bracken.** مدل Bracken برای یک طول رید ساخته می‌شود. اگر `-r` با طولی بخواند که مدلش ساخته نشده، Bracken می‌ایستد؛ اگر مدل طول دیگری را به‌کار ببرید، پخش ریدها کمتر درست است. طول ریدهای **پس از بریدن** را بسنجید (ماژول ۰۱).

**۳. شمار گونه‌های Kraken2 را «تنوع» خواندن.** نه گونه در نمونه‌ی دوگونه‌ای! بی پالایش، Kraken2 «هر چه هست» را می‌یابد و «آنچه نیست» را هم. پیش از گزارش تنوع، درس ۲ را بخوانید.

---

## 📘 برای کنجکاوها

- ‏**‏minimizer:** ‏Kraken2 برای کم کردن حافظه، تنها **minimizer** هر k-mer (کوچک‌ترین تکه‌ی ۳۱ بازی آن، به یک ترتیب ویژه) را نگه می‌دارد؛ برای همین پایگاه Standard در ۱۰۰ گیگابایت جا می‌شود.
- ‏**‏`--memory-mapping`:** پایگاه را به‌جای بارگذاری کامل در حافظه، از دیسک می‌خواند؛ برای پایگاه‌های بزرگ روی کامپیوتر کم‌حافظه.
- ‏**‏KrakenTools و Krona:** ‏`kreport2krona.py` گزارش را به نمودار دایره‌ای تعاملی Krona تبدیل می‌کند؛ `extract_kraken_reads.py` ریدهای یک تاکسون را جدا می‌کند.

---

## جمع‌بندی

- ‏Kraken2 هر k-mer رید را با برچسب LCA پایگاه می‌سنجد و رید را به پربارترین مسیر درخت می‌دهد؛ ریدهای مشترک در گره‌های بالا می‌مانند.
- سه خروجی: گزارش صفحه (درصد طبقه‌بندی)، `.kraken` (هر رید)، `.kreport` (هر تاکسون، با عمق درخت).
- ‏Bracken ریدهای سطح‌های بالاتر را میان گونه‌ها پخش می‌کند؛ به طول رید وابسته است.
- حتی با Bracken، روی این پایگاه *E. coli* ۲۷٪ (درست: ۴۲٪) و ۹ گونه (درست: ۲) گزارش شد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
kraken2 --db DB --threads 4 --paired --report s.kreport --output s.kraken R1.fq.gz R2.fq.gz
bracken -d DB -i s.kreport -o s.bracken -w s.breport -r 125 -l S -t 10
awk -F'\t' '$1 == "U"' s.kraken | wc -l                    # unclassified pairs
awk -F'\t' '$6 ~ /Escherichia/' s.kreport                  # rows of a taxon
cut -f 1,6,7 s.bracken                                     # name, reads, fraction
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| پروفایل تاکسونومیک | فهرست تاکسون‌های نمونه با فراوانی هر کدام |
| ‏k-mer | هر تکه‌ی پیوسته‌ی k بازی یک توالی |
| ‏LCA (*lowest common ancestor*) | پایین‌ترین گره‌ی مشترک چند تاکسون در درخت |
| ‏taxid | شناسه‌ی عددی یک تاکسون در NCBI Taxonomy |
| رتبه (*rank*) | سطح در درخت: گونه، جنس، خانواده، … |
| سویه (*strain*) | یک جدایه‌ی مشخص از یک گونه، با ژنوم خودش |
| ‏decoy | گونه‌ی خویشاوندی که در پایگاه هست ولی در نمونه نیست |

---

## منابع

**مستند و مقاله**
- Wood DE, Lu J, Langmead B (2019). *Improved metagenomic analysis with Kraken 2.* Genome Biology 20:257. https://doi.org/10.1186/s13059-019-1891-0
- Lu J, et al. (2017). *Bracken: estimating species abundance in metagenomics data.* PeerJ Computer Science 3:e104. https://doi.org/10.7717/peerj-cs.104
- Lu J, et al. (2022). *Metagenome analysis using the Kraken software suite.* Nature Protocols 17:2815–2839. https://doi.org/10.1038/s41596-022-00738-y
- Pupo GM, et al. (2000). *Multiple independent origins of Shigella clones of Escherichia coli.* PNAS 97(19):10567–10572. https://doi.org/10.1073/pnas.180094797
- Kraken2 manual: https://github.com/DerrickWood/kraken2/wiki/Manual · Pre-built databases: https://benlangmead.github.io/aws-indexes/k2
- Bracken: https://github.com/jenniferlu717/Bracken

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins University). دوره‌ای ویژه‌ی Kraken2 در Coursera نیافتیم؛ نزدیک‌ترین: https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Linux* (The Linux Foundation). دوره‌ای ویژه‌ی پروفایل متاژنوم در edX نیافتیم؛ نزدیک‌ترین: https://www.edx.org/learn/computer-programming/the-linux-foundation-introduction-to-linux
- ‏YouTube: *#13 Bracken with Jennifer Lu* (The Bioinformatics Chat؛ گفت‌وگو با نویسنده‌ی Bracken): https://www.youtube.com/watch?v=xbJ-0wtTzf4
- YouTube: *GTN Tutorial: Taxonomic Profiling and Visualization of Metagenomic Data* (Galaxy Project): https://www.youtube.com/watch?v=jszMnBKm6ig

<sub>نشانی‌های YouTube و DOIها در 2026-10-13 وارسی شدند؛ نشانی Coursera در وارسی پایان دوره سنجیده می‌شود.</sub>

</div>
