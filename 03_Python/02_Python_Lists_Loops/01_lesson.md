<div dir="rtl">

# درس: فهرست، حلقه، شرط و دیکشنری

**بخش:** `03_Python` · **ماژول:** `02_Python_Lists_Loops` · **پیش‌نیاز:** ماژول [نخستین گام‌ها](../01_Python_Start/) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** Python 3.13 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. چند مقدار را در یک **فهرست** (list) نگه دارید، بیفزایید، مرتب کنید و جمع و میانگین بگیرید.
2. با **حلقه‌ی `for`** روی یک فهرست یا روی بازهای یک توالی بگردید، و با `range` توالی را **کدون به کدون** ببرید.
3. با **`if` / `elif` / `else`** تصمیم بگیرید.
4. با **دیکشنری** (dict) چیزها را بشمارید و یک **جدول کد ژنتیکی** بسازید.
5. یک توالی DNA را با کد خودتان **ترجمه** کنید.

همه‌ی کدها را در پایتون تعاملی (`python3`، پس از `conda activate bioinfo_course`) بنویسید.

---

## ۱. داستان: از یک توالی به چند ژن

در ماژول پیشین با **یک** توالی کار کردیم. ولی پرسش‌های واقعی درباره‌ی **چندین** چیزند: «میانگین طول این ژن‌ها چقدر است؟»، «هر باز چند بار آمده؟»، «این توالی به چه پروتئینی ترجمه می‌شود؟». برای این‌ها سه ابزار لازم است:
- **فهرست:** چند مقدار، به ترتیب.
- **حلقه:** یک کار برای هر مقدار (همان `for` بخش ۰۱، با نوشتاری دیگر).
- **دیکشنری:** جفت‌های «کلید ← مقدار»، مانند «کدون ← اسیدآمینه».

---

## ۲. فهرست (list)

<div dir="ltr">

```python
>>> genes = ["rpoA", "rpoB", "rpoC"]
>>> lengths = [990, 4029, 4224]
>>> len(genes)
3
>>> genes[1]
'rpoB'
>>> genes[-1]
'rpoC'
```

</div>

**فهرست** چند مقدار را درون `[ ]` و جداشده با ویرگول نگه می‌دارد. شماره‌گذاری مانند رشته **از ۰** است. `genes[1]` دومین ژن است.

### افزودن و دیدن

<div dir="ltr">

```python
>>> genes.append("gyrA")
>>> lengths.append(2628)
>>> genes
['rpoA', 'rpoB', 'rpoC', 'gyrA']
>>> lengths
[990, 4029, 4224, 2628]
```

</div>

‏`.append(x)` یک مقدار به **پایان** فهرست می‌افزاید. برخلاف رشته، فهرست **تغییرپذیر** است: خود فهرست عوض می‌شود، بی نیاز به `=` تازه.

### خلاصه‌گیری

<div dir="ltr">

```python
>>> sum(lengths)
11871
>>> min(lengths), max(lengths)
(990, 4224)
>>> sum(lengths) / len(lengths)
2967.75
>>> sorted(lengths)
[990, 2628, 4029, 4224]
>>> sorted(genes)
['gyrA', 'rpoA', 'rpoB', 'rpoC']
>>> "rpoB" in genes
True
>>> genes.index("gyrA")
3
```

</div>

| تابع یا متد | کار |
| :--- | :--- |
| `sum(L)` / `min(L)` / `max(L)` | جمع / کمینه / بیشینه |
| `sum(L) / len(L)` | میانگین |
| `sorted(L)` | **نسخه‌ی مرتب‌شده** (عدد: کوچک به بزرگ؛ متن: الفبایی). خود `L` عوض نمی‌شود |
| `x in L` | آیا x در فهرست هست؟ |
| `L.index(x)` | شماره‌ی x در فهرست |

(دو مقدار با ویرگول، مانند `min(L), max(L)`، با هم در پرانتز نشان داده می‌شوند؛ به آن **تاپل** می‌گویند.)

> 📺 **فیلم:** *Python Tutorial for Beginners 4: Lists, Tuples, and Sets*: https://www.youtube.com/watch?v=W8KRzm-HUcc (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۵.۱ (More on Lists): https://docs.python.org/3/tutorial/datastructures.html

---

## ۳. حلقه‌ی `for`

### روی یک فهرست

<div dir="ltr">

```python
>>> for g in genes:
...     print(g)
...
rpoA
rpoB
rpoC
gyrA
```

</div>

#### کالبدشکافی

<div dir="ltr">

```text
for   g   in   genes   :
 ①    ②   ③     ④      ⑤
    print(g)           ⑥
```

</div>

| بخش | یعنی |
| :-: | :--- |
| ① ③ | ‏`for … in`: «برای هر … در …» |
| ② | **متغیر حلقه**: در هر دور، یکی از مقدارهای فهرست |
| ④ | فهرستی که روی آن می‌گردیم |
| ⑤ | **دونقطه**: پایان سرآیند حلقه (اجباری) |
| ⑥ | **بدنه**، با **۴ فاصله فرورفته**. هر خطی که فرورفته باشد جزو حلقه است |

**فرورفتگی در پایتون معنا دارد.** در Bash بدنه میان `do` و `done` بود؛ در پایتون، بدنه هر چیزی است که **فرورفته** است. پایان فرورفتگی یعنی پایان حلقه. در پایتون تعاملی، پس از بدنه یک Enter خالی بزنید تا حلقه اجرا شود (`...` خالی).

### دو فهرست با هم: `zip`

<div dir="ltr">

```python
>>> for g, n in zip(genes, lengths):
...     print(g, n, n // 3 - 1)
...
rpoA 990 329
rpoB 4029 1342
rpoC 4224 1407
gyrA 2628 875
```

</div>

‏`zip` دو فهرست را **جفت‌جفت** کنار هم می‌گذارد: در هر دور، `g` یک ژن و `n` طول همان ژن است. `n // 3 - 1` شمار اسیدآمینه‌هاست (کدون‌ها منهای کدون پایان): **RpoB با ۱٬۳۴۲**، همان عدد UniProt (بخش ۰۰). ✓

### روی یک توالی، کدون به کدون: `range`

<div dir="ltr">

```python
>>> list(range(0, 12, 3))
[0, 3, 6, 9]
>>> for i in range(0, 12, 3):
...     print(i, dna[i:i+3])
...
0 ATG
3 GTT
6 TAC
9 TCC
```

</div>

‏(`dna` همان ۶۰ باز آغاز rpoB ماژول پیشین است؛ اگر پایتون را بسته‌اید، دوباره بسازیدش.)

| ‏`range(آغاز، پایان، گام)` | عددها |
| :--- | :--- |
| `range(0, 12, 3)` | ۰، ۳، ۶، ۹ (پایان، یعنی ۱۲، جزو آن نیست؛ مانند تکه‌برداری) |
| `range(5)` | ۰ تا ۴ |
| `range(0, len(dna), 3)` | آغاز هر کدون در کل توالی |

### ساختن یک فهرست در حلقه

<div dir="ltr">

```python
>>> codons = []
>>> for i in range(0, len(dna), 3):
...     codons.append(dna[i:i+3])
...
>>> len(codons)
20
>>> codons[:5]
['ATG', 'GTT', 'TAC', 'TCC', 'TAT']
```

</div>

الگوی رایج: **یک فهرست خالی (`[]`)، سپس در حلقه `.append`**. ۶۰ باز = ۲۰ کدون.

> 📺 **فیلم:** *Python Tutorial for Beginners 7: Loops and Iterations*: https://www.youtube.com/watch?v=6iF8Xb7Z3wQ (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۴.۲ (`for` Statements): https://docs.python.org/3/tutorial/controlflow.html

---

## ۴. تصمیم: `if`، `elif`، `else`

<div dir="ltr">

```python
>>> for n in lengths:
...     if n > 4000:
...         print(n, "long")
...     elif n > 2000:
...         print(n, "medium")
...     else:
...         print(n, "short")
...
990 short
4029 long
4224 long
2628 medium
```

</div>

#### کالبدشکافی

| بخش | یعنی |
| :--- | :--- |
| ‏`if شرط:` | اگر شرط درست است، بدنه‌ی فرورفته‌اش اجرا شود |
| ‏`elif شرط:` | «وگرنه، اگر…»؛ تنها اگر شرط‌های پیشین نادرست بودند |
| `else:` | «وگرنه»؛ هیچ‌کدام درست نبود |

نخستین شرطی که درست باشد اجرا می‌شود و بقیه نادیده می‌مانند. **فرورفتگی دوگانه:** بدنه‌ی `if` درون حلقه است، پس ۸ فاصله فرورفته است.

| سنجش | یعنی |
| :--- | :--- |
| `==` / `!=` | برابر / نابرابر (یک `=` یعنی «بگذار»؛ مانند `awk`) |
| `<` `>` `<=` `>=` | کوچک‌تر، بزرگ‌تر… |
| `and` / `or` / `not` | و / یا / نه |
| `x in L` | عضویت |

> 📺 **فیلم:** *Python Tutorial for Beginners 6: Conditionals and Booleans*: https://www.youtube.com/watch?v=DZwmZ8Usvnk (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۴.۱ (`if` Statements): https://docs.python.org/3/tutorial/controlflow.html

---

## ۵. دیکشنری (dict)

**دیکشنری** جفت‌های **کلید ← مقدار** را نگه می‌دارد، مانند یک فرهنگ لغت: «واژه ← معنی». با کلید، مقدار را بی‌درنگ پیدا می‌کنید.

### شمردن بازها

<div dir="ltr">

```python
>>> counts = {}
>>> for base in dna:
...     if base in counts:
...         counts[base] = counts[base] + 1
...     else:
...         counts[base] = 1
...
>>> counts
{'A': 21, 'T': 17, 'G': 11, 'C': 11}
>>> counts["G"]
11
>>> counts.get("N", 0)
0
```

</div>

### دنبال کردن دور به دور (چهار باز نخست: `A T G G`)

| دور | `base` | پیش از دور | `base in counts`؟ | پس از دور |
| :-: | :-: | :--- | :-: | :--- |
| ۱ | A | `{}` | نه | `{'A': 1}` |
| ۲ | T | `{'A': 1}` | نه | `{'A': 1, 'T': 1}` |
| ۳ | G | `{'A': 1, 'T': 1}` | نه | `{…, 'G': 1}` |
| ۴ | G | `{…, 'G': 1}` | **بله** | `{…, 'G': 2}` |

| نوشتن | یعنی |
| :--- | :--- |
| `{}` | دیکشنری خالی |
| `d[key] = value` | بگذار (یا عوض کن) |
| `d[key]` | مقدار این کلید؛ اگر نباشد **خطا** (`KeyError`) |
| `d.get(key, 0)` | مقدار این کلید، یا `0` اگر نباشد (بی خطا) |
| `key in d` | آیا این کلید هست؟ |
| `d.items()` | همه‌ی جفت‌ها، برای حلقه |

‏`for base in dna` روی **نویسه‌های** یک رشته می‌گردد: یک باز در هر دور.

### چاپ مرتب

<div dir="ltr">

```python
>>> for base, n in sorted(counts.items()):
...     print(base, n)
...
A 21
C 11
G 11
T 17
```

</div>

> 📺 **فیلم:** *Python Tutorial for Beginners 5: Dictionaries*: https://www.youtube.com/watch?v=daefaLgNkw0 (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۵.۵ (Dictionaries): https://docs.python.org/3/tutorial/datastructures.html

---

## ۶. جدول کد ژنتیکی و ترجمه

یک دیکشنری کوچک «کدون ← اسیدآمینه»:

<div dir="ltr">

```python
>>> code = {"ATG": "M", "GTT": "V", "TAC": "Y", "TCC": "S", "TAT": "Y"}
>>> code["ATG"]
'M'
>>> protein = ""
>>> for c in codons[:5]:
...     protein = protein + code[c]
...
>>> protein
'MVYSY'
```

</div>

**این خروجی یعنی:** پنج کدون نخست rpoB به `MVYSY` ترجمه شد، همان آغاز پروتئین RpoB. `protein = protein + …` رشته را دور به دور بلندتر می‌کند (مانند `s+=l` در `awk`).

### جدول کامل: ۶۴ کدون با سه حلقه‌ی تودرتو

نوشتن ۶۴ کدون با دست خسته‌کننده است. جدول کد ژنتیکی یک **الگو** دارد: اگر بازها را به ترتیب `T C A G` بچینیم، اسیدآمینه‌ها این رشته‌ی ۶۴ نویسه‌ای‌اند (`*` = پایان):

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
```

</div>

سه حلقه‌ی **تودرتو**: برای هر باز یکم، هر باز دوم، و هر باز سوم، یک کدون (`TTT`، `TTC`، …، `GGG`) ساخته و به حرف هم‌شماره‌اش در `amino` وصل می‌شود. ۴ × ۴ × ۴ = **۶۴** کدون. حالا کل ۶۰ باز:

<div dir="ltr">

```python
protein = ""
for i in range(0, len(dna), 3):
    protein = protein + code[dna[i:i+3]]
print(protein)
```

</div>

<div dir="ltr">

```text
MVYSYTEKKRIRKDFGKRPQ
```

</div>

**همان ۲۰ اسیدآمینه‌ی بخش ۰۰**، این بار با کد خودتان. ✓ (در ماژول ۰۴، Biopython همین کار را با یک فرمان می‌کند، ولی اکنون می‌دانید درونش چه می‌گذرد.)

<details>
<summary>✋ <b>امتحان کن:</b> در جدول کامل، <code>code["CAC"]</code> و <code>code["TAC"]</code> چیست؟ این دو کدون در داستان دوره چه نقشی دارند؟</summary>

‏`code["CAC"]` = `'H'` (هیستیدین) و `code["TAC"]` = `'Y'` (تیروزین). این همان جهش **H526Y** است که در بخش ۰۲ در VCF «سویه‌ی مقاوم» پیدا کردیم: کدون ۵۲۶ rpoB از `CAC` به `TAC`.
</details>

> 📺 **فیلم:** *From DNA to RNA to Protein using Biopython*: https://www.youtube.com/watch?v=HzRyytIasFg (Lana Dominkovic)
> 📄 **مرجع:** NCBI, The Genetic Codes: https://www.ncbi.nlm.nih.gov/Taxonomy/Utils/wprintgc.cgi

---

## ۷. سه اشتباه رایج (با پیام واقعی)

### اشتباه ۱: فرورفتگی فراموش‌شده: `IndentationError`

<div dir="ltr">

```python
for g in ["rpoA", "rpoB"]:
print(g)
```

</div>

<div dir="ltr">

```text
IndentationError: expected an indented block after 'for' statement on line 1
```

</div>

بدنه‌ی حلقه باید فرورفته باشد. **همیشه ۴ فاصله** (نه Tab؛ و هرگز ترکیب این دو).

### اشتباه ۲: دونقطه‌ی فراموش‌شده: `SyntaxError`

<div dir="ltr">

```text
    for g in ["rpoA", "rpoB"]
                             ^
SyntaxError: expected ':'
```

</div>

پایان سرآیند `for`، `if`، `elif` و `else` همیشه `:` است.

### اشتباه ۳: کلیدی که نیست: `KeyError`

<div dir="ltr">

```python
code = {"ATG": "M"}
print(code["TAA"])
```

</div>

<div dir="ltr">

```text
KeyError: 'TAA'
```

</div>

کدون `TAA` در این دیکشنری کوچک نیست. یا جدول را کامل کنید، یا `code.get("TAA", "?")` بنویسید. (همانند آن، `lengths[2]` روی فهرست دوعضوی `IndexError: list index out of range` می‌دهد.)

---

## ۸. جمع‌بندی

- **فهرست** `[…]`: شماره از ۰، `.append`، `len`، `sum/min/max`، `sorted`، `in`.
- ‏**`for x in …:`** با بدنه‌ی فرورفته؛ `zip` برای دو فهرست با هم؛ `range(0, len(s), 3)` برای کدون‌ها.
- ‏**`if / elif / else`** با `==`، `!=`، `<`، `>`، `and`، `or`، `in`.
- **دیکشنری** `{کلید: مقدار}`: `d[k]`، `d[k] = v`، `d.get(k, 0)`، `k in d`، `d.items()`؛ الگوی شمردن.
- جدول کد ژنتیکی = دیکشنری ۶۴تایی؛ ترجمه = حلقه روی کدون‌ها.
- خطاها: `IndentationError`، `SyntaxError: expected ':'`، `KeyError`، `IndexError`.

---

## کارت دستورهای این درس

| می‌خواهم… | پایتون |
| :--- | :--- |
| فهرست | `L = [990, 4029]` |
| افزودن | `L.append(2628)` |
| میانگین | `sum(L) / len(L)` |
| نسخه‌ی مرتب | `sorted(L)` |
| حلقه روی فهرست | `for x in L:` |
| حلقه روی دو فهرست | `for a, b in zip(A, B):` |
| حلقه روی کدون‌ها | `for i in range(0, len(s), 3): s[i:i+3]` |
| تصمیم | `if … : … elif … : … else: …` |
| شمردن با دیکشنری | `d[k] = d.get(k, 0) + 1` |
| همه‌ی جفت‌ها، مرتب | `for k, v in sorted(d.items()):` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> نوشتار کوتاه‌تر</summary>

پایتون نوشتارهای کوتاه‌تری هم دارد که در کد دیگران زیاد می‌بینید:

- **شمردن با `.get`** (یک خط به جای چهار): `counts[base] = counts.get(base, 0) + 1`.
- **ساختن فهرست در یک خط** (*list comprehension*): `codons = [dna[i:i+3] for i in range(0, len(dna), 3)]`، همان حلقه‌ی بخش ۳.
- **ساختن دیکشنری با `zip`**: `dict(zip(genes, lengths))` → `{'rpoA': 990, 'rpoB': 4029, …}`.
- ‏**`collections.Counter`**: `Counter(dna)` بازها را در یک فرمان می‌شمارد.

این‌ها کار را کوتاه‌تر می‌کنند، ولی هیچ چیز تازه‌ای نمی‌کنند؛ نخست شکل بلندشان را خوب بفهمید.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| فهرست (list) | مجموعه‌ای مرتب از مقدارها `[…]`، تغییرپذیر |
| حلقه (loop) | تکرار یک کار برای هر عضو یک مجموعه |
| فرورفتگی (indentation) | فاصله‌ی آغاز خط؛ در پایتون مرز بدنه‌ها را تعیین می‌کند |
| شرط (condition) | سنجشی که درست یا نادرست است |
| دیکشنری (dict) | جفت‌های کلید ← مقدار `{…}` |
| کلید (key) | آنچه با آن مقدار را پیدا می‌کنید (مانند کدون) |
| حلقه‌ی تودرتو (nested loop) | حلقه‌ای درون حلقه‌ی دیگر |

---

## منابع

### راهنما و درس رایگان
- آموزش رسمی پایتون، بخش‌های ۴ (More Control Flow Tools) و ۵ (Data Structures): https://docs.python.org/3/tutorial/controlflow.html
- ‏Software Carpentry — *Programming with Python*، درس‌های «Repeating Actions with Loops» و «Storing Multiple Values in Lists»: https://swcarpentry.github.io/python-novice-inflammation/
- Rosalind — Python Village: https://rosalind.info/problems/list-view/?location=python-village

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل‌های ساختارهای داده و کنترل جریان)
- Model ML (2009). *Bioinformatics Programming Using Python*. O'Reilly.

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Python for Genomic Data Science*. هفته‌های ۲ و ۳: https://www.coursera.org/learn/python-genomics

**edX:**
- UC San Diego — *Introduction to Genomic Data Science*: https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- Lana Dominkovic — *From DNA to RNA to Protein using Biopython*: https://www.youtube.com/watch?v=HzRyytIasFg

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی کدها در 2026-10-20 با Python 3.13.15 اجرا شدند. پیام‌های خطا تنها با خط آخرشان (و گاهی خط پیش از آن) آمده‌اند.

</div>
