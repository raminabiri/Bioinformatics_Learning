<div dir="rtl">

# درس ۲: ساختار پیش‌بینی‌شده؛ AlphaFold، pLDDT و سنجیدن مدل با آزمایش

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `01_Protein_Structure` · **پیش‌نیاز:** [درس ۱](01_lesson_pdb.md) · **زمان:** حدود ۵۰ دقیقه · **ابزار:** gemmi 0.7.5؛ AlphaFold DB؛ ColabFold و AlphaFold Server از مستندات · **آخرین بازبینی:** 2026-10-24

> **وضعیت:** بخش‌های ۳ و ۴ ✅ اجرا شده‌اند (۰٫۲ ثانیه، ۱۳۵ مگابایت). ساختن مدل تازه با ColabFold یا AlphaFold 3 (بخش ۵) ✍️ از مستندات است: به GPU نیاز دارد.
>
> **یک نکته‌ی فنی:** سایت AlphaFold DB و نسخه‌ی آن در Google Cloud در 2026-10-24 به سرور ما پاسخ ندادند (خطای 403؛ Google پیام «در منطقه‌ی شما در دسترس نیست» داد). همان مدل (AF-P0A8V2-F1) را از **RCSB** گرفتیم، که مدل‌های AlphaFold DB را با پروانه‌ی CC-BY 4.0 بازپخش می‌کند. میانگین pLDDT آن (۹۰٫۰۵) با عددی که RCSB برای این مدل گزارش می‌کند یکی است. شما مدل را از خود AlphaFold DB بگیرید (گام ۱)؛ نسخه‌ی ما هم در `99_scripts_data/data/` هست.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید AlphaFold از کجا ساختار را «حدس» می‌زند و چه چیزی را نمی‌داند.
2. ‏**pLDDT** (اطمینان هر باقی‌مانده) و **PAE** (اطمینان جای نسبی دو بخش) را تفسیر کنید.
3. یک مدل AlphaFold را روی ساختار تجربی هم‌پوشانی (superpose) کنید و **RMSD** را بخوانید.
4. بگویید کِی یک مدل پیش‌بینی‌شده برای کار با دارو (داکینگ) بس است و کِی نه.

<div dir="ltr">

```bash
conda activate structural
cd ~/struct
P=~/Bioinformatics_Learning-main/09_Structural_Bioinformatics/99_scripts_data
```

</div>

---

## ۱. داستان

برای RpoB *E. coli* ساختار تجربی داریم. ولی فرض کنید روی یک باکتری کم‌مطالعه کار می‌کنید و ساختار RpoB آن در PDB نیست. آیا می‌توان به یک مدل پیش‌بینی‌شده اعتماد کرد؟ برای پاسخ، مدل AlphaFold همان RpoB *E. coli* را با ساختار تجربی درس ۱ می‌سنجیم؛ جایی که پاسخ درست را داریم.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏AlphaFold چه می‌کند؟

‏**AlphaFold 2** (DeepMind، ۲۰۲۱) یک شبکه‌ی عصبی است که از **توالی** پروتئین و **هم‌ردیفی توالی‌های خویشاوند** (MSA؛ ماژول 08/04) جای همه‌ی اتم‌ها را پیش‌بینی می‌کند. منطق MSA: اگر دو اسید آمینه در طول تکامل **با هم** تغییر کرده‌اند، به احتمال زیاد در ساختار کنار هم‌اند. شبکه با ساختارهای PDB آموزش دیده است.

- ‏**AlphaFold DB** (EMBL-EBI و DeepMind) مدل‌های از پیش ساخته‌شده‌ی بیش از ۲۰۰ میلیون پروتئین را دارد. نام هر مدل: `AF-<UniProt>-F1`.
- ‏**AlphaFold 3** (۲۰۲۴) کمپلکس با DNA، RNA، یون و مولکول کوچک را هم پیش‌بینی می‌کند (از راه AlphaFold Server).
- ‏**ColabFold** نسخه‌ی سریع‌تر و آزاد AlphaFold 2 است.

**آنچه AlphaFold نمی‌داند:** یک مدل ایستا می‌دهد، نه حرکت؛ در AlphaFold 2 لیگاند نیست؛ و اثر یک جهش نقطه‌ای را در بسیاری از موارد درست پیش‌بینی نمی‌کند.

### ‏۲.۲ ‏pLDDT و PAE

| معیار | پرسش | کجا ذخیره می‌شود |
| :--- | :--- | :--- |
| ‏**pLDDT** (۰ تا ۱۰۰) | «جای **این** باقی‌مانده نسبت به همسایه‌هایش چقدر درست است؟» | ستون B-factor فایل مدل |
| ‏**PAE** (به Å) | «اگر مدل را روی باقی‌مانده‌ی i هم‌پوشانی کنم، جای باقی‌مانده‌ی j چقدر خطا دارد؟» | یک فایل JSON جدا (ماتریس) |

رده‌های pLDDT (طبق مقاله‌ی AlphaFold DB): **بیش از ۹۰** بسیار بالا، **۷۰ تا ۹۰** مطمئن، **۵۰ تا ۷۰** کم، **کمتر از ۵۰** بسیار کم (در بسیاری از موارد ناحیه‌ی بی‌نظم). **PAE** برای پروتئین‌های چنددامنه‌ای مهم است: هر دامنه شاید pLDDT بالا داشته باشد، ولی **زاویه‌ی میان دو دامنه** نامطمئن باشد. pLDDT این را نشان نمی‌دهد و PAE نشان می‌دهد.

> 📺 **فیلم:** *AlphaFold: The making of a scientific breakthrough* (DeepMind): https://www.youtube.com/watch?v=gg7WjuFs8F4 · *Evaluating Predictions: pLDDT and PAE*: https://www.youtube.com/watch?v=dXc00b2Tb0Q
> 📄 **مرجع:** Jumper J, et al. (2021). *Highly accurate protein structure prediction with AlphaFold.* Nature 596:583–589. https://doi.org/10.1038/s41586-021-03819-2 · Varadi M, et al. (2022). *AlphaFold Protein Structure Database: massively expanding the structural coverage of protein-sequence space with high-accuracy models.* Nucleic Acids Research 50:D439–D444. https://doi.org/10.1093/nar/gkab1061

---

## ۳. گام ۱: گرفتن مدل و خواندن pLDDT

صفحه‌ی مدل را باز کنید: https://alphafold.ebi.ac.uk/entry/P0A8V2 (همان صفحه‌ای که در ماژول 00/02 دیدید)، فایل **PDB** را دانلود کنید و نامش را `AF-P0A8V2-F1.pdb` بگذارید. اگر دانلود نشد، نسخه‌ی همراه دوره را به کار ببرید:

<div dir="ltr">

```bash
zcat $P/data/AF-P0A8V2-F1_from_RCSB-CSM.pdb.gz > AF-P0A8V2-F1.pdb
grep -m3 "^ATOM" AF-P0A8V2-F1.pdb
```

</div>

**خروجی واقعی** (از نسخه‌ی همراه دوره؛ فایل خود AlphaFold DB سرآیند بلندتری دارد ولی سطرهای ATOM همین قالب را دارند):

<div dir="ltr">

```
ATOM      1  N   MET A   1     -32.816  20.068 -14.273  1.00 46.72           N
ATOM      2  CA  MET A   1     -32.742  18.981 -13.276  1.00 46.72           C
ATOM      3  C   MET A   1     -33.960  19.104 -12.379  1.00 46.72           C
```

</div>

ستون پیش از نام عنصر، در ساختار تجربی B-factor بود؛ **در مدل AlphaFold همان‌جا pLDDT است**: ‏`46.72` برای Met1، یعنی «بسیار کم». همه‌ی اتم‌های یک باقی‌مانده یک pLDDT دارند.

---

## ۴. گام ۲: سنجیدن مدل با ساختار تجربی

اسکریپت `af_compare.py`:
1. رده‌های pLDDT را می‌شمارد،
2. کربن‌های آلفای باقی‌مانده‌های مشترک (با شماره‌ی یکسان) را برمی‌دارد و با `gemmi.superpose_positions` مدل را روی ساختار تجربی **هم‌پوشانی** می‌کند (چرخش و جابه‌جایی‌ای که کمترین فاصله را بدهد)،
3. ‏**RMSD** (ریشه‌ی میانگین مربع فاصله‌ها) را گزارش می‌کند،
4. و برای باقی‌مانده‌هایی که می‌دهید (این‌جا ۱۴ باقی‌مانده‌ی جایگاه ریفامپیسین از درس ۱)، pLDDT و فاصله‌ی کربن آلفا پس از هم‌پوشانی را چاپ می‌کند.

<div dir="ltr">

```bash
python3 $P/01_Protein_Structure/scripts/af_compare.py AF-P0A8V2-F1.pdb 5UAC.cif.gz C \
    509,510,512,513,514,516,526,529,531,533,540,564,572,687
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
model residues: 1342  mean pLDDT: 90.1
  very high (>90)      846  (63.0%)
  confident (70-90)    474  (35.3%)
  low (50-70)           20  (1.5%)
  very low (<50)         2  (0.1%)
common residues: 1342  CA RMSD after superposition: 1.39 A
residue  pLDDT  CA distance after superposition (A)
    509   92.0  0.47
    510   91.6  0.64
    512   95.3  0.71
    513   94.1  1.38
    514   93.4  1.27
    516   90.2  0.59
    526   95.4  0.53
    529   95.2  0.75
    531   95.1  0.35
    533   92.7  0.50
    540   88.1  0.72
    564   93.2  0.58
    572   95.2  0.76
    687   95.4  0.51
```

</div>

**توضیح خروجی:**

1. **۹۸٪ باقی‌مانده‌ها pLDDT بالای ۷۰ دارند.** تنها ۲۲ باقی‌مانده زیر ۷۰‌اند: دو سر زنجیره (Met1 با ۴۶٫۷ و Glu1342 با ۴۰٫۹) و دو حلقه‌ی کوتاه پیرامون ۷۴۳ تا ۷۴۶ و ۸۹۲ تا ۹۱۱. دو سر زنجیره در بیشتر پروتئین‌ها انعطاف‌پذیرند.
2. ‏**RMSD کربن آلفا ۱٫۳۹ Å** روی همه‌ی ۱۳۴۲ باقی‌مانده. برای پروتئینی با این اندازه، این یعنی مدل و آزمایش کمابیش یکی‌اند. بخشی از همین ۱٫۳۹ Å هم از خود ساختار تجربی است: وضوح آن ۳٫۸ Å بود.
3. **همه‌ی باقی‌مانده‌های جایگاه pLDDT ≥ ۸۸** دارند و کربن آلفای آن‌ها پس از هم‌پوشانی کمتر از ۱٫۴ Å با آزمایش فاصله دارد. پس برای این پروتئین، **شکل جایگاه ریفامپیسین در مدل قابل اعتماد است**.
4. **یک هشدار:** AlphaFold با ساختارهای PDB آموزش دیده و ساختارهای RNAP باکتری‌ها هم در آن بوده‌اند. پس این هم‌خوانی بالا برای یک پروتئین **کم‌مطالعه** تضمین نمی‌شود؛ آنجا pLDDT و PAE را با دقت بیشتری بخوانید.
5. ما تنها کربن آلفا را سنجیدیم (زنجیره‌ی اصلی). جای **زنجیره‌های جانبی** در جایگاه، برای داکینگ مهم‌تر است و در مدل‌ها نامطمئن‌تر.

<details>
<summary>✋ امتحان کن: چرا اسکریپت باقی‌مانده‌ها را با «شماره» جفت می‌کند؟ در چه حالتی این کار نادرست است؟</summary>

چون هم مدل AlphaFold و هم زنجیره‌ی C ساختار 5UAC از Met1 پروتئین *E. coli* شماره‌گذاری شده‌اند، شماره‌ی یکسان یعنی اسید آمینه‌ی یکسان. اگر یک ساختار شماره‌گذاری دیگری داشته باشد (برای نمونه RpoB *M. tuberculosis* که S531 در آن S450 است، یا ساختاری که از یک برچسب His شماره‌گذاری شده)، باید نخست توالی‌ها را هم‌ردیف کرد (ماژول 08/04) و جفت‌ها را از روی هم‌ردیفی برداشت.

</details>

> 📺 **فیلم:** *AlphaFold Protein Structure Database* (معرفی پایگاه): https://www.youtube.com/watch?v=Gk-PyJSNlcI · *Exploring Computed Structure Models on RCSB.org*: https://www.youtube.com/watch?v=QJv7kMqqSgo
> 📄 **مرجع:** Varadi M, et al. (2024). *AlphaFold Protein Structure Database in 2024: providing structure coverage for over 214 million protein sequences.* Nucleic Acids Research 52:D368–D375. https://doi.org/10.1093/nar/gkad1011

---

## ۵. ساختن یک مدل تازه (از مستندات)

اگر پروتئین شما در AlphaFold DB نیست (برای نمونه یک پروتئین جهش‌یافته یا کمپلکس):

- ‏**ColabFold** در مرورگر (Google Colab، با GPU رایگان): دفترچه‌ی `AlphaFold2.ipynb` در https://github.com/sokrypton/ColabFold؛ یا روی کامپیوتر با GPU (نصب با LocalColabFold):

<div dir="ltr">

```bash
colabfold_batch input_sequences.fasta out_dir
```

</div>

  خروجی: چند مدل رده‌بندی‌شده، با pLDDT در B-factor و یک فایل JSON برای PAE هر مدل.
- ‏**AlphaFold Server** (https://alphafoldserver.com): نسخه‌ی وب AlphaFold 3، برای کمپلکس پروتئین با DNA، RNA، یون و لیگاند؛ نیاز به حساب Google.
- ‏**SWISS-MODEL** (https://swissmodel.expasy.org): مدل‌سازی **هومولوژی**؛ ساختار یک پروتئین خویشاوند را الگو می‌گیرد. سریع است و منبع الگو را آشکارا می‌گوید.

> 📺 **فیلم:** *Molecular Dynamics Simulation Using Free GPU on Google Colab* (کار با Colab و GPU، همان محیط ColabFold): https://www.youtube.com/watch?v=F-SsbOw2YrM
> 📄 **مرجع:** Mirdita M, et al. (2022). *ColabFold: making protein folding accessible to all.* Nature Methods 19:679–682. https://doi.org/10.1038/s41592-022-01488-1 · Abramson J, et al. (2024). *Accurate structure prediction of biomolecular interactions with AlphaFold 3.* Nature 630:493–500. https://doi.org/10.1038/s41586-024-07487-w · Waterhouse A, et al. (2018). *SWISS-MODEL: homology modelling of protein structures and complexes.* Nucleic Acids Research 46:W296–W303. https://doi.org/10.1093/nar/gky427

---

## ۶. سه اشتباه رایج

1. **خواندن pLDDT به‌عنوان B-factor.** در مدل AlphaFold، عدد بزرگ‌تر یعنی **بهتر**؛ در ساختار تجربی، B-factor بزرگ‌تر یعنی **بدتر**.
2. **داکینگ در ناحیه‌ی pLDDT کم.** زیر ۷۰، جای زنجیره‌های جانبی (و گاهی زنجیره‌ی اصلی) نامطمئن است و نتیجه‌ی داکینگ بی‌معنا می‌شود.
3. **انتظار اینکه AlphaFold اثر جهش را نشان دهد.** مدل S531L با مدل وحشی کمابیش یکی می‌شود؛ AlphaFold برای پیش‌بینی ساختار تاخورده ساخته شده، نه برای سنجیدن پایداری یا اتصال.

---

## 📘 برای کنجکاوها

- ‏PAE را در صفحه‌ی هر مدل AlphaFold DB می‌توان دید (نمودار مربعی سبز). یک دامنه = مربع سبز تیره روی قطر؛ دو دامنه با جای نسبی نامطمئن = خانه‌های روشن بیرون از قطر.
- در ناحیه‌های pLDDT بسیار کم، AlphaFold در بسیاری از موارد «نوار» درازی می‌کشد؛ این شکل واقعی نیست، نشانه‌ی بی‌نظمی است.

---

## جمع‌بندی

- ‏AlphaFold از توالی و MSA ساختار را پیش‌بینی می‌کند؛ pLDDT در ستون B-factor است و PAE در فایل جدا.
- مدل RpoB: ‏۹۸٪ باقی‌مانده‌ها با pLDDT بالای ۷۰؛ ‏RMSD ‏۱٫۳۹ Å با ساختار تجربی؛ جایگاه ریفامپیسین با pLDDT ≥ ۸۸.
- برای پروتئین‌های کم‌مطالعه، هم‌خوانی این‌چنینی تضمین نیست؛ pLDDT و PAE را بخوانید.
- مدل تازه: ColabFold، AlphaFold Server یا SWISS-MODEL.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
grep -m3 "^ATOM" AF-XXXX-F1.pdb                                   # pLDDT is in the B-factor column
python3 af_compare.py MODEL.pdb EXPERIMENT.cif.gz CHAIN 516,526,531
colabfold_batch input_sequences.fasta out_dir                     # documented, needs a GPU
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| پیش‌بینی ساختار | به دست آوردن ساختار سه‌بعدی از توالی، بی آزمایش |
| ‏pLDDT | اطمینان AlphaFold به جای هر باقی‌مانده (۰ تا ۱۰۰) |
| ‏PAE | خطای برآوردشده‌ی جای نسبی دو باقی‌مانده (Å) |
| هم‌پوشانی (superposition) | چرخاندن و جابه‌جا کردن یک ساختار تا بیشترین هم‌خوانی با دیگری |
| ‏RMSD | ریشه‌ی میانگین مربع فاصله‌ی اتم‌های جفت‌شده (Å) |
| مدل‌سازی هومولوژی | ساختن مدل از روی ساختار یک پروتئین خویشاوند |
| ناحیه‌ی بی‌نظم | بخشی از پروتئین بی ساختار ثابت |

---

## منابع

**مقاله و مستند**
- Jumper J, et al. (2021). *Highly accurate protein structure prediction with AlphaFold.* Nature 596:583–589. https://doi.org/10.1038/s41586-021-03819-2
- Varadi M, et al. (2022). *AlphaFold Protein Structure Database.* Nucleic Acids Res 50:D439–D444. https://doi.org/10.1093/nar/gkab1061
- Varadi M, et al. (2024). *AlphaFold Protein Structure Database in 2024.* Nucleic Acids Res 52:D368–D375. https://doi.org/10.1093/nar/gkad1011
- Abramson J, et al. (2024). *AlphaFold 3.* Nature 630:493–500. https://doi.org/10.1038/s41586-024-07487-w
- Mirdita M, et al. (2022). *ColabFold.* Nature Methods 19:679–682. https://doi.org/10.1038/s41592-022-01488-1
- Waterhouse A, et al. (2018). *SWISS-MODEL.* Nucleic Acids Res 46:W296–W303. https://doi.org/10.1093/nar/gky427
- AlphaFold DB: https://alphafold.ebi.ac.uk · RCSB computed structure models: https://www.rcsb.org/docs/general-help/computed-structure-models-and-rcsborg

**کتاب**
- ‏Lesk AM (2016). *Introduction to Protein Science: Architecture, Function, and Genomics*, 3rd ed. Oxford University Press. (فصل‌های ساختار و پیش‌بینی ساختار)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل پیش‌بینی ساختار پروتئین)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Drug Discovery* (UC San Diego): https://www.coursera.org/learn/drug-discovery
- ‏edX: *Introduction to Drug Discovery* (EPFLx): https://www.edx.org/learn/biology-life-sciences/ecole-polytechnique-federale-de-lausanne-introduction-to-drug-discovery
- ‏YouTube: *AlphaFold: The making of a scientific breakthrough* (DeepMind): https://www.youtube.com/watch?v=gg7WjuFs8F4
- ‏YouTube: *Evaluating Predictions: pLDDT and PAE*: https://www.youtube.com/watch?v=dXc00b2Tb0Q
- ‏YouTube: *AlphaFold Protein Structure Database*: https://www.youtube.com/watch?v=Gk-PyJSNlcI

<sub>مدل از RCSB (`models.rcsb.org/AF_AFP0A8V2F1.bcif.gz`، منبع AlphaFoldDB) در 2026-10-24 گرفته و به PDB تبدیل شد؛ میانگین pLDDT آن با `rcsb_ma_qa_metric_global` (۹۰٫۰۵) یکی است. نشانی‌های فیلم از جست‌وجوی وب‌اند و در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
