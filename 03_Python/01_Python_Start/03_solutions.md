<div dir="rtl">

# پاسخ تشریحی: نخستین گام‌ها در پایتون

> کدها در 2026-10-20 با Python 3.13.15 اجرا شدند.

---

## تمرین ۱: ماشین‌حساب ژنوم

<div dir="ltr">

```python
>>> size = 2800000
>>> size * 50 / 150
933333.3333333334
>>> size / 3000
933.3333333333334
>>> size * 50 / 300
466666.6666666667
```

</div>

1. نزدیک به **۹۳۳ هزار رید**.
2. نزدیک به **۹۳۳ صفحه**.
3. نزدیک به **۴۶۷ هزار رید** (نصف، چون طول رید دو برابر شد).
4. همان پاسخ‌های بخش ۰۰، که آن‌جا با ماشین‌حساب گرفتیم. سود متغیر: اگر اندازه‌ی ژنوم را عوض کنید، تنها یک خط عوض می‌شود.

**نکته:** برای عدد رید، عدد درست می‌خواهیم. `round(size * 50 / 150)` می‌دهد `933333`.

---

## تمرین ۲: آغاز gyrA

<div dir="ltr">

```python
>>> g = "ATGAGCGACCTTGCGAGAGAAATTACACCG"
>>> len(g)
30
>>> g[0:3]
'ATG'
>>> g[3:6]
'AGC'
>>> g[6:9]
'GAC'
>>> g.count("A"), g.count("C"), g.count("G"), g.count("T")
(10, 7, 8, 5)
>>> gc = (g.count("G") + g.count("C")) / len(g)
>>> round(gc * 100, 1)
50.0
>>> g.replace("T", "U")
'AUGAGCGACCUUGCGAGAGAAAUUACACCG'
```

</div>

1. **۳۰ باز**؛ کدون‌ها `ATG`، `AGC`، `GAC` (M، S، D؛ آغاز `MSDLAREITP` که در بخش ۰۰ دیدیم).
2. ‏A = ۱۰، C = ۷، G = ۸، T = ۵؛ جمع ۳۰. ✓ (چهار مقدار با ویرگول در پرانتز نشان داده شدند؛ به این «تاپل» می‌گویند. در ماژول بعد بیشتر می‌بینید.)
3. (۸ + ۷) ÷ ۳۰ = **۵۰٫۰٪**.
4. `AUGAGCGACCUUGCGAGAGAAAUUACACCG`.

---

## تمرین ۳: از مختصات ژنوم به شماره‌ی پایتون

<div dir="ltr">

```python
>>> start = 4181245
>>> 4181260 - start
15
>>> dna[4181260 - start]
'A'
>>> dna[4181260 - start : 4181262 - start + 1]
'ACC'
>>> dna[1590:1593]
''
```

</div>

1. شماره‌ی **۱۵** (یعنی شانزدهمین باز)؛ باز **`A`**.
2. پایان تکه‌برداری را باید **+۱** کرد، چون پایان در پایتون جزو تکه نیست: `dna[15:18]` = **`ACC`**. این **کدون ششم** است (۱۵ ÷ ۳ + ۱ = ۶): ترئونین، ششمین حرف `MVYSYT`.
3. یک رشته‌ی **خالی** `''`. `dna` تنها ۶۰ باز دارد و شماره‌ی ۱۵۹۰ بسیار بیرون از آن است. تکه‌برداری بیرون از رشته خطا نمی‌دهد و چیزی برنمی‌گرداند (تنها `dna[i]` با یک شماره خطا می‌دهد). برای کدون ۵۳۱ باید **کل ژن** را داشته باشید؛ در ماژول ۰۴ با Biopython همین کار را می‌کنیم.

---

## تمرین ۴: نخستین اسکریپت خودتان

<div dir="ltr">

```python
# gc.py: length and GC content of the start of gyrA
name = "gyrA"
seq = "ATGAGCGACCTTGCGAGAGAAATTACACCG"

gc = (seq.count("G") + seq.count("C")) / len(seq)
print(f"{name}: length {len(seq)} bp, GC {gc * 100:.1f}%")
print(f"first codon {seq[:3]}, last codon {seq[-3:]}")
```

</div>

<div dir="ltr">

```bash
python3 gc.py
```

</div>

<div dir="ltr">

```text
gyrA: length 30 bp, GC 50.0%
first codon ATG, last codon CCG
```

</div>

**اشتباه رایج:** اجرای `python3 gc.py` درون پایتون تعاملی (`>>>`). این یک دستور **ترمینال** است؛ نخست با `exit()` از پایتون بیرون بیایید.

---

## تمرین ۵: خطا را پیدا کنید

خط آخر خطای هر کد:

<div dir="ltr">

```text
TypeError: can only concatenate str (not "float") to str
IndexError: string index out of range
NameError: name 'G' is not defined
```

</div>

| کد | خطا | چرا | درست |
| :-: | :--- | :--- | :--- |
| ۱ | `TypeError` | چسباندن رشته و عدد اعشاری | ‏`print("GC:", gc)` یا `print(f"GC: {gc}")` |
| ۲ | `IndexError` | ۳۰ نویسه، شماره‌های ۰ تا ۲۹ | آخرین باز: `seq[29]` یا `seq[-1]` |
| ۳ | `NameError` | ‏`G` بی نقل‌قول نام متغیر شمرده شد | `seq.count("G")` |

</div>
