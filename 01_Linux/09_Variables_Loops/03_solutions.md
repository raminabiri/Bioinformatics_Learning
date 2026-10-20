<div dir="rtl">

# پاسخ تشریحی: متغیر و حلقه

> دستورها در 2026-10-20 با bash 5.2، GNU grep 3.11 و mawk 1.3.4 در پوشه‌ی `01_Linux/99_scripts_data/data` اجرا شدند.

---

## تمرین ۱: یک نام، چند دستور

<div dir="ltr">

```bash
genome="ecoli_k12.fna"
wc -l "$genome"
head -n 1 "$genome"
```

</div>

<div dir="ltr">

```text
58022 ecoli_k12.fna
>NC_000913.3 Escherichia coli str. K-12 substr. MG1655, complete genome
```

</div>

3. تنها خط یکم: `genome="host_chr21_region.fa"`. دو دستور بعدی بی تغییر می‌مانند. سود متغیر همین است: **نام را یک جا عوض کنید، همه‌جا عوض شود.**

---

## تمرین ۲: جدول فایل‌های FASTA

<div dir="ltr">

```bash
for fa in ecoli_k12.fna host_chr21_region.fa sample.fasta; do
  printf "%s\t%s\t%s\n" "$fa" "$(grep -c '^>' "$fa")" "$(grep -v '^>' "$fa" | tr -d '\n' | wc -c)"
done
```

</div>

<div dir="ltr">

```text
ecoli_k12.fna	1	4641652
host_chr21_region.fa	1	500000
sample.fasta	1	14
```

</div>

هر سه یک توالی دارند: ژنوم *E. coli* (۴٬۶۴۱٬۶۵۲)، تکه‌ی کروموزوم ۲۱ (۵۰۰٬۰۰۰، که ۱۰۰٬۰۰۰ تایش N است)، و پروتئین ۱۴ اسیدآمینه‌ای.

**اشتباه رایج:** فراموش کردن نقل‌قول‌های درون `$( … )`. `"$(grep -c '^>' "$fa")"` درست است: نقل‌قول بیرونی دور کل جایگزینی، و نقل‌قول درونی دور `$fa`.

---

## تمرین ۳: ژن‌های داستان ما

<div dir="ltr">

```bash
for g in rpoA rpoB gyrA; do
  printf "%s\t" "$g"
  grep -P '\tgene\t' ecoli_k12.gff | grep "Name=$g;" | cut -f4,5,7
done
```

</div>

<div dir="ltr">

```text
rpoA	3440040	3441029	-
rpoB	4181245	4185273	+
gyrA	2336793	2339420	-
```

</div>

**چرا نقل‌قول دوتایی؟** الگو باید `$g` را **جایگزین** کند: در دور یکم `Name=rpoA;`، در دور دوم `Name=rpoB;` و… . با نقل‌قول تکی (`'Name=$g;'`)، `grep` به دنبال متن واقعی `Name=$g;` می‌گشت و هیچ چیز نمی‌یافت. (در الگوی `grep` یکم نقل‌قول تکی درست است، چون متغیری در آن نیست.)

‏`printf "%s\t"` بی `\n` نام ژن را چاپ می‌کند و روی همان خط می‌ماند؛ خروجی `cut` درست پس از آن می‌آید.

---

## تمرین ۴: GC هر نمونه

<div dir="ltr">

```bash
for f in fastq/*_R1.fastq.gz; do
  s=$(basename "$f" _R1.fastq.gz)
  gc=$(zcat "$f" | awk 'NR%4==2' | tr -cd 'GC' | wc -c)
  tot=$(zcat "$f" | awk 'NR%4==2' | tr -d '\n' | wc -c)
  echo "$s $gc $tot" | awk '{printf "%s\t%.2f\n", $1, $2/$3*100}'
done
```

</div>

<div dir="ltr">

```text
minigut	46.79
minigut_sample2	40.51
```

</div>

1. ‏`minigut`: **۴۶٫۷۹٪** (۲٬۹۴۷٬۴۷۶ G و C از ۶٬۳۰۰٬۰۰۰ باز). `minigut_sample2`: **۴۰٫۵۱٪** (۱٬۵۲۸٬۸۶۳ از ۳٬۷۷۳٬۹۴۳).
2. هر نمونه ترکیب دیگری از باکتری‌ها دارد، و هر گونه GC خودش را دارد. `minigut` از *E. coli* (GC نزدیک ۵۱٪) و *Bacteroides fragilis* (نزدیک ۴۳٪) ساخته شده. در `minigut_sample2` بیشتر ریدها مال *Acinetobacter baumannii* با GC پایین (نزدیک ۳۹٪) است. **GC ریدها اثر انگشت ترکیب نمونه است**؛ در ماژول کنترل کیفیت بخش ۰۶ دوباره به آن برمی‌گردیم.

---

## تمرین ۵: حساب در Bash

<div dir="ltr">

```bash
n=$(zcat fastq/minigut_sample2_R1.fastq.gz | wc -l)
echo $((n/4))
N=$(grep -v '^>' host_chr21_region.fa | tr -cd 'Nn' | wc -c)
L=$(grep -v '^>' host_chr21_region.fa | tr -d '\n' | wc -c)
echo $((N*100/L))
```

</div>

<div dir="ltr">

```text
24993
20
```

</div>

1. **۲۴٬۹۹۳ رید.**
2. **۲۰٪.** اگر نخست تقسیم کنید (`$((N/L*100))`)، `N/L` = ۱۰۰٬۰۰۰ ÷ ۵۰۰٬۰۰۰ = ۰٫۲ است که در عدد درست **۰** می‌شود، و ۰ × ۱۰۰ = **۰**! با ضرب پیش از تقسیم، ۱۰٬۰۰۰٬۰۰۰ ÷ ۵۰۰٬۰۰۰ = ۲۰. برای درصدهای اعشاری، `awk` را به کار ببرید.

</div>
