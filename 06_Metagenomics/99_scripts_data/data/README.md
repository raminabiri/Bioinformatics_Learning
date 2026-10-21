<div dir="rtl">

# داده‌ی بخش ۰۶

## ریدها
همان چهار فایل FASTQ بخش ۰۱ (`01_Linux/99_scripts_data/data/fastq`)؛ md5 یکسان. درس ۱ ماژول ۰۱ آن‌ها را در `~/meta/raw` کپی می‌کند. اگر نسخه‌ی دوره را ندارید، `download.sh` آن‌ها را از منبع می‌گیرد.

| فایل | شرح | md5 |
| :--- | :--- | :--- |
| `minigut_R1.fastq.gz`، `minigut_R2.fastq.gz` | ۵۰٬۰۰۰ جفت رید، ۱۲۶ باز | `10691078950a63150244e7517ded803d`، `090cf62530b6874f7fc746ed550bd6bf` |
| `minigut_sample2_R1.fastq.gz`، `minigut_sample2_R2.fastq.gz` | ۲۴٬۹۹۳ جفت رید، ۱۵۱ باز | `1d088537e5180930578097a999d2ca72`، `83a9588a59325f3798fc2f8d8ef1f3ea` |
| `host_chr21_region.fa` | ناحیه‌ی ۵۰۰ کیلوبازی chr21 انسان (hg38)، مرجع کوچک میزبان (ماژول ۰۲) | `68b50cfb970f4c490bf87388b7f43b3f` |
| `human_chr1_region.fa` | ناحیه‌ی ۳۰۰ کیلوبازی chr1 (GRCh38)، **بیرون** از مرجع (ماژول ۰۲) | — |

**منبع:** https://github.com/nf-core/test-datasets/tree/mag. این داده‌ها برای آزمودن گردش کار nf-core/mag ساخته شده‌اند. ریدها **شبیه‌سازی‌شده‌اند** و نام هر رید شناسه‌ی ژنوم مبدأ را دارد (`@NC_006347.1_0/1` = رید از ژنوم *Bacteroides fragilis* YCH46).

## پاسخ معلوم
- ‏`ground_truth.tsv`: ترکیب واقعی هر نمونه، با شمردن نام ریدهای R1 (همان فایل بخش ۰۱). ستون‌ها: نمونه، شمار جفت، accession، نام جاندار.
- ‏`ground_truth_species.tsv`: همان، در سطح **گونه** و با taxid، برای سنجیدن پروفایل Kraken2/Bracken (ماژول ۰۳).

خلاصه: `minigut` = *B. fragilis* (۵۷٫۸٪) + *E. coli* (۴۲٫۲٪). `minigut_sample2` = ۲۱ ژنوم که *Acinetobacter baumannii* با ۶۴٫۶٪ غالب است، و *Candida albicans* (۳٫۵٪).

</div>
