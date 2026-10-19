# ماژول 02: توالی‌یابی long-read و اسمبلی هیبرید (Long-read & Hybrid Assembly)

| | |
| :--- | :--- |
| **بخش** | `10_Advanced` |
| **پیش‌نیاز** | 07_Bacterial_Genomics/01 |
| **زمان تقریبی** | ۸ ساعت |
| **ابزارها** | Filtlong، Porechop_ABI، Flye، Medaka، Polypolish، Unicycler، CheckM2 |
| **داده (پیشنهادی)** | ریدهای Nanopore + Illumina از یک ایزوله‌ی عمومی |
| **وضعیت** | ⚪ طراحی‌شده — سرفصل و اهداف مشخص است؛ درس طبق [STYLE_GUIDE](../../STYLE_GUIDE.md) نوشته و تست خواهد شد |

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. ریدهای Nanopore را QC و فیلتر کنید.
2. ژنوم کامل (کروموزوم + پلاسمیدها) را با Flye و polishing بسازید.
3. اسمبلی هیبرید و short-read را مقایسه کنید.

## سرفصل درس
1. فناوری Nanopore/PacBio و پروفایل خطا
2. QC و فیلتر (Filtlong)؛ برش آداپتور (Porechop_ABI)
3. Flye، polishing با Medaka و Polypolish
4. ارزیابی: circularity، CheckM2، مقایسه با short-read

## تمرین‌های برنامه‌ریزی‌شده
- بستن ژنوم یک ایزوله و تعیین پلاسمید حامل ژن مقاومت (پیوند با 08/03)
