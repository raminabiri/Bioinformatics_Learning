<div dir="rtl">

# پاسخ تشریحی: DESeq2، vegan و ggtree

خروجی‌ها از اجرای واقعی در 2026-10-20 (R 4.6.1، DESeq2 1.52.0، vegan 2.7.6، ggtree 4.2.0) گرفته شده‌اند. داده‌ی DESeq2 با بذر تصادفی ثابت (`42`) ساخته می‌شود، پس شمارش‌ها روی هر کامپیوتر یکسان‌اند. با نسخه‌ی دیگری از DESeq2، شاید رقم‌های پایانی کمی فرق کنند.

---

## پاسخ ۱: خلاصه‌ی DESeq2

<div dir="ltr">

```bash
cd ~/r_practice/deseq2
awk -F'\t' 'NR > 1 && $7 != "NA" && $7 < 0.05 && $3 > 0' deseq2_results.tsv | wc -l
awk -F'\t' 'NR > 1 && $7 != "NA" && $7 < 0.05 && $3 < -2' deseq2_results.tsv | wc -l
```

</div>

<div dir="ltr">

```text
47
29
```

</div>

- (الف) **۴۷**؛ همان خط `LFC > 0 (up) : 47` خلاصه.
- (ب) **۲۹**. «۴ برابر کاهش» = یک‌چهارم = log2FoldChange کمتر از ‎−2.

**اشتباه رایج:** `$3 < 2` به‌جای `$3 < -2`، که همه‌ی ژن‌های با تغییر کمتر از ۴ برابر افزایش را هم می‌شمارد. یا فراموش کردن `$7 != "NA"`. (در mawk و gawk، `"NA" < 0.05` به‌صورت متنی سنجیده می‌شود و نادرست درمی‌آید، پس NA بی‌شرط دوم هم کنار می‌رود؛ ولی آشکار نوشتنش روشن‌تر و ایمن‌تر است.)

---

## پاسخ ۲: یک ژن را دنبال کنید

<div dir="ltr">

```bash
grep -w b3357 deseq2_results.tsv | cut -f1,2,3,7
grep -w b3357 counts.tsv
grep -w crp truth.tsv
```

</div>

<div dir="ltr">

```text
b3357	117.857416167156	1.32216076905383	0.000383486217684426
b3357	52	85	67	183	200	130
b3357	crp	1.72
```

</div>

- (الف) log2FoldChange = **1.32**، padj = **0.00038** (۳٫۸ × ۱۰⁻⁴). کمتر از ۰٫۰۵، پس **معنادار**.
- (ب) ‎2^1.32 ≈ **۲٫۵ برابر**. با شمارش خام بسنجید: WT نزدیک به ۶۸، RifR نزدیک به ۱۷۰.
- (ج) بله، crp در پاسخ‌نامه هست با تغییر واقعی **1.72** (کمابیش ۳٫۳ برابر). DESeq2 آن را کمی **کمتر** برآورد کرد (1.32). با تنها ۳ تکرار و نوسان طبیعی، برآورد اندازه‌ی تغییر دقیق نیست؛ ولی **جهت** و **معنادار بودن** درست است.

---

## پاسخ ۳: rpoB چه شد؟

<div dir="ltr">

```bash
D=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
grep -w rpoB $D/ecoli_k12.gff | grep -o "locus_tag=b[0-9]*" | head -1
grep -w b3987 deseq2_results.tsv | cut -f1,2,3,7
grep -w b3987 truth.tsv
```

</div>

<div dir="ltr">

```text
locus_tag=b3987
b3987	819.014970560338	0.351256185387464	0.982588379834687
```

</div>

‏rpoB = `b3987`. log2FoldChange = 0.35، padj = **0.98**: تغییر معناداری نیست. و در `truth.tsv` **نیست** (دستور سوم چیزی چاپ نکرد): در شبیه‌سازی هم تغییری به آن داده نشده بود.

**نتیجه‌ی زیستی: هیچ.** داده شبیه‌سازی‌شده است و ژن‌های «تغییرکرده» تصادفی برگزیده شدند. این تمرین تنها مهارت **پیدا کردن یک ژن** را می‌سنجد. (در زیست‌شناسی واقعی هم جهش نقطه‌ای H526Y توالی پروتئین را عوض می‌کند، نه لزوماً اندازه‌ی بیان خود rpoB را.)

---

## پاسخ ۴: آستانه‌ی سخت‌گیرانه‌تر

<div dir="ltr">

```bash
cp $P/03_Bioc_Examples/scripts/run_deseq2.R my_deseq2.R
sed -i 's/padj_cutoff <- 0.05/padj_cutoff <- 0.01/' my_deseq2.R
grep -n "padj_cutoff <-" my_deseq2.R
Rscript my_deseq2.R counts.tsv samples.tsv WT strict 2>/dev/null | grep -A3 "adjusted"
python3 $P/03_Bioc_Examples/scripts/compare_truth.py strict_results.tsv truth.tsv 0.01
```

</div>

<div dir="ltr">

```text
20:padj_cutoff <- 0.01   # false discovery rate for calling a gene "changed"
adjusted p-value < 0.01
LFC > 0 (up)       : 45, 1%
LFC < 0 (down)     : 39, 0.91%
outliers [1]       : 0, 0%
padj < 0.01: 84 genes called changed; 100 truly changed
found (true positives):  82
false alarms:            2
missed:                  18
wrote missed.tsv
```

</div>

| آستانه | گزارش‌شده | درست | هشدار کاذب | از دست‌رفته |
| :---: | :---: | :---: | :---: | :---: |
| ۰٫۰۵ | ۹۳ | ۸۸ | ۵ | ۱۲ |
| ۰٫۰۱ | ۸۴ | ۸۲ | **۲** | **۱۸** |

- (الف) **۴۵ up، ۳۹ down**.
- (ب) **۸۲** درست، **۲** هشدار کاذب، **۱۸** از دست‌رفته.
- (ج) **به دست آمد:** هشدار کاذب از ۵ به ۲ (فهرست «تمیزتر»). **از دست رفت:** ۶ ژن واقعی دیگر. هیچ آستانه‌ای هر دو را با هم کم نمی‌کند؛ ۰٫۰۵ قرارداد رایج است و آستانه‌ی برگزیده باید در روش‌ها نوشته شود.

**نکته:** `padj` در جدول عوض **نمی‌شود**؛ تنها مرز گزینش و خلاصه عوض می‌شود. (`compare_truth.py` با آستانه‌ی ۰٫۰۱ روی جدول اصلی `deseq2_results.tsv` هم همین ۸۲/۲/۱۸ را می‌دهد.)

---

## پاسخ ۵: سطح طبقه‌بندی

خروجی‌های درس ۲:

<div dir="ltr">

```text
level: organism                                      level: genus
 minigut          2   0.681  0.488  0.982            minigut          2   0.681  0.488  0.982
 minigut_sample2 21   1.608  0.572  0.528            minigut_sample2 18   1.535  0.569  0.531
 Bray-Curtis: 1                                      Bray-Curtis: 0.969
```

</div>

- (الف) **‏minigut** (یکنواختی ۰٫۹۸): دو باکتری با سهم ۵۸٪ و ۴۲٪، نزدیک به هم‌اندازه. در `minigut_sample2` یک جنس (Acinetobacter، ۶۵٪) چیره است و بیشتر موجودات زیر ۵٪اند.
- (ب) دو موجود `minigut` از دو جنس **جدا**‌اند (Bacteroides و Escherichia)، پس ادغام جنس چیزی را عوض نمی‌کند. در `minigut_sample2`، دو گونه‌ی Staphylococcus یکی شدند (‎−۱) و سه گونه‌ی Streptococcus یکی شدند (‎−۲): ۲۱ − ۳ = **۱۸**.
- (ج) در سطح موجود، **هیچ ستون مشترکی** نبود: E. coli در دو نمونه با دو نام متفاوت نوشته شده (`Escherichia coli K-12 MG1655` و `Escherichia coli str. K-12 substr. MG1655`) و Bacteroides دو گونه‌ی متفاوت است (fragilis و vulgatus). Bray–Curtis = ۱ یعنی «هیچ چیز مشترک»؛ از دید vegan درست است، از دید زیستی نه.

---

## پاسخ ۶: نمونه‌ی همسان

**پیش‌بینی:** `minigut` و `minigut_copy` یکسان‌اند ← **۰**. ‏`minigut_copy` همان `minigut` است، پس فاصله‌اش تا `minigut_sample2` همان **۰٫۹۶۹** است.

<div dir="ltr">

```bash
head -3 three.tsv
Rscript $P/03_Bioc_Examples/scripts/diversity.R three.tsv three genus 2>/dev/null
```

</div>

<div dir="ltr">

```text
sample	read_pairs	accession	organism
minigut	28912	NC_006347.1	Bacteroides fragilis YCH46
minigut_copy	28912	NC_006347.1	Bacteroides fragilis YCH46
level: genus  samples: 3  taxa: 18 
          sample reads richness shannon simpson evenness
         minigut 50000        2   0.681   0.488    0.982
    minigut_copy 50000        2   0.681   0.488    0.982
 minigut_sample2 24993       18   1.535   0.569    0.531

Bray-Curtis dissimilarity (0 = same, 1 = nothing shared):
                minigut minigut_copy
minigut_copy      0.000             
minigut_sample2   0.969        0.969
saved three_alpha.tsv three_bray.tsv three_rarecurve.png 
```

</div>

پیش‌بینی درست بود. این‌گونه آزمون («ورودی‌ای که پاسخش را می‌دانم») بهترین راه وارسی هر اسکریپت آماده است. کالبدشکافی awk: `{print}` هر سطر را چاپ می‌کند؛ اگر سطر از `minigut` باشد، ستون یکم را `minigut_copy` می‌کند و **یک بار دیگر** چاپ می‌کند (`OFS="\t"` تا جداکننده Tab بماند).

---

## پاسخ ۷: درخت چهاربرگی

<div dir="ltr">

```bash
cd ~/r_practice/tree
printf '(((A:1,B:1):1,C:2):1,D:3);\n' > four.nwk
Rscript $P/03_Bioc_Examples/scripts/plot_tree.R four.nwk four.png 2>/dev/null
```

</div>

<div dir="ltr">

```text
tips (leaves): 4 
first tips: A B C D 
saved four.png
```

</div>

- (الف) **۴** برگ.
- (ب) **گروه (A,B)**: C با نیای مشترک A و B خواهر است، نه با یکی از آن‌ها به‌تنهایی. هیچ تک‌برگی «نزدیک‌ترین» C نیست؛ A و B هر دو به یک اندازه به C نزدیک‌اند.
- (ج) A ← نیای (A,B): ۱؛ ← نیای ((A,B),C): ۱؛ ← ریشه: ۱؛ ریشه ← D: ۳. روی‌هم **۶**.

---

## پاسخ ۸ (فکری): «DESeq2 گفت تغییر نکرده»

<div dir="ltr">

```bash
grep -w ybiB ~/r_practice/deseq2/missed.tsv
```

</div>

<div dir="ltr">

```text
b0800	ybiB	-2.37	5.589	-2.595	0.166
```

</div>

پاسخ به همکار: ybiB در واقع (در این شبیه‌سازی) **۵ برابر کاهش** یافته بود (‎−2.37) و DESeq2 حتی اندازه‌ی تغییر را درست برآورد کرد (‎−2.6). ولی `baseMean` آن تنها **۵٫۶** رید است: با این چند رید، نوسان تصادفی آن‌قدر بزرگ است که DESeq2 نمی‌تواند مطمئن باشد. **«معنادار نبود» یعنی «شواهد کافی نبود»، نه «تغییر نکرد».**

دو راه برای آزمایش بعدی:
1. **تکرار زیستی بیشتر** (برای نمونه ۵ یا ۶ به‌جای ۳): برآورد نوسان طبیعی دقیق‌تر می‌شود.
2. **توالی‌یابی عمیق‌تر** (رید بیشتر در هر نمونه): ژن‌های کم‌بیان شمار رید بیشتری می‌گیرند و به سمت راست نمودار MA می‌روند، جایی که تغییرها قابل اعتمادترند.

</div>
