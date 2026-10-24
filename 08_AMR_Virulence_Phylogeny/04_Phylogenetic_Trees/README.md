<div dir="rtl">

# ماژول ۰۴: درخت‌های فیلوژنتیک (Phylogenetics)

| | |
| :--- | :--- |
| **بخش** | `08_AMR_Virulence_Phylogeny` |
| **پیش‌نیاز** | ماژول‌های [۰۱](../01_AMR_Resistance_Genes/) تا [۰۳](../03_Mobile_Elements_CRISPR/)؛ اجرای اسکریپت R (بخش ۰۴) |
| **زمان تقریبی** | ۵ ساعت (۳ درس، نزدیک به ۲ ساعت و ۴۵ دقیقه، و تمرین‌ها) |
| **ابزار** | ‏MAFFT 7.525، R با ape 5.8.1 و ggtree 4.2.0 (اجرا شده)؛ IQ-TREE 3.1.4 و Gubbins (از مستندات) |
| **داده** | ‏۱۵ ژن بتالاکتاماز واقعی (۱۳ آلل CTX-M، ‏KLUC-1، ‏TEM-1) از پایگاه AMRFinderPlus؛ هم‌ردیفی core genome **شبیه‌سازی‌شده‌ی** ۲۰ ایزوله از سه بیمارستان با درخت درست معلوم (`simulate_outbreak.py`) |
| **وضعیت** | درس‌های ۱ و ۳ ✅ اجرا شده (2026-10-24)؛ درس ۲ (IQ-TREE، Gubbins) ✍️ از مستندات |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. هم‌ردیفی چندگانه بسازید و از آن درخت NJ با bootstrap و ریشه‌ی outgroup بسازید.
2. ‏ML را با IQ-TREE (ModelFinder، UFBoot، SH-aLRT، `+ASC`) اجرا و با آستانه‌های درست تفسیر کنید.
3. اثر بازترکیبی را بشناسید و بدانید Gubbins چه می‌کند.
4. درخت شیوع را با ماتریس SNP و metadata بسازید و تفسیر کنید.
5. به سناریوی ۱ ماژول 00/01 پاسخ دهید: آیا انتقال میان بیمارستان‌ها رخ داده است؟

## ترتیب مطالعه
1. ‏[01_lesson_msa_nj.md](01_lesson_msa_nj.md): درس ۱، MAFFT، فاصله، NJ، bootstrap، روی ژن‌های CTX-M.
2. ‏[02_lesson_ml_iqtree.md](02_lesson_ml_iqtree.md): درس ۲، ML با IQ-TREE و بازترکیبی با Gubbins.
3. ‏[03_lesson_outbreak_tree.md](03_lesson_outbreak_tree.md): درس ۳، درخت شیوع ۲۰ ایزوله با metadata.
4. ‏[04_exercises.md](04_exercises.md): ۸ تمرین؛ زیر عنوان هر تمرین راهنمایی آمده است.
5. ‏[05_solutions.md](05_solutions.md): پاسخ تشریحی.

## ورودی و خروجی
- **ورودی:** ‏`99_scripts_data/data/ctxm_alleles.fna`؛ داده‌ی ساخته‌شده با `99_scripts_data/04_Phylogenetic_Trees/scripts/simulate_outbreak.py`.
- **خروجی:** ‏`ctxm_aln.fna`، `ctxm_nj.nwk`/`.png`، `outbreak_nj_snp_dist.tsv`، `outbreak_nj.nwk`/`.png`.

</div>
