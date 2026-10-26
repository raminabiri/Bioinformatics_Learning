<div dir="rtl">

# بخش ۱۳ (نسخه‌ی ۲): ترنسکریپتومیکس با RNA-seq (RNA-seq Transcriptomics)

از طراحی آزمایش تا ژن‌های تغییرکرده. نسخه‌ی ۱ تنها اجرای DESeq2 روی داده‌ی شبیه‌سازی‌شده را داشت (04/03).

| | |
| :--- | :--- |
| **پیش‌نیاز** | بخش‌های ۰۴، ۰۵ و ۰۶، و ماژول 11/04 |
| **داده‌ی مشترک (پیشنهادی)** | ریدهای شبیه‌سازی‌شده با تغییر بیان معلوم (پاسخ معلوم)؛ GSE52778 برای داده‌ی واقعی؛ یک داده‌ی RNA-seq باکتری زیر تنش آنتی‌بیوتیک |
| **وضعیت** | ⚪ طرح نسخه‌ی ۲ (2026-10-26)؛ نقشه‌ی کامل در [V2_ROADMAP.md](../V2_ROADMAP.md) |

| ماژول | عنوان | ابزار و پایگاه | وضعیت |
| :---: | :--- | :--- | :---: |
| ۰۱ | [طراحی آزمایش و کنترل کیفیت](01_Design_QC/) | ‏FastQC، MultiQC، RSeQC (معرفی) | ⚪ طرح |
| ۰۲ | [هم‌ترازی و شمارش](02_Alignment_Quantification/) | ‏HISAT2، STAR (از مستندات)، Salmon، kallisto، featureCounts | ⚪ طرح |
| ۰۳ | [بیان افتراقی](03_Differential_Expression/) | ‏DESeq2، edgeR، limma-voom (اسکریپت‌های آماده)، PCA، heatmap، volcano | ⚪ طرح |
| ۰۴ | [بازتولید یک یافته‌ی منتشرشده](04_Reuse_Public_Data/) | GEO، DESeq2، Snakemake | ⚪ طرح |
| ۰۵ | ‏[RNA-seq باکتری](05_Bacterial_RNAseq/) | Bowtie2، featureCounts، DESeq2 | ⚪ طرح |

</div>
