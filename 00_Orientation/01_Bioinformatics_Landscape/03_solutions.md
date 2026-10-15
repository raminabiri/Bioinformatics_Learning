# پاسخ تشریحی: نقشه‌ی بیوانفورماتیک و کاربردها

---

## تمرین ۱

| # | زیرشاخه | داده‌ی ورودی | اولین ایست بازرسی QC | دیتابیس مرجع | بخش |
| :-: | :--- | :--- | :--- | :--- | :-: |
| 1 | ژنومیکس میکروبی + اپیدمیولوژی ژنومیک + مقاومت | ریدهای Illumina (و ترجیحاً Nanopore) هر ایزوله | کیفیت ریدها؛ سپس کیفیت اسمبلی و **آلودگی** (CheckM) | ژنوم مرجع *K. pneumoniae*، PubMLST، CARD/AMRFinderPlus | 04، 05 |
| 2 | متاژنومیکس Shotgun (عملکردی) | ریدهای DNA کل جامعه | کیفیت ریدها + **درصد ریدهای انسانی** + عمق کافی برای پروفایل عملکردی | UniRef/ChocoPhlAn (HUMAnN)، MetaCyc یا KEGG | 03 |
| 3 | بیوانفورماتیک ساختاری | توالی پروتئین؛ ساختار تجربی یا مدل | کیفیت ساختار: resolution/R-free برای ساختار تجربی، pLDDT برای مدل AlphaFold | PDB، AlphaFold DB، UniProt (آنوتیشن جایگاه فعال)، ChEMBL/PubChem | 06 |
| 4 | آمپلیکون 16S | ریدهای ناحیه‌ی V3–V4 (یا V4) | کیفیت ریدها و **میزان ادغام جفت‌ریدها**؛ کنترل منفی | SILVA یا Greengenes2 | 03 |
| 5 | ژنومیکس انسانی/بالینی | WES (BAM/VCF) | پوشش ژن‌های هدف؛ کیفیت فراخوانی واریانت | ClinVar، gnomAD، OMIM | 07 |

**نکته‌های تشریحی:**
- **سناریوی ۱:** سؤال «آیا انتقال رخ داده؟» یعنی فاصله‌ی ژنتیکی سویه‌ها (SNP distance و فیلوژنی) مهم است، نه فقط حضور ژن مقاومت. کارباپنمازها اغلب روی پلاسمیدند؛ پس ممکن است **پلاسمید** بین سویه‌های نامرتبط منتقل شده باشد. به همین دلیل توالی‌یابی long-read برای بستن پلاسمیدها ارزشمند است (بخش ۰۷).
- **سناریوی ۲ در برابر ۴:** این مقایسه‌ی کلیدی است. 16S فقط ترکیب تاکسونومیک می‌دهد (معمولاً تا سطح جنس) و توان عملکردی را **مستقیم اندازه نمی‌گیرد**. ابزارهای پیش‌بینی عملکرد از 16S (مثل PICRUSt2) استنباط می‌کنند، نه اندازه‌گیری. برای سؤال عملکردی، Shotgun لازم است.
- **سناریوی ۳:** اگر ساختار تجربی وجود ندارد، مدل AlphaFold مفید است، ولی pLDDT پایین در ناحیه‌ی مورد نظر یعنی آن ناحیه قابل اعتماد نیست. داکینگ روی ناحیه‌ی با اطمینان کم نتیجه‌ی بی‌معنی می‌دهد.
- **سناریوی ۵:** فراوانی واریانت در جمعیت (gnomAD) معمولاً اولین فیلتر است؛ واریانتی که در جمعیت سالم فراوان است، به احتمال زیاد عامل بیماری نادر نیست.

---

## تمرین ۲

### ۲.۱ موارد غایب (حداقل ۸ مورد)
1. **کیت و روش استخراج DNA.** در متاژنومیکس کیت استخراج روی ترکیب تأثیر جدی دارد، مثلاً در لیز باکتری‌های گرم‌مثبت.
2. **کیت آماده‌سازی کتابخانه** و اندازه‌ی insert.
3. **مدل دستگاه** (مثلاً NovaSeq 6000) و **طول و نوع خوانش** (2×150 PE).
4. **عمق توالی‌یابی** (تعداد رید در هر نمونه، دست‌کم میانگین و بازه).
5. **نسخه‌ی Trimmomatic** و **پارامترهای واقعی**. «پیش‌فرض» در Trimmomatic عملاً معنی ندارد، چون مراحل trimming باید صریحاً تعیین شوند.
6. **ابزار و ژنوم مرجع حذف میزبان** (مثلاً Bowtie2 در برابر GRCh38/T2T-CHM13، با نسخه).
7. **نسخه‌ی Kraken2 و نسخه/تاریخ دیتابیس.** دیتابیس «standard» مرتب بازسازی می‌شود.
8. **ابزار تخمین فراوانی** (مثلاً Bracken) و آستانه‌ی confidence در Kraken2.
9. **نرمال‌سازی** قبل از آزمون (فراوانی نسبی؟ تبدیل CLR؟ rarefaction؟).
10. **اصلاح برای آزمون‌های چندگانه** (FDR).
11. **شناسه‌ی آرشیو داده** و **لینک کد**.
12. **کنترل‌های منفی** (blank استخراج و کتابخانه) و نحوه‌ی برخورد با آلودگی.

### ۲.۲ تضاد با FAIR
جمله‌ی *"available from the corresponding author upon reasonable request"* داده را نه **Findable** می‌کند (شناسه‌ی پایدار ندارد) و نه **Accessible** (دسترسی به پاسخ نویسنده وابسته است). مطالعات نشان داده‌اند بخش بزرگی از این درخواست‌ها بی‌پاسخ می‌ماند. راه درست ثبت در ENA/SRA و ذکر `PRJ…` است. برای داده‌ی انسانی حساس، آرشیو با دسترسی کنترل‌شده (مثل EGA) استفاده می‌شود؛ حتی در آن صورت هم داده شناسه‌ی پایدار دارد.

### ۲.۳ مشکل آماری
**عدم اصلاح برای آزمون‌های چندگانه.** با صدها taxon، آزمون Wilcoxon جداگانه با آستانه‌ی p < 0.05 به‌طور میانگین ۵٪ از taxonهای بی‌تفاوت را به‌اشتباه معنادار نشان می‌دهد. با ۳۰۰ taxon، این یعنی حدود ۱۵ کشف کاذب. باید FDR (مثلاً Benjamini–Hochberg) گزارش شود.

دو مشکل دیگر هم قابل قبول است:
- داده‌ی میکروبیوم **ترکیبی (compositional)** است. آزمون مستقیم روی فراوانی نسبی می‌تواند تغییر کاذب نشان دهد، چون افزایش یک taxon خودبه‌خود سهم بقیه را کم می‌کند. روش‌هایی مثل ANCOM-BC، ALDEx2 یا MaAsLin2 این را در نظر می‌گیرند.
- طراحی «قبل/بعد» **زوجی** است. Wilcoxon rank-sum (مستقل) برای آن نادرست است و باید Wilcoxon signed-rank یا مدل اثرات تصادفی به کار رود.

### ۲.۴ نمونه‌ی بازنویسی‌شده
> *"DNA was extracted from 0.2 g stool using the <kit, version> with bead-beating (<instrument, settings>). Libraries were prepared with <kit> (insert size ~<n> bp) and sequenced on an Illumina <model> (2×150 bp), yielding <mean ± SD> million read pairs per sample. Extraction and library blanks were sequenced alongside samples. Reads were trimmed with fastp v0.23.4 (`--detect_adapter_for_pe --cut_tail --cut_mean_quality 20 -l 50`). Host reads were removed by mapping to GRCh38 (<release>) with Bowtie2 v2.5.4 (`--very-sensitive`). Taxonomic profiles were generated with Kraken2 v<…> (`--confidence 0.1`) against the <database name, build date> database, and abundances were re-estimated with Bracken v<…> at genus level. Differential abundance between time points was tested with MaAsLin2 v<…> (CLR transform; subject as random effect), with Benjamini–Hochberg FDR < 0.1. Raw reads are deposited in ENA under PRJEB<…>; all code is available at <repository URL> (commit <hash>)."*

---

## تمرین ۳

### ۳.۱ تعداد Run و Sample و دستگاه
بررسی‌شده در 2026-10-12 با ENA Portal API (همین اعداد در مرورگر ENA هم دیده می‌شود):

```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB7774&result=read_run&fields=run_accession,sample_accession,instrument_model,library_layout&format=tsv" \
  | tail -n +2 | awk -F'\t' '{r++; s[$2]=1; i[$3]++; l[$4]++} END{print r" runs, "length(s)" samples"; for(k in i) print k": "i[k]; for(k in l) print k": "l[k]}'
```
```text
312 runs, 156 samples
Illumina HiSeq 2000: 312
PAIRED: 156
SINGLE: 156
```
(ترتیب سطرها ممکن است در اجرای شما فرق کند.)
پس **۱۵۶ نمونه، ۳۱۲ Run، همه با Illumina HiSeq 2000**.

### ۳.۲ فیلدهای نشان‌دهنده‌ی Interoperability
در BioSample نمونه‌ی `SAMEA3136648` این فیلدها دیده می‌شوند:
- `ENA-CHECKLIST: ERC000015`، یعنی metadata طبق یک **چک‌لیست استاندارد ENA** (از خانواده‌ی MIxS، برای human-gut) پر شده است.
- `environment (biome): human gut`، `environment (feature): human-associated habitat`، `environment (material): faeces`. این‌ها سه فیلد استاندارد محیطی MIxS هستند که مقدارشان باید از هستی‌شناسی ENVO باشد.
- `investigation type: metagenome` و `organism: human gut metagenome`. این دومی یک taxon استاندارد در NCBI Taxonomy برای داده‌ی متاژنومی است.
- `geographic location (country and/or sea): Austria` همراه با latitude/longitude در قالب استاندارد.

### ۳.۳ دو Run برای یک نمونه
```bash
curl -s "https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJEB7774&result=read_run&fields=run_accession,sample_accession,library_layout,read_count&format=tsv" | grep SAMEA3136648
```
```text
ERR688506	SAMEA3136648	PAIRED	32474886
ERR688359	SAMEA3136648	SINGLE	1158189
```
یکی از Runها **single-end با حدود ۱٫۲ میلیون رید** است و دیگری **paired-end با حدود ۳۲٫۵ میلیون جفت‌رید**. برای تحلیل اصلی Run پیرد-اند (`ERR688506`) را برمی‌داریم، چون حدود ۲۸ برابر داده‌ی بیشتر دارد و paired-end است.

درس کلی‌تر: **واحد تحلیل «Sample» است، نه «Run».** همیشه قبل از دانلود جدول Run↔Sample را ببینید. اگر چند Run از یک کتابخانه هستند (مثلاً چند lane)، باید با هم ادغام شوند. اگر از نوع متفاوت‌اند (مثل اینجا)، باید آگاهانه یکی را انتخاب کنید. اشتباه رایج این است که هر Run را یک نمونه‌ی مستقل حساب کنیم؛ این کار تعداد نمونه را مصنوعی دو برابر می‌کند و آمار را کاذب می‌کند.

### ۳.۴ کمبود برای Reusability
متغیرهای بالینی و مخدوش‌کننده‌ها در BioSample نیستند: **گروه تشخیصی** (سالم، آدنوما، کارسینوما)، **سن، جنس، BMI**، **مصرف آنتی‌بیوتیک یا دارو** (مثل متفورمین که اثر شناخته‌شده‌ای روی میکروبیوم دارد) و رژیم غذایی. این اطلاعات معمولاً در جدول تکمیلی مقاله می‌آید. برای استفاده‌ی مجدد باید آن جدول را با شناسه‌ی نمونه‌ها **تطبیق** دهید، که خودش منبع خطاست. ثبت متغیرهای کلیدی در خود BioSample (تا حد مجاز اخلاقی) داده را Reusableتر می‌کند.

---

## تمرین ۴
پاسخ واحد ندارد. یک طرح خوب این ویژگی‌ها را دارد:
- **فرضیه‌ی قابل‌رد** («فیبر فراوانی ژن‌های butyryl-CoA:acetate CoA-transferase را افزایش می‌دهد»)، نه فقط «بررسی میکروبیوم».
- **کنترل‌های منفی** (blank استخراج) و ترجیحاً یک **mock community** به‌عنوان کنترل مثبت.
- **معیار عددی** برای هر ایست بازرسی، مثلاً «نمونه‌های با کمتر از ۵ میلیون جفت‌رید پس از حذف میزبان کنار گذاشته می‌شوند».
- **مخدوش‌کننده‌ها** از قبل فهرست شده و در مدل آماری لحاظ شده‌اند.
- **نسخه‌ی ابزارها** در فایل محیط و **داده** در ENA با چک‌لیست مناسب.
