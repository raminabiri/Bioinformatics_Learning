<div dir="rtl">

# پاسخ تشریحی: پوشه‌ها و فایل‌ها

> دستورها در 2026-10-20 روی کامپیوتر دوره اجرا شدند. نشانی‌های مطلق روی کامپیوتر شما با `/home/<نام‌کاربری>/` آغاز می‌شوند.

---

## تمرین ۱: گشتی در درخت دوره

<div dir="ltr">

```bash
cd ~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data
pwd
ls -l
cd ../..
pwd
cd ~
```

</div>

1. نشانی مطلق پوشه‌ی داده، برای نمونه `/home/sara/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data`.
2. **۳۳ بایت.** (در ستون پنجم `ls -l`.) اگر فایل‌های ماژول بعد را دانلود کرده باشید، فایل‌های دیگری هم می‌بینید.
3. ‏`cd ../..`: یک پله به `99_scripts_data` و یک پله به `01_Linux`.
4. ‏`cd ~` (یا تنها `cd`، که بی ورودی هم به خانه می‌رود).

**اشتباه رایج:** نوشتن `cd..` (بی فاصله). `cd..` یک دستور ناشناخته است: `bash: cd..: command not found`.

---

## تمرین ۲: میز کار پروژه

<div dir="ltr">

```bash
cd ~
mkdir -p ecoli_project/{data,results,scripts}
ls ecoli_project
cp Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/sample.fasta ecoli_project/data/my_protein.fasta
ls -lh ecoli_project/data/my_protein.fasta
cat ecoli_project/data/my_protein.fasta
```

</div>

<div dir="ltr">

```text
data
results
scripts
-rw-rw-r-- 1 ubuntu ubuntu 33 Oct 20 06:58 ecoli_project/data/my_protein.fasta
>protein_sample-1
MKTAYIAKQRQISF
```

</div>

1. ‏`{data,results,scripts}` را Bash به سه نشانی باز می‌کند و `mkdir -p` هر سه را (و `ecoli_project` را) می‌سازد.
2. چون در مقصد نام فایل آمده، کپی با نام تازه ساخته شد.
3. **۳۳ بایت** (`33`؛ برای فایل‌های کوچک‌تر از ۱ کیلوبایت، `-h` همان عدد بایت را نشان می‌دهد). تاریخ و ساعت روی کامپیوتر شما فرق دارد.
4. توالی `MKTAYIAKQRQISF` **۱۴ اسیدآمینه** دارد.

---

## تمرین ۳: مطلق یا نسبی؟

1. برای نمونه `/home/sara/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/sample.fasta`.
2. از `~/ecoli_project/data` دو پله بالا به `~` می‌رسیم، سپس پایین به پوشه‌ی دوره:

   <div dir="ltr">

   ```bash
   cd ~/ecoli_project/data
   ls ../../Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/
   ```

   </div>

   <div dir="ltr">

   ```text
   sample.fasta
   ```

   </div>

   پس نشانی نسبی: `../../Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/sample.fasta`.
3. **نشانی مطلق.** نشانی نسبی تنها از همان پوشه‌ی کنونی درست است. راه میانبر: `~/Bioinformatics_Learning-main/…` هم از هر جا درست است، چون `~` همیشه همان پوشه‌ی خانه است.

---

## تمرین ۴: پیام‌های خطا را بخوانید

| پیام | چه رخ داده | دستور درست |
| :--- | :--- | :--- |
| `mkdir: cannot create directory ‘thesis/raw/2026’: No such file or directory` | پوشه‌ی پدر (`thesis/raw`) هنوز نیست | `mkdir -p thesis/raw/2026` |
| `rm: cannot remove 'old_results': Is a directory` | ‏`old_results` پوشه است و `rm` بی `-r` پوشه پاک نمی‌کند | پس از `ls old_results`: `rm -r old_results` |
| `cp: -r not specified; omitting directory 'ecoli_project'` | برای کپی پوشه `-r` لازم است | `cp -r ecoli_project backup` |
| `bash: cd: too many arguments` | نام پوشه فاصله دارد و دو ورودی دیده شده | ‏`cd "my data"`؛ بهتر: نام بی فاصله |

---

## تمرین ۵: پشتیبان بگیرید و پاک کنید

<div dir="ltr">

```bash
cd ~
cp -r ecoli_project ecoli_project_backup
mv ecoli_project/data/my_protein.fasta ecoli_project/data/protein_v2.fasta
ls ecoli_project/data ecoli_project_backup/data
ls ecoli_project_backup
rm -r ecoli_project_backup
```

</div>

<div dir="ltr">

```text
ecoli_project_backup/data:
my_protein.fasta

ecoli_project/data:
protein_v2.fasta
```

</div>

1. ‏`cp -r` کل پوشه را با همه‌ی زیرپوشه‌ها و فایل‌ها کپی می‌کند.
2. در پشتیبان هنوز **`my_protein.fasta`** است. کپی پس از ساخته شدن، مستقل از اصل است. وقتی `ls` چند پوشه را با هم نشان می‌دهد، بالای فهرست هر پوشه نامش را می‌نویسد (و پوشه‌ها را به ترتیب الفبایی خودش می‌چیند، نه به ترتیبی که نوشتید).
3. پیش از `rm -r`، با `ls ecoli_project_backup` مطمئن شوید همان پوشه‌ای است که می‌خواهید پاک کنید. یک حرف اشتباه (`ecoli_project` به جای `ecoli_project_backup`) پروژه‌ی اصلی را برای همیشه پاک می‌کند.

</div>
