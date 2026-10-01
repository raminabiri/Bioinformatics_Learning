# 🧬 Bioinformatics Learning Roadmap (Zero to Hero)

Welcome to the **Bioinformatics Learning Repository**. This repository contains a structured, step-by-step roadmap for computational biology and bioinformatics, based on our official curriculum.

## 📁 Repository Structure
Each session directory in this repository is structured as follows:
- `lesson.md`: Main theoretical background and tutorial
- `codes.sh`: Command snippets and executable scripts
- `Qs.md`: Practical exercises and hands-on scenarios
- `As.md`: Detailed answer key and solutions

---

## 🗺️ Core Bioinformatics Roadmap (Foundations to Intermediate)

| Phase | Main Subject / Focus | Tools, Software & Databases | Description & Output |
| :--- | :--- | :--- | :--- |
| **Phase 1: Foundations, Terminal & Data Retrieval** | Infrastructure, Environment Management & Data Downloading | • Bash & Linux Terminal (Basic commands, navigation, scripting)<br>• Conda / Mamba (Environment management & package installation)<br>• Raw Data Downloading: SRA Toolkit (Download from NCBI SRA)<br>• Data Formats: FASTA, FASTQ, BAM, VCF, GFF, GBK<br>• Git & GitHub (Version control) | System setup, package management, and raw sequencing data retrieval from public databases. |
| **Phase 2: Metagenomics Analysis, 16S & Alignment** | NGS Sequence Processing & Metagenomics | • QC & Trimming: FastQC, Trimmomatic, Cutadapt, Sickle<br>• Genome Alignment: Bowtie2, BWA, HISAT2, STAR, BLAST<br>• 16S & Amplicon Analysis: QIIME2, DADA2 (R package)<br>• Metagenomic Taxonomy & Function: Kraken2, MetaPhlAn, HUMAnN | From raw data quality control to taxonomic identification and functional profiling of microbial communities. |
| **Phase 3: Bacterial Genomics, Annotation & Typing** | Assembly, Quality Evaluation & Bacterial Profiling | • Assembly QC: QUAST, CheckM<br>• Genome Annotation: Prokka, Bakta (+ Bakta Database)<br>• Molecular Typing: mlst<br>• Comparative Genomics (Pan-genome): Roary, Panaroo<br>• Variant Identification: Snippy | Automated bacterial genome annotation, genome quality assessment, MLST typing, and pan-genome analysis. |
| **Phase 4: Resistance Genes, Virulence, MGEs & Phylogeny** | AMR, Virulence & Evolution Analysis | • Antimicrobial Resistance (AMR): CARD / ARO Database, AMRFinderPlus, ABRicate<br>• Virulence Factors: VFDB (Search tool + Database)<br>• Mobile Genetic Elements: CRISPRCasFinder, ISfinder, MobileElementFinder, PlasmidFinder<br>• Phylogenetic Trees: IQ-TREE, RAxML | Identification of drug resistance genes, virulence factors, plasmids, CRISPR, and phylogenetic tree reconstruction. |
| **Phase 5: Structural Bioinformatics & Drug Screening** | 3D Modeling, Docking & Compound Databases | • 3D Structure Prediction: AlphaFold, SWISS-MODEL, Modeller<br>• Chemical/Drug Compound Database: ZINC Database<br>• Molecular Docking: AutoDock Vina, HADDOCK, SwissDock<br>• Molecular Dynamics (MD): GROMACS, AMBER<br>• Visualization & Analysis: PyMOL, ChimeraX, Discovery Studio | Protein structure prediction, compound retrieval from ZINC, molecular docking, and dynamics simulation. |
| **Phase 6: Programming, Data Mining & Automation** | Script Development & Data Analysis | • Python & Biopython (Scripting & sequence analysis)<br>• Pandas & NumPy (Large dataset processing & merging)<br>• R & Bioconductor (Statistical analysis & advanced plotting)<br>• Dify & AI Pipelines (Smart analysis workflow design) | Coding to integrate tools, automate analytical pipelines, and extract statistical reports. |

---

## 🚀 Advanced PhD Bioinformatics Roadmap

| Phase | Main Subject / Focus | Tools, Software & Databases | Description & Output |
| :--- | :--- | :--- | :--- |
| **Phase 1 Advanced: Workflow Management & Containerization** | Automated Pipeline Design & Cloud Computing | • Containerization: Docker / Singularity<br>• Workflow Management: Nextflow / Snakemake<br>• High-Performance Computing: SLURM / HPC Cluster Management | Designing automated, error-free, scalable pipelines for large datasets on supercomputers. |
| **Phase 2 Advanced: Long-Read Sequencing & Hybrid Assembly** | Nanopore & PacBio Processing | • Long-Read QC & Filtering: Filtlong, Porechop<br>• Long-Read & Hybrid Assembly: Flye, Unicycler, Canu<br>• Polishing: Medaka, Racon<br>• Genome Completeness Assessment: BUSCO | Generating complete/closed genomes by combining Nanopore and Illumina data. |
| **Phase 3 Advanced: Human Genomics & Variant Calling** | Medical Bioinformatics & Mutation Interpretation | • VCF/BAM File Management: samtools, bcftools, bedtools<br>• Variant Calling: GATK (HaplotypeCaller), FreeBayes<br>• Clinical Mutation Annotation: ANNOVAR, Ensembl VEP | Accurate identification and clinical annotation of human and pathogenic genetic variants. |
| **Phase 4 Advanced: Single-Cell Transcriptomics (scRNA-Seq)** | Cellular Diversity Analysis at Single-Cell Level | • Upstream Processing: Cell Ranger (10x Genomics)<br>• Analysis in R: Seurat<br>• Analysis in Python: Scanpy | Cell clustering, cell type identification, and gene expression analysis at single-cell resolution. |
| **Phase 5 Advanced: Deep Learning & Protein Language Models** | Specialized AI in Bioinformatics | • Machine & Deep Learning: Scikit-Learn, PyTorch, TensorFlow<br>• Protein Language Models (PLMs): ESM-2, ProtBERT, ESMFold<br>• Advanced AI Platforms: BioNeMo | Developing custom biological prediction models and leveraging state-of-the-art protein language models. |

---
---

# 🧬 نقشه راه جامع آموزش بیوانفورماتیک (از صفر تا صد)

به **مخزن آموزش بیوانفورماتیک** خوش آمدید. این مخزن شامل نقشه راه گام‌به‌گام و کاربردی بر اساس سرفصل‌های رسمی دوره آموزشی ما است.

## 📁 ساختار پوشه‌های مخزن
پوشه مربوط به هر جلسه در این مخزن به صورت زیر سازمان‌دهی شده است:
- `lesson.md`: متن اصلی درس و مباحث تئوری
- `codes.sh`: کدهای نمونه و دستورات قابل اجرا
- `Qs.md`: تمرین‌ها و سناریوهای عملی
- `As.md`: پاسخ‌نامه تشریحی و کلید تمرین‌ها

---

## 🗺️ نقشه راه دوره اصلی (مقدماتی تا متوسط)

| فاز (Phase) | موضوع / محور اصلی | نرم‌افزارها، ابزارها و پایگاه‌های داده | توضیحات و خروجی فاز |
| :--- | :--- | :--- | :--- |
| **فاز ۱: پایه، ترمینال و دریافت داده** | زیرساخت، مدیریت محیط و دانلود داده | • Bash & Linux Terminal (دستورات پایه، پیمایش، اسکریپت‌نویسی)<br>• Conda / Mamba (مدیریت محیط‌ها و نصب پکیج‌ها)<br>• دریافت داده‌های خام: SRA Toolkit (دانلود از NCBI SRA)<br>• فرمت‌های داده: FASTA, FASTQ, BAM, VCF, GFF, GBK<br>• Git & GitHub (کنترل نسخه) | آماده‌سازی سیستم، مدیریت پکیج‌ها و دریافت داده‌های توالی‌یابی خام از پایگاه‌های داده |
| **فاز ۲: آنالیز متارژنومیکس، ۱۶S و ترازسازی** | پردازش توالی‌های NGS و متاژنوم | • کنترل کیفیت و پالایش: FastQC, Trimmomatic, Cutadapt, Sickle<br>• ترازسازی ژنوم (Alignment): Bowtie2, BWA, HISAT2, STAR, BLAST<br>• آنالیز ۱۶S & Amplicon: QIIME2, DADA2 (پکیج R)<br>• تاکسونومی و فانکشن متاژنوم: Kraken2, MetaPhlAn, HUMAnN | از کنترل کیفیت داده‌های خام تا شناسایی تاکسونومیک و پروفایل کارکردی جوامع میکروبی |
| **فاز ۳: ژنومیکس باکتریایی، آنوتیشن و تایپینگ** | اسمبلی، ارزشیابی و شناسایی ویژگی‌های باکتری | • ارزیابی کیفیت اسمبلی: QUAST, CheckM<br>• آنوتیشن ژنوم (Genome Annotation): Prokka, Bakta (+ دیتابیس Bakta)<br>• تایپینگ و تایپ مولکولی: mlst<br>• ژنومیکس مقایسه‌ای (Pan-genome): Roary, Panaroo<br>• شناسایی واریانت‌ها: Snippy | آنوتیشن خودکار ژنوم‌های باکتریایی، سنجش سلامت ژنوم، تعیین تایپ مولکولی و آنالیز پنگنوم |
| **فاز ۴: ژن‌های مقاومت، ضراوت، عناصر متحرک و فیلوژنی** | آنالیز مقاومت دارویی، ضراوت و تکامل | • مقاومت آنتی‌بیوتیکی (AMR): CARD / ARO Database, AMRFinderPlus, ABRicate<br>• فاکتورهای ضراوت (Virulence Factors): VFDB (ابزار جستجو + دیتابیس)<br>• عناصر ژنتیکی متحرک و کروموزومی: CRISPRCasFinder, ISfinder, MobileElementFinder, PlasmidFinder<br>• درخت‌های فیلوژنتیک: IQ-TREE, RAxML | شناسایی ژن‌های مقاومت دارویی، فاکتورهای بیماری‌زایی، پلاسمیدها، کریسپر و رسم درخت‌های تکاملی |
| **فاز ۵: بیوانفورماتیک ساختاری و غربالگری دارویی** | مدلسازی ۳بعدی، داکینگ و پایگاه داده ترکیبات | • پیش‌بینی ساختار سه‌بعدی: AlphaFold, SWISS-MODEL, Modeller<br>• پایگاه داده ترکیبات شیمیایی/دارویی: ZINC Database<br>• داکینگ مولکولی: AutoDock Vina, HADDOCK, SwissDock<br>• دینامیک مولکولی (MD): GROMACS, AMBER<br>• تجزیه‌وتحلیل و تجسم: PyMOL, ChimeraX, Discovery Studio | از پیش‌بینی ساختار پروتئین تا استخراج ترکیبات از ZINC، داکینگ دارویی و شبیه‌سازی دینامیک |
| **فاز ۶: برنامه‌نویسی تخصصی، داده‌کاوی و اتوماسیون** | توسعه اسکریپت و تحلیل داده | • Python & Biopython (اسکریپت‌‌نویسی و آنالیز توالی)<br>• Pandas & NumPy (پردازش و ادغام داده‌های بزرگ)<br>• R & Bioconductor (تحلیل‌های آماری و رسم نمودارهای پیشرفته)<br>• Dify & AI Pipelines (طراحی خطوط تحلیل هوشمند) | کدنویسی برای متصل کردن ابزارها، اتوماسیون مسیرهای تحلیلی و استخراج گزارش‌های آماری |

---

## 🚀 نقشه راه دوره پیشرفته (PhD Advanced)

| فاز (Phase) | موضوع / محور اصلی | نرم‌افزارها، ابزارها و پایگاه‌های داده | توضیحات و خروجی فاز |
| :--- | :--- | :--- | :--- |
| **فاز ۱ پیشرفته: مدیریت خطوط تحلیل و کانتینرسازی** | طراحی Pipelines خودکار و پردازش ابری | • کانتینرسازی: Docker / Singularity<br>• سیستم‌های مدیریت ورک‌فلو: Nextflow / Snakemake<br>• پردازش سنگین و کلاستر: SLURM / HPC Cluster Management | طراحی اتوماتیک، بدون خطا و مقیاس‌پذیر خطوط تحلیلی بزرگ روی سوپرکامپیوترها |
| **فاز ۲ پیشرفته: توالی‌یابی Long-Read و اسمبلی هایبرید** | پردازش نانوپور و پاک‌بیو | • کنترل کیفیت و پالایش Long-Read: Filtlong, Porechop<br>• اسمبلی Long-Read & Hybrid: Flye, Unicycler, Canu<br>• پالایش اسمبلی (Polishing): Medaka, Racon<br>• ارزیابی تکمیلی: BUSCO | تولید ژنوم‌های کاملاً بسته (Complete/Closed Genomes) با ترکیب نانوپور و ایلومینا |
| **فاز ۳ پیشرفته: ژنومیکس انسانی و Variant Calling** | بیوانفورماتیک پزشکی و تفسیر جهش‌ها | • مدیریت فایل‌های VCF/BAM: samtools, bcftools, bedtools<br>• فراخوانی واریانت‌ها: GATK (HaplotypeCaller), FreeBayes<br>• آنوتیشن بالینی جهش‌ها: ANNOVAR, Ensembl VEP | شناسایی و آنوتیشن دقیق جهش‌های ژنتیکی انسانی و بیماری‌زا |
| **فاز ۴ پیشرفته: ترانسکریپتومیکس تک‌سلولی (scRNA-Seq)** | آنالیز تنوع سلولی در سطح تک‌سلول | • پردازش اولیه: Cell Ranger (10x Genomics)<br>• آنالیز در R: Seurat<br>• آنالیز در پایتون: Scanpy | خوشه‌بندی سلولی، تعیین نوع سلول‌ها و بررسی بیان ژن در سطح Single-Cell |
| **فاز ۵ پیشرفته: یادگیری عمیق و مدل‌های زبانی پروتئین** | هوش مصنوعی تخصصی در بیوانفورماتیک | • یادگیری ماشین و عمیق: Scikit-Learn, PyTorch, TensorFlow<br>• مدل‌های زبانی پروتئین (PLMs): ESM-2, ProtBERT, ESMFold<br>• پلتفرم‌های پیشرفته: BioNeMo | توسعه مدل‌های پیش‌بینی زیستی اختصاصی و استفاده از پیشرفته‌ترین مدل‌های هوش مصنوعی پروتئین |
