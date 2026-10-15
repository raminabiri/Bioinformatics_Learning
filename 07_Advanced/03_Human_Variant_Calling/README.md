# ماژول 03: فراخوانی و تفسیر واریانت انسانی (Human Variant Calling)

| | |
| :--- | :--- |
| **بخش** | `07_Advanced` |
| **پیش‌نیاز** | 03_Metagenomics/02 (SAM/BAM) |
| **زمان تقریبی** | ۸ ساعت |
| **ابزارها** | BWA-MEM2، samtools، GATK (HaplotypeCaller)، bcftools، Ensembl VEP |
| **داده (پیشنهادی)** | داده‌ی عمومی آموزشی (مثلاً یک ناحیه از نمونه‌های Genome in a Bottle) |
| **وضعیت** | ⚪ طراحی‌شده — سرفصل و اهداف مشخص است؛ درس طبق [STYLE_GUIDE](../../STYLE_GUIDE.md) نوشته و تست خواهد شد |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. مسیر best practices را از FASTQ تا VCF اجرا کنید.
2. واریانت‌ها را با VEP آنوتیت و با ClinVar/gnomAD تفسیر کنید.
3. دقت فراخوانی را با truth set (GIAB) بسنجید.

## سرفصل درس
1. mapping، mark duplicates، BQSR
2. HaplotypeCaller و genotyping
3. فیلتر و ارزیابی با GIAB
4. آنوتیشن و طبقه‌بندی ACMG (مفاهیم)

## تمرین‌های برنامه‌ریزی‌شده
- فراخوانی روی یک ناحیه‌ی کوچک و محاسبه‌ی precision/recall با GIAB
