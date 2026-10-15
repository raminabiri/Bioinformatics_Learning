# داده‌ی بخش ۰۳

## دانلود
```bash
bash data/download.sh      # از هر مسیری قابل اجراست؛ فایل‌ها در data/raw و data/host ذخیره می‌شوند
```

| فایل | شرح | md5 |
| :--- | :--- | :--- |
| `raw/minigut_R1.fastq.gz`, `raw/minigut_R2.fastq.gz` | ۵۰٬۰۰۰ جفت‌رید، 126 bp | `10691078950a63150244e7517ded803d`, `090cf62530b6874f7fc746ed550bd6bf` |
| `raw/minigut_sample2_R1.fastq.gz`, `raw/minigut_sample2_R2.fastq.gz` | ۲۴٬۹۹۳ جفت‌رید، 151 bp | `1d088537e5180930578097a999d2ca72`, `83a9588a59325f3798fc2f8d8ef1f3ea` |
| `host/host_chr21_region.fa` | ناحیه‌ی 500 kb از chr21 انسان (hg38)، مرجع کوچک میزبان | `68b50cfb970f4c490bf87388b7f43b3f` |
| `ground_truth.tsv` | ترکیب واقعی هر نمونه (در git ثبت شده) | — |

**منبع:** https://github.com/nf-core/test-datasets/tree/mag. این داده‌ها برای تست پایپ‌لاین nf-core/mag ساخته شده‌اند. ریدها **شبیه‌سازی‌شده‌اند** و نام هر رید شناسه‌ی ژنوم مبدأ را دارد:
```text
@NC_006347.1_0/1        ← رید از ژنوم Bacteroides fragilis YCH46
```

## ground truth
`ground_truth.tsv` با شمردن نام ریدهای R1 ساخته شده و نام ارگانیسم‌ها از NCBI Nucleotide گرفته شده است (2026-10-12):
```bash
zcat raw/minigut_sample2_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@//; s/^([A-Z]+_?[0-9]+\.[0-9]+).*/\1/' | sort | uniq -c | sort -rn
```
خلاصه: `minigut` = *B. fragilis* (۵۷٫۸٪) + *E. coli* (۴۲٫۲٪). `minigut_sample2` = ۲۱ ژنوم که *Acinetobacter baumannii* با ۶۴٫۶٪ غالب است.

## نکته درباره‌ی داده‌ی قبلی
داده‌ای که پیش‌تر با نام `gut_sample_R1/R2` در این دوره استفاده می‌شد، در واقع **آمپلیکون SARS-CoV-2** (MiSeq، از nf-core/viralrecon) بود، نه متاژنوم روده. برای مرجع در `data/_archive_sarscov2_amplicon/` نگه داشته شده و در درس‌ها استفاده نمی‌شود.
