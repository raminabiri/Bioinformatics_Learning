<div dir="rtl">

# درس: GEO؛ از یک آزمایش دگزامتازون تا ژن‌هایی که پاسخ می‌دهند

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `04_GEO` · **پیش‌نیاز:** ماژول‌های [11/01](../01_Entrez_EDirect/) و [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) (NR3C1)؛ pandas (ماژول [03/06](../../03_Python/06_Pandas/)) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** curl 8.20.0، Python 3 با pandas 2.3.3، EDirect 24.0؛ GEO2R (✍️ وب)؛ GEOquery 2.80.0 (📘) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده**، جز GEO2R که ابزار وب است (✍️ از مستندات). همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). اسکریپت ۰٫۴ ثانیه و ۱۳۳ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. چهار گونه رکورد GEO (**GSE**، **GSM**، **GPL**، **GDS**) را از هم جدا کنید.
2. فایل **series matrix** را بگیرید و جدول نمونه‌ها را از آن بسازید.
3. **جدول شمارش آماده‌ی NCBI** برای یک آزمایش RNA-seq را بگیرید و با pandas بخوانید.
4. با **CPM** و **log2 fold change** نخستین نگاه را به ژن‌های پاسخ‌دهنده بیندازید و با پاسخ معلوم بسنجید.
5. بگویید **GEO2R** چه می‌کند و چرا جای تحلیل کامل (بخش ۱۳) را نمی‌گیرد.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m04 && cd ~/ncbi/m04
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
P=~/Bioinformatics_Learning-main/11_V2_NCBI_Databases/99_scripts_data
```

</div>

---

## ۱. داستان

در ماژول 11/02 دیدید NR3C1 گیرنده‌ی **دگزامتازون** است: دامنه‌ی LBD دارو را می‌گیرد و دامنه‌ی DBD به DNA می‌چسبد تا ژن‌های هدف را روشن یا خاموش کند. ولی **کدام** ژن‌ها؟ پاسخ در آزمایش‌های بیان ژن است و بزرگ‌ترین بایگانی آن‌ها **GEO** (Gene Expression Omnibus) است. یک آزمایش مشهور: **GSE52778** (Himes و همکاران، ۲۰۱۴). سلول‌های ماهیچه‌ی صاف راه هوایی از چهار فرد را با داروهای آسم (دگزامتازون، آلبوترول یا هر دو) تیمار کردند و RNA-seq گرفتند. این همان داده‌ی بسته‌ی مشهور `airway` در Bioconductor است که در بخش ۱۳ با DESeq2 کامل تحلیلش می‌کنید. این‌جا یاد می‌گیرید داده را از GEO بگیرید و یک نگاه نخست بیندازید.

**پاسخ معلوم:** گلوکوکورتیکوئیدها ژن‌هایی چون **FKBP5**، **TSC22D3** (GILZ)، **PER1**، **DUSP1**، **KLF15** و **ZBTB16** را روشن می‌کنند؛ مقاله‌ی Himes هم **CRISPLD2** را یافت.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ چهار گونه رکورد

| رکورد | چیست | نمونه | ‏UID در Entrez (`db=gds`) |
| :--- | :--- | :--- | :--- |
| ‏**GSE** (Series) | یک آزمایش کامل: همه‌ی نمونه‌ها + شرح | ‏`GSE52778` | ‏`2` + شماره → `200052778` |
| ‏**GSM** (Sample) | یک نمونه | ‏`GSM1275862` | با `3` آغاز می‌شود |
| ‏**GPL** (Platform) | دستگاه یا آرایه | ‏`GPL11154` (HiSeq 2000، انسان) | ‏`1` + شماره → `100011154` |
| ‏**GDS** (DataSet) | زیرمجموعه‌ی ویراسته‌ی GEO از یک GSE، با گروه‌بندی آماده | (برای GSE52778 نیست) | با عدد کوچک |

**تشبیه:** GPL مدل دوربین است، GSM هر عکس، و GSE آلبوم یک سفر. GDS آلبومی است که ویراستار GEO از روی آلبوم شما مرتب کرده است؛ ولی GEO پس از سال‌های نخست دیگر GDS تازه نساخت، پس بیشتر آزمایش‌های RNA-seq آن را ندارند.

### ۲.۲ شمارش، CPM و log2 fold change

در RNA-seq برای هر ژن در هر نمونه **شمار ریدها** (count) را داریم. ولی نمونه‌ها شمار کل رید گوناگون دارند (اندازه‌ی کتابخانه، library size). ‏**CPM** (counts per million) شمار را بر کل ریدهای نمونه بخش می‌کند و در یک میلیون ضرب: «اگر این نمونه درست یک میلیون رید داشت، این ژن چند رید می‌گرفت؟»

‏**log2 fold change** ‏(log2FC) = ‏log2(CPM تیمار) − log2(CPM شاهد). ‏`+1` یعنی دو برابر، `+3` یعنی هشت برابر، `−1` یعنی نصف. چون از log2 صفر نمی‌شود گرفت، یک **pseudocount** (عدد ۱) به CPM می‌افزاییم.

> 📺 **فیلم:** *Lesson 2: Downloading Data from Gene Expression Omnibus (GEO)* (Mike Saint-Antoine): https://www.youtube.com/watch?v=BQTHgwsrv2w
> 📄 **مرجع:** Clough E, et al. (2024). *NCBI GEO: archive for gene expression and epigenomics data sets: 23-year update.* Nucleic Acids Res 52(D1):D138–D144. https://doi.org/10.1093/nar/gkad965

---

## ۳. گام ۱: GSE52778 در Entrez

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=gds --data-urlencode "term=GSE52778[ACCN]" --data-urlencode retmax=20 \
  | grep -o '<Id>[^<]*' | cut -d'>' -f2 | cut -c1 | sort | uniq -c
curl -sS "$B/esummary.fcgi?db=gds&id=200052778&version=2.0" > gse_sum.xml
grep -oE '<(Accession|title|GPL|taxon|gdsType|PDAT)>[^<]*' gse_sum.xml | head -7
grep -oE '<int>[^<]*' gse_sum.xml
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`db=gds` | پایگاه «GEO DataSets» در Entrez: هر چهار گونه رکورد GEO در آن است |
| ‏`[ACCN]` | فیلد accession |
| ‏`cut -c1` | نخستین رقم UID = گونه‌ی رکورد |
| ‏`<int>` | در خلاصه‌ی GSE، شناسه‌های PubMed مقاله‌ها |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
      1 1
      1 2
     16 3
<Accession>GSE52778
<title>Human Airway Smooth Muscle Transcriptome Changes in Response to Asthma Medications
<GPL>11154
<taxon>Homo sapiens
<gdsType>Expression profiling by high throughput sequencing
<PDAT>2014/01/01
<Accession>GSM1275876
<int>24926665
<int>36599824
```

</div>

**توضیح خروجی:**
- ‏۱۸ رکورد زیر این accession: **۱** GPL (رقم ۱)، **۱** GSE (رقم ۲) و **۱۶** GSM (رقم ۳). ‏`<Accession>` دوم نخستین GSM فهرست درون خلاصه است.
- ‏`gdsType`: «Expression profiling by **high throughput sequencing**» = RNA-seq (برای ریزآرایه «by array»).
- دو مقاله در PubMed: مقاله‌ی اصلی (۲۰۱۴) و یک مقاله‌ی بعدی (۲۰۲۳) که همین داده را دوباره به کار برده است.

---

## ۴. گام ۲: series matrix و جدول نمونه‌ها

**چرا؟** پیش از هر عدد باید بدانیم هر GSM چیست: کدام فرد (cell line)، کدام تیمار.

<div dir="ltr">

```bash
curl -sS -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSE52nnn/GSE52778/matrix/GSE52778_series_matrix.txt.gz
ls -la GSE52778_series_matrix.txt.gz
zcat GSE52778_series_matrix.txt.gz | wc -l
zcat GSE52778_series_matrix.txt.gz | grep -E '^!Sample_(title|characteristics_ch1)' | cut -c1-110
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`GSE52nnn/GSE52778/matrix/` | ساختار پوشه‌های FTP در GEO: سه رقم پایانی با `nnn` |
| ‏`^!Sample_` | سطرهای فراداده‌ی نمونه‌ها؛ هر سطر یک ویژگی برای **همه‌ی** ۱۶ نمونه، جدا با Tab |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
-rw-rw-r-- 1 ubuntu ubuntu 3396 Oct 27 14:40 GSE52778_series_matrix.txt.gz
77
!Sample_title	"N61311_untreated"	"N61311_Dex"	"N61311_Alb"	"N61311_Alb_Dex"	"N052611_untreated"	"N0
!Sample_characteristics_ch1	"treatment: Untreated"	"treatment: Dexamethasone"	"treatment: Albuterol"	"trea
!Sample_characteristics_ch1	"tissue: human airway smooth muscle cells"	"tissue: human airway smooth musc
!Sample_characteristics_ch1	"ercc_mix: -"	"ercc_mix: -"	"ercc_mix: -"	"ercc_mix: -"	"ercc_mix: -"	"ercc_
!Sample_characteristics_ch1	"cell line: N61311"	"cell line: N61311"	"cell line: N61311"	"cell line: N61311"	"
!Sample_characteristics_ch1	"cell type: airway smooth muscle cells"	"cell type: airway smooth muscle cells"
```

</div>

**توضیح خروجی:**
- فایل تنها **۳ کیلوبایت** و **۷۷ سطر** است. برای ریزآرایه، series matrix جدول بیان را هم دارد؛ برای **RNA-seq نه**: تنها فراداده. شمارش‌ها جای دیگری‌اند (گام ۳). این بزرگ‌ترین شگفتی کاربران تازه‌کار GEO است.
- ‏`characteristics_ch1` چند سطر دارد، هر کدام یک ویژگی («treatment: …»، «cell line: …»). ‏`ch1` = کانال ۱ (یادگار ریزآرایه‌های دورنگ).
- طرح: **۴ فرد × ۴ تیمار** = ۱۶ نمونه.

اسکریپت [geo_counts.py](../99_scripts_data/04_GEO/scripts/geo_counts.py) همین سطرها را به یک جدول pandas برمی‌گرداند:

<div dir="ltr">

```python
        if key == "!Sample_geo_accession":
            rows["gsm"] = values
        elif key == "!Sample_characteristics_ch1":
            name = values[0].split(":")[0]             # e.g. "treatment"
            rows[name] = [v.split(": ", 1)[1] for v in values]
samples = pd.DataFrame(rows).set_index("gsm")[["cell line", "treatment"]]
```

</div>

‏`split(": ", 1)[1]` بخش پس از نخستین «: » را برمی‌دارد (`"treatment: Dexamethasone"` → `"Dexamethasone"`)؛ نام ویژگی از نخستین نمونه برداشته می‌شود.

---

## ۵. گام ۳: جدول شمارش آماده‌ی NCBI

**چرا؟** در سال‌های اخیر NCBI برای بسیاری از آزمایش‌های RNA-seq انسان و موش، ریدها را **خودش** با یک گردش کار یکسان روی ژنوم GRCh38 شمرده و جدول را در کنار GSE گذاشته است. پس برای نگاه نخست لازم نیست ۱۶ نمونه‌ی FASTQ را (۱۱/03) بگیرید و هم‌ردیف کنید.

<div dir="ltr">

```bash
curl -sS -L -o counts.tsv.gz \
  "https://www.ncbi.nlm.nih.gov/geo/download/?type=rnaseq_counts&acc=GSE52778&format=file&file=GSE52778_raw_counts_GRCh38.p13_NCBI.tsv.gz"
ls -la counts.tsv.gz
zcat counts.tsv.gz | head -3 | cut -c1-120
zcat counts.tsv.gz | wc -l
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
-rw-rw-r-- 1 ubuntu ubuntu 740924 Oct 27 14:40 counts.tsv.gz
GeneID	GSM1275862	GSM1275863	GSM1275864	GSM1275865	GSM1275866	GSM1275867	GSM1275868	GSM1275869	GSM12758
100287102	6	8	8	3	5	10	11	7	6	8	4	10	2	1	2	2
653635	357	292	351	285	469	428	523	442	367	415	404	354	371	381	367	341
39377
```

</div>

**توضیح خروجی:**
- ‏۷۴۰ کیلوبایت؛ ‏**۳۹٬۳۷۶** ژن (سطر نخست سرستون است) × ۱۶ نمونه.
- سطرها با **NCBI Gene ID** (11/01) نام دارند، نه نام ژن؛ ستون‌ها با GSM. ‏NR3C1 همان `2908` است.
- ‏`raw_counts`: شمار خام، **نه** نرمال‌شده؛ برای DESeq2 (بخش ۱۳) درست همین لازم است.

> 📺 **فیلم:** *Lesson 2: Downloading Data from Gene Expression Omnibus (GEO)*: https://www.youtube.com/watch?v=BQTHgwsrv2w
> 📄 **مرجع:** راهنمای «RNA-seq counts» در GEO (چگونه شمرده شده‌اند): https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html

---

## ۶. گام ۴: نخستین نگاه؛ دگزامتازون در برابر بی‌تیمار

**چرا؟** پیش از تحلیل آماری، باید ببینیم پاسخ معلوم در داده هست یا نه. اگر FKBP5 بالا نرفته باشد، یا نمونه‌ها جابه‌جا نام‌گذاری شده‌اند یا ما چیزی را بد خوانده‌ایم.

بخش اصلی اسکریپت:

<div dir="ltr">

```python
cpm = counts / lib * 1e6
t = samples[samples.treatment == treated].reset_index().set_index("cell line")["gsm"]
c = samples[samples.treatment == control].reset_index().set_index("cell line")["gsm"]
lfc = pd.DataFrame({line: np.log2(cpm[t[line]] + 1) - np.log2(cpm[c[line]] + 1) for line in t.index})
```

</div>

| بخش | کار |
| :--- | :--- |
| ‏`counts / lib * 1e6` | ‏CPM: هر ستون بر جمع همان ستون |
| ‏`t` و `c` | برای هر cell line، GSM تیمار و GSM شاهد |
| ‏`lfc` | ‏log2FC **جفتی**: هر فرد با شاهد **خودش** سنجیده می‌شود، نه با میانگین همه |
| ‏`lines_up` (در اسکریپت) | در چند فرد از ۴ فرد ژن بالا رفته است |

<div dir="ltr">

```bash
/usr/bin/time -f "time=%es maxRSS=%MKB" python3 $P/04_GEO/scripts/geo_counts.py \
    GSE52778_series_matrix.txt.gz counts.tsv.gz Dexamethasone Untreated \
    2908 2289 1831 1843 5187 83716 7704 28999
```

</div>

**خروجی واقعی (2026-10-27؛ جدول نمونه‌ها و اندازه‌ی کتابخانه‌ها کوتاه شده):**

<div dir="ltr">

```
           cell line                treatment
gsm
GSM1275862    N61311                Untreated
GSM1275863    N61311            Dexamethasone
GSM1275864    N61311                Albuterol
GSM1275865    N61311  Albuterol_Dexamethasone
GSM1275866   N052611                Untreated
…
library size (million reads):
GSM1275862    21.0
GSM1275863    19.2
…
GSM1275867    39.1
…
selected genes (Dexamethasone vs Untreated):
        mean_cpm_Untreated  mean_cpm_Dexamethasone  mean_log2FC  lines_up
GeneID
2908                 179.3                    84.2        -1.06         0
2289                  15.1                   217.3         3.84         4
1831                  18.4                   178.4         3.04         4
1843                  36.9                   270.9         2.84         4
5187                   7.3                    63.8         2.97         4
83716                 39.0                   239.3         2.51         4
7704                   0.8                   104.8         5.88         4
28999                  2.3                    48.8         3.77         4

top 10 up among 11520 genes with control CPM >= 5:
        mean_cpm_Untreated  mean_cpm_Dexamethasone  mean_log2FC  lines_up
GeneID
2289                  15.1                   217.3         3.84         4
25939                 82.7                  1132.6         3.67         4
2878                  80.1                  1018.7         3.63         4
4128                  20.6                   190.6         3.19         4
12                    23.1                   218.7         3.08         4
1831                  18.4                   178.4         3.04         4
730                   18.0                   159.8         3.04         4
5187                   7.3                    63.8         2.97         4
783                    5.4                    46.0         2.84         4
1843                  36.9                   270.9         2.84         4
time=0.38s maxRSS=132548KB
```

</div>

نام ژن‌ها را با EDirect (11/01) بیابیم:

<div dir="ltr">

```bash
esummary -db gene -id 2289,25939,2878,4128,12,1831,730,5187,783,1843,2908,83716,7704,28999 \
  | xtract -pattern DocumentSummary -element Id Name Description | cut -c1-80
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
12	SERPINA3	serpin family A member 3
730	C7	complement C7
783	CACNB2	calcium voltage-gated channel auxiliary subunit beta 2
1831	TSC22D3	TSC22 domain family member 3
1843	DUSP1	dual specificity phosphatase 1
2289	FKBP5	FKBP prolyl isomerase 5
2878	GPX3	glutathione peroxidase 3
2908	NR3C1	nuclear receptor subfamily 3 group C member 1
4128	MAOA	monoamine oxidase A
5187	PER1	period circadian regulator 1
7704	ZBTB16	zinc finger and BTB domain containing 16
25939	SAMHD1	SAM and HD domain containing deoxynucleoside triphosphate triphosph
28999	KLF15	KLF transcription factor 15
83716	CRISPLD2	cysteine rich secretory protein LCCL domain containing 2
```

</div>

**توضیح خروجی:**
- **پاسخ معلوم برقرار است.** ‏FKBP5 ‏(×۱۴، log2FC ‏۳٫۸۴)، TSC22D3، DUSP1، PER1، KLF15، ZBTB16 (از نزدیک صفر به ۱۰۵ CPM) و CRISPLD2، **همه در هر ۴ فرد** بالا رفته‌اند.
- ‏**NR3C1 پایین آمده** (log2FC ‏−۱٫۰۶، در هیچ فردی بالا نرفته): گیرنده پس از فعال شدن، بیان **خودش** را کم می‌کند؛ یک **بازخورد منفی** شناخته‌شده.
- ده ژن بالایی، بیشترشان ژن‌های شناخته‌شده‌ی پاسخ به گلوکوکورتیکوئیدند (FKBP5، TSC22D3، PER1، DUSP1، SERPINA3، GPX3، MAOA). ‏FKBP5 در صدر است؛ همان ژنی که در پژوهش‌ها «نشانگر» فعال بودن گیرنده‌ی گلوکوکورتیکوئید است.
- اندازه‌ی کتابخانه‌ها از ۱۹٫۲ تا ۳۹٫۱ میلیون است، دو برابر فرق. بی CPM، `GSM1275867` (۳۹ میلیون) همه‌ی ژن‌هایش را «بالاتر» نشان می‌داد.
- **این آمار نیست.** هیچ p-value، هیچ تصحیح آزمون چندگانه، و ژن‌های کم‌بیان با pseudocount بزرگ‌نمایی می‌شوند (به همین علت `CPM >= 5` گذاشتیم). برای نتیجه‌ی قابل گزارش، بخش ۱۳ (DESeq2) لازم است.

<details>
<summary>✋ امتحان کن: چرا log2FC «جفتی» (هر فرد با خودش) بهتر از میانگین همه‌ی تیمارها در برابر میانگین همه‌ی شاهدهاست؟</summary>

چون چهار فرد از پایه با هم فرق دارند (ژنتیک، سن). اگر میانگین بگیرید، فرق میان افراد با اثر دارو قاطی می‌شود. در طرح جفتی هر فرد شاهد خودش است و تنها اثر دارو می‌ماند. ‏DESeq2 همین را با گذاشتن «cell line» در طرح (`~ cell + dex`) انجام می‌دهد (بخش ۱۳).

</details>

---

## ۷. گام ۵: GEO2R ✍️ (از مستندات)

‏**GEO2R** یک ابزار وب در صفحه‌ی هر GSE است: گروه‌ها را با کلیک می‌سازید و GEO روی همان جدول شمارش NCBI، **DESeq2** (برای RNA-seq) یا **limma** (برای ریزآرایه) را اجرا می‌کند. گام‌ها (از راهنمای GEO2R):

1. ‏https://www.ncbi.nlm.nih.gov/geo/geo2r/?acc=GSE52778 را باز کنید.
2. ‏«Define groups»: دو گروه بسازید (`dex`، `untreated`) و نمونه‌ها را با نگاه به ستون «treatment» به گروه‌ها بدهید.
3. ‏«Analyze»: جدول ژن‌ها با `log2FoldChange`، `pvalue` و `padj`، به‌اضافه‌ی نمودار volcano.

**چرا جای تحلیل کامل را نمی‌گیرد؟**
- طرح، سنجش **گروه‌ها**ست که با کلیک ساخته می‌شوند؛ نمی‌توانید مانند DESeq2 در بخش ۱۳ فرمول طرح (مانند `~ cell + dex`) بنویسید، پس طرح جفتی گام ۴ به‌آسانی در دسترس نیست.
- تنها جدول شمارش NCBI را می‌پذیرد؛ کنترل کیفیت، کنار گذاشتن نمونه‌ی بد و انتخاب پارامترها در دست شما نیست.
- برای یک نگاه سریع یا پیدا کردن یک ژن در یک آزمایش، عالی است؛ برای مقاله نه.

> 📺 **فیلم:** *Use GEO2R to Analyze Data in GEO, the Gene Expression Omnibus* (National Library of Medicine): https://www.youtube.com/watch?v=9RyWjzSnaE0
> 📄 **مرجع:** راهنمای GEO2R: https://www.ncbi.nlm.nih.gov/geo/info/geo2r.html · Himes BE, et al. (2014). *RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells.* PLoS ONE 9:e99625. https://doi.org/10.1371/journal.pone.0099625

---

## ۸. سه اشتباه رایج

1. **جستن جدول بیان در series matrix یک آزمایش RNA-seq.** تنها فراداده است (۷۷ سطر). شمارش‌ها در «NCBI-generated RNA-seq counts» یا در فایل‌های پیوست (supplementary) ثبت‌کننده‌اند.
2. **سنجیدن شمار خام نمونه‌ها با هم.** اندازه‌ی کتابخانه‌ها تا دو برابر فرق دارد؛ دست‌کم CPM، و برای آمار، نرمال‌سازی DESeq2.
3. **اعتماد به برچسب‌ها بی وارسی.** پیش از هر تحلیل، یک پاسخ معلوم (این‌جا FKBP5) را بسنجید. اگر نمونه‌ها جابه‌جا نام‌گذاری شده باشند، همین‌جا پیداست.

---

## 📘 برای کنجکاوها

- ‏**GEOquery** (بسته‌ی R) همان series matrix را می‌خواند. اجرای واقعی (2026-10-27، GEOquery 2.80.0):

  <div dir="ltr">

  ```r
  library(GEOquery)
  g <- getGEO("GSE52778", GSEMatrix = TRUE, destdir = ".")[[1]]
  dim(g)
  table(pData(g)[["treatment:ch1"]])
  ```

  </div>

  <div dir="ltr">

  ```
  Features  Samples
         0       16
  Albuterol Albuterol_Dexamethasone  Dexamethasone  Untreated
          4                       4              4          4
  ```

  </div>

  ‏`Features 0`: همان یافته‌ی گام ۲؛ جدول بیان تهی است.
- ‏**ERCC:** ویژگی «ercc_mix» می‌گوید به کدام نمونه‌ها RNA مصنوعی شناخته‌شده (spike-in) افزوده شد تا دقت شمارش سنجیده شود.
- **دو کانال:** در ریزآرایه‌های دورنگ هر نمونه دو برچسب (Cy3، Cy5) داشت؛ `ch1` و `ch2` از آن دوران مانده‌اند.

---

## جمع‌بندی

- ‏GEO: ‏GSE (آزمایش)، GSM (نمونه)، GPL (دستگاه)، GDS (ویراسته؛ برای RNA-seq کم‌یاب). در Entrez رقم نخست UID گونه را می‌گوید.
- ‏series matrix برای RNA-seq تنها فراداده است؛ GSE52778 = ‏۴ فرد × ۴ تیمار.
- جدول شمارش NCBI: ‏۳۹٬۳۷۶ ژن × ۱۶ نمونه، با Gene ID.
- نگاه نخست (CPM، log2FC جفتی): FKBP5، TSC22D3، DUSP1، PER1، KLF15، ZBTB16 و CRISPLD2 در هر ۴ فرد بالا؛ NR3C1 پایین (بازخورد منفی).
- ‏GEO2R برای نگاه سریع؛ تحلیل آماری کامل در بخش ۱۳.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
curl … esearch db=gds term=GSExxx[ACCN]                    # UID: 1=GPL 2=GSE 3=GSM
curl -O https://ftp.ncbi.nlm.nih.gov/geo/series/GSEnnn/GSExxx/matrix/GSExxx_series_matrix.txt.gz
zcat GSExxx_series_matrix.txt.gz | grep '^!Sample_characteristics_ch1'
curl -L -o counts.tsv.gz "https://www.ncbi.nlm.nih.gov/geo/download/?type=rnaseq_counts&acc=GSExxx&format=file&file=GSExxx_raw_counts_GRCh38.p13_NCBI.tsv.gz"
python3 geo_counts.py MATRIX COUNTS TREATED CONTROL [GENEID ...]
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏GEO | بایگانی داده‌های بیان ژن و اپی‌ژنومیک در NCBI |
| ‏GSE / GSM / GPL / GDS | آزمایش / نمونه / دستگاه / مجموعه‌ی ویراسته |
| ‏series matrix | فایل جدولی یک GSE با فراداده‌ی نمونه‌ها (و بیان، برای ریزآرایه) |
| شمار خام (raw count) | شمار ریدهای هر ژن، پیش از هر نرمال‌سازی |
| اندازه‌ی کتابخانه (library size) | شمار کل ریدهای یک نمونه |
| ‏CPM | شمار در هر میلیون رید |
| ‏log2 fold change | ‏log2 نسبت بیان تیمار به شاهد |
| ‏pseudocount | عدد کوچکی که پیش از log افزوده می‌شود تا صفر نماند |
| طرح جفتی (paired design) | سنجیدن هر فرد با شاهد خودش |
| بازخورد منفی | کم شدن یک فرایند به دست فراورده‌ی خودش |
| ‏spike-in (ERCC) | ‏RNA مصنوعی با غلظت معلوم برای سنجش دقت |

---

## منابع

**مقاله و مستند**
- ‏Himes BE, et al. (2014). *RNA-Seq transcriptome profiling identifies CRISPLD2 as a glucocorticoid responsive gene that modulates cytokine function in airway smooth muscle cells.* PLoS ONE 9(6):e99625. https://doi.org/10.1371/journal.pone.0099625
- ‏Clough E, et al. (2024). *NCBI GEO: archive for gene expression and epigenomics data sets: 23-year update.* Nucleic Acids Res 52(D1):D138–D144. https://doi.org/10.1093/nar/gkad965
- ‏Barrett T, et al. (2013). *NCBI GEO: archive for functional genomics data sets—update.* Nucleic Acids Res 41(D1):D991–D995. https://doi.org/10.1093/nar/gks1193
- ‏Davis S, Meltzer PS (2007). *GEOquery: a bridge between the Gene Expression Omnibus (GEO) and BioConductor.* Bioinformatics 23:1846–1847. https://doi.org/10.1093/bioinformatics/btm254
- راهنمای GEO2R: https://www.ncbi.nlm.nih.gov/geo/info/geo2r.html · شمارش‌های RNA-seq در GEO: https://www.ncbi.nlm.nih.gov/geo/info/rnaseqcounts.html

**کتاب**
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۱۱: بیان ژن و ریزآرایه؛ GEO)
- ‏Love MI, Anders S, Huber W. *Analyzing RNA-seq data with DESeq2* (راهنمای آنلاین Bioconductor؛ داده‌ی airway): https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Bioconductor for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/bioconductor
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *Use GEO2R to Analyze Data in GEO, the Gene Expression Omnibus* (National Library of Medicine): https://www.youtube.com/watch?v=9RyWjzSnaE0
- ‏YouTube: *Lesson 2: Downloading Data from Gene Expression Omnibus (GEO)* (Mike Saint-Antoine): https://www.youtube.com/watch?v=BQTHgwsrv2w

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند؛ GEO2R ابزار وب است و از راهنمای آن نوشته شد (✍️؛ صفحه‌ی راهنما از سرور پشت reCAPTCHA بود، پس جزئیات آن در وارسی پایانی با مرورگر سنجیده شود). Coursera از سرور در دسترس نیست (451). DOIها با doi.org، و صفحه‌های GEO با درخواست مستقیم وارسی شدند؛ فیلم‌ها با noembed.</sub>

</div>
