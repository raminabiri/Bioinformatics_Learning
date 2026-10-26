<div dir="rtl">

# درس: Git؛ دفترچه‌ی آزمایشگاه برای کد

**بخش:** `05_Reproducible_Work` · **ماژول:** `01_Git_Basics` · **پیش‌نیاز:** بخش‌های [لینوکس](../../01_Linux/) تا [بسته‌های R](../../04_R_Packages/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** git 2.43 · **آخرین اجرا:** 2026-10-21

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک پوشه‌ی پروژه را به **مخزن Git** تبدیل کنید (`git init`) و نام و ایمیلتان را تنظیم کنید.
2. با `.gitignore` داده‌های بزرگ را از مخزن بیرون نگه دارید.
3. چرخه‌ی روزانه را اجرا کنید: `git status` ← `git add` ← `git commit`.
4. تغییرات را ببینید (`git diff`، `git log`) و تغییر نادرست را دور بریزید (`git restore`).
5. نسخه‌ی کهنه‌ی یک اسکریپت را ببینید و اجرا کنید (`git show`).

**پیش از آغاز:** Git روی بیشتر لینوکس‌ها و macOS از پیش نصب است:

<div dir="ltr">

```bash
git --version
```

</div>

<div dir="ltr">

```text
git version 2.43.0
```

</div>

اگر نبود: `sudo apt install git` (Ubuntu/WSL) یا `conda install -c conda-forge git`.

---

## ۱. داستان: «شکل ۳ با کدام نسخه ساخته شد؟»

پوشه‌ی پروژه‌ی بسیاری از دانشجوها این شکل را دارد:

<div dir="ltr">

```text
count_genes.sh
count_genes_v2.sh
count_genes_v2_final.sh
count_genes_v2_final_REALLY_final.sh
```

</div>

شش ماه بعد، داور مقاله می‌پرسد: «عدد جدول ۲ با کدام نسخه‌ی اسکریپت به دست آمد؟» و پاسخی نیست.

‏**Git** این مشکل را حل می‌کند. هر بار که می‌گویید، یک **عکس** کامل از پروژه می‌گیرد، با تاریخ، نام شما و یک یادداشت کوتاه. همیشه **یک** فایل `count_genes.sh` دارید و هر نسخه‌ی کهنه‌اش هر وقت بخواهید برمی‌گردد.

---

## ۲. مفهوم به زبان ساده: دفترچه‌ی آزمایشگاه

| در آزمایشگاه | در Git |
| :--- | :--- |
| میز کار، جایی که کار می‌کنید | **پوشه‌ی کاری** (*working tree*): فایل‌های پروژه |
| نمونه‌هایی که برای ثبت جدا می‌کنید | **ناحیه‌ی آماده‌سازی** (*staging area*): `git add` |
| ثبت در دفترچه با تاریخ و امضا | **‏commit**: `git commit` |
| خود دفترچه، که برگه‌هایش کنده نمی‌شود | **مخزن** (*repository*): پوشه‌ی پنهان `.git` |

<div dir="ltr">

```text
 working tree  ──git add──►  staging area  ──git commit──►  repository (history)
      ▲                                                            │
      └────────────── git restore / git show ◄─────────────────────┘
```

</div>

- ‏**‏commit** یک عکس کامل از فایل‌های ثبت‌شده است، با یک **شناسه‌ی یکتا** (*hash*) مانند `cc62ffa`.
- چرا گام میانی (staging)؟ تا بتوانید از ده فایل تغییرکرده، تنها سه تا را که به یک کار مربوط‌اند با هم ثبت کنید.

**قاعده‌ی طلایی: Git برای کد و متن است، نه داده.** FASTQ، BAM و پایگاه‌های داده در Git نمی‌روند؛ تنها **اسکریپت دانلود** آن‌ها. همین دوره این‌گونه ساخته شده: `download.sh` در Git است، خود FASTQها نه.

---

## ۳. ساختن مخزن

### گام ۱: `git init`

<div dir="ltr">

```bash
mkdir -p ~/git_practice && cd ~/git_practice
git init -b main ecoli_project
cd ecoli_project
```

</div>

<div dir="ltr">

```text
Initialized empty Git repository in /home/you/git_practice/ecoli_project/.git/
```

</div>

(در خروجی، به‌جای `/home/you` نشانی پوشه‌ی خانه‌ی شما می‌آید.)

| تکه | یعنی | اگر نباشد |
| :--- | :--- | :--- |
| `git init` | این پوشه را مخزن کن (پوشه‌ی پنهان `.git` را می‌سازد) | — |
| `-b main` | نام شاخه‌ی اصلی `main` باشد | در برخی نسخه‌ها `master` می‌شود؛ مهم نیست، ولی درس با `main` است |
| `ecoli_project` | نام پوشه؛ اگر نباشد ساخته می‌شود | ‏Git پوشه‌ی کنونی را مخزن می‌کند |

‏`ls -a` پوشه‌ی `.git` را نشان می‌دهد. **هرگز دستی در آن دست نبرید**؛ همه‌ی تاریخچه آن‌جاست.

### گام ۲: شما که هستید؟

هر commit امضای نویسنده را دارد. یک بار برای همیشه:

<div dir="ltr">

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.org"
```

</div>

‏`--global` یعنی برای همه‌ی مخزن‌های شما روی این کامپیوتر. اگر این کار را نکنید، نخستین commit با این پیام شکست می‌خورد:

<div dir="ltr">

```text
Author identity unknown

*** Please tell me who you are.

Run

  git config --global user.email "you@example.com"
  git config --global user.name "Your Name"
```

</div>

### گام ۳: `git status`؛ پرکاربردترین دستور

<div dir="ltr">

```bash
git status
```

</div>

<div dir="ltr">

```text
On branch main

No commits yet

nothing to commit (create/copy files and use "git add" to track)
```

</div>

‏`git status` می‌گوید کجایید و چه چیزی تغییر کرده است. **هر وقت شک کردید، `git status` بزنید.** پیام‌هایش اغلب دستور بعدی را هم پیشنهاد می‌کنند (`use "git add" to track`).

---

## ۴. نخستین commit

### یک اسکریپت و یک «داده‌ی بزرگ»

اسکریپت شمارش ژن‌ها (همان `awk` ماژول ۰۷ بخش ۰۱) را بنویسید. با `nano scripts/count_genes.sh` یا این دستور:

<div dir="ltr">

```bash
mkdir -p data/raw results scripts
cat > scripts/count_genes.sh << 'EOF'
#!/usr/bin/env bash
set -euo pipefail
awk -F'\t' '$3=="gene"' "$1" | wc -l
EOF
GFF=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ecoli_k12.gff
bash scripts/count_genes.sh $GFF
```

</div>

<div dir="ltr">

```text
4506
```

</div>

‏(`cat > فایل << 'EOF'` … `EOF` چند خط را یک‌جا در فایل می‌نویسد؛ همان کار `nano` بی ویرایشگر.)

حالا یک «فایل داده» و یک «خروجی» هم بسازید، مانند پروژه‌ی واقعی:

<div dir="ltr">

```bash
echo fake > data/raw/a.fastq.gz
echo x > results/out.txt
git status
```

</div>

<div dir="ltr">

```text
On branch main

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	data/
	results/
	scripts/

nothing added to commit but untracked files present (use "git add" to track)
```

</div>

‏**‏Untracked** یعنی «Git این‌ها را می‌بیند ولی دنبالشان نمی‌کند». `data/` و `results/` نباید هرگز ثبت شوند.

### ‏`.gitignore`: فهرست چیزهایی که Git نبیند

<div dir="ltr">

```bash
printf 'data/raw/\n*.fastq.gz\nresults/\n' > .gitignore
cat .gitignore
git status --short
```

</div>

<div dir="ltr">

```text
data/raw/
*.fastq.gz
results/
?? .gitignore
?? scripts/
```

</div>

| خط `.gitignore` | یعنی |
| :--- | :--- |
| `data/raw/` | کل این پوشه را نادیده بگیر |
| `*.fastq.gz` | هر فایلی با این پسوند، هر جا باشد (`*` همان `*` بخش ۰۱) |
| `results/` | خروجی‌ها را نادیده بگیر؛ از روی اسکریپت دوباره ساخته می‌شوند |

‏`--short` شکل کوتاه `status` است: `??` = دنبال‌نشده. `data/` و `results/` از فهرست رفتند.

‏**‏`.gitignore` را پیش از نخستین commit بسازید.** فایلی که یک بار commit شود، در تاریخچه **می‌ماند**، حتی اگر بعداً پاکش کنید.

### ‏`git add`: گذاشتن در ناحیه‌ی آماده‌سازی

<div dir="ltr">

```bash
git add .gitignore scripts/count_genes.sh
git status
```

</div>

<div dir="ltr">

```text
On branch main

No commits yet

Changes to be committed:
  (use "git rm --cached <file>..." to unstage)
	new file:   .gitignore
	new file:   scripts/count_genes.sh

```

</div>

‏`Changes to be committed` = آماده‌ی ثبت. (در شکل کوتاه، `A` = *added*.)

### ‏`git commit`: ثبت

<div dir="ltr">

```bash
git commit -m "Add gene counting script and .gitignore"
```

</div>

<div dir="ltr">

```text
[main (root-commit) cc62ffa] Add gene counting script and .gitignore
 2 files changed, 6 insertions(+)
 create mode 100644 .gitignore
 create mode 100644 scripts/count_genes.sh
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `-m "…"` | پیام commit؛ اگر نباشد، Git ویرایشگری باز می‌کند تا پیام بنویسید |
| ‏`main` | شاخه‌ای که commit در آن ثبت شد |
| ‏`root-commit` | نخستین commit مخزن |
| ‏`cc62ffa` | ۷ نویسه‌ی آغاز **hash** این commit |
| ‏`2 files changed, 6 insertions(+)` | ‏۲ فایل، روی‌هم ۶ خط تازه |

> ‏📝 **hash شما فرق می‌کند.** hash از روی محتوا، نام، ایمیل و **زمان** commit ساخته می‌شود. hashهای این درس با اسکریپت [git_demo.sh](../99_scripts_data/01_Git_Basics/scripts/git_demo.sh) ساخته شده‌اند که نام و تاریخ را ثابت می‌کند؛ اگر آن را اجرا کنید، دقیقاً همین hashها را می‌گیرید.

**پیام خوب** می‌گوید **چه** شد، کوتاه و روشن: «Add gene counting script» خوب است؛ «update» یا «changes» بد است، چون شش ماه بعد چیزی نمی‌گوید.

### ‏`git log`: تاریخچه

<div dir="ltr">

```bash
git log
```

</div>

<div dir="ltr">

```text
commit cc62ffa1286cf6f46fd504b2b1db1fdb39cf612a
Author: Student <student@example.org>
Date:   Tue Oct 13 10:00:00 2026 +0000

    Add gene counting script and .gitignore
```

</div>

‏hash کامل ۴۰ نویسه است؛ ۷ نویسه‌ی آغازش برای بیشتر کارها بس است.

<details>
<summary>✋ امتحان کن: پس از commit، <code>git status</code> چه می‌گوید؟</summary>

<div dir="ltr">

```text
On branch main
nothing to commit, working tree clean
```

</div>

«پوشه‌ی کاری تمیز است»: هر چه هست ثبت شده (به جز فایل‌های نادیده‌گرفته‌شده که Git اصلاً نمی‌بیند).

</details>

> 📺 **فیلم:** *Reproducible Research 2026, 02: Version Control with Git*: https://www.youtube.com/watch?v=S0kw9OB2Tf0 (Bioinformatics.ca)
> 📄 **مرجع:** Blischak JD, Davenport ER, Wilson G (2016). *A Quick Introduction to Version Control with Git and GitHub.* PLoS Comput Biol 12:e1004668. https://doi.org/10.1371/journal.pcbi.1004668

---

## ۵. تغییر، دیدن تغییر، ثبت دوباره

اسکریپت را عوض کنید تا ژن‌ها را **به تفکیک رشته** بشمارد (همان `cut | sort | uniq -c` ماژول ۰۶ بخش ۰۱):

<div dir="ltr">

```bash
sed -i 's/wc -l/cut -f7 | sort | uniq -c/' scripts/count_genes.sh
git status --short
git diff
```

</div>

<div dir="ltr">

```text
 M scripts/count_genes.sh
diff --git a/scripts/count_genes.sh b/scripts/count_genes.sh
index 0d7b585..3a9de92 100644
--- a/scripts/count_genes.sh
+++ b/scripts/count_genes.sh
@@ -1,3 +1,3 @@
 #!/usr/bin/env bash
 set -euo pipefail
-awk -F'\t' '$3=="gene"' "$1" | wc -l
+awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
```

</div>

- ‏`M` = *modified*: فایلی که Git دنبال می‌کند تغییر کرده.
- در `git diff`: خط با **`-`** = پیش از تغییر؛ خط با **`+`** = پس از تغییر؛ خط‌های بی‌نشانه = بی‌تغییر (برای نشان دادن جای تغییر).
- ‏`@@ -1,3 +1,3 @@` = «از خط ۱، ۳ خط» در نسخه‌ی کهنه و نو.

اجرا و ثبت:

<div dir="ltr">

```bash
bash scripts/count_genes.sh $GFF
git commit -am "Count genes per strand"
git log --oneline
```

</div>

<div dir="ltr">

```text
   2216 +
   2290 -
[main 31e9354] Count genes per strand
 1 file changed, 1 insertion(+), 1 deletion(-)
31e9354 Count genes per strand
cc62ffa Add gene counting script and .gitignore
```

</div>

- ‏`-a` در `commit -am`: «همه‌ی فایل‌های **دنبال‌شده**‌ی تغییرکرده را خودت add کن». برای فایل **تازه** کار نمی‌کند؛ آن را باید یک بار `git add` کرد.
- ‏`--oneline`: هر commit در یک خط، تازه‌ترین بالا.

---

## ۶. برگشتن

### تغییر نادرست را دور بریزید: `git restore`

فرض کنید اشتباهی خطی خطرناک به اسکریپت افزودید:

<div dir="ltr">

```bash
echo "rm -rf /" >> scripts/count_genes.sh
git diff --stat
git restore scripts/count_genes.sh
git status --short
tail -1 scripts/count_genes.sh
```

</div>

<div dir="ltr">

```text
 scripts/count_genes.sh | 1 +
 1 file changed, 1 insertion(+)
awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
```

</div>

‏`git restore فایل` فایل را به **آخرین commit** برمی‌گرداند. `status` چیزی چاپ نکرد: تمیز. ⚠️ تغییرهای commit‌نشده با `restore` **برای همیشه** می‌روند.

### نسخه‌ی کهنه را ببینید و اجرا کنید: `git show`

<div dir="ltr">

```bash
git show HEAD~1:scripts/count_genes.sh
bash <(git show HEAD~1:scripts/count_genes.sh) $GFF
```

</div>

<div dir="ltr">

```text
#!/usr/bin/env bash
set -euo pipefail
awk -F'\t' '$3=="gene"' "$1" | wc -l
4506
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `HEAD` | آخرین commit شاخه‌ی کنونی |
| `HEAD~1` | یک commit پیش از آن (`~2` = دو تا پیش‌تر)؛ یا خود hash: `cc62ffa` |
| `:scripts/count_genes.sh` | این فایل، **در آن commit** |
| `bash <( … )` | خروجی دستور درون پرانتز را مانند یک فایل اسکریپت اجرا کن |

پوشه‌ی کاری **عوض نشد**؛ تنها نسخه‌ی کهنه خوانده و اجرا شد. **این پاسخ پرسش داور است:** «عدد ۴٬۵۰۶ با commit `cc62ffa` ساخته شد؛ با این دستور دوباره ساخته می‌شود.»

<details>
<summary>✋ امتحان کن: کدام commitها فایل <code>scripts/count_genes.sh</code> را تغییر داده‌اند؟</summary>

<div dir="ltr">

```bash
git log --oneline -- scripts/count_genes.sh
```

</div>

<div dir="ltr">

```text
31e9354 Count genes per strand
cc62ffa Add gene counting script and .gitignore
```

</div>

‏`-- فایل` تاریخچه را به همان فایل محدود می‌کند.

</details>

> 📺 **فیلم:** *How Git Works: Explained in 4 Minutes*: https://www.youtube.com/watch?v=e9lnsKot_SQ (ByteByteGo)
> 📄 **مرجع:** Pro Git, بخش Undoing Things: https://git-scm.com/book/en/v2/Git-Basics-Undoing-Things

---

## ۷. سه اشتباه رایج

‏**۱. commit بی add.**

<div dir="ltr">

```bash
echo "# note" >> scripts/count_genes.sh
echo "x" > notes.txt
git commit -m "try"
```

</div>

<div dir="ltr">

```text
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
	modified:   scripts/count_genes.sh

Untracked files:
  (use "git add <file>..." to include in what will be committed)
	notes.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

</div>

هیچ چیز ثبت نشد. نخست `git add` (یا `commit -a` برای فایل‌های دنبال‌شده).

**۲. افزودن فایلی که نادیده گرفته شده.**

<div dir="ltr">

```bash
git add data/raw/a.fastq.gz
```

</div>

<div dir="ltr">

```text
The following paths are ignored by one of your .gitignore files:
data/raw
hint: Use -f if you really want to add them.
```

</div>

‏Git از شما محافظت کرد. **`-f` نزنید.** اگر دیدید داده‌ای ناخواسته add شده (`A  data/raw/a.fastq.gz` در `status`)، پیش از commit با `git rm --cached فایل` بیرونش بیاورید (`--cached` = تنها از Git، خود فایل روی دیسک می‌ماند).

‏**۳. commitهای بزرگ و بی‌معنا.** یک commit با پیام «update» که ده تغییر نامربوط دارد، بعداً قابل فهم یا برگشت نیست. **هر commit = یک تغییر منطقی**، با پیامی که آن را می‌گوید.

---

## 📘 برای کنجکاوها

- ‏**‏`git log -p`** تاریخچه را همراه `diff` هر commit نشان می‌دهد؛ `git show 31e9354` تغییرهای یک commit را.
- **چه چیزی در پروژه‌ی بیوانفورماتیک commit شود:** اسکریپت‌ها (Bash، Python، R)، فایل‌های محیط (`envs/*.yml`)، Snakefile و `config.yaml` (ماژول‌های ۰۳ و ۰۴)، `README.md`، اسکریپت‌های دانلود با md5. **نه:** داده‌ی خام، خروجی‌های بزرگ، رمز و توکن.
- ‏**‏`git revert` و `git commit --amend`** برای خنثی کردن یا اصلاح commitها در ماژول بعد.

---

## جمع‌بندی

- ‏Git از پروژه عکس (**commit**) می‌گیرد؛ هر commit یک hash، نویسنده، تاریخ و پیام دارد.
- سه ناحیه: پوشه‌ی کاری ← `git add` ← staging ← `git commit` ← تاریخچه.
- ‏`.gitignore` پیش از نخستین commit؛ داده در Git نمی‌رود.
- ‏`git status` و `git diff` پیش از هر commit؛ `git log --oneline` برای تاریخچه.
- ‏`git restore` تغییر commit‌نشده را دور می‌ریزد؛ `git show HEAD~1:فایل` نسخه‌ی کهنه را نشان می‌دهد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
git init -b main project                     # new repository
git config --global user.name "Name"         # once per computer
git config --global user.email "me@uni.edu"
git status        /  git status --short      # what changed?
git add file1 file2                          # stage
git commit -m "Say what changed"             # record
git commit -am "..."                         # stage all tracked + record
git diff                                     # changes not yet staged
git log --oneline [-- file]                  # history
git restore file                             # discard uncommitted change (lost!)
git show HEAD~1:path/file                    # file as it was one commit ago
git rm --cached file                         # untrack, keep on disk
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| مخزن (*repository*) | پروژه همراه با همه‌ی تاریخچه‌اش (پوشه‌ی `.git`) |
| ‏commit | عکس ثبت‌شده‌ی پروژه با پیام، نویسنده و تاریخ |
| ‏hash | شناسه‌ی یکتای هر commit (۴۰ نویسه؛ ۷ تای آغاز بس است) |
| ‏staging area | ناحیه‌ی آماده‌سازی؛ چیزهایی که commit بعدی ثبت می‌کند |
| ‏working tree | پوشه‌ی کاری؛ فایل‌هایی که می‌بینید و ویرایش می‌کنید |
| ‏untracked | فایلی که Git دنبالش نمی‌کند |
| ‏`.gitignore` | فهرست فایل‌ها و پوشه‌هایی که Git نادیده می‌گیرد |
| ‏HEAD | آخرین commit شاخه‌ی کنونی |
| ‏diff | تفاوت دو نسخه، خط‌به‌خط |

---

## منابع

**مقاله و مستند**
- Blischak JD, Davenport ER, Wilson G (2016). *A Quick Introduction to Version Control with Git and GitHub.* PLoS Comput Biol 12(1):e1004668. https://doi.org/10.1371/journal.pcbi.1004668
- Software Carpentry, *Version Control with Git*: https://swcarpentry.github.io/git-novice/

**کتاب**
- ‏Chacon S, Straub B. *Pro Git* (کتاب رایگان)، فصل ۲ «Git Basics»: https://git-scm.com/book/en/v2
- ‏Chacon S, Straub B (2014). *Pro Git*, 2nd ed. Apress (نسخه‌ی رایگان: https://git-scm.com/book/en/v2). (فصل ۲)
- ‏Buffalo V (2015). *Bioinformatics Data Skills*. O'Reilly. (فصل ۵: Git برای دانشمندان)

**فیلم و دوره‌ی آموزشی**
- Coursera: *Version Control with Git* (Atlassian): https://www.coursera.org/learn/version-control-with-git
- edX: *Git and GitHub Basics* (IBM): https://www.edx.org/learn/github/ibm-git-and-github-basics
- YouTube: *Reproducible Research 2026, 02: Version Control with Git* (Bioinformatics.ca): https://www.youtube.com/watch?v=S0kw9OB2Tf0
- YouTube: *How to set up git for a bioinformatics project* (Riffomonas Project): https://www.youtube.com/watch?v=DnwEaa5QtpI
- ‏YouTube (فارسی): *آموزش گیت و گیت‌هاب ۲۰۲۶ با جادی، قسمت اول* (مکتب‌خونه): https://www.youtube.com/watch?v=8RmjKD_YSlg

<sub>نشانی‌های YouTube در 2026-10-13 وارسی شدند. نشانی‌های Coursera و edX از نمایه‌ی جست‌وجو گرفته شدند؛ وارسی مستقیم همه‌ی نشانی‌ها در پایان دوره انجام می‌شود.</sub>

</div>
