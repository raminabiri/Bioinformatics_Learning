# بخش ۰۷: مباحث پیشرفته (سطح دکتری)

موضوعات پیشرفته‌ای که بر بخش‌های ۰۰ تا ۰۶ بنا می‌شوند (از شیت «پیشرفته» فایل Excel دوره). هر ماژول مستقل است و پیش‌نیازش را جداگانه اعلام می‌کند.

| ماژول | عنوان | ابزارهای اصلی | وضعیت |
| :---: | :--- | :--- | :---: |
| 01 | [پایپلاین، کانتینر و HPC](01_Workflows_Containers_HPC/) | Nextflow، nf-core، Docker/Apptainer، SLURM | ⚪ طراحی‌شده |
| 02 | [توالی‌یابی long-read و اسمبلی هیبرید](02_Long_Read_Hybrid_Assembly/) | Filtlong، Porechop_ABI، Flye، Medaka، Polypolish، Unicycler، CheckM2 | ⚪ طراحی‌شده |
| 03 | [فراخوانی و تفسیر واریانت انسانی](03_Human_Variant_Calling/) | BWA-MEM2، samtools، GATK (HaplotypeCaller)، bcftools، Ensembl VEP | ⚪ طراحی‌شده |
| 04 | [ترنسکریپتومیکس تک‌سلولی](04_Single_Cell_RNAseq/) | Cell Ranger (مفاهیم)، Seurat، Scanpy | ⚪ طراحی‌شده |
| 05 | [یادگیری ماشین و مدل‌های زبانی پروتئین](05_Deep_Learning_Protein_LMs/) | scikit-learn، PyTorch، ESM-2، ESMFold | ⚪ طراحی‌شده |
| 06 | [پایپلاین‌های هوشمند با LLM](06_AI_Pipelines_Dify/) | Dify، API مدل‌های زبانی | ⚪ طراحی‌شده |

## داده‌ی مشترک بخش
هر ماژول داده‌ی خودش را دارد و موقع نوشتن درس انتخاب، تست و در `data/download.sh` ثبت می‌شود.

## رشته‌ی مشترک دوره
ماژول ۰۱ پایپلاین‌های بخش ۰۳ و ۰۴ را با Nextflow/nf-core و کانتینر بازسازی می‌کند. ماژول ۰۲ پلاسمیدهای ناقص بخش ۰۵ را با long-read می‌بندد.
