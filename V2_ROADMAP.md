<div dir="rtl">

# نقشه‌ی راه نسخه‌ی ۲ دوره

**تاریخ:** 2026-10-26 · **وضعیت:** طرح؛ هیچ درسی هنوز نوشته نشده است.

نسخه‌ی ۱ دوره بخش‌های **۰۰ تا ۰۹** است. نسخه‌ی ۲ از بخش **۱۱** آغاز می‌شود و نام همه‌ی پوشه‌هایش با `NN_V2_` آغاز می‌شود. طرح پیشین بخش ۱۰: ماژول‌های ۰۱، ۰۵ و ۰۶ در بخش‌های ۲۰ تا ۲۲ آمده‌اند؛ ماژول‌های ۰۲ تا ۰۴ (ریدهای بلند، واریانت انسانی، تک‌سلولی) به دوره‌های جدا رفته‌اند (پایین را ببینید) ([10_Advanced](10_Advanced/)).

## هدف نسخه‌ی ۲
1. **پایگاه‌های داده:** بیشتر پایگاه‌های NCBI و پایگاه‌های بزرگ جهانی، هر کدام با یک پرسش زیستی واقعی.
2. **اومیکس:** ترنسکریپتومیکس، تحلیل کارکردی و شبکه، تنظیم بیان (miRNA، عامل رونویسی)، پیوند ژن و دارو، اپی‌ژنومیکس، پروتئومیکس و متابولومیکس.
3. **هر چه نسخه‌ی ۱ به آن نرسید:** مرورگرهای ژنوم، اسمبلی متاژنوم، ژنومیکس جمعیت، Nextflow و HPC، یادگیری ماشین و مدل‌های زبانی.

## بخش‌ها

| بخش | عنوان | محور | ماژول |
| :---: | :--- | :--- | :---: |
| ۱۱ | [پایگاه‌های داده‌ی NCBI](11_V2_NCBI_Databases/) | ‏Entrez و EDirect، Gene و RefSeq، BioProject و SRA Toolkit، GEO، dbSNP و ClinVar، PubMed و PubTator، BLAST+ و Primer-BLAST، Pathogen Detection | ۸ |
| ۱۲ | [پایگاه‌ها و مرورگرهای ژنومی جهانی](12_V2_Global_Databases_Browsers/) | ‏Ensembl و BioMart، UCSC، IGV، InterPro و HMMER، GO و KEGG و Reactome، GTEx و TCGA و cBioPortal | ۶ |
| ۱۳ | [ترنسکریپتومیکس با RNA-seq](13_V2_RNAseq_Transcriptomics/) | طراحی، HISAT2 و STAR و Salmon، DESeq2 و edgeR، بازتولید یک مقاله، RNA-seq باکتری | ۵ |
| ۱۴ | [تحلیل کارکردی و شبکه](14_V2_Functional_Enrichment_Networks/) | ‏Enrichr، g:Profiler، GSEA، STRING، GeneMANIA، Cytoscape، NetworkAnalyst، WGCNA | ۴ |
| ۱۵ | [تنظیم بیان، miRNA و پیوند ژن و دارو](15_V2_Regulation_miRNA_Drug_Gene/) | ‏miRBase، miRTarBase، TargetScan، JASPAR، MEME، RegulonDB، DGIdb، DrugBank، PharmGKB | ۴ |
| ۱۶ | [اپی‌ژنومیکس](16_V2_Epigenomics/) | ‏ChIP-seq، ATAC-seq، متیلاسیون DNA | ۳ |
| ۱۷ | [پروتئومیکس، متابولومیکس و چنداومیکس](17_V2_Proteomics_Metabolomics_MultiOmics/) | ‏PRIDE، MetaboAnalyst، HMDB، MOFA2 | ۳ |
| ۱۸ | [اسمبلی متاژنوم، MAG و ویروم](18_V2_Metagenome_Assembly_Viromics/) | ‏MEGAHIT، MetaBAT2، GTDB-Tk، HUMAnN، geNomad | ۴ |
| ۱۹ | [ژنومیکس جمعیت و GWAS](19_V2_Population_Genomics_GWAS/) | ‏PLINK، ADMIXTURE، GWAS Catalog، pyseer | ۳ |
| ۲۰ | [گردش کار، کانتینر و HPC](20_V2_Workflows_Containers_HPC/) | ‏Docker، Apptainer، Nextflow، nf-core، SLURM | ۳ |
| ۲۱ | [یادگیری ماشین و مدل‌های زبانی پروتئین](21_V2_Machine_Learning_PLMs/) | ‏scikit-learn، PyTorch، ESM-2، ESMFold | ۳ |
| ۲۲ | [گردش کار هوشمند با مدل‌های زبانی](22_V2_AI_Pipelines_LLM/) | ‏API مدل‌های زبانی، Dify | ۲ |

**رشته‌ی مشترک:** رشته‌ی باکتریایی نسخه‌ی ۱ (*E. coli*، *rpoB*، مقاومت) ادامه می‌یابد. بیشتر ابزارهای اومیکس (Enrichr، DGIdb، miRNA) برای انسان ساخته شده‌اند و باکتری‌ها miRNA ندارند، پس داده‌ی انسانی **GSE52778** (airway، دگزامتازون؛ پاسخ معلوم: ژن‌های پاسخ به گلوکوکورتیکوئید) به رشته‌ی دوم بدل می‌شود. STRING از *E. coli* K-12 پشتیبانی می‌کند و پل میان دو رشته است.

**دسترسی از سرور (2026-10-26):** ‏STRING، Enrichr، g:Profiler، GEO، GeneMANIA، NetworkAnalyst، miRBase، TargetScan، MetaboAnalyst و PRIDE پاسخ دادند؛ DGIdb با GraphQL پاسخ داد. ‏Reactome و Expression Atlas پاسخ ندادند. ‏Cytoscape و IGV برنامه‌ی رومیزی‌اند و روی لپ‌تاپ هنرجو اجرا می‌شوند.

## ارتقای بخش‌های نسخه‌ی ۱
ابزارهایی که در فایل Excel دوره (شیت «مقدماتی تا متوسط») آمده‌اند یا در نسخه‌ی ۱ تنها «از مستندات» نوشته شدند:

| بخش نسخه‌ی ۱ | کار نسخه‌ی ۲ |
| :--- | :--- |
| ۰۲ | ‏Mamba؛ SRA Toolkit (بخش 11/03) |
| ۰۳ | ‏NumPy |
| ۰۶ | ‏Trimmomatic، Cutadapt و Sickle در کنار fastp؛ BWA (دوره‌ی NGS)؛ HISAT2 و STAR (بخش ۱۳) |
| ۰۷ | اجرای واقعی همه‌ی ماژول‌ها (در نسخه‌ی ۱ هیچ‌کدام اجرا نشد) |
| ۰۸ | اجرای واقعی RGI و ABRicate؛ ISfinder، MobileElementFinder و CRISPRCasFinder؛ IQ-TREE و RAxML-NG؛ Gubbins |
| ۰۹ | ‏SWISS-MODEL، Modeller، ZINC، HADDOCK، SwissDock، GROMACS، AMBER، ChimeraX و Discovery Studio؛ بیشترشان در دوره‌ی جدای بیوانفورماتیک ساختاری |

## دوره‌های جدا (بیرون از این مخزن)
1. بیوانفورماتیک ساختاری (تخصصی)
2. ‏NGS و توالی‌یابی نسل سوم (آزمایشگاه و بیوانفورماتیک): ریدهای بلند و اسمبلی هیبرید، فراخوانی واریانت، تک‌سلولی و فضایی
3. زبان R و آمار زیستی
4. آمار و طراحی آزمایش برای داده‌های اومیکس
5. ژنومیکس پزشکی و تفسیر بالینی واریانت: آنوتیشن (VEP، ANNOVAR)، ClinVar و gnomAD، معیارهای ACMG
6. اپیدمیولوژی ژنومیک و فیلودینامیک پاتوژن‌ها
7. زیست‌شناسی سامانه‌ها و مدل‌سازی متابولیک
8. شیمی‌انفورماتیک و طراحی دارو به کمک رایانه
9. یادگیری ماشین و هوش مصنوعی در زیست‌شناسی (تخصصی)
10. برنامه‌نویسی پیشرفته و توسعه‌ی نرم‌افزار بیوانفورماتیک

بخش‌های نسخه‌ی ۲ مقدمه‌ی کاربردی این موضوع‌هایند؛ دوره‌ی جدا ژرفا و نظریه را می‌دهد.

**جای دوره‌ها (2026-10-26):** پوشه‌ها در `/data/Education/new/`:
- ‏۱ (ساختاری): `structural_bioinf`، که از پیش آغاز شده است؛ کاربر بعداً آن را کامل می‌کند.
- ‏۳ (R و آمار زیستی): بعداً، به دست کاربر. دوره‌ی `statistics` از پیش هست.
- ‏۲، ۴ تا ۹: `ngs_third_generation`، `omics_statistics_design`، `medical_genomics`، `genomic_epidemiology`، `systems_biology`، `cheminformatics_drug_design`، `ml_ai_biology`؛ تنها پوشه، طرح با کاربر.
- ‏۱۰ (برنامه‌نویسی پیشرفته): کنار گذاشته شد؛ کاربر با آن موافق نبود.

## قاعده‌های نگارش
همان [STYLE_GUIDE.md](STYLE_GUIDE.md): گام‌به‌گام، کالبدشکافی هر دستور، خروجی واقعی، داده‌ی با پاسخ معلوم، دست‌کم ۵ تمرین با راهنمایی و پاسخ تشریحی، 📺 و 📄 زیر هر تکنیک، و کتاب در منابع. کارهای سنگین با برچسب ✍️ «از مستندات»، یا با برنامه‌ی جدای رایانه.

</div>
