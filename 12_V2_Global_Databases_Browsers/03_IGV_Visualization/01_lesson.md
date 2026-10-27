<div dir="rtl">

# درس: دیدن ریدها و واریانت‌ها با IGV؛ SNP واقعی یا خطای توالی‌یابی؟

**بخش:** `12_V2_Global_Databases_Browsers` · **ماژول:** `03_IGV_Visualization` · **پیش‌نیاز:** BAM، VCF، `samtools` و `bcftools` ([02/04](../../02_BioLinux/04_Align_Variant_Formats/))؛ GFF ([02/03](../../02_BioLinux/03_Annotation_Formats/))؛ مرورگر ژنوم و ترک‌ها ([12/02](../02_UCSC_Genome_Browser/)) · **زمان:** حدود ۸۰ دقیقه · **ابزار:** ‏IGV رومیزی 2.19.8 (روی لپ‌تاپ شما، ✍️)، samtools 1.24 و bcftools 1.24 و igv-reports 1.16.0 (محیط `databases`) · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده**، جز IGV رومیزی که برنامه‌ی گرافیکی است و روی سرور دوره (بی نمایشگر) اجرا نشد (✍️ از مستندات). همان شواهد را با `samtools tview`، `samtools mpileup` و `bcftools` گرفتیم و گزارش HTML ‏igv.js را با igv-reports ساختیم. همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). ‏igv-reports ‏۲٫۲ ثانیه و ۵۶ مگابایت حافظه.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ژنوم، GFF، BAM و VCF را در **IGV** بار کنید و به یک واریانت بروید.
2. رنگ‌ها و نشانه‌های IGV را بخوانید: پوشش (coverage)، باز نابرابر، رشته، حذف، کیفیت نگاشت.
3. همان نما را در خط فرمان با **`samtools tview`** و شمارش‌ها را با **`mpileup`** بگیرید.
4. با چهار پرسش، **SNP واقعی** را از **خطای توالی‌یابی** جدا کنید.
5. از واریانت‌ها گزارش **HTML** (igv-reports) یا تصویر (IGV batch) بسازید.

**پیش از آغاز:** داده همان «سویه‌ی مقاوم» ماژول 02/04 است؛ ژنوم و GFF از بخش ۰۱.

<div dir="ltr">

```bash
mkdir -p ~/global/m03 && cd ~/global/m03
conda activate databases
C=~/Bioinformatics_Learning-main
ln -s $C/01_Linux/99_scripts_data/data/ecoli_k12.fna ref.fna
ln -s $C/01_Linux/99_scripts_data/data/ecoli_k12.gff ecoli_k12.gff
for f in resistant.bam resistant.bam.bai resistant.vcf.gz resistant.vcf.gz.tbi; do
  ln -s $C/02_BioLinux/99_scripts_data/04_Align_Variant_Formats/data/$f .
done
samtools faidx ref.fna
```

</div>

‏`ln -s` یک **پیوند نمادین** (میان‌بر) می‌سازد تا فایل‌ها را کپی نکنیم. ‏`samtools faidx` ایندکس ژنوم (`ref.fna.fai`) را می‌سازد؛ IGV و `tview` آن را لازم دارند.

---

## ۱. داستان

در 02/04 دیدید که فراخوان واریانت (`bcftools call`) در سویه‌ی مقاوم به ریفامپیسین چهار واریانت یافت، از جمله **rpoB H526Y**. داور مقاله‌ی شما می‌پرسد: «آیا این واریانت‌ها را **با چشم** روی ریدها وارسی کرده‌اید؟». این پرسش جدی است: نرم‌افزار فراخوان گاهی خطای توالی‌یابی، خطای هم‌ترازی یا ناحیه‌ی تکراری را واریانت می‌پندارد. ابزار استاندارد برای دیدن ریدها **IGV** (Integrative Genomics Viewer، مؤسسه‌ی Broad) است.

**پاسخ معلوم:** داده **شبیه‌سازی** شده است (اسکریپت `make_examples.sh` در 02/04). پس می‌دانیم دقیقاً چه در آن هست:
- چهار واریانت واقعی: SNP در 4175500 ‏(C→T)، **4182820 ‏(C→T، rpoB H526Y)**، 4193210 ‏(G→A) و یک حذف ۱ بازی در 4189000.
- ‏۳۰۰۰ جفت رید ۱۵۰ بازی (~۳۰ برابر پوشش) با **نرخ خطای ۰٫۲٪** (`wgsim -e 0.002`). پس باید خطاهای پراکنده هم ببینیم.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ نمای هم‌ترازی چه نشان می‌دهد؟

ژنوم مرجع را یک **خط‌کش** بالای صفحه بینگارید. هر رید یک نوار زیر آن است که جایی چسبیده که بیشترین همانندی را داشته است. IGV بازهایی را که **با مرجع یکی‌اند**، خاکستری و بی‌نشان می‌کشد و تنها **نابرابرها** را رنگی نشان می‌دهد. پس چشم شما تنها به جاهایی می‌رود که چیزی فرق دارد.

<div dir="ltr">

```text
reference   ...TACGCACAAACGTC...
read 1      ...........T......          <- mismatch: coloured letter
read 2      ...........T......
read 3      ......C....T......          <- a single odd base: probably an error
read 4      ...........T......
coverage    ▁▁▁▁▁▁▁▁▁▁▁█▁▁▁▁▁▁          <- coverage bar coloured where alt > 20%
```

</div>

### ۲.۲ چهار پرسش برای «SNP یا خطا؟»

| پرسش | ‏SNP واقعی (باکتری، تک‌لاد) | خطای توالی‌یابی |
| :--- | :--- | :--- |
| **۱. چند درصد ریدها؟** | نزدیک به ۱۰۰٪ (در انسان، دولاد: ۵۰٪ یا ۱۰۰٪) | یک یا دو رید از ده‌ها |
| **۲. هر دو رشته؟** | ریدهای رو به جلو و رو به عقب هر دو | گاهی تنها یک رشته (**strand bias**) |
| **۳. کیفیت باز؟** | بالا | اغلب پایین‌تر (در داده‌ی واقعی) |
| **۴. کیفیت نگاشت (MAPQ)؟** | بالا (رید جایش یکتاست) | اگر پایین: ناحیه‌ی تکراری، نه واریانت |

### ۲.۳ رنگ‌ها و نشانه‌های IGV

| در IGV | معنا |
| :--- | :--- |
| ستون پوشش رنگی | در آن جایگاه بیش از ۲۰٪ بازها با مرجع فرق دارند (آستانه‌ی پیش‌فرض) |
| حرف رنگی در رید | باز نابرابر؛ رنگ کم‌رنگ = کیفیت پایین |
| رید سفید یا توخالی | کیفیت نگاشت صفر (MAPQ = 0): رید جای یکتا ندارد |
| خط سیاه افقی | حذف (deletion) |
| نشان بنفش `I` | درج (insertion) |
| رنگ رید (گزینه‌ی *Color by strand*) | سرخ = رشته‌ی رو به جلو، آبی = رو به عقب |

---

## ۳. گام ۱: ‏IGV رومیزی (✍️)

**چرا؟** پرکاربردترین راه وارسی چشمی، و همانی که داوران و آزمایشگاه‌های بالینی می‌خواهند.

✍️ **گام‌ها (از راهنمای IGV؛ روی لپ‌تاپ شما):**
1. ‏IGV را از https://igv.org/download نصب کنید (نسخه‌ی پایدار در زمان نگارش: **2.19.8**؛ جاوا ۲۱ را خود بسته دارد). نسخه‌ی **igv.org/app** هم در مرورگر کار می‌کند.
2. ‏**Genomes ← Load Genome from File…** ← `ecoli_k12.fna` (فایل `.fai` باید کنارش باشد). ‏*E. coli* در فهرست ژنوم‌های آماده‌ی IGV نیست.
3. ‏**File ← Load from File…** ← `ecoli_k12.gff`، `resistant.bam` (فایل `.bai` کنارش) و `resistant.vcf.gz` (فایل `.tbi` کنارش).
4. در جعبه‌ی بالای صفحه بنویسید `NC_000913.3:4182800-4182840` یا تنها `rpoB` و Enter بزنید.
5. ستون 4182820 را ببینید: در **همه**‌ی ریدها `T` است. روی رید راست‌کلیک کنید ← **Sort alignments by ← base** تا ریدهای دارای باز دیگر بالا بیایند؛ و **Color alignments by ← read strand** تا رشته‌ها را ببینید.
6. روی ستون پوشش بزنید: پنجره‌ای شمار هر باز را می‌دهد (برای نمونه `T: 34 (100%, 19+, 15-)`).
7. ‏**File ← Save PNG Image…** (یا SVG، برای مقاله) از نمای کنونی تصویر می‌سازد.

<details>
<summary>✋ امتحان کن: چرا IGV ژنوم را از فایل می‌خواهد ولی برای انسان نه؟</summary>

‏IGV برای ژنوم‌های پرکاربرد (hg38، hg19، موش و…) نسخه‌ی آماده با آنوتیشن روی سرور خود دارد و آن‌ها را از فهرست بار می‌کند. برای ژنوم دیگر، FASTA و ایندکس آن را خودتان می‌دهید. اسمبلی ژنوم باید **همان** باشد که ریدها روی آن هم‌تراز شده‌اند (12/02): نام کروموزوم در BAM (`NC_000913.3`) باید با نام در FASTA یکی باشد، وگرنه IGV هیچ ریدی نشان نمی‌دهد.

</details>

> 📺 **فیلم:** *IGV | Sequencing Data Basics* (کانال رسمی IGV): https://www.youtube.com/watch?v=E_G8z_2gTYM · *IGV | Data Navigation Basics (V2)*: https://www.youtube.com/watch?v=YpNg0hNUuo8
> 📄 **مرجع:** Robinson JT, et al. (2011). *Integrative genomics viewer.* Nat Biotechnol 29:24–26. https://doi.org/10.1038/nbt.1754 · Thorvaldsdóttir H, Robinson JT, Mesirov JP (2013). *IGV: high-performance genomics data visualization and exploration.* Brief Bioinform 14:178–192. https://doi.org/10.1093/bib/bbs017

---

## ۴. گام ۲: همان نما در خط فرمان (`samtools tview`)

**چرا؟** روی سرور بی نمایشگر هم باید بتوانید ریدها را ببینید. `samtools tview` همان نمای IGV را با **متن** می‌کشد.

<div dir="ltr">

```bash
samtools tview -d T -p NC_000913.3:4182806 -w 40 resistant.bam ref.fna | head -16
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-d T` | خروجی **متنی** (بی آن، `tview` پنجره‌ی تعاملی باز می‌کند و با `q` بسته می‌شود) |
| ‏`-p chr:pos` | از این جایگاه آغاز کن (لبه‌ی **چپ** نما) |
| ‏`-w 40` | پهنای نما: ۴۰ باز |
| ‏`ref.fna` | ژنوم مرجع؛ بی آن، بازهای برابر هم با حرف نشان داده می‌شوند |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
     4182811   4182821   4182831        
TGTCTGAGATTACGCACAAACGTCGTATCTCCGCACTCGG
..............T.........................
...,,,,,,,,,,,t,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,  .....T.........................
........    ..T.........................
,,,,,,,,,,,,,,t,,,,,     ,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,t,,,,       ..............
,,,,,,,,,,,,,,t,,,,,        ............
,,,,,,,,,,,,,,t,,,,,,,,,                
..............T..............           
..............T...............          
..............T....C..................  
,,,,,,,,,,,,,,t,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,t,,,,,,,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,t,,,,,,,,,,,,,,,,,,,,,,,,,
..............T.........................
```

</div>

**خواندن خروجی:**
- سطر ۱ خط‌کش است (عدد زیر رقم یکانش قرار دارد)، سطر ۲ **مرجع**، سطر ۳ **توافق** (consensus) ریدها، و از سطر ۴ به بعد هر سطر یک یا چند رید.
- ‏`.` = باز برابر با مرجع روی رشته‌ی **رو به جلو**؛ `,` = برابر، روی رشته‌ی **رو به عقب**. حرف بزرگ = نابرابر رو به جلو، حرف کوچک = نابرابر رو به عقب. ‏`*` = حذف. فاصله = آن‌جا رید نیست.
- ستون پانزدهم، **4182820**: مرجع `C` (درون `CAC`)، و در **همه**‌ی ریدها `T` یا `t`، روی هر دو رشته. این rpoB H526Y است.
- پنج باز آن‌سوتر، **4182825**: در **یک** رید (رو به جلو) `C` به جای `A`. این همان چیزی است که باید «خطا» بنامیم.

<details>
<summary>✋ امتحان کن: پیش از گام بعد، تنها با همین تصویر بگویید 4182825 واریانت است یا نه.</summary>

نه. تنها یک رید از نزدیک به ۳۰، روی یک رشته. باکتری تک‌لاد است: واریانت واقعی باید در نزدیک به **همه**‌ی ریدها باشد. گام ۳ همین را با عدد نشان می‌دهد.

</details>

> 📺 **فیلم:** *IGV | View SNPs | Homozygous, Heterozygous, Strand Bias* (کانال رسمی IGV): https://www.youtube.com/watch?v=eZUI6lcIX3I
> 📄 **مرجع:** Danecek P, et al. (2021). *Twelve years of SAMtools and BCFtools.* GigaScience 10(2):giab008. https://doi.org/10.1093/gigascience/giab008 · راهنمای `tview`: https://www.htslib.org/doc/samtools-tview.html

---

## ۵. گام ۳: شمردن شواهد

**چرا؟** چشم فریب می‌خورد؛ عدد نه. برای هر جایگاه، شمار بازها را روی **هر رشته** جدا می‌خواهیم.

### ۵.۱ یک جایگاه با `samtools mpileup`

<div dir="ltr">

```bash
for p in 4182820 4182825 4172023; do
  samtools mpileup -f ref.fna -r NC_000913.3:$p-$p resistant.bam 2> /dev/null | cut -f2-6
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
4182820	C	33	ttttTTTtttTTTTtTTTTtttTTttTtTtTTT	6<<<<<<<<<<<<<<<<<<<<<<<W<<<<<<<6
4182825	A	31	,$,..C,,,....,....,,,..,,.,.,...	<<<<<<<<<<<<<<<<<<<<<<W<<<<<<<<
4172023	A	28	,$,,,..,....,,,,,.,.,.,t,,t.^K,	<<<<WW<<<<<<<<<<<<<<<<<<<6<W
```

</div>

**ستون‌ها:** جایگاه، باز مرجع، **عمق**، بازهای ریدها (همان نشانه‌های `tview`) و **کیفیت** هر باز (Phred، ‏ASCII−33؛ `<` = ۲۷). ‏`$` پایان یک رید و `^K` آغاز یک رید را نشان می‌دهند (و بازی نیستند).

- **4182820:** ‏۳۳ از ۳۳ باز `T`، کوچک و بزرگ آمیخته: هر دو رشته. ✅ SNP.
- **4182825:** ‏یک `C` از ۳۱. ✅ خطا.
- **4172023:** ‏دو `t` از ۲۸، و هر دو **کوچک**: هر دو روی رشته‌ی رو به عقب. ✅ خطا (دو خطای تصادفی هم‌جا؛ با ۱۴۵۰ خطای پراکنده در این ناحیه، چنین هم‌جایی‌ای پیش می‌آید).

**یادداشت درباره‌ی کیفیت:** همه‌ی بازها کیفیت `<` (۲۷) دارند، **خطاها هم**. ‏`wgsim` کیفیت ثابت می‌سازد. در داده‌ی واقعی Illumina بازهای نادرست اغلب کیفیت پایین‌تری دارند و IGV آن‌ها را کم‌رنگ می‌کشد. این‌جا پرسش ۳ جدول ۲.۲ کمکی نمی‌کند و باید به پرسش‌های ۱ و ۲ تکیه کنیم.

### ۵.۲ همه‌ی ناحیه با `bcftools mpileup`

<div dir="ltr">

```bash
bcftools mpileup -f ref.fna -r NC_000913.3:4172000-4198000 -a FORMAT/AD,FORMAT/ADF,FORMAT/ADR -Q 0 -q 0 \
    resistant.bam 2> /dev/null > pile.vcf
bcftools query -i 'FORMAT/AD[0:1] > 0' -f '%POS\t%REF\t%ALT\t[%AD]\t[%ADF]\t[%ADR]\n' pile.vcf > alts.tsv
wc -l < alts.tsv
awk -F'\t' '{split($4, a, ","); alt = 0; for (i = 2; i <= length(a); i++) alt += a[i];
             f = alt / (a[1] + alt);
             if (alt == 1) one++; else if (f > 0.8) hi++; else mid++}
            END {print "one read:", one, " >80%:", hi, " other:", mid}' alts.tsv
awk -F'\t' '{split($4, a, ","); if (a[2] > 0.8 * (a[1] + a[2])) print}' alts.tsv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-a FORMAT/AD,ADF,ADR` | شمار هر باز: کل (AD)، رو به جلو (ADF)، رو به عقب (ADR) |
| ‏`-Q 0 -q 0` | هیچ بازی را برای کیفیت پایین کنار نگذار (می‌خواهیم **همه**‌ی نابرابرها را ببینیم) |
| بی `bcftools call` | هر جایگاه را نگه دار، نه تنها واریانت‌ها |
| ‏`-i 'FORMAT/AD[0:1] > 0'` | جایگاه‌هایی که دست‌کم یک باز دیگر دارند |
| ‏`split($4, a, ",")` | ‏AD را بشکن: `a[1]` باز مرجع، بقیه بازهای دیگر |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
1510
one read: 1451  >80%: 4  other: 55
4175500	C	T,<*>	0,27,0	0,10,0	0,17,0
4182820	C	T,<*>	0,34,0	0,19,0	0,15,0
4188999	CG	C	1,38	0,20	1,18
4193210	G	A,<*>	0,29,0	0,17,0	0,12,0
```

</div>

**توضیح خروجی:**
- در ۲۶ کیلوباز، **۱۵۱۰** جایگاه دست‌کم یک باز نابرابر دارند. **۱۴۵۱** تای آن‌ها تنها **یک** رید: همان خطاهای ۰٫۲٪.
- تنها **چهار** جایگاه بیش از ۸۰٪ رید دیگر دارند، و این‌ها **دقیقاً** چهار واریانت شبیه‌سازی‌شده‌اند. ✅ هر چهار روی هر دو رشته دیده می‌شوند (ADF و ADR هر دو بزرگ).
- ‏`<*>` در ALT یعنی «هر باز دیگری» (برای شمارش در `call`)؛ ‏`0` پایانی شمار آن است.
- **۵۵** جایگاه دو رید دارند ولی کمتر از ۸۰٪: بیشترشان کمتر از ۹٪، و بالاترین 4176822 با ۲ از ۱۴ رید (۱۴٪) در جایی کم‌پوشش. در آن جایگاه هم دو رید دو باز **گوناگون** دارند (`T` و `C`، ‏AD ‏`12,1,1`): دو خطای جدا، نه یک واریانت. ‏`bcftools call` (02/04) هیچ‌کدام را واریانت نخواند.

<details>
<summary>✋ امتحان کن: با همین شمارش‌ها نرخ خطا را برآورد کنید.</summary>

بازهای نابرابر «خطاگونه» (جایگاه‌هایی که باز مرجع بیش از پنج برابر بقیه است) را بشمارید و بر کل بازهای هم‌تراز بخش کنید (`samtools depth -a`). پاسخ: ۱۵۶۰ / ۷۸۶٬۸۰۱ = **۰٫۱۹۸٪**، همان ۰٫۲٪ ‏`wgsim`. ✅ (تمرین ۳.)

</details>

### ‏۵.۳ ‏MAPQ: ریدهایی که جای یکتا ندارند

ریدها **تنها** از ناحیه‌ی ۴٬۱۷۰٬۰۰۱ تا ۴٬۲۰۰٬۰۰۰ شبیه‌سازی شدند (02/04). پس همه باید همان‌جا بنشینند. ببینیم:

<div dir="ltr">

```bash
samtools view -c resistant.bam
samtools view -c -q 10 resistant.bam
samtools view resistant.bam | awk '$5 < 10 {if ($4 >= 4170001 && $4 <= 4200000) inside++; else outside++}
                                   END {print "MAPQ<10 inside region:", inside, " elsewhere:", outside}'
samtools view resistant.bam NC_000913.3:3470145-3471329 | cut -f5 | sort | uniq -c
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
6000
5552
MAPQ<10 inside region: 224  elsewhere: 224
     30 1
```

</div>

**توضیح خروجی:**
- از ۶۰۰۰ رید، **۴۴۸** کیفیت نگاشت کمتر از ۱۰ دارند (`-q 10` تنها ریدهای MAPQ ≥ ۱۰ را می‌شمارد: ۵۵۵۲). ستون پنجم SAM همان MAPQ است.
- نیمی از آن‌ها (۲۲۴) **بیرون** از ناحیه‌ی شبیه‌سازی نشسته‌اند! برای نمونه ۳۰ رید روی ژن **tufA** ‏(3470145 تا 3471329)، همه با MAPQ ‏۱.
- چرا؟ ناحیه‌ی ما ژن **tufB** و اپرون rRNA ‏**rrnB** را دارد. *E. coli* دو ژن tuf دارد که **۱۳ باز** از ۱۱۸۵ باز با هم فرق دارند (۹۸٫۹٪ یکسان)، و **هفت** اپرون rRNA. با فهرست ژن‌های GFF، ریدهای MAPQ پایین دیگر روی همان rRNAهای دیگر نشسته‌اند (rrlH، rrlG، rrlD، rrlC، rrlA، rrlE). ریدی که در دو جا یکسان می‌خورد، تصادفی یکی را می‌گیرد و هم‌ترازکننده با MAPQ پایین می‌گوید «مطمئن نیستم».
- **پیامد:** اگر در tufA «واریانتی» بیابید که تنها ریدهای MAPQ پایین آن را دارند، در واقع تفاوت tufB با tufA است، نه جهش. در IGV این ریدها **سفید یا توخالی** کشیده می‌شوند. پیش‌فرض `bcftools mpileup` ‏`--min-MQ 0` است، یعنی این ریدها را **نگه می‌دارد**؛ برای کنار گذاشتنشان `-q 20` (یا هر آستانه‌ی دیگر) بدهید.

---

## ۶. گام ۴: حذف در نما

<div dir="ltr">

```bash
samtools tview -d T -p NC_000913.3:4188980 -w 40 resistant.bam ref.fna | head -8
bcftools view -H resistant.vcf.gz NC_000913.3:4188999 | cut -f1-5
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
 4188981   4188991   4189001            
TCCGACGGTCCGGAAGCGCCGCACGACATTCTGCGTCTGC
....................C...................
....................*...................
,,,,,,,,,,,,,,,,,,,,c,,,,,,,,,,,,,,,,,,,
,,,,,,,,,,,,,,,,,,,,*,,,,,,,, ..........
,,,,,,,,,,,,,,,,,,,,*,,,,,,,,,,         
....................*...........
NC_000913.3	4188999	.	CG	C
```

</div>

**خواندن خروجی:**
- ستون بیست‌ویکم، **4189000**: مرجع `G`، و در ریدها `*` یعنی این باز **نیست**. همان حذف ۱ بازی شبیه‌سازی‌شده.
- ‏VCF آن را در **4188999** با `CG → C` می‌نویسد: قاعده‌ی VCF یک باز **پیش** از حذف (`C`) را هم نگه می‌دارد تا هیچ ستونی تهی نماند (همانند SPDI در 11/05).
- **دام:** یک رید به جای `*`، باز `c` دارد. هم‌ترازکننده نزدیک **پایان** آن رید، یک نابرابر را «ارزان‌تر» از یک شکاف دیده است. و چون `*` باز نیست، **سطر توافق** (سطر سوم) در این ستون همان تک `C` را نشان می‌دهد! به سطر توافق کورکورانه اعتماد نکنید؛ ریدها را ببینید. در خروجی `bcftools mpileup` گام ۳ همین به شکل جایگاه 4189000 با «G→C، یک از یک» آمد.

---

## ۷. گام ۵: گزارش HTML با igv-reports

**چرا؟** برای ده‌ها واریانت، باز کردن IGV و رفتن به هر کدام کند است. **igv-reports** برای هر واریانت VCF تکه‌ی کوچکی از BAM، ژنوم و GFF را برمی‌دارد و همه را در **یک فایل HTML** با **igv.js** (IGV در مرورگر) می‌گذارد. فایل را برای همکار یا داور می‌فرستید و آن را بی نصب چیزی باز می‌کند.

<div dir="ltr">

```bash
create_report resistant.vcf.gz --fasta ref.fna \
    --tracks resistant.vcf.gz resistant.bam ecoli_k12.gff \
    --flanking 40 --info-columns DP --standalone \
    --title "rpoB region: resistant isolate" --output report.html
ls -lh report.html
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`resistant.vcf.gz` (نخست) | جایگاه‌هایی که برایشان نما ساخته می‌شود (هر سطر VCF یک نما) |
| ‏`--tracks …` | ترک‌های هر نما: خود VCF، ریدها و آنوتیشن |
| ‏`--flanking 40` | ۴۰ باز در هر سو |
| ‏`--info-columns DP` | ستون عمق (از INFO ‏VCF) در جدول بالای صفحه |
| ‏`--standalone` | خود igv.js را هم درون فایل بگذار تا بی اینترنت باز شود |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
Working on variant 1/4
Working on variant 2/4
Working on variant 3/4
Working on variant 4/4
-rw-rw-r-- 1 ubuntu ubuntu 1.3M Oct 27 18:21 report.html
```

</div>

‏`report.html` را در مرورگر باز کنید: بالای صفحه جدول چهار واریانت (جایگاه، REF، ALT، DP) است. با زدن هر سطر، نمای igv.js همان جایگاه را با ریدها، GFF و VCF نشان می‌دهد و ریدها بر پایه‌ی باز مرتب شده‌اند. بی `--standalone`، فایل ۳۲ کیلوبایت است ولی igv.js را از اینترنت (cdn.jsdelivr.net) می‌گیرد.

(ما کوشیدیم با Chrome بی‌سر از این صفحه تصویر بگیریم؛ igv.js در آن حالت بار نشد و تصویر تهی ماند. در مرورگر عادی بی‌مشکل باز می‌شود.)

> 📺 **فیلم:** *IGV | VCF Basics | VCF File Explanation & Viewing in IGV* (کانال رسمی IGV): https://www.youtube.com/watch?v=EpD2ZHM7Q8Q
> 📄 **مرجع:** Robinson JT, et al. (2023). *igv.js: an embeddable JavaScript implementation of the Integrative Genomics Viewer (IGV).* Bioinformatics 39(1):btac830. https://doi.org/10.1093/bioinformatics/btac830 · igv-reports: https://github.com/igvteam/igv-reports

---

## ۸. گام ۶: تصویر برای گزارش (IGV batch، ✍️)

**چرا؟** برای مقاله یا گزارش بالینی، تصویرهای **یکسان** و **تکرارپذیر** می‌خواهید، نه چند اسکرین‌شات دستی.

‏IGV رومیزی **اسکریپت batch** می‌پذیرد: هر سطر یک دستور. فایل `rpoB_snapshots.igv.txt` در `99_scripts_data/03_IGV_Visualization/scripts/`:

<div dir="ltr">

```text
new
genome ecoli_k12.fna
load ecoli_k12.gff
load resistant.bam
load resistant.vcf.gz
snapshotDirectory snapshots
goto NC_000913.3:4182800-4182840
sort base NC_000913.3:4182820
collapse ecoli_k12.gff
snapshot rpoB_H526Y.png
goto NC_000913.3:4182805-4182845
sort base NC_000913.3:4182825
snapshot error_4182825.png
goto NC_000913.3:4188980-4189020
snapshot deletion_4188999.png
exit
```

</div>

✍️ **اجرا (از راهنمای batch ‏IGV):** در IGV ‏**Tools ← Run Batch Script…** و فایل را برگزینید؛ یا از خط فرمان `igv.sh -b rpoB_snapshots.igv.txt`. مسیر فایل‌ها نسبت به پوشه‌ای است که IGV از آن اجرا می‌شود؛ اگر IGV فایلی را نیافت، مسیر کامل بنویسید. پوشه‌ی `snapshots/` سه تصویر PNG می‌گیرد (برای SVG، پسوند را `.svg` کنید).

| دستور | کار |
| :--- | :--- |
| ‏`new` | همه‌ی ترک‌های پیشین را پاک کن |
| ‏`genome` / `load` | ژنوم و ترک‌ها را بار کن |
| ‏`goto` | به این ناحیه برو |
| ‏`sort base POS` | ریدها را بر پایه‌ی باز در این جایگاه مرتب کن |
| ‏`collapse TRACK` | ترک را فشرده نشان بده (همان dense در UCSC) |
| ‏`snapshotDirectory` / `snapshot` | پوشه و نام تصویر |

> 📺 **فیلم:** *IGV | View SNPs | Homozygous, Heterozygous, Strand Bias* (همان فیلم گام ۲)
> 📄 **مرجع:** Robinson JT, et al. (2017). *Variant Review with the Integrative Genomics Viewer.* Cancer Res 77(21):e31–e34. https://doi.org/10.1158/0008-5472.CAN-17-0337 · راهنمای batch: https://igv.org/doc/desktop/UserGuide/tools/batch/

---

## ۹. سه اشتباه رایج

1. **نام کروموزوم یا اسمبلی ناهمخوان.** ‏BAM روی `NC_000913.3` است؛ اگر ژنوم IGV کروموزوم را `chr` یا `U00096.3` (نام GenBank همین ژنوم) بنامد، هیچ ریدی دیده نمی‌شود و IGV گاهی **هیچ خطایی** نمی‌دهد. پیش از هر چیز `samtools view -H` و `cut -f1 ref.fna.fai` را بسنجید.
2. **«دیدم، پس درست است».** یک رید یا دو رید روی یک رشته، واریانت نیست (4172023). در ناحیه‌های پرپوشش، حتی ده رید خطادار هم پیش می‌آید؛ پس **درصد** و **هر دو رشته** را بسنجید، نه تنها «هست یا نیست». اگر ریدها MAPQ صفر دارند (سفید در IGV)، ناحیه تکراری است و واریانت را باور نکنید.
3. **اعتماد به سطر توافق یا نمای دور.** در نمای دور (بیش از چند ده کیلوباز) IGV ریدها را نشان نمی‌دهد و تنها پوشش را می‌کشد. و سطر توافق در جایگاه حذف تک بازی را نشان داد که در یک رید بود (گام ۴). همیشه تا سطح باز بزرگ کنید.

---

## 📘 برای کنجکاوها

- **دولاد (انسان):** در نمونه‌ی انسانی، SNP ناهم‌سان (heterozygous) در **نزدیک به ۵۰٪** ریدها دیده می‌شود و هم‌سان (homozygous) در ۱۰۰٪. خطا همچنان چند درصد است. فیلم «View SNPs» کانال IGV همین را نشان می‌دهد.
- **رنگ بر پایه‌ی اندازه‌ی قطعه:** در IGV جفت‌ریدهایی که فاصله‌شان از انتظار بیشتر است، رنگ دیگری می‌گیرند. این نشانه‌ی **واریانت ساختاری** (حذف یا جابه‌جایی بزرگ) است. جای کامل آن، دوره‌ی جداگانه‌ی NGS است.
- ‏**igv.js در Jupyter:** بسته‌ی `igv-notebook` همین نما را درون دفترچه‌ی Jupyter می‌آورد.

---

## جمع‌بندی

- ‏IGV ژنوم، آنوتیشن، ریدها و واریانت‌ها را روی هم نشان می‌دهد؛ تنها نابرابرها رنگی‌اند.
- روی سرور: `samtools tview -d T` (نما)، `samtools mpileup` (یک جایگاه)، `bcftools mpileup -a AD,ADF,ADR` (همه‌ی ناحیه).
- ‏SNP یا خطا؟ درصد ریدها، هر دو رشته، کیفیت باز، کیفیت نگاشت. در این داده: ۴ جایگاه ≥۹۷٪ روی هر دو رشته (واریانت‌های واقعی) در برابر ۱۴۵۱ جایگاه تک‌رید (خطای ۰٫۲٪).
- ‏VCF حذف را با یک باز پیش از آن می‌نویسد (`CG → C` در 4188999).
- برای هم‌رسانی: igv-reports (یک HTML)؛ برای مقاله: IGV batch (PNG یا SVG تکرارپذیر).

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
samtools faidx ref.fna                                               # index the genome (IGV, tview)
samtools tview -d T -p CHR:POS -w 40 aln.bam ref.fna                 # text view of reads
samtools mpileup -f ref.fna -r CHR:POS-POS aln.bam                   # bases and qualities at one site
bcftools mpileup -f ref.fna -r REGION -a FORMAT/AD,FORMAT/ADF,FORMAT/ADR -Q 0 -q 0 aln.bam > pile.vcf
bcftools query -i 'FORMAT/AD[0:1] > 0' -f '%POS\t%REF\t%ALT\t[%AD]\t[%ADF]\t[%ADR]\n' pile.vcf
samtools stats aln.bam | grep '^SN' | grep 'error rate'               # mismatches / aligned bases
create_report calls.vcf.gz --fasta ref.fna --tracks calls.vcf.gz aln.bam genes.gff --standalone --output report.html
igv.sh -b script.igv.txt                                              # IGV batch snapshots (desktop)
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏IGV | مرورگر ژنوم رومیزی مؤسسه‌ی Broad برای داده‌ی خود شما |
| ‏igv.js | همان IGV در مرورگر وب |
| پوشش (coverage، depth) | شمار ریدهایی که از یک باز می‌گذرند |
| باز نابرابر (mismatch) | بازی در رید که با مرجع فرق دارد |
| سوگیری رشته (strand bias) | دیده شدن یک باز تنها روی یکی از دو رشته |
| ‏MAPQ | کیفیت نگاشت: چقدر مطمئنیم رید جای درستی نشسته است |
| کیفیت باز (Phred) | اطمینان دستگاه به هر باز؛ ۲۰ = ۱٪ خطا، ۳۰ = ۰٫۱٪ |
| سطر توافق (consensus) | بیشترین باز هر ستون در میان ریدها |
| پیوند نمادین (`ln -s`) | میان‌بری به فایل دیگر، بی کپی |
| ‏pileup | فهرست همه‌ی بازهای ریدها در هر جایگاه |
| ‏ADF / ADR | شمار هر باز روی رشته‌ی رو به جلو / رو به عقب |
| اسکریپت batch | فهرست دستورهای IGV برای کار خودکار |
| تک‌لاد / دولاد | یک نسخه (باکتری) / دو نسخه (انسان) از هر کروموزوم |

---

## منابع

**مقاله و مستند**
- ‏Robinson JT, et al. (2011). *Integrative genomics viewer.* Nat Biotechnol 29:24–26. https://doi.org/10.1038/nbt.1754
- ‏Thorvaldsdóttir H, Robinson JT, Mesirov JP (2013). *Integrative Genomics Viewer (IGV): high-performance genomics data visualization and exploration.* Brief Bioinform 14:178–192. https://doi.org/10.1093/bib/bbs017
- ‏Robinson JT, et al. (2017). *Variant Review with the Integrative Genomics Viewer.* Cancer Res 77(21):e31–e34. https://doi.org/10.1158/0008-5472.CAN-17-0337
- ‏Robinson JT, et al. (2023). *igv.js: an embeddable JavaScript implementation of the Integrative Genomics Viewer (IGV).* Bioinformatics 39(1):btac830. https://doi.org/10.1093/bioinformatics/btac830
- ‏Danecek P, et al. (2021). *Twelve years of SAMtools and BCFtools.* GigaScience 10(2):giab008. https://doi.org/10.1093/gigascience/giab008
- راهنماها: IGV ‏https://igv.org/doc/desktop/ · batch ‏https://igv.org/doc/desktop/UserGuide/tools/batch/ · igv-reports ‏https://github.com/igvteam/igv-reports · samtools ‏https://www.htslib.org/doc/samtools.html

**کتاب**
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۱۱: کار با داده‌ی هم‌ترازی؛ SAM و BAM و `samtools tview`)
- ‏Baxevanis AD, Bader GD, Wishart DS, eds. (2020). *Bioinformatics*, 4th ed. Wiley. (فصل ۴: *Genome Browsers*)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Command Line Tools for Genomic Data Science* (Johns Hopkins): https://www.coursera.org/learn/genomic-tools
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *IGV | Sequencing Data Basics* (IGV): https://www.youtube.com/watch?v=E_G8z_2gTYM
- ‏YouTube: *IGV | View SNPs | Homozygous, Heterozygous, Strand Bias* (IGV): https://www.youtube.com/watch?v=eZUI6lcIX3I
- ‏YouTube: *IGV | VCF Basics* (IGV): https://www.youtube.com/watch?v=EpD2ZHM7Q8Q

<sub>دستورهای خط فرمان در 2026-10-27 روی سرور دوره اجرا شدند (samtools و bcftools 1.24، igv-reports 1.16.0). IGV رومیزی برنامه‌ی گرافیکی است و سرور نمایشگر ندارد؛ igv.org هم از سرور در دسترس نبود. پس گام‌های IGV و فرمان‌های batch از راهنمای IGV و فیلم‌های کانال رسمی IGV نوشته شدند (✍️)، و نسخه‌ی 2.19.8 از صفحه‌ی دانلود IGV است. فیلم‌ها با noembed وارسی شدند؛ DOIها با Crossref. فصل کتاب Buffalo از فهرست کتاب (فصل ۹ بازه‌ها، فصل ۱۱ هم‌ترازی).</sub>

</div>
