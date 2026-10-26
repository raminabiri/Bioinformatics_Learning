<div dir="rtl">

# درس: تابع و فایل؛ خواندن GFF و FASTA با پایتون

**بخش:** `03_Python` · **ماژول:** `03_Python_Functions_Files` · **پیش‌نیاز:** ماژول [فهرست، حلقه و دیکشنری](../02_Python_Lists_Loops/) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** Python 3.13 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک **تابع** بنویسید (`def`)، به آن ورودی بدهید و نتیجه‌اش را برگردانید (`return`).
2. یک فایل را **خط‌به‌خط** بخوانید (`with open`)، هر خط را به ستون‌ها بشکنید (`split`) و عدد را از متن بسازید (`int`).
3. یک فایل GFF را خلاصه کنید و یک **جدول TSV** بنویسید.
4. یک خواننده‌ی ساده‌ی **FASTA** بنویسید که توالی‌های چندخطی را درست بچسباند.
5. نام فایل را از ترمینال به اسکریپت بدهید (`sys.argv`).

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
cd ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data       # داده‌ی بخش ۰۱
P=~/Bioinformatics_Learning-main/03_Python/99_scripts_data/03_Python_Functions_Files/scripts
```

</div>

---

## ۱. داستان: همان پرسش‌ها، این بار با پایتون

در بخش ۰۱ با `awk` پرسیدیم: «ژنوم چند ژن دارد؟ روی کدام رشته؟ میانگین طولشان؟». حالا همان‌ها را با پایتون می‌پرسیم. چرا دوباره؟ چون در پایتون:
- منطق پیچیده‌تر (چند شرط، چند خروجی، ترجمه، مکمل معکوس) **خوانا** می‌ماند؛
- کدی که یک بار نوشتید، در یک **تابع** دوباره به کار می‌رود؛
- و در ماژول‌های بعد، Biopython و pandas روی همین پایه ساخته می‌شوند.

دو ابزار تازه لازم است: **تابع** و **خواندن فایل**.

---

## ۲. تابع: کدی که نام دارد

در ماژول‌های پیشین، فرمول GC را چند بار نوشتیم. بهتر است آن را یک بار در یک **تابع** بنویسیم:

<div dir="ltr">

```python
>>> def gc_content(seq):
...     """Return the fraction of G and C in a DNA sequence."""
...     gc = seq.count("G") + seq.count("C")
...     return gc / len(seq)
...
>>> gc_content("ATGGTTTAC")
0.3333333333333333
>>> gc_content("GGCC")
1.0
```

</div>

### کالبدشکافی

<div dir="ltr">

```text
def  gc_content ( seq ) :
 ①       ②         ③   ④
    """Return the fraction…"""     ⑤
    gc = seq.count("G") + …        ⑥
    return gc / len(seq)           ⑦
```

</div>

| بخش | یعنی |
| :-: | :--- |
| ① | ‏`def`: «یک تابع تعریف کن» (*define*) |
| ② | **نام** تابع |
| ③ | **ورودی** (پارامتر): نامی که درون تابع، به مقدار داده‌شده اشاره می‌کند |
| ④ | دونقطه، و بدنه‌ی فرورفته |
| ⑤ | ‏**docstring**: یک جمله که می‌گوید تابع چه می‌کند (اختیاری، ولی بسیار سودمند) |
| ⑥ | بدنه: کار تابع |
| ⑦ | ‏**`return`**: نتیجه را به کسی که تابع را خوانده **برگردان** |

تعریف کردن تابع کاری انجام **نمی‌دهد**؛ تنها آن را آماده می‌کند. با `gc_content("GGCC")` تابع **خوانده** (اجرا) می‌شود: `seq` درون تابع `"GGCC"` می‌شود و نتیجه، `1.0`، برگردانده می‌شود.

### تابع دوم: مکمل معکوس

<div dir="ltr">

```python
>>> def reverse_complement(seq):
...     comp = {"A": "T", "T": "A", "G": "C", "C": "G", "N": "N"}
...     out = ""
...     for b in reversed(seq):
...         out = out + comp[b]
...     return out
...
>>> reverse_complement("ATGAGC")
'GCTCAT'
```

</div>

همان کد تمرین ۵ ماژول پیشین، که حالا یک نام دارد و هر جا لازم باشد با یک خط به کار می‌رود.

### ‏`return` یا `print`؟

<div dir="ltr">

```python
>>> def show_gc(seq):
...     print(round(gc_content(seq) * 100, 1))
...
>>> r = show_gc("GGCC")
100.0
>>> print(r)
None
```

</div>

‏`show_gc` نتیجه را **چاپ** کرد ولی **برنگرداند**؛ پس `r` چیزی ندارد: `None` («هیچ»). **تابعی که نتیجه‌اش باید جای دیگری به کار رود، باید `return` کند.** `print` تنها برای نشان دادن به آدم است. (درون تابع `show_gc`، تابع `gc_content` خوانده شد: تابع‌ها می‌توانند یکدیگر را به کار ببرند.)

> 📺 **فیلم:** *Python Tutorial for Beginners 8: Functions*: https://www.youtube.com/watch?v=9Os0o3wzS_I (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۴.۸ (Defining Functions): https://docs.python.org/3/tutorial/controlflow.html

---

## ۳. خواندن یک فایل، خط‌به‌خط

<div dir="ltr">

```python
with open("ecoli_k12.gff") as f:
    for line in f:
        …
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `open("ecoli_k12.gff")` | فایل را برای **خواندن** باز کن |
| `with … as f:` | نام فایل باز را `f` بگذار؛ و **پس از پایان بدنه، فایل را خودکار ببند** |
| `for line in f:` | خط‌به‌خط بخوان، **بی** بارگذاری کل فایل در حافظه (مانند `awk`) |

هر `line` یک رشته است، **همراه با نویسه‌ی پایان خط** (`"\n"`) در آخرش.

### شکستن خط به ستون‌ها

<div dir="ltr">

```python
>>> line = "NC_000913.3\tRefSeq\tgene\t190\t255\t.\t+\t.\tID=gene-b0001;Name=thrL\n"
>>> cols = line.rstrip("\n").split("\t")
>>> cols
['NC_000913.3', 'RefSeq', 'gene', '190', '255', '.', '+', '.', 'ID=gene-b0001;Name=thrL']
>>> cols[2]
'gene'
>>> int(cols[4]) - int(cols[3]) + 1
66
```

</div>

‏(`\t` در رشته‌ی پایتون یعنی Tab، و `\n` پایان خط.)

| تکه | یعنی |
| :--- | :--- |
| `.rstrip("\n")` | پایان‌خط را از سمت راست بردار (*right strip*) |
| `.split("\t")` | رشته را در هر Tab بشکن و یک **فهرست** بساز؛ مانند `awk -F'\t'` |
| `cols[2]` | ستون **سوم** (شماره از ۰!)؛ در `awk` این `$3` بود |
| `int("190")` | رشته‌ی `"190"` را به **عدد** ۱۹۰ تبدیل کن |

| awk | پایتون |
| :--- | :--- |
| `$1` | `cols[0]` |
| `$3` | `cols[2]` |
| `$5-$4+1` | `int(cols[4]) - int(cols[3]) + 1` |

**ستون‌ها رشته‌اند، نه عدد**، حتی وقتی عدد به نظر می‌رسند. پیش از حساب، `int()` لازم است (بخش ۷).

> 📺 **فیلم:** *Python Tutorial: File Objects, Reading and Writing to Files*: https://www.youtube.com/watch?v=Uh2ebFW8OYM (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۷.۲ (Reading and Writing Files): https://docs.python.org/3/tutorial/inputoutput.html

---

## ۴. یک اسکریپت کامل: خلاصه‌ی GFF

اسکریپت [gff_genes.py](../99_scripts_data/03_Python_Functions_Files/scripts/gff_genes.py):

<div dir="ltr">

```python
# gff_genes.py: read a GFF file line by line and summarise its genes
# Usage: python3 gff_genes.py ecoli_k12.gff
import sys

gff_file = sys.argv[1]

n_genes = 0
strands = {}
total_length = 0
rpo_genes = []

with open(gff_file) as f:
    for line in f:
        if line.startswith("#"):          # skip comment lines
            continue
        cols = line.rstrip("\n").split("\t")
        if cols[2] != "gene":             # keep only gene lines
            continue
        start = int(cols[3])
        end = int(cols[4])
        strand = cols[6]
        n_genes = n_genes + 1
        total_length = total_length + (end - start + 1)
        strands[strand] = strands.get(strand, 0) + 1
        if "Name=rpo" in cols[8]:
            rpo_genes.append(start)

print("genes:", n_genes)
print("strands:", strands)
print(f"mean length: {total_length / n_genes:.1f}")
print("rpo genes start at:", rpo_genes)
```

</div>

<div dir="ltr">

```bash
python3 $P/gff_genes.py ecoli_k12.gff
```

</div>

<div dir="ltr">

```text
genes: 4506
strands: {'+': 2216, '-': 2290}
mean length: 897.4
rpo genes start at: [2709437, 2866559, 3213047, 3344717, 3440040, 3599929, 3822106, 4181245, 4185350]
```

</div>

**همان عددهای بخش ۰۱** (۴٬۵۰۶ ژن، ۲٬۲۱۶ و ۲٬۲۹۰، میانگین ۸۹۷٫۴)، و جای آغاز ۹ ژن rpo (۴٬۱۸۱٬۲۴۵ همان rpoB است). اجرا کمتر از یک دهم ثانیه طول کشید.

### کالبدشکافی بخش‌های تازه

| تکه | یعنی |
| :--- | :--- |
| `import sys` | کتابخانه‌ی `sys` را بیاور (برای `sys.argv`) |
| `sys.argv[1]` | **ورودی یکم** اسکریپت از ترمینال؛ همان `$1` در Bash. (`sys.argv[0]` نام خود اسکریپت است) |
| `line.startswith("#")` | آیا خط با `#` آغاز می‌شود؟ |
| `continue` | «بقیه‌ی این دور را رها کن و به خط بعد برو»؛ همان `next` در `awk` |
| `cols[2] != "gene"` | نوع خط `gene` **نیست**؟ |
| `strands.get(strand, 0) + 1` | الگوی شمردن ماژول پیشین |
| `"Name=rpo" in cols[8]` | آیا ستون ۹ این متن را دارد؟ |

**ساختار رایج اسکریپت‌های بیوانفورماتیک:** (۱) ورودی‌ها، (۲) متغیرهای خالی برای نتیجه، (۳) حلقه روی خط‌ها با **گزینش زودهنگام** (`continue`)، (۴) چاپ خلاصه.

---

## ۵. نوشتن یک فایل: جدول TSV

<div dir="ltr">

```python
with open("genes.tsv", "w") as out:
    out.write("name\tstart\tend\tstrand\tlength\n")
    …
    out.write(f"{name}\t{start}\t{end}\t{strand}\t{end - start + 1}\n")
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `open(…, "w")` | برای **نوشتن** باز کن (*write*). ⚠️ مانند `>` در Bash، فایل پیشین **پاک** می‌شود |
| `out.write(…)` | این رشته را در فایل بنویس. **`\n` را خودتان بگذارید**؛ `write` برخلاف `print` به خط بعد نمی‌رود |

اسکریپت [gene_table.py](../99_scripts_data/03_Python_Functions_Files/scripts/gene_table.py) همین کار را برای همه‌ی ژن‌ها می‌کند. یک تابع کمکی هم دارد که **نام ژن** را از ستون ۹ بیرون می‌کشد:

<div dir="ltr">

```python
def get_attribute(attributes, key):
    """From a GFF column 9 like 'ID=x;Name=rpoB;...' return the value of key, or '' if absent."""
    for part in attributes.split(";"):
        if part.startswith(key + "="):
            return part[len(key) + 1:]
    return ""
```

</div>

ستون ۹ را در `;` می‌شکند؛ تکه‌ای را که با `Name=` آغاز می‌شود پیدا می‌کند؛ و بقیه‌اش را (پس از `Name=`) برمی‌گرداند. اگر نبود، رشته‌ی خالی. **یک تابع می‌تواند چند `return` داشته باشد؛ نخستین `return`ی که اجرا شود، تابع را پایان می‌دهد.**

<div dir="ltr">

```bash
python3 $P/gene_table.py ecoli_k12.gff genes.tsv
head -n 4 genes.tsv
grep -P '^gyrA\t' genes.tsv
```

</div>

<div dir="ltr">

```text
wrote 4506 genes to genes.tsv
name	start	end	strand	length
thrL	190	255	+	66
thrA	337	2799	+	2463
thrB	2801	3733	+	933
gyrA	2336793	2339420	-	2628
```

</div>

یک جدول تمیز، که `cut`، `sort`، `awk` و (در ماژول ۰۶) pandas آن را می‌فهمند. این‌جا Bash و پایتون کنار هم کار کردند: پایتون جدول را ساخت و `grep` در آن جستجو کرد.

---

## ۶. یک خواننده‌ی ساده‌ی FASTA

‏FASTA چندخطی است: یک توالی در چندین خط. باید خط‌ها را **بچسبانیم**؛ همان کاری که در بخش ۰۱ با `tr -d '\n'` کردیم. اسکریپت [fasta_gc.py](../99_scripts_data/03_Python_Functions_Files/scripts/fasta_gc.py):

<div dir="ltr">

```python
def read_fasta(path):
    """Return a dictionary {sequence id: sequence} for a FASTA file."""
    seqs = {}
    name = None
    with open(path) as f:
        for line in f:
            line = line.rstrip("\n")
            if line.startswith(">"):
                name = line[1:].split()[0]    # the identifier: first word after '>'
                seqs[name] = []
            else:
                seqs[name].append(line)
    result = {}
    for name in seqs:
        result[name] = "".join(seqs[name])   # glue the lines of each sequence together
    return result
```

</div>

### خط‌به‌خط

| خط | کار |
| :--- | :--- |
| `if line.startswith(">")` | خط عنوان است: |
| `line[1:].split()[0]` | `>` را بردار (`[1:]`)، در **فاصله** بشکن (`split()` بی ورودی = هر فاصله‌ای)، و واژه‌ی یکم را بگیر: **شناسه** |
| `seqs[name] = []` | برای این توالی یک فهرست خالی بساز |
| `else: seqs[name].append(line)` | خط توالی است: به فهرست توالی **کنونی** بیفزا |
| ‏`"".join(فهرست)` | همه‌ی تکه‌های فهرست را **بی جداکننده** به هم بچسبان (`"-".join(["a","b"])` می‌شد `"a-b"`) |

<div dir="ltr">

```bash
python3 $P/fasta_gc.py ecoli_k12.fna host_chr21_region.fa
```

</div>

<div dir="ltr">

```text
ecoli_k12.fna	NC_000913.3	4641652	50.79
host_chr21_region.fa	chr21part	500000	40.05
```

</div>

**همان طول‌ها و درصد GC بخش‌های ۰۱ و ۰۲** (`seqkit fx2tab`). تابع `gc_content` این اسکریپت حروف کوچک را بزرگ می‌کند (`.upper()`) و GC را تنها بر پایه‌ی A، C، G و T حساب می‌کند، پس `N`ها و حروف کوچک کروموزوم ۲۱ دردسری نمی‌سازند. `sys.argv[1:]` یعنی «همه‌ی ورودی‌ها از یکم به بعد»، پس اسکریپت هر شمار فایل را می‌پذیرد.

<details>
<summary>✋ <b>امتحان کن:</b> اگر <code>read_fasta</code> را روی یک فایل با سه توالی اجرا کنید، دیکشنری چند کلید دارد؟ اگر دو توالی شناسه‌ی یکسان داشته باشند چه می‌شود؟</summary>

سه کلید، یکی برای هر شناسه. اگر دو توالی **شناسه‌ی یکسان** داشته باشند، دومی با `seqs[name] = []` فهرست اولی را **پاک** می‌کند و تنها توالی دوم می‌ماند، بی هیچ پیام خطایی. برای همین شناسه‌های یک FASTA باید یکتا باشند.
</details>

---

## ۷. سه اشتباه رایج (با پیام واقعی)

### اشتباه ۱: حساب با ستون‌های متنی

<div dir="ltr">

```python
cols = "NC_000913.3\tRefSeq\tgene\t190\t255".split("\t")
print(cols[4] - cols[3] + 1)
```

</div>

<div dir="ltr">

```text
TypeError: unsupported operand type(s) for -: 'str' and 'str'
```

</div>

`"255" - "190"`: دو رشته را نمی‌شود از هم کم کرد. `int(cols[4]) - int(cols[3]) + 1`.

### اشتباه ۲: فراموش کردن ورودی یا نام نادرست فایل

<div dir="ltr">

```bash
python3 $P/gff_genes.py
python3 $P/gff_genes.py nofile.gff
```

</div>

<div dir="ltr">

```text
IndexError: list index out of range
FileNotFoundError: [Errno 2] No such file or directory: 'nofile.gff'
```

</div>

(آخرین خط هر پیام.) بی ورودی، `sys.argv` تنها نام اسکریپت را دارد و `sys.argv[1]` نیست (`IndexError`). با نام نادرست، `open` فایل را پیدا نمی‌کند. (وارسی ورودی‌ها با پیام روشن، مانند `count_reads.sh` بخش ۰۱، در پایتون هم شدنی است؛ کادر کنجکاوها.)

### اشتباه ۳: فراموش کردن `return`

<div dir="ltr">

```python
def gc_content(seq):
    gc = seq.count("G") + seq.count("C")
    gc / len(seq)
print(gc_content("GGCC"))
```

</div>

<div dir="ltr">

```text
None
```

</div>

حساب انجام شد، ولی نتیجه **برگردانده نشد**. هیچ خطایی نیامد؛ تنها `None`. اگر تابعی `None` داد، نخست دنبال `return` بگردید.

---

## ۸. جمع‌بندی

- **تابع:** `def name(param):` + بدنه + `return`؛ docstring با `"""…"""`؛ تعریف کار نمی‌کند، خواندن (`name(x)`) کار می‌کند.
- **خواندن:** `with open(path) as f: for line in f:`؛ `.rstrip("\n")`، `.split("\t")`، `int()`.
- **نوشتن:** `with open(path, "w") as out: out.write(…\n)`.
- **ورودی از ترمینال:** `import sys`، `sys.argv[1]`، `sys.argv[1:]`.
- ‏`continue` برای رد کردن خط‌های ناخواسته؛ `"".join(list)` برای چسباندن تکه‌ها.
- ستون‌ها رشته‌اند تا `int` کنید؛ ستون سوم GFF `cols[2]` است.

---

## کارت دستورهای این درس

| می‌خواهم… | پایتون |
| :--- | :--- |
| تابع | `def f(x):` … `return y` |
| خواندن خط‌به‌خط | `with open(p) as f:` / `for line in f:` |
| پاک کردن پایان‌خط | `line.rstrip("\n")` |
| شکستن در Tab / فاصله | `line.split("\t")` / `line.split()` |
| متن به عدد | `int("190")`، `float("0.5")` |
| رد کردن یک خط | `continue` |
| نوشتن فایل | `with open(p, "w") as out:` / `out.write("…\n")` |
| ورودی‌های اسکریپت | `import sys` / `sys.argv[1]` / `sys.argv[1:]` |
| چسباندن تکه‌ها | `"".join(parts)` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> پیام روشن برای ورودی نادرست، و <code>if __name__ == "__main__"</code></summary>

همان وارسی `count_reads.sh` (بخش ۰۱) در پایتون:

<div dir="ltr">

```python
import sys
if len(sys.argv) != 2:
    sys.exit("Usage: python3 gff_genes.py file.gff")
```

</div>

‏`sys.exit("پیام")` پیام را در stderr چاپ می‌کند و با کد خروج ۱ می‌ایستد.

در اسکریپت‌های بزرگ‌تری که در اینترنت می‌بینید، در بسیاری از موارد این الگو هست:

<div dir="ltr">

```python
def main():
    …

if __name__ == "__main__":
    main()
```

</div>

یعنی «تنها اگر این فایل **مستقیم** اجرا شد، `main` را بخوان». این‌گونه تابع‌های فایل را می‌شود در اسکریپت دیگری با `import` به کار برد، بی آن‌که کل اسکریپت اجرا شود.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| تابع (function) | کدی با نام که ورودی می‌گیرد و نتیجه برمی‌گرداند |
| پارامتر / ورودی (parameter / argument) | نام ورودی در تعریف / مقداری که هنگام خواندن داده می‌شود |
| `return` | برگرداندن نتیجه از تابع |
| `None` | «هیچ»؛ نتیجه‌ی تابعی که `return` ندارد |
| docstring | توضیح تابع، درون `"""…"""` در خط یکم بدنه |
| `with open(…)` | باز کردن فایل که پس از بدنه خودکار بسته می‌شود |
| `sys.argv` | فهرست ورودی‌های اسکریپت از ترمینال |

---

## منابع

### راهنما و درس رایگان
- آموزش رسمی پایتون، بخش ۴.۸ (Defining Functions) و ۷.۲ (Reading and Writing Files): https://docs.python.org/3/tutorial/inputoutput.html
- ‏Software Carpentry — *Programming with Python*، درس‌های «Creating Functions» و «Command-Line Programs»: https://swcarpentry.github.io/python-novice-inflammation/
- ‏Rosalind — Python Village (تمرین‌های «Working with Files»): https://rosalind.info/problems/list-view/?location=python-village

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل‌های تابع و کار با فایل)
- Model ML (2009). *Bioinformatics Programming Using Python*. O'Reilly.

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Python for Genomic Data Science*. هفته‌ی ۴ (تابع‌ها و فایل‌ها): https://www.coursera.org/learn/python-genomics

**edX:**
- UC San Diego — *Introduction to Genomic Data Science*: https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- rebelScience — *Bioinformatics in Python: Intro*: https://www.youtube.com/watch?v=3joOQ3A3KBQ

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی کدها در 2026-10-20 با Python 3.13.15 اجرا شدند.

</div>
