<div dir="rtl">

# ماژول ۰۲: برداشتن DNA میزبان با Bowtie2 و samtools

| | |
| :--- | :--- |
| **بخش** | `06_Metagenomics` |
| **پیش‌نیاز** | ماژول [کنترل کیفیت](../01_Read_QC_Trimming/) (ریدهای بریده‌شده)؛ [SAM/BAM، FLAG و MAPQ](../../02_BioLinux/04_Align_Variant_Formats/) |
| **زمان تقریبی** | ۴ ساعت (۱٫۵ ساعت درس + ۲٫۵ ساعت تمرین) |
| **ابزار** | ‏Bowtie2 2.5.4، samtools 1.20، wgsim؛ محیط [`envs/metagenomics.yml`](../../envs/metagenomics.yml) |
| **داده** | ‏`~/meta/qc/trimmed/` + دو ناحیه‌ی کوچک ژنوم انسان (دانلود با `curl` در آغاز درس؛ کمتر از ۱ مگابایت) |
| **وضعیت** | ✅ قالب تازه (2026-10-21)؛ خروجی‌ها از اجرای 2026-10-13 |

> ⚠️ **مرجع میزبان این ماژول تنها برای تمرین است** (۵۰۰ کیلوباز از chr21). در کار واقعی کل ژنوم انسان (T2T-CHM13 یا GRCh38 کامل) به کار می‌رود؛ شاخص آماده: https://benlangmead.github.io/aws-indexes/bowtie

## اهداف یادگیری
پس از این ماژول می‌توانید:
1. دلیل علمی و اخلاقی برداشتن ریدهای میزبان را بگویید.
2. شاخص Bowtie2 بسازید، ریدهای جفتی را هم‌تراز کنید و گزارش Bowtie2 و `samtools flagstat` را بخوانید.
3. با `samtools view -f 12 -F 256` جفت‌هایی را نگه دارید که هیچ ریدشان روی میزبان ننشسته، و بدانید چرا `--un-conc` نشت دارد.
4. حساسیت و ویژگی برداشتن میزبان را با یک آزمایش کنترل‌شده (ریدهای انسانی شبیه‌سازی‌شده) بسنجید.

## ترتیب مطالعه
1. ‏[01_lesson.md](01_lesson.md): درس.
2. ‏[02_exercises.md](02_exercises.md): تمرین‌ها؛ زیر عنوان هر تمرین راهنمایی آمده است.
3. ‏[03_solutions.md](03_solutions.md): پاسخ تشریحی.
4. اسکریپت‌ها: [99_scripts_data/02_Host_Removal_Alignment/scripts](../99_scripts_data/02_Host_Removal_Alignment/scripts/) (`make_spiked_sample.sh`، `run_host_removal.sh`، `check.sh`).

## ورودی و خروجی

<div dir="ltr">

```text
~/meta/
├── qc/trimmed/          input (module 01)
└── host/
    ├── ref/             host_chr21_region.fa, human_chr1_region.fa
    ├── index/           Bowtie2 index (host.*.bt2)
    ├── spiked/          minigut + 10,000 simulated human pairs (control)
    ├── bam/             <sample>.host.bam (+ .bai), for inspection
    ├── logs/            <sample>.bowtie2.log, <sample>.flagstat
    └── clean/           host-free reads   <- input of module 03
```

</div>

</div>
