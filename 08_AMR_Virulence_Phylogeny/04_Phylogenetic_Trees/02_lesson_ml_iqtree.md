<div dir="rtl">

# درس ۲: درخت maximum likelihood با IQ-TREE، و بازترکیبی

**بخش:** `08_AMR_Virulence_Phylogeny` · **ماژول:** `04_Phylogenetic_Trees` · **پیش‌نیاز:** [درس ۱](01_lesson_msa_nj.md) · **زمان:** حدود ۴۵ دقیقه · **ابزار (از مستندات):** IQ-TREE 3.1.4 (بسته‌ی Bioconda با دستورهای `iqtree` و `iqtree3`)، Gubbins، iTOL · **آخرین بازبینی:** 2026-10-24

> ✍️ **وضعیت: نوشته‌شده، اجرا نشده.** ‏IQ-TREE و Gubbins روی سرور ما نصب نیستند و سرور به conda دسترسی ندارد. دستورها، نام گزینه‌ها و نام فایل‌های خروجی از مستند رسمی (IQ-TREE Tutorial و FAQ، راهنمای Gubbins) آمده‌اند و منبعشان کنار هر کدام نوشته شده. IQ-TREE روی هم‌ردیفی‌های این ماژول سبک است (چند ثانیه تا یکی‌دو دقیقه)؛ اجرای آن تمرین ۶ است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. فرق روش فاصله‌ای (NJ) و maximum likelihood (ML) را بگویید.
2. ‏ModelFinder را برای برگزیدن مدل جایگزینی به کار ببرید و نام مدل (مانند `TN+F+G4`) را بخوانید.
3. ‏UFBoot و SH-aLRT را اجرا و با آستانه‌های درست تفسیر کنید.
4. بدانید چرا برای هم‌ردیفی SNP-تنها باید `+ASC` بدهید.
5. بگویید بازترکیبی چگونه درخت باکتری را به هم می‌ریزد و Gubbins چه می‌کند.

---

## ۱. داستان

درخت NJ درس ۱ گروه‌های CTX-M را درست نشان داد، ولی یک طول شاخه‌ی منفی داشت و گره‌های ژرفش ضعیف بودند. داوران یک مجله در بسیاری از موارد می‌پرسند: «چرا ML نه؟» در این درس روش استاندارد امروز را می‌بینید: ‏**IQ-TREE** با انتخاب خودکار مدل و پشتیبانی سریع.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏NJ در برابر ML

| | ‏NJ (درس ۱) | ML |
| :--- | :--- | :--- |
| ورودی | ماتریس فاصله (هر جفت یک عدد) | خود هم‌ردیفی، ستون‌به‌ستون |
| پرسش | کدام درخت با این فاصله‌ها جور است؟ | **کدام درخت و کدام مدل، احتمال دیدن این داده را بیشینه می‌کنند؟** |
| سرعت | بسیار سریع | کندتر (جست‌وجو میان درخت‌ها) |
| طول شاخه‌ی منفی | ممکن | نه |

**تشبیه:** ‏NJ مانند ساختن شجره‌نامه‌ی یک خانواده تنها از روی «چقدر شبیه هم‌اند» است. ML مانند این است که برای هر شجره‌نامه‌ی ممکن بپرسیم: «اگر این شجره درست بود، چقدر احتمال داشت دقیقاً همین چهره‌ها را ببینیم؟» و شجره‌ای را برگزینیم که بیشترین احتمال را دارد.

### ۲.۲ نام مدل‌ها در IQ-TREE

‏IQ-TREE مدل را با یک نام چندتکه می‌نویسد. برای نمونه `TN+F+G4`:

| تکه | معنا |
| :--- | :--- |
| ‏`TN` (یا `HKY`، `GTR`، `K2P`، `JC`) | مدل جایگزینی پایه (TN همان TN93 درس ۱ است) |
| ‏`+F` | فراوانی بازها از داده برآورد می‌شود |
| ‏`+G4` | سرعت تکامل در جایگاه‌های گوناگون فرق دارد (توزیع گاما با ۴ رده) |
| ‏`+I` | بخشی از جایگاه‌ها هرگز تغییر نمی‌کنند |
| ‏`+R` | مدل سرعت آزادتر از گاما (FreeRate) |
| ‏`+ASC` | تصحیح برای هم‌ردیفی‌ای که **تنها** جایگاه‌های متغیر دارد (بخش ۴) |

‏**ModelFinder** (`-m MFP`) ده‌ها مدل را می‌آزماید و بهترین را با معیار اطلاعاتی برمی‌گزیند (پیش‌فرض: BIC)، سپس درخت را با همان مدل می‌سازد.

### ‏۲.۳ ‏UFBoot و SH-aLRT

‏bootstrap معمولی (درس ۱) برای ML کند است: ۱۰۰۰ بار ساختن کامل درخت. IQ-TREE دو روش سریع دارد:

- ‏**UFBoot** (ultrafast bootstrap، `-B 1000`): به گفته‌ی Tutorial، ۱۰۰۰ کمترین شمار پیشنهادی است.
- ‏**SH-aLRT** (`-alrt 1000`): یک آزمون آماری برای هر شاخه.

**آستانه‌ها با bootstrap معمولی فرق دارند.** به گفته‌ی FAQ رسمی IQ-TREE: «برای UFBoot تنها از ۹۵٪ به بالا به یک شاخه اعتماد کنید» و «اگر SH-aLRT ≥ ۸۰٪ و UFBoot ≥ ۹۵٪ باشد، اطمینان بیشتری هست». پس UFBoot برابر ۸۰ **ضعیف** است، در حالی که bootstrap معمولی ۸۰ را در بسیاری از موارد «خوب» می‌خوانند.

> 📺 **فیلم:** *IQ-TREE Tutorial* (برای مبتدی، IQ-TREE 2 و 3): https://www.youtube.com/watch?v=It72loV3Fs8 · *IQTree Tutorial – Beginner*: https://www.youtube.com/watch?v=jvVJLemaQl8
> 📄 **مرجع:** Minh BQ, et al. (2020). *IQ-TREE 2: new models and efficient methods for phylogenetic inference in the genomic era.* Molecular Biology and Evolution 37:1530–1534. https://doi.org/10.1093/molbev/msaa015 · Kalyaanamoorthy S, et al. (2017). *ModelFinder: fast model selection for accurate phylogenetic estimates.* Nature Methods 14:587–589. https://doi.org/10.1038/nmeth.4285 · Hoang DT, et al. (2018). *UFBoot2: improving the ultrafast bootstrap approximation.* Mol Biol Evol 35:518–522. https://doi.org/10.1093/molbev/msx281

---

## ۳. گام‌به‌گام: IQ-TREE روی هم‌ردیفی CTX-M (از مستندات)

<div dir="ltr">

```bash
conda activate phylo
cd ~/phylo
iqtree -s ctxm_aln.fna -m MFP -B 1000 -alrt 1000 -T AUTO --prefix ctxm_ml
```

</div>

| گزینه | کار |
| :--- | :--- |
| ‏`-s` | فایل هم‌ردیفی |
| ‏`-m MFP` | ‏ModelFinder Plus: برگزیدن مدل و سپس ساختن درخت |
| ‏`-B 1000` | ‏۱۰۰۰ تکرار UFBoot |
| ‏`-alrt 1000` | ‏۱۰۰۰ تکرار SH-aLRT |
| ‏`-T AUTO` | شمار هسته‌ها را خودش برمی‌گزیند |
| ‏`--prefix ctxm_ml` | پیشوند همه‌ی فایل‌های خروجی |

**فایل‌های خروجی** (از IQ-TREE Tutorial):

| فایل | چه دارد |
| :--- | :--- |
| ‏`ctxm_ml.iqtree` | گزارش اصلی و خواندنی: مدل برگزیده، پارامترها، درخت متنی |
| ‏`ctxm_ml.treefile` | درخت ML در قالب Newick؛ برچسب گره‌ها `SH-aLRT/UFBoot` است، برای نمونه `98.5/100` |
| ‏`ctxm_ml.contree` | درخت توافقی bootstrap، با پشتیبانی‌ها |
| ‏`ctxm_ml.log` | گزارش کامل اجرا (همان که روی صفحه می‌آید) |

**چه چیزی را بخوانید (اجرا نشده):** در `ctxm_ml.iqtree`، سطر «Best-fit model according to BIC» مدل برگزیده را می‌گوید. درخت را با درخت NJ درس ۱ بسنجید: پنج گروه CTX-M باید باز هم پشتیبانی بالا بگیرند؛ ببینید آیا گره‌های ژرف (۳۴ و ۴۷ در NJ) در ML با UFBoot ≥ ۹۵ پشتیبانی می‌شوند یا نه. هیچ عددی را از پیش نمی‌گوییم؛ این تمرین ۶ است.

**دیدن درخت:** فایل `.treefile` را در **iTOL** (https://itol.embl.de، بارگذاری از راه مرورگر) یا با `ggtree` در R باز کنید. برچسب‌های `SH-aLRT/UFBoot` را می‌توان در iTOL به‌صورت عدد روی شاخه‌ها نشان داد.

---

## ۴. هم‌ردیفی SNP-تنها و `+ASC`

در درس ۳ هم‌ردیفی کامل یک ژنوم را به **تنها جایگاه‌های متغیر** (SNPها) کوتاه می‌کنیم؛ ابزارهایی مانند Snippy (فایل `core.aln`، ماژول 07/05) و snp-sites هم همین را می‌دهند. ولی مدل ML فرض می‌کند بیشتر جایگاه‌ها **ثابت**‌اند. اگر همه‌ی جایگاه‌های ثابت را برداریم و به مدل نگوییم، مدل گمان می‌کند تکامل بسیار سریع بوده و **طول شاخه‌ها را بیش از اندازه** برآورد می‌کند.

دو راه درست:

<div dir="ltr">

```bash
# 1) tell the model that only variable sites are present
iqtree -s outbreak_nj_snps.fasta -m MFP+ASC -B 1000 -alrt 1000 --prefix outbreak_ml
# 2) or give the full alignment (constant sites included)
iqtree -s outbreak/core_full.aln -m MFP -B 1000 -alrt 1000 --prefix outbreak_ml_full
```

</div>

به گفته‌ی FAQ رسمی، اگر هم‌ردیفی جایگاه ثابتی داشته باشد، مدل `+ASC` نمی‌تواند به کار رود؛ IQ-TREE در این حالت یک فایل با پسوند `.varsites` می‌نویسد که تنها جایگاه‌های متغیر را دارد، و می‌توان همان را دوباره به `-s` داد.

> 📄 **مرجع:** IQ-TREE FAQ (UFBoot، SH-aLRT، `+ASC`): https://iqtree.github.io/doc/Frequently-Asked-Questions · IQ-TREE Tutorial: https://iqtree.github.io/doc/Tutorial

<details>
<summary>✋ امتحان کن: همکارتان core.aln (تنها SNPها) را بی <code>+ASC</code> به IQ-TREE داده و می‌گوید «درخت درست است، تنها شاخه‌ها کمی بلندند». آیا مشکلی هست؟</summary>

بله. شکل درخت (topology) شاید درست باشد، ولی **طول شاخه‌ها** نادرست است. اگر آن‌ها را به «شمار SNP» برگردانید یا برای تخمین زمان (molecular clock) به کار ببرید، نتیجه اشتباه می‌شود. با `+ASC` یا با هم‌ردیفی کامل دوباره اجرا کنید.

</details>

---

## ۵. بازترکیبی (recombination) و Gubbins

باکتری‌ها گاهی تکه‌ای از DNA یک سویه‌ی **دیگر** را جایگزین DNA خود می‌کنند (بازترکیبی همولوگ). یک رویداد بازترکیبی می‌تواند ده‌ها SNP را **یک‌جا** وارد کند؛ SNPهایی که از جهش‌های تدریجی نیامده‌اند. نتیجه:

- شاخه‌ی آن سویه **بلندتر** از واقعیت می‌شود (دو سویه‌ی خویشاوند دور به نظر می‌رسند).
- گاهی شکل درخت هم عوض می‌شود.

<div dir="ltr">

```
ژنوم:   ───────────[ ناحیه‌ی بازترکیب: ۴۰ SNP ]──────────── ۲ SNP پراکنده
بی Gubbins:  این سویه ۴۲ SNP با بقیه فاصله دارد  ← «خویشاوند نیست»
با Gubbins:  ناحیه کنار گذاشته می‌شود، ۲ SNP     ← «همان شیوع است»
```

</div>

‏**Gubbins** نواحی‌ای را پیدا می‌کند که SNPهایشان **بسیار متراکم**‌اند، آن‌ها را بازترکیب می‌شمارد و کنار می‌گذارد، و درخت را با SNPهای باقی‌مانده دوباره می‌سازد (چند دور). ورودی آن **هم‌ردیفی کامل** است (مانند `core.full.aln` در Snippy یا `core_full.aln` درس ۳)، نه SNP-تنها؛ چون برای دیدن تراکم، فاصله‌ی SNPها لازم است.

<div dir="ltr">

```bash
conda create -n gubbins -c conda-forge -c bioconda gubbins
conda activate gubbins
run_gubbins.py --prefix gubbins_out outbreak/core_full.aln
```

</div>

**خروجی‌ها** (راهنمای Gubbins):

| فایل | چه دارد |
| :--- | :--- |
| ‏`gubbins_out.recombination_predictions.gff` | نواحی بازترکیب، با قالب GFF |
| ‏`gubbins_out.final_tree.tre` | درخت نهایی؛ **طول شاخه‌ها به شمار جهش نقطه‌ای** |
| ‏`gubbins_out.filtered_polymorphic_sites.fasta` | ‏SNPهای باقی‌مانده پس از کنار گذاشتن بازترکیب |
| ‏`gubbins_out.per_branch_statistics.csv` | برای هر شاخه، از جمله **r/m**: نسبت اثر بازترکیبی به جهش |

راهنمای Gubbins پیشنهاد می‌کند برای نخستین درخت یک روش سریع (`--first-tree-builder`، مانند `rapidnj` یا `fasttree`) و برای دورهای بعد یک روش ML (`--tree-builder iqtree` یا `raxmlng`) به کار رود.

**پیش‌بینی برای داده‌ی درس ۳ (اجرا نشده):** شبیه‌سازی ما **هیچ** بازترکیبی ندارد (هر SNP یک جهش جدا در یک جایگاه تازه است). پس انتظار داریم Gubbins ناحیه‌ی بازترکیبی نیابد یا بسیار کم بیابد. این یک کنترل منفی خوب است.

> 📺 **فیلم:** *IQ-TREE 2* (درس دانشگاهی، استنباط درخت): https://www.youtube.com/watch?v=MHMLguBQKZU
> 📄 **مرجع:** Croucher NJ, et al. (2015). *Rapid phylogenetic analysis of large samples of recombinant bacterial whole genome sequences using Gubbins.* Nucleic Acids Research 43:e15. https://doi.org/10.1093/nar/gku1196 · راهنمای Gubbins: https://github.com/nickjcroucher/gubbins/blob/master/docs/gubbins_manual.md · iTOL: Letunic I, Bork P (2024). *Interactive Tree of Life (iTOL) v6.* Nucleic Acids Research 52:W78–W82. https://doi.org/10.1093/nar/gkae268

---

## ۶. سه اشتباه رایج

1. **خواندن UFBoot مانند bootstrap معمولی.** ‏UFBoot برابر ۸۵ ضعیف است؛ آستانه ۹۵ است (و SH-aLRT ‏۸۰).
2. ‏**SNP-تنها بی `+ASC`.** طول شاخه‌ها بیش از اندازه برآورد می‌شود.
3. **نادیده گرفتن بازترکیبی در گونه‌های پربازترکیب.** در گونه‌هایی مانند *Streptococcus pneumoniae* بازترکیبی بسیار است؛ بی Gubbins، فاصله‌ی SNP و درخت گمراه‌کننده می‌شوند. در *E. coli* و *K. pneumoniae* هم نواحی بازترکیب بزرگ (برای نمونه پیرامون ژن‌های کپسول) دیده می‌شود.

---

## جمع‌بندی

- ‏ML درختی را برمی‌گزیند که احتمال داده را بیشینه کند؛ IQ-TREE با `-m MFP` مدل را هم خودش برمی‌گزیند.
- ‏UFBoot (`-B 1000`) و SH-aLRT (`-alrt 1000`): به یک شاخه با UFBoot ≥ ۹۵ و SH-aLRT ≥ ۸۰ اعتماد کنید.
- هم‌ردیفی SNP-تنها `+ASC` می‌خواهد، یا هم‌ردیفی کامل را بدهید.
- بازترکیبی SNPهای متراکم وارد می‌کند؛ Gubbins آن‌ها را از هم‌ردیفی کامل پیدا و کنار می‌گذارد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
iqtree -s ALN.fasta -m MFP -B 1000 -alrt 1000 -T AUTO --prefix NAME       # full alignment
iqtree -s SNPS.fasta -m MFP+ASC -B 1000 -alrt 1000 -T AUTO --prefix NAME   # variable sites only
run_gubbins.py --prefix gubbins_out core_full.aln                         # recombination
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏maximum likelihood (ML) | برگزیدن درختی که احتمال دیدن داده را بیشینه کند |
| ‏ModelFinder | ابزار IQ-TREE برای برگزیدن بهترین مدل جایگزینی |
| ‏BIC | معیاری برای سنجیدن مدل‌ها که پیچیدگی بیشتر را جریمه می‌کند |
| ‏UFBoot / SH-aLRT | دو روش سریع سنجیدن پشتیبانی شاخه در IQ-TREE |
| ‏ascertainment bias (`+ASC`) | خطایی که از برداشتن جایگاه‌های ثابت پدید می‌آید، و تصحیح آن |
| بازترکیبی همولوگ | جایگزینی تکه‌ای از DNA با تکه‌ی هم‌ریشه از سویه‌ی دیگر |
| ‏r/m | نسبت جایگزینی‌های آمده از بازترکیبی به جایگزینی‌های آمده از جهش |
| ‏iTOL | ابزار وب برای نمایش و آراستن درخت |

---

## منابع

**مستند و مقاله**
- Minh BQ, et al. (2020). *IQ-TREE 2.* Mol Biol Evol 37:1530–1534. https://doi.org/10.1093/molbev/msaa015 · IQ-TREE Tutorial: https://iqtree.github.io/doc/Tutorial · FAQ: https://iqtree.github.io/doc/Frequently-Asked-Questions
- Kalyaanamoorthy S, et al. (2017). *ModelFinder.* Nature Methods 14:587–589. https://doi.org/10.1038/nmeth.4285
- Hoang DT, et al. (2018). *UFBoot2.* Mol Biol Evol 35:518–522. https://doi.org/10.1093/molbev/msx281
- Croucher NJ, et al. (2015). *Gubbins.* Nucleic Acids Res 43:e15. https://doi.org/10.1093/nar/gku1196 · manual: https://github.com/nickjcroucher/gubbins/blob/master/docs/gubbins_manual.md
- Letunic I, Bork P (2024). *iTOL v6.* Nucleic Acids Res 52:W78–W82. https://doi.org/10.1093/nar/gkae268

**کتاب**
- ‏Yang Z (2014). *Molecular Evolution: A Statistical Approach*. Oxford University Press. (فصل‌های مدل جایگزینی و درست‌نمایی بیشینه)
- Felsenstein J (2004). *Inferring Phylogenies*. Sinauer.

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Molecular Evolution (Bioinformatics IV)* (UC San Diego): https://www.coursera.org/learn/molecularevolution
- ‏edX: *Essentials of Genomics and Biomedical Informatics* (IsraelX): https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics
- ‏YouTube: *IQ-TREE Tutorial*: https://www.youtube.com/watch?v=It72loV3Fs8
- ‏YouTube: *IQTree Tutorial – Beginner*: https://www.youtube.com/watch?v=jvVJLemaQl8
- ‏YouTube: *IQ-TREE 2* (BIO 450): https://www.youtube.com/watch?v=MHMLguBQKZU

<sub>گزینه‌ها و فایل‌های IQ-TREE از Tutorial و FAQ رسمی، نسخه‌ی بسته‌ی Bioconda (3.1.4، دستورهای `iqtree` و `iqtree3`) از اسکریپت ساخت آن (`build.sh`) در bioconda-recipes، و خروجی‌های Gubbins از راهنمای رسمی، همه در 2026-10-24 خوانده شدند. نشانی‌های فیلم در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
