# پاسخ تشریحی: حذف DNA میزبان و مبانی همترازی

> اجرا شده در 2026-10-13 با Bowtie2 2.5.4، samtools 1.20 و wgsim 1.20 (seed = 42). اعداد شما باید دقیقاً همین‌ها باشند.

---

## تمرین ۱: حساسیت و ویژگی

```bash
IN=work/02_host/spiked bash 02_Host_Removal_Alignment/scripts/run_host_removal.sh minigut_spiked
zcat work/02_host/clean/minigut_spiked_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```
```text
   4725 HUMAN_chr1
  21018 NC_000913.3
  28827 NC_006347.1
```

| منشأ | ورودی | باقی‌مانده | حذف‌شده |
| :--- | ---: | ---: | ---: |
| باکتری (*E. coli* + *B. fragilis*) | 49,845 | 49,845 | 0 (۰٪) |
| انسان chr21 (در مرجع) | 5,000 | 0 | 5,000 (۱۰۰٪) |
| انسان chr1 (خارج از مرجع) | 5,000 | 4,725 | 275 (۵٫۵٪) |

- **حساسیت برای نواحی موجود در مرجع:** 5000 / 5000 = **۱۰۰٪**
- **حساسیت برای همه‌ی ریدهای انسانی:** (5000 + 275) / 10000 = **۵۲٫۸٪**
- **ویژگی (ریدهای باکتریایی حفظ‌شده):** 49845 / 49845 = **۱۰۰٪**

**کدام عدد را گزارش کنیم؟** «حساسیت» باید نسبت به **همه‌ی** ریدهای انسانی واقعی تعریف شود، یعنی ۵۲٫۸٪. عدد ۱۰۰٪ فقط می‌گوید الگوریتم همترازی خوب کار می‌کند، نه اینکه **حذف میزبان** خوب کار کرده است. محدودیت اصلی اینجا الگوریتم نیست، **مرجع** است. گزارش ۱۰۰٪ بدون ذکر این شرط گمراه‌کننده است. در پروژه‌ی واقعی با ژنوم کامل انسان، این دو عدد به هم نزدیک می‌شوند (تمرین ۵).

---

## تمرین ۲: `--un-conc` در برابر `samtools -f 12`

```bash
zcat work/02_host/unconc_R1.fastq.gz | awk 'NR%4==1' \
  | sed -E 's/^@?(HUMAN_chr[0-9]+|NC_[0-9.]+).*/\1/' | sort | uniq -c
```
```text
   4926 HUMAN_chr1
      2 HUMAN_chr21
  21018 NC_000913.3
  28827 NC_006347.1
```

| منشأ | `samtools -f 12` | `--un-conc` |
| :--- | ---: | ---: |
| chr21 باقی‌مانده | 0 | **2** |
| chr1 باقی‌مانده | 4,725 | **4,926** |
| باکتری باقی‌مانده | 49,845 | 49,845 |

### ۲.۳ دو جفت chr21 که نشت کردند
```bash
zcat work/02_host/unconc_R1.fastq.gz | awk 'NR%4==1' | grep chr21
samtools view work/02_host/bam/minigut_spiked.host.bam | awk '$2==97 || $2==145' | cut -f1-9
```
```text
HUMAN_chr21_chr21part_303783_304289_..._991    97   chr21part  303783  32  126M  =  304164  0
HUMAN_chr21_chr21part_303783_304289_..._991    145  chr21part  304164  42  126M  =  303783  0
HUMAN_chr21_chr21part_405423_405938_..._107d   97   chr21part  405423  1   126M  =  405813  0
HUMAN_chr21_chr21part_405423_405938_..._107d   145  chr21part  405813  1   126M  =  405423  0
```
- `97` = PAIRED, MREVERSE, READ1 و `145` = PAIRED, REVERSE, READ2. **هر دو mate همتراز شده‌اند** (بیت 4 روشن نیست) ولی بیت **PROPER_PAIR (2) خاموش است**.
- نام رید wgsim مختصات قطعه‌ی واقعی را دارد: 303783 تا 304289 یعنی **۵۰۷ باز**، و 405423 تا 405938 یعنی **۵۱۶ باز**. هر دو بیشتر از `-X 500` پیش‌فرض‌اند. Bowtie2 جفت را «concordant» حساب نمی‌کند و `--un-conc` آن را بیرون می‌دهد، با اینکه هر دو mate انسانی‌اند و روی مرجع انسانی نشسته‌اند.
- تفاوت chr1 (۴۹۲۶ در برابر ۴۷۲۵ = ۲۰۱ جفت) دو جزء دارد: **۱۹۶ جفت که فقط یک mate‌شان** روی تکرارهای مشترک chr21 نشسته (ترکیب FLAGهای 73/133، 69/137، 89/165 و 101/153) و **۵ جفت discordant** که هر دو mate نشسته‌اند (97/145، 81/161، 65/129). `--un-conc` همه را نگه می‌دارد. `-f 12` حذفشان می‌کند، چون یک mate انسانی کافی است تا کل جفت مشکوک باشد. (۷۴ جفت دیگر chr1 به‌صورت proper pair نشسته‌اند و با هر دو روش حذف می‌شوند: 74 + 196 + 5 = 275.)

### ۲.۴ با `-X 1000`؟
```bash
bowtie2 ... -X 1000 --un-conc-gz work/02_host/unconcX_R%.fastq.gz ...
```
```text
   4926 HUMAN_chr1
  21018 NC_000913.3
  28827 NC_006347.1
```
دو جفت chr21 حذف شدند، ولی این **راه‌حل کلی نیست**:
1. توزیع insert هر کتابخانه فرق دارد و همیشه دنباله‌ای بلندتر از هر `-X` وجود دارد.
2. مشکل جفت‌های تک‌mate (۲۰۱ جفت chr1) با `-X` حل نمی‌شود.

راه‌حل کلی این است که **منطق را عوض کنید**: «جفتی را نگه دار که هیچ mate‌اش همتراز نشده» (`-f 12`)، نه «جفتی که concordant همتراز نشده».

---

## تمرین ۳: FLAG

```bash
for f in 77 141 99 147 97 145 73 133; do
  printf "%s\t%s\t%s\n" $f "$(samtools flags $f | cut -f3)" \
     "$(samtools view work/02_host/bam/minigut_spiked.host.bam | awk -v f=$f '$2==f' | wc -l)"
done
```
| FLAG | معنی | تعداد رکورد | در حذف میزبان |
| :-: | :--- | ---: | :--- |
| 77 | PAIRED, UNMAP, MUNMAP, READ1 | 54,570 | **نگه دار** (هر دو mate unmapped) |
| 141 | PAIRED, UNMAP, MUNMAP, READ2 | 54,570 | **نگه دار** |
| 99 | PAIRED, PROPER_PAIR, MREVERSE, READ1 | 2,548 | حذف |
| 147 | PAIRED, PROPER_PAIR, REVERSE, READ2 | 2,548 | حذف |
| 97 | PAIRED, MREVERSE, READ1 (جفت، ولی نه proper) | 4 | حذف (همان نشت `--un-conc`) |
| 145 | PAIRED, REVERSE, READ2 | 4 | حذف |
| 73 | PAIRED, MUNMAP, READ1 (خودش mapped، mate نه) | 50 | حذف |
| 133 | PAIRED, UNMAP, READ2 (خودش unmapped، mate mapped) | 50 | حذف |

**نکته:** 77 و 141 دقیقاً هم‌تعدادند (۵۴٬۵۷۰). این همان تعداد جفت‌های تمیز است: 49,845 باکتری + 4,725 chr1. ۷۳ و ۱۳۳ هم هم‌تعدادند، چون دو نیمه‌ی یک وضعیت‌اند (R1 mapped و R2 unmapped). جفت‌های proper دو جهت دارند: 99/147 (R1 رو به جلو) و 83/163 (R1 معکوس) با ۲٬۵۲۴ رکورد.

---

## تمرین ۴: MAPQ

### ۴.۱
```text
   5924 0-1
     50 2-9
    726 10-29
   3300 >=30
```
### ۴.۲ چرا MAPQ پایین؟
```bash
python3 - <<'EOF'
s = ''.join(l.strip() for l in open('data/host/host_chr21_region.fa') if not l.startswith('>')).upper()
from collections import Counter
k = 40
c = Counter(s[i:i+k] for i in range(len(s)-k+1) if 'N' not in s[i:i+k])
rep = sum(1 for v in c.values() if v > 1)
print('distinct 40-mers', len(c), 'repeated', rep, round(rep/len(c)*100, 1), '%')
EOF
```
```text
distinct 40-mers 276706 repeated 121329 43.8 %
```
**۴۳٫۸٪** از ۴۰-مرهای این ناحیه بیش از یک بار تکرار شده‌اند. ناحیه شامل یک **قطعه‌ی تکراری بزرگ** است (مثلاً بازهای ابتدای ناحیه در موقعیت 381,778 دوباره آمده‌اند)، و دو بلوک N هم دارد (۲۰٪ ناحیه). ریدی که از چنین بخشی می‌آید دو محل همترازی با امتیاز برابر دارد (تگ `XS:i` برابر `AS:i`). Bowtie2 نمی‌تواند یکی را ترجیح دهد و MAPQ صفر یا یک می‌دهد. در ژنوم کامل انسان هم حدود نیمی از توالی تکراری است (Alu، L1، تکرارهای قطعه‌ای، سانترومرها)، پس این پدیده عادی است.

### ۴.۳ پیامد فیلتر MAPQ ≥ 30
```bash
samtools view -F 4 -q 30 work/02_host/bam/minigut_spiked.host.bam | cut -f1 | sort -u | grep -c chr21
# 1650
```
فقط **۱٬۶۵۰ از ۵٬۰۰۰ جفت chr21** دست‌کم یک mate با MAPQ ≥ 30 دارند. با این فیلتر **۳٬۳۵۰ جفت انسانی (۶۷٪)** در داده‌ی «تمیز» باقی می‌ماند. در حذف میزبان سؤال «انسانی است یا نه؟» است، نه «دقیقاً کجای ژنوم انسان؟». MAPQ به سؤال دوم جواب می‌دهد.

---

## تمرین ۵: مرجع کامل‌تر

```bash
mkdir -p work/02_host/index_full
cat data/host/host_chr21_region.fa data/host/human_chr1_region.fa > work/02_host/index_full/host_full.fa
IN=work/02_host/spiked REF=work/02_host/index_full/host_full.fa IDX=work/02_host/index_full/host_full \
  bash 02_Host_Removal_Alignment/scripts/run_host_removal.sh minigut_spiked
```
```text
== minigut_spiked
   16.71% overall alignment rate   clean pairs: 49845
```
```text
  21018 NC_000913.3
  28827 NC_006347.1
```

| منشأ | ورودی | باقی‌مانده | حذف‌شده |
| :--- | ---: | ---: | ---: |
| باکتری | 49,845 | 49,845 | ۰٪ |
| انسان chr21 | 5,000 | 0 | ۱۰۰٪ |
| انسان chr1 | 5,000 | 0 | ۱۰۰٪ |

**تفسیر:** حساسیت برای همه‌ی ریدهای انسانی از ۵۲٫۸٪ به **۱۰۰٪** رسید و ویژگی ۱۰۰٪ ماند. در پروژه‌ی واقعی یعنی:
- **کل ژنوم** میزبان را ایندکس کنید. T2T-CHM13 حدود ۲۰۰ مگاباز توالی دارد که در GRCh38 نیست (سانترومرها و تکرارها)، و ریدهای این نواحی با GRCh38 حذف نمی‌شوند.
- طرف دیگر ماجرا: **مرجع بزرگ‌تر خطر حذف کاذب را بالا می‌برد.** ژنوم انسان قطعاتی دارد که به توالی میکروبی شبیه است، مثل آلودگی‌های قدیمی اسمبلی یا ژن‌های حفاظت‌شده مثل rRNA. ریدهای باکتریایی هم ممکن است روی این قطعات بنشینند و حذف شوند. Hostile دقیقاً به همین دلیل نواحی‌ای از T2T-CHM13 را که با ژنوم‌های میکروبی مشترک‌اند **mask** می‌کند. هدف این است که حساسیت بالا بماند و ریدهای باکتریایی از دست نروند. روی داده‌ی کوچک ما این اثر دیده نمی‌شود، چون مرجع فقط ۸۰۰ kb است.

---

## تمرین ۶: Methods (نمونه)

> *Host reads were removed by aligning quality-trimmed read pairs to the human reference genome (<T2T-CHM13v2.0 / GRCh38 with alt and decoy sequences; index source and version>) with Bowtie2 v2.5.4 (`--very-sensitive`). Read pairs were retained only if neither mate aligned to the host (samtools v1.20 `view -f 12 -F 256`, followed by `samtools fastq`); no mapping-quality filter was applied. The proportion of host reads per sample is reported in Table S<n>. Sensitivity and specificity of this procedure were verified on a spike-in control in which 10,000 simulated human read pairs (wgsim v1.20) were added to a sample of known bacterial composition: all bacterial pairs were retained and all human pairs from regions present in the reference were removed.*

نکته‌ها: مرجع و نسخه‌ی آن، منطق نگه‌داشتن جفت‌ها (دقیقاً کدام FLAG)، **نبودن** فیلتر MAPQ، و درصد میزبان هر نمونه.
