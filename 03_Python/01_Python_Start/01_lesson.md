<div dir="rtl">

# درس: نخستین گام‌ها در پایتون؛ عدد، متغیر و رشته‌ی DNA

**بخش:** `03_Python` · **ماژول:** `01_Python_Start` · **پیش‌نیاز:** بخش [بایولینوکس](../../02_BioLinux/) (به‌ویژه ماژول [Conda](../../02_BioLinux/01_Conda_Bioconda/)) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** Python 3.13 · **آخرین اجرا:** 2026-10-20

---

## در یک نگاه

**این درس برای کسی است که** تا حالا برنامه ننوشته است.

**در پایان این درس می‌توانید:**
1. پایتون را به دو شیوه اجرا کنید: **تعاملی** (`>>>`) و **اسکریپت** (`python3 file.py`).
2. با عددها حساب کنید و مقدارها را در **متغیر** نگه دارید.
3. یک توالی DNA را به‌عنوان **رشته** (string) نگه دارید: طول، تکه‌برداری، شمردن بازها، جایگزینی.
4. نتیجه را با **f-string** مرتب چاپ کنید.
5. پیام‌های خطای رایج پایتون را بخوانید.

**پیش از آغاز:**

<div dir="ltr">

```bash
conda activate bioinfo_course
```

</div>

---

## ۱. داستان: چرا پایتون، پس از Bash؟

در بخش‌های ۰۱ و ۰۲، با Bash و ابزارهای آماده بسیاری کارها را کردیم: شمردن، گزینش، آمار. Bash برای **وصل کردن ابزارها** عالی است. ولی وقتی کار **منطق** می‌خواهد، Bash دشوار می‌شود. برای نمونه:
- «هر ژن را بخوان؛ اگر روی رشته‌ی منفی است، مکمل معکوسش را بگیر؛ ترجمه کن؛ اگر میانه‌اش کدون پایان دارد، نامش را گزارش کن.»

چنین کاری در پایتون چند خط ساده و خواناست. پایتون (کنار R) زبان اصلی بیوانفورماتیک است، و کتابخانه‌ی **Biopython** (ماژول ۰۴) بیشتر فرمت‌های زیستی را می‌شناسد. ولی نخست باید خود زبان را بشناسیم. **در این ماژول، یک توالی DNA همراه ماست: ۶۰ باز نخست rpoB** (بخش ۰۰).

---

## ۲. پایتون تعاملی: یک ماشین‌حساب هوشمند

در ترمینال بنویسید:

<div dir="ltr">

```bash
python3
```

</div>

<div dir="ltr">

```text
Python 3.13.15 | packaged by conda-forge | (main, Sep  2 2026, 22:01:58) [GCC 15.3.0]
…
>>>
```

</div>

(نسخه و تاریخ برای شما ممکن است کمی فرق کنند.) اعلان پایتون **`>>>`** است، نه `$`. یعنی اکنون **پایتون** فرمان‌های شما را می‌خواند، نه Bash. هر چه بنویسید و Enter بزنید، پایتون همان‌جا اجرا می‌کند و نتیجه را نشان می‌دهد. برای بیرون آمدن: `exit()` یا `Ctrl+D`.

⚠️ **دستورهای Bash (`ls`، `cd`…) در `>>>` کار نمی‌کنند**، و دستورهای پایتون در `$`. همیشه به اعلان نگاه کنید.

### حساب

<div dir="ltr">

```python
>>> 4641652 / 1000
4641.652
>>> 4641652 // 1000
4641
>>> 4641652 % 1000
652
>>> 2 ** 10
1024
>>> round(50.7907, 1)
50.8
```

</div>

| نشانه | کار | نمونه |
| :-: | :--- | :--- |
| `+ - * /` | جمع، تفریق، ضرب، تقسیم | `/` همیشه اعشاری می‌دهد: `7 / 2` = `3.5` |
| `//` | تقسیم **درست** (بی اعشار) | `7 // 2` = `3`؛ همان `$(( ))` در Bash |
| `%` | **باقی‌مانده** | `7 % 2` = `1`؛ همان `%` در `awk` |
| `**` | توان | `2 ** 10` = `1024` |
| `round(x, n)` | گرد کردن به n رقم اعشار | |

برخلاف `$(( ))` در Bash، پایتون اعشار را خودش درست حساب می‌کند.

---

## ۳. متغیر

<div dir="ltr">

```python
>>> genome_length = 4641652
>>> read_length = 150
>>> coverage = 30
>>> genome_length * coverage / read_length
928330.4
```

</div>

همان حساب درس «بیوانفورماتیک چیست؟» (بخش ۰۰): برای پوشش ۳۰ برابر، نزدیک به ۹۲۸ هزار رید لازم است.

### کالبدشکافی

| تکه | یعنی |
| :--- | :--- |
| `genome_length` | **نام** متغیر: حروف انگلیسی، عدد و `_`؛ با عدد آغاز نشود. به شیوه‌ی پایتون، واژه‌ها را با `_` جدا می‌کنیم |
| `=` | «این مقدار را در این نام بگذار». **برخلاف Bash، فاصله دو سوی `=` آزاد است** |
| `4641652` | **مقدار** |

پس از ساختن، **بی `$`** به کار می‌رود: `genome_length`، نه `$genome_length`.

| | Bash | پایتون |
| :--- | :--- | :--- |
| ساختن | ‏`n=5` (بی فاصله) | `n = 5` |
| به کار بردن | `$n` | `n` |
| حساب | `$((n * 2))` | `n * 2` |

> 📺 **فیلم:** *Bioinformatics in Python: Intro*: https://www.youtube.com/watch?v=3joOQ3A3KBQ (rebelScience)
> 📄 **مرجع:** The Python Tutorial, بخش ۳ (An Informal Introduction to Python): https://docs.python.org/3/tutorial/introduction.html

---

## ۴. رشته: DNA در پایتون

یک **رشته** (string، `str`) متنی است درون نقل‌قول (تکی یا دوتایی؛ هر دو یکسان‌اند). یک توالی DNA برای پایتون تنها یک رشته است:

<div dir="ltr">

```python
>>> dna = "ATGGTTTACTCCTATACCGAGAAAAAACGTATTCGTAAGGATTTTGGTAAACGTCCACAA"
>>> len(dna)
60
```

</div>

‏`len()` طول را می‌دهد (*length*): ۶۰ باز.

### شماره‌ی هر باز: از ۰

<div dir="ltr">

```python
>>> dna[0]
'A'
>>> dna[1]
'T'
>>> dna[-1]
'A'
```

</div>

| نوشتن | یعنی |
| :--- | :--- |
| `dna[0]` | **نخستین** نویسه. پایتون از **۰** می‌شمارد، درست مانند BED (بخش ۰۲) |
| `dna[1]` | دومین |
| `dna[-1]` | **آخرین** (عدد منفی یعنی از پایان) |

خروجی‌ها درون نقل‌قول تکی‌اند (`'A'`): پایتون تعاملی این‌گونه نشان می‌دهد که نتیجه یک **رشته** است.

### تکه‌برداری (slicing)

<div dir="ltr">

```python
>>> dna[0:3]
'ATG'
>>> dna[3:6]
'GTT'
>>> dna[:12]
'ATGGTTTACTCC'
>>> dna[-3:]
'CAA'
```

</div>

#### کالبدشکافی `dna[0:3]`

<div dir="ltr">

```text
 نویسه:   A   T   G   G   T   T
 مرز:    0   1   2   3   4   5   6
         └───────────┘
           dna[0:3] = 'ATG'
```

</div>

`[آغاز:پایان]` از **مرز** آغاز تا **مرز** پایان: آغاز **جزو** تکه است و پایان **نه**. درست همان «نیمه‌باز» BED. پس:
- طول تکه = پایان − آغاز (۳ − ۰ = ۳).
- ‏`dna[0:3]` کدون یکم، `dna[3:6]` کدون دوم، و کدون n ام: `dna[3*(n-1) : 3*n]`.
- اگر آغاز را ننویسید (`dna[:12]`)، از اول؛ اگر پایان را ننویسید (`dna[-3:]`)، تا آخر.

**تبدیل مختصات GFF به پایتون:** ژنی که در GFF از `start` تا `end` است (شماره از ۱، دوسر بسته)، در پایتون `genome[start-1 : end]` است؛ همان قاعده‌ی «آغاز − ۱» برای BED.

<details>
<summary>✋ <b>امتحان کن:</b> کدون دهم این توالی چیست؟ (یادتان باشد شماره از ۰ است.)</summary>

کدون دهم: `dna[27:30]` (۳ × ۹ = ۲۷ تا ۳ × ۱۰ = ۳۰). در پایتون بنویسید `dna[27:30]`؛ پاسخ `'CGT'` (آرژینین، R؛ دهمین اسیدآمینه‌ی `MVYSYTEKKR`).
</details>

### کارهای رشته: متدها

رشته‌ها **متد** دارند: کارهایی که با `.نام()` پس از رشته نوشته می‌شوند.

<div dir="ltr">

```python
>>> dna.count("A")
21
>>> dna.count("G") + dna.count("C")
22
>>> dna.lower()
'atggtttactcctataccgagaaaaaacgtattcgtaaggattttggtaaacgtccacaa'
>>> dna.replace("T", "U")
'AUGGUUUACUCCUAUACCGAGAAAAAACGUAUUCGUAAGGAUUUUGGUAAACGUCCACAA'
>>> dna.find("TAC")
6
>>> dna.startswith("ATG")
True
>>> "GAATTC" in dna
False
```

</div>

| متد | کار | در این‌جا |
| :--- | :--- | :--- |
| `.count("A")` | شمار رخدادها | ۲۱ آدنین |
| `.lower()` / `.upper()` | حروف کوچک / بزرگ | |
| `.replace("T", "U")` | جایگزینی | **رونویسی**: DNA به mRNA |
| `.find("TAC")` | جای نخستین رخداد (**از ۰**)؛ اگر نبود، `-1` | ۶، یعنی باز هفتم |
| `.startswith("ATG")` | آیا با این آغاز می‌شود؟ | ‏`True` (درست) |
| `"X" in dna` | آیا X درون رشته هست؟ | ‏`False` (نادرست): EcoRI در این ۶۰ باز نیست |

‏`True` و `False` دو مقدار ویژه‌ی پایتون‌اند: «درست» و «نادرست». در ماژول بعد با آن‌ها تصمیم می‌گیریم (`if`).

### درصد GC

<div dir="ltr">

```python
>>> gc = (dna.count("G") + dna.count("C")) / len(dna)
>>> gc
0.36666666666666664
>>> round(gc * 100, 1)
36.7
```

</div>

‏GC این ۶۰ باز **۳۶٫۷٪** است. (رقم‌های بسیار پس از ممیز طبیعی است: کامپیوتر عددهای اعشاری را در مبنای ۲ نگه می‌دارد و برخی را دقیق نمی‌تواند. برای نمایش، گرد کنید.)

---

## ۵. چاپ مرتب: f-string

<div dir="ltr">

```python
>>> name = "rpoB"
>>> f"{name} starts with {dna[:3]} and has GC = {gc:.3f}"
'rpoB starts with ATG and has GC = 0.367'
>>> f"{gc * 100:.1f}%"
'36.7%'
```

</div>

#### کالبدشکافی

| تکه | یعنی |
| :--- | :--- |
| `f"…"` | یک **f-string**: رشته‌ای که `{…}`های درونش اجرا و جایگزین می‌شوند (f = *format*) |
| `{name}` | مقدار متغیر `name` |
| `{dna[:3]}` | هر عبارت پایتون می‌تواند درون `{}` باشد |
| `{gc:.3f}` | ‏`gc` با **۳ رقم اعشار** (همان `%.3f` در `printf`) |

### گونه‌های داده

<div dir="ltr">

```python
>>> type(dna)
<class 'str'>
>>> type(len(dna))
<class 'int'>
>>> type(gc)
<class 'float'>
```

</div>

| گونه | یعنی | نمونه |
| :--- | :--- | :--- |
| `str` | رشته (متن) | `"ATG"` |
| `int` | عدد درست | `60` |
| `float` | عدد اعشاری | `0.367` |
| `bool` | درست یا نادرست | `True` |

‏`"ATG" + "GTT"` دو رشته را **به هم می‌چسباند** (`'ATGGTT'`) و `"AT" * 3` تکرار می‌کند (`'ATATAT'`). ولی **رشته و عدد را نمی‌شود جمع کرد** (بخش ۷).

> 📺 **فیلم:** *Python Tutorial for Beginners 2: Strings*: https://www.youtube.com/watch?v=k9TUPpGqYTo (Corey Schafer)
> 📄 **مرجع:** The Python Tutorial, بخش ۷.۱ (Fancier Output Formatting): https://docs.python.org/3/tutorial/inputoutput.html

---

## ۶. اسکریپت پایتون

کد تعاملی با بستن پایتون از دست می‌رود. همان کد را در یک **فایل** بنویسید. با `nano first.py`:

<div dir="ltr">

```python
# first.py: my first Python script
# The first 60 bases of the rpoB gene of E. coli K-12
dna = "ATGGTTTACTCCTATACCGAGAAAAAACGTATTCGTAAGGATTTTGGTAAACGTCCACAA"

gc = (dna.count("G") + dna.count("C")) / len(dna)
print("length:", len(dna))
print("first codon:", dna[0:3])
print(f"GC content: {gc * 100:.1f}%")
```

</div>

اجرا از **ترمینال** (اعلان `$`، نه `>>>`):

<div dir="ltr">

```bash
python3 first.py
```

</div>

<div dir="ltr">

```text
length: 60
first codon: ATG
GC content: 36.7%
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `# …` | **یادداشت**؛ اجرا نمی‌شود (مانند Bash) |
| `print(a, b)` | چاپ؛ چند مقدار با ویرگول، با یک فاصله میانشان |
| خط خالی | تنها برای خوانایی |

**در اسکریپت، تنها `print` چیزی نشان می‌دهد.** در `>>>`، نوشتن `gc` نتیجه را نشان می‌داد؛ در اسکریپت باید `print(gc)` بنویسید.

---

## ۷. سه اشتباه رایج (با پیام واقعی)

پایتون هنگام خطا یک **Traceback** چاپ می‌کند: چند خط که می‌گوید کجا و چرا. **خط آخر** مهم‌ترین است: نوع خطا و توضیحش. (نشانی فایل‌ها را کوتاه کرده‌ایم.)

### اشتباه ۱: غلط تایپی در نام: `NameError`

<div dir="ltr">

```text
  File "err.py", line 1, in <module>
    print(lenght)
          ^^^^^^
NameError: name 'lenght' is not defined
```

</div>

متغیری به نام `lenght` (به جای `length`) ساخته نشده بود. پایتون جای خطا را با `^^^` نشان می‌دهد. همین خطا اگر نقل‌قول را فراموش کنید هم می‌آید: `"ATG".count(A)` (به جای `"A"`) پیام `name 'A' is not defined` می‌دهد، چون `A` بی نقل‌قول نام یک متغیر شمرده می‌شود.

### اشتباه ۲: جمع رشته و عدد: `TypeError`

<div dir="ltr">

```text
    print("length: " + len(dna))
          ~~~~~~~~~~~^~~~~~~~~~
TypeError: can only concatenate str (not "int") to str
```

</div>

«تنها می‌توانم رشته را به رشته بچسبانم، نه عدد را». راه‌ها: `print("length:", len(dna))` (ویرگول) یا `f"length: {len(dna)}"`.

### اشتباه ۳: شماره‌ای بیرون از رشته: `IndexError`

<div dir="ltr">

```python
dna = "ATG"
print(dna[3])
```

</div>

<div dir="ltr">

```text
IndexError: string index out of range
```

</div>

‏`"ATG"` سه نویسه دارد با شماره‌های **۰، ۱ و ۲**. `dna[3]` نیست. یادتان باشد: آخرین شماره = طول − ۱.

(تکه‌برداری ولی خطا نمی‌دهد: `"ATGGTTTAC"[9:20]` تنها یک رشته‌ی **خالی** `''` می‌دهد. این مهربانی گاهی اشتباه را پنهان می‌کند.)

---

## ۸. جمع‌بندی

- ‏`python3` پایتون تعاملی (`>>>`) را باز می‌کند؛ `python3 file.py` یک اسکریپت را اجرا می‌کند.
- حساب: `+ - * /`، `//` (تقسیم درست)، `%` (باقی‌مانده)، `**`؛ متغیر: `name = value` و سپس `name` (بی `$`).
- رشته: `len()`، شماره از **۰**، `s[i]`، تکه‌برداری نیمه‌باز `s[a:b]` (طول b − a)؛ GFF به پایتون: `[start-1:end]`.
- متدها: `.count`، `.upper/.lower`، `.replace`، `.find`، `.startswith`، و `in`.
- ‏f-string: `f"{x:.2f}"`؛ در اسکریپت، تنها `print` نشان می‌دهد.
- در پیام خطا، خط آخر را بخوانید: `NameError`، `TypeError`، `IndexError`، `SyntaxError`.

---

## کارت دستورهای این درس

| می‌خواهم… | پایتون |
| :--- | :--- |
| پایتون تعاملی / بیرون آمدن | `python3` / `exit()` |
| اجرای اسکریپت | `python3 file.py` |
| متغیر | `dna = "ATG…"` |
| طول | `len(dna)` |
| نخستین / آخرین باز | `dna[0]` / `dna[-1]` |
| کدون n ام | `dna[3*(n-1):3*n]` |
| ژن GFF از start تا end | `genome[start-1:end]` |
| شمار یک باز | `dna.count("G")` |
| ‏DNA به RNA | `dna.replace("T", "U")` |
| آیا الگو هست؟ | `"GAATTC" in dna` |
| چاپ با دو رقم اعشار | `print(f"{x:.2f}")` |
| گونه‌ی یک مقدار | `type(x)` |

---

<details>
<summary>📘 <b>برای کنجکاوها (اختیاری):</b> چرا <code>0.1 + 0.2</code> در پایتون ۰٫۳ نیست؟</summary>

<div dir="ltr">

```python
>>> 0.1 + 0.2
0.30000000000000004
```

</div>

کامپیوتر عددهای اعشاری را در **مبنای ۲** نگه می‌دارد، و ۰٫۱ در مبنای ۲ (مانند ۱/۳ در مبنای ۱۰) بی‌پایان است؛ پس کمی گرد می‌شود. این در **همه‌ی** زبان‌های برنامه‌نویسی هست، نه تنها پایتون. پیامد: عددهای اعشاری را با `==` نسنجید (`0.1 + 0.2 == 0.3` نادرست است)، و برای نمایش گرد کنید. همین بود که در درس `awk` (بخش ۰۱) ۱۱۸۷٫۲۵ به ۱۱۸۷٫۲ گرد شد.
</details>

---

## واژه‌نامه‌ی این درس

| اصطلاح | معنی |
| :--- | :--- |
| مفسر تعاملی (REPL، `>>>`) | پایتونی که هر خط را همان‌جا اجرا می‌کند |
| اسکریپت | فایل `.py` که با `python3 file.py` اجرا می‌شود |
| متغیر | نامی برای یک مقدار |
| رشته (`str`) | متن درون نقل‌قول؛ یک توالی DNA در پایتون |
| شماره (index) | جای هر نویسه، از ۰ |
| تکه‌برداری (slice) | ‏`s[a:b]`: نویسه‌های a تا پیش از b |
| متد (method) | کاری که با `.نام()` روی یک مقدار انجام می‌شود |
| f-string | رشته‌ای با `{…}` برای جای‌گذاری مقدارها |
| Traceback | گزارش خطای پایتون؛ خط آخرش مهم‌ترین است |

---

## منابع

### راهنما و درس رایگان
- آموزش رسمی پایتون (The Python Tutorial)، بخش ۳ (An Informal Introduction to Python): https://docs.python.org/3/tutorial/introduction.html
- Software Carpentry — *Programming with Python*: https://swcarpentry.github.io/python-novice-inflammation/
- ‏Rosalind — Python Village (تمرین‌های گام‌به‌گام پایتون برای زیست‌شناسان): https://rosalind.info/problems/list-view/?location=python-village

### کتاب
- ‏Bassi S (2017). *Python for Bioinformatics*, 2nd ed. CRC Press. (فصل‌های نخست: آغاز کار با پایتون)
- Model ML (2009). *Bioinformatics Programming Using Python*. O'Reilly.

### فیلم‌های آموزشی

**Coursera:**
- ‏Johns Hopkins University — *Python for Genomic Data Science*. هفته‌ی یکم، پایه‌های پایتون: https://www.coursera.org/learn/python-genomics
- UC San Diego — *Biology Meets Programming: Bioinformatics for Beginners*: https://www.coursera.org/learn/bioinformatics

**edX:**
- ‏UC San Diego — *Introduction to Genomic Data Science* (برنامه‌نویسی پایتون برای DNA): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science

**YouTube:**
- rebelScience — *Bioinformatics in Python: Intro*: https://www.youtube.com/watch?v=3joOQ3A3KBQ

> **وارسی نشانی‌ها:** همه‌ی نشانی‌ها در پایان کار دوره یک‌جا وارسی می‌شوند. همه‌ی کدها در 2026-10-20 با Python 3.13.15 اجرا شدند. پیام‌های خطا از اجرای اسکریپت گرفته شده‌اند و نشانی فایل در آن‌ها کوتاه شده است.

</div>
