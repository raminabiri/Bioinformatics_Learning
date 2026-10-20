<div dir="rtl">

# پاسخ تشریحی: فهرست، حلقه، شرط و دیکشنری

> کدها در 2026-10-20 با Python 3.13.15 اجرا شدند. طول ژن‌ها از `ecoli_k12.gff` (بخش ۰۱) است.

---

## تمرین ۱: ژن‌های هدف آنتی‌بیوتیک‌ها

<div dir="ltr">

```python
names = ["rpoA", "rpoB", "rpoC", "gyrA", "gyrB"]
lens = [990, 4029, 4224, 2628, 2415]
print(sum(lens), sum(lens) / len(lens))

longest = names[0]
best = lens[0]
for n, l in zip(names, lens):
    if l > best:
        best = l
        longest = n
print(longest, best)

for n, l in zip(names, lens):
    print(n, l % 3)
```

</div>

<div dir="ltr">

```text
14286 2857.2
rpoC 4224
rpoA 0
rpoB 0
rpoC 0
gyrA 0
gyrB 0
```

</div>

1. جمع **۱۴٬۲۸۶** و میانگین **۲٬۸۵۷٫۲**.
2. ‏**rpoC** با ۴٬۲۲۴ باز.
3. **بله**؛ باقی‌مانده‌ی همه بر ۳ صفر است. هر ژن پروتئین‌ساز از کدون‌های سه‌تایی ساخته شده (همراه با کدون پایان). اگر طول ژنی در آنوتیشن مضرب ۳ نباشد، یا ژن کاذب است یا آنوتیشن خطا دارد (یا یک استثنای زیستی مانند لغزش ریبوزوم).

**اشتباه رایج:** گذاشتن `best = 0` در آغاز درست است؛ ولی `longest = ""` و فراموش کردن عوض کردن هر دو با هم، نام نادرست می‌دهد.

---

## تمرین ۲: ترجمه‌ی آغاز gyrA

<div dir="ltr">

```python
bases = "TCAG"
amino = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
code = {}
i = 0
for b1 in bases:
    for b2 in bases:
        for b3 in bases:
            code[b1 + b2 + b3] = amino[i]
            i = i + 1

g = "ATGAGCGACCTTGCGAGAGAAATTACACCG"
p = ""
for i in range(0, len(g), 3):
    p = p + code[g[i:i+3]]
print(p)
```

</div>

<div dir="ltr">

```text
MSDLAREITP
```

</div>

همان ۱۰ اسیدآمینه‌ای که در ExPASy (بخش ۰۰، قاب ۱) و UniProt دیدیم. ✓

---

## تمرین ۳: شمردن با دیکشنری

<div dir="ltr">

```python
counts = {}
for b in g:
    counts[b] = counts.get(b, 0) + 1
print(counts, (counts["G"] + counts["C"]) / len(g))
```

</div>

<div dir="ltr">

```text
{'A': 10, 'T': 5, 'G': 8, 'C': 7} 0.5
```

</div>

1. ‏A = ۱۰، T = ۵، G = ۸، C = ۷. (ترتیب کلیدها همان ترتیب نخستین دیده شدنشان است.)
2. (۸ + ۷) ÷ ۳۰ = **۰٫۵**، یعنی ۵۰٪؛ همان پاسخ ماژول پیشین با `.count`. ✓

---

## تمرین ۴: سه قاب خواندن

<div dir="ltr">

```python
for frame in [0, 1, 2]:
    prot = ""
    for i in range(frame, len(dna) - 2, 3):
        prot = prot + code[dna[i:i+3]]
    print(frame + 1, prot, prot.count("*"))
```

</div>

<div dir="ltr">

```text
1 MVYSYTEKKRIRKDFGKRPQ 0
2 WFTPIPRKNVFVRILVNVH 0
3 GLLLYREKTYS*GFW*TST 2
```

</div>

1. **قاب ۱**: با `M` آغاز می‌شود و همان آغاز RpoB است.
2. قاب ۱: ۰، قاب ۲: ۰، قاب ۳: **۲** کدون پایان.
3. **نه.** در این ۶۰ باز، قاب ۲ هم کدون پایانی ندارد. در یک تکه‌ی کوتاه، «نبود کدون پایان» کافی نیست؛ آغاز با `M` و سنجش با پروتئین شناخته‌شده لازم است (همان نتیجه‌ی تمرین ۱ ماژول ابزارهای وب). در کل ژن (۱٬۳۴۳ کدون)، قاب‌های نادرست کمابیش همیشه کدون پایان دارند.

**نکته:** `len(dna) - 2` جلوی آن را می‌گیرد که در قاب ۲ و ۳ یک «کدون» ناقص یک یا دو بازی در پایان ساخته شود (که در `code` نیست و `KeyError` می‌داد).

---

## تمرین ۵: مکمل معکوس با دیکشنری

<div dir="ltr">

```python
comp = {"A": "T", "T": "A", "G": "C", "C": "G"}
rc = ""
for b in reversed(g):
    rc = rc + comp[b]
print(rc)
```

</div>

<div dir="ltr">

```text
CGGTGTAATTTCTCTCGCAAGGTCGCTCAT
```

</div>

دقیقاً همان پاسخ `tr 'ACGTacgt' 'TGCAtgca' | rev` در بخش ۰۱. ✓ دو گام `tr` (مکمل) و `rev` (وارونه) این‌جا در یک حلقه انجام شد: وارونه با `reversed`، مکمل با `comp`.

**نکته:** این دیکشنری حروف کوچک یا `N` ندارد؛ برای توالی‌ای مانند `host_chr21_region.fa` باید آن‌ها را هم بیفزایید، وگرنه `KeyError` می‌گیرید.

</div>
