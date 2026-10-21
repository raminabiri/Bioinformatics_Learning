<div dir="rtl">

# درس: شاخه، ادغام و GitHub

**بخش:** `05_Reproducible_Work` · **ماژول:** `02_Git_Branches_GitHub` · **پیش‌نیاز:** ماژول [پایه‌های Git](../01_Git_Basics/) · **زمان:** حدود ۶۰ دقیقه · **ابزار:** git 2.43، یک حساب GitHub (رایگان) · **آخرین اجرا:** 2026-10-21

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک **شاخه** (*branch*) برای آزمایش بسازید و میان شاخه‌ها جابه‌جا شوید.
2. شاخه را با `git merge` در شاخه‌ی اصلی **ادغام** کنید و یک **تضاد** (*conflict*) را آگاهانه حل کنید.
3. نسخه‌ی پایان‌نامه یا مقاله را با **tag** نشانه‌گذاری کنید.
4. پیام commit را اصلاح کنید (`--amend`) و یک commit را با امنیت خنثی کنید (`revert`).
5. مخزن را در **GitHub** بگذارید (`push`) و مخزن دیگران را بگیرید (`clone`).

**پیش از آغاز:** مخزن `~/git_practice/ecoli_project` ماژول ۰۱ را با **دو** commit درس لازم دارید (`cc62ffa` و `31e9354`). اگر در تمرین‌ها commit سومی افزودید، یا اگر می‌خواهید hashها دقیقاً همانند درس باشند، این اسکریپت کل جلسه را در یک پوشه‌ی تازه می‌سازد:

<div dir="ltr">

```bash
GFF=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ecoli_k12.gff
bash ~/Bioinformatics_Learning-main/05_Reproducible_Work/99_scripts_data/01_Git_Basics/scripts/git_demo.sh $GFF ~/git_demo
```

</div>

---

## ۱. داستان: آزمایشی که شاید شکست بخورد

اسکریپت شما (`count_genes.sh`) کار می‌کند و نتیجه‌هایش در فصل ۲ پایان‌نامه است. حالا استاد می‌گوید: «ببین اگر تنها ژن‌های tRNA را بشماری چه می‌شود.» هم‌زمان، خودتان می‌خواهید نام کروموزوم را هم به خروجی بیفزایید.

اگر مستقیم روی اسکریپت اصلی آزمایش کنید و آزمایش شکست بخورد، نسخه‌ی سالم را خراب کرده‌اید. **شاخه** یعنی یک خط کار **موازی**: آزمایش را آن‌جا انجام می‌دهید؛ اگر خوب بود، آن را با خط اصلی **ادغام** می‌کنید، و اگر نه، دورش می‌اندازید.

---

## ۲. مفهوم به زبان ساده: شاخه‌های یک درخت

<div dir="ltr">

```text
                 ● Count only tRNA genes          ← branch add-trna
                /
● ─── ● ────────
 cc62ffa  31e9354 \
                   ● Also report chromosome       ← branch main
```

</div>

- هر شاخه **یک برچسب متحرک** است که به آخرین commit خودش اشاره می‌کند. با هر commit تازه، برچسب جلو می‌رود.
- ‏**‏`main`** شاخه‌ی اصلی است؛ نسخه‌ای که همیشه باید کار کند.
- **ادغام** (*merge*) دو خط را دوباره یکی می‌کند. اگر دو شاخه **یک خط** از **یک فایل** را جور دیگری عوض کرده باشند، Git نمی‌داند کدام درست است و از شما می‌پرسد: این **تضاد** است.

---

## ۳. ساختن شاخه و جابه‌جایی

<div dir="ltr">

```bash
cd ~/git_practice/ecoli_project
git branch
```

</div>

<div dir="ltr">

```text
* main
```

</div>

‏`git branch` شاخه‌ها را فهرست می‌کند؛ `*` = شاخه‌ای که اکنون در آن هستید.

<div dir="ltr">

```bash
git switch -c add-trna
git branch
```

</div>

<div dir="ltr">

```text
Switched to a new branch 'add-trna'
* add-trna
  main
```

</div>

| تکه | یعنی | اگر نباشد |
| :--- | :--- | :--- |
| `git switch` | به شاخه‌ی دیگری برو | — |
| `-c` | آن شاخه را **بساز** (*create*) و برو | ‏`fatal: invalid reference: add-trna`، چون هنوز نیست |
| `add-trna` | نام شاخه: کوتاه، بی فاصله، گویای کار | — |

‏(در راهنماهای کهنه‌تر `git checkout -b` را می‌بینید؛ همین کار را می‌کند.)

### آزمایش در شاخه

<div dir="ltr">

```bash
sed -i 's/\$3=="gene"/$3=="gene" \&\& $9 ~ \/gene_biotype=tRNA\//' scripts/count_genes.sh
git commit -am "Count only tRNA genes"
```

</div>

<div dir="ltr">

```text
[add-trna a920e2b] Count only tRNA genes
 1 file changed, 1 insertion(+), 1 deletion(-)
```

</div>

‏`[add-trna …]`: commit در شاخه‌ی آزمایشی ثبت شد، نه در `main`.

### برگشت به `main`: فایل هم برمی‌گردد

<div dir="ltr">

```bash
git switch main
tail -1 scripts/count_genes.sh
```

</div>

<div dir="ltr">

```text
Switched to branch 'main'
awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
```

</div>

شرط tRNA در فایل **نیست**! با جابه‌جایی شاخه، Git فایل‌های پوشه‌ی کاری را به نسخه‌ی همان شاخه درمی‌آورد. آزمایش گم نشده؛ در شاخه‌ی `add-trna` منتظر است.

> ⚠️ پیش از `git switch`، تغییرهای commit‌نشده را commit کنید. اگر تغییر commit‌نشده با شاخه‌ی مقصد تضاد داشته باشد، Git جابه‌جایی را نمی‌پذیرد.

### هم‌زمان، کار در `main`

<div dir="ltr">

```bash
sed -i 's/cut -f7/cut -f1,7/' scripts/count_genes.sh
git commit -am "Also report chromosome"
git log --oneline --graph --all
```

</div>

<div dir="ltr">

```text
[main 19a45e2] Also report chromosome
 1 file changed, 1 insertion(+), 1 deletion(-)
* a920e2b Count only tRNA genes
| * 19a45e2 Also report chromosome
|/  
* 31e9354 Count genes per strand
* cc62ffa Add gene counting script and .gitignore
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `--graph` | خط‌ها را با `*`، `|` و `/` بکش |
| `--all` | همه‌ی شاخه‌ها، نه تنها شاخه‌ی کنونی |
| ‏`|/` | دو شاخه از `31e9354` جدا شده‌اند |

همان شکل بخش ۲.

<details>
<summary>✋ امتحان کن: اکنون در کدام شاخه‌اید و اسکریپت کدام نسخه است؟</summary>

‏`git branch` ← `* main`. اسکریپت نسخه‌ی `19a45e2` است: همه‌ی ژن‌ها، با `cut -f1,7` (کروموزوم و رشته)، بی شرط tRNA.

</details>

---

## ۴. ادغام و حل تضاد

<div dir="ltr">

```bash
git merge add-trna
echo "exit=$?"
```

</div>

<div dir="ltr">

```text
Auto-merging scripts/count_genes.sh
CONFLICT (content): Merge conflict in scripts/count_genes.sh
Automatic merge failed; fix conflicts and then commit the result.
exit=1
```

</div>

‏`git merge add-trna` یعنی «شاخه‌ی add-trna را **در شاخه‌ی کنونی** (main) ادغام کن». هر دو شاخه خط `awk` را عوض کرده‌اند، پس تضاد رخ داد. `git status` گام بعد را می‌گوید:

<div dir="ltr">

```bash
git status
```

</div>

<div dir="ltr">

```text
On branch main
You have unmerged paths.
  (fix conflicts and run "git commit")
  (use "git merge --abort" to abort the merge)

Unmerged paths:
  (use "git add <file>..." to mark resolution)
	both modified:   scripts/count_genes.sh

no changes added to commit (use "git add" and/or "git commit -a")
```

</div>

### فایل در حالت تضاد

<div dir="ltr">

```bash
cat scripts/count_genes.sh
```

</div>

<div dir="ltr">

```text
#!/usr/bin/env bash
set -euo pipefail
<<<<<<< HEAD
awk -F'\t' '$3=="gene"' "$1" | cut -f1,7 | sort | uniq -c
=======
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f7 | sort | uniq -c
>>>>>>> add-trna
```

</div>

| نشانه | یعنی |
| :--- | :--- |
| `<<<<<<< HEAD` | آغاز نسخه‌ی **شاخه‌ی کنونی** (main) |
| `=======` | مرز دو نسخه |
| `>>>>>>> add-trna` | پایان نسخه‌ی **شاخه‌ی دیگر** |

**حل تضاد یک تصمیم علمی است، نه فنی.** Git نمی‌داند شما چه می‌خواهید. این‌جا **هر دو** تغییر را می‌خواهیم: تنها tRNA (از add-trna) **و** کروموزوم و رشته (از main). پس فایل را با `nano` باز کنید، سه خط نشانه را پاک کنید و یک خط درست بنویسید:

<div dir="ltr">

```bash
#!/usr/bin/env bash
set -euo pipefail
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f1,7 | sort | uniq -c
```

</div>

سپس `add` (یعنی «این تضاد حل شد») و `commit`:

<div dir="ltr">

```bash
git add scripts/count_genes.sh
git commit -m "Merge add-trna: tRNA genes per chromosome and strand"
git log --oneline --graph --all
bash scripts/count_genes.sh $GFF
```

</div>

<div dir="ltr">

```text
[main 43ce93e] Merge add-trna: tRNA genes per chromosome and strand
*   43ce93e Merge add-trna: tRNA genes per chromosome and strand
|\  
| * a920e2b Count only tRNA genes
* | 19a45e2 Also report chromosome
|/  
* 31e9354 Count genes per strand
* cc62ffa Add gene counting script and .gitignore
     49 NC_000913.3	+
     37 NC_000913.3	-
```

</div>

دو خط دوباره یکی شدند (`|\`). نتیجه: ۸۶ tRNA، به تفکیک کروموزوم و رشته؛ ترکیب هر دو تغییر.

> **اگر ادغام بی‌تضاد باشد** (دو شاخه فایل‌ها یا خط‌های جدا را عوض کرده باشند)، Git خودش ادغام می‌کند و تنها یک ویرایشگر برای پیام commit ادغام باز می‌کند (یا با `--no-edit` پیام پیش‌فرض را می‌پذیرد). تمرین ۲ را ببینید.
>
> **اگر ترسیدید:** `git merge --abort` همه چیز را به پیش از ادغام برمی‌گرداند.

### پاک کردن شاخه‌ی ادغام‌شده

<div dir="ltr">

```bash
git branch -d add-trna
```

</div>

<div dir="ltr">

```text
Deleted branch add-trna (was a920e2b).
```

</div>

‏`-d` تنها شاخه‌ای را پاک می‌کند که **ادغام شده** باشد؛ commitهایش در تاریخچه می‌مانند (`a920e2b` را در گراف بالا ببینید).

---

## ۵. نشانه‌گذاری نسخه‌ی پایان‌نامه: `git tag`

<div dir="ltr">

```bash
git tag -a v1.0-thesis-ch2 -m "Version used for thesis chapter 2"
git tag
git log --oneline --decorate -1
```

</div>

<div dir="ltr">

```text
v1.0-thesis-ch2
43ce93e (HEAD -> main, tag: v1.0-thesis-ch2) Merge add-trna: tRNA genes per chromosome and strand
```

</div>

| تکه | یعنی |
| :--- | :--- |
| `-a` | ‏tag «کامل»، با نام سازنده، تاریخ و پیام |
| `v1.0-thesis-ch2` | نام tag: هر نامی، بی فاصله |
| `-m "…"` | پیام tag |

‏tag یک **برچسب ثابت** است: برخلاف شاخه، با commitهای بعدی جلو نمی‌رود. هر وقت بخواهید: `git show v1.0-thesis-ch2:scripts/count_genes.sh`. در پایان‌نامه می‌نویسید: «تحلیل‌های فصل ۲ با نسخه‌ی `v1.0-thesis-ch2` (commit `43ce93e`) انجام شد.»

---

## ۶. «اشتباه کردم!»

### پیام commit غلط تایپی داشت: `--amend`

<div dir="ltr">

```bash
echo "# Usage: bash count_genes.sh file.gff" >> scripts/count_genes.sh
git commit -qam "Add usge note"
git log --oneline -1
git commit --amend -m "Add usage note"
git log --oneline -2
```

</div>

<div dir="ltr">

```text
597a9a3 Add usge note
[main ed406c5] Add usage note
 Date: Tue Oct 13 11:00:00 2026 +0000
 1 file changed, 1 insertion(+)
ed406c5 Add usage note
43ce93e Merge add-trna: tRNA genes per chromosome and strand
```

</div>

‏`--amend` آخرین commit را **جایگزین** می‌کند (hash عوض شد: `597a9a3` ← `ed406c5`). ⚠️ تنها برای commitی که هنوز **push نشده** (بخش ۷)؛ وگرنه تاریخچه‌ی شما با GitHub ناهمسان می‌شود.

### ‏commit را خنثی کنید، با امنیت: `git revert`

<div dir="ltr">

```bash
git revert --no-edit HEAD
git log --oneline -3
```

</div>

<div dir="ltr">

```text
[main ae3f591] Revert "Add usage note"
 Date: Tue Oct 13 11:00:00 2026 +0000
 1 file changed, 1 deletion(-)
ae3f591 Revert "Add usage note"
ed406c5 Add usage note
43ce93e Merge add-trna: tRNA genes per chromosome and strand
```

</div>

‏`revert` یک commit **تازه** می‌سازد که کار commit دیگری را برعکس می‌کند. تاریخچه پاک **نمی‌شود**؛ هم اشتباه و هم اصلاحش ثبت‌اند. این راه امن برای commitهایی است که push شده‌اند.

| می‌خواهم | دستور | ‏push‌شده؟ |
| :--- | :--- | :--- |
| تغییر commit‌نشده را دور بریزم | ‏`git restore فایل` | — |
| پیام یا محتوای آخرین commit را اصلاح کنم | `git commit --amend` | تنها اگر **نه** |
| یک commit را خنثی کنم | `git revert <hash>` | بله، امن |

---

## ‏۷. GitHub: مخزن در اینترنت

‏**GitHub** (یا GitLab، Codeberg) نسخه‌ای از مخزن شما را روی سرور نگه می‌دارد: **پشتیبان**، **همکاری**، و **انتشار کد همراه مقاله**. خود همین دوره یک مخزن GitHub است.

### گرفتن مخزن دیگران: `git clone`

<div dir="ltr">

```bash
cd ~/git_practice
git clone https://github.com/raminabiri/Bioinformatics_Learning.git
cd Bioinformatics_Learning
git remote -v
git log --oneline | head -3
```

</div>

<div dir="ltr">

```text
Cloning into 'Bioinformatics_Learning'...
origin	https://github.com/raminabiri/Bioinformatics_Learning.git (fetch)
origin	https://github.com/raminabiri/Bioinformatics_Learning.git (push)
87c221b Rebuild part 04 as R Packages: install, run with Rscript, DESeq2/vegan/ggtree examples, pipelines
b5afb1b Rewrite BioLinux and Python parts in the new step-by-step format
1152a4a Complete the Linux part: variables/loops and scripts modules
```

</div>

‏(در 2026-10-21. دوره به‌روز می‌شود، پس commitهای بالای فهرست شما تازه‌ترند.)

- ‏`clone` کل مخزن را **با همه‌ی تاریخچه** می‌گیرد، نه تنها فایل‌های کنونی (برخلاف دانلود ZIP در بخش ۰۱).
- ‏`origin` نام پیش‌فرض نسخه‌ی روی سرور (*remote*) است.
- برای گرفتن تغییرهای تازه‌ی دوره: درون پوشه، `git pull`.

### گذاشتن مخزن خودتان: `git push`

1. در github.com یک حساب بسازید و با دکمه‌ی **New repository** یک مخزن **خالی** بسازید (بی README، تا با مخزن شما تضاد نداشته باشد).
2. **احراز هویت:** GitHub از 2021 گذرواژه‌ی حساب را برای `git push` نمی‌پذیرد. یکی از این دو را بسازید (راهنمای گام‌به‌گام در منابع):
   - ‏**‏Personal Access Token**: یک رمز ویژه که به‌جای گذرواژه وارد می‌کنید؛ یا
   - **کلید SSH**: یک بار تنظیم، سپس بی‌رمز.
3. مخزن محلی را به آن وصل و push کنید:

<div dir="ltr">

```bash
cd ~/git_practice/ecoli_project
git remote add origin https://github.com/<your-user>/ecoli_project.git
git push -u origin main
git push origin v1.0-thesis-ch2
```

</div>

| دستور | یعنی |
| :--- | :--- |
| `git remote add origin <url>` | نشانی مخزن GitHub را با نام `origin` به یاد بسپار (یک بار) |
| `git push -u origin main` | شاخه‌ی main را بفرست؛ `-u` = از این پس `git push` تنها بس است |
| `git push origin <tag>` | ‏tagها جداگانه فرستاده می‌شوند |
| `git pull` | تغییرهای GitHub (برای نمونه از همکار) را بگیر و ادغام کن |

> 📝 این گام‌ها در این درس روی سرور دوره اجرا **نشده‌اند**، چون حساب و توکن شخصی می‌خواهند. دستورها از مستندات رسمی GitHub‌اند (منابع). بی‌توکن، `git push` روی سرور بی‌ترمینال این پیام را داد: `fatal: could not read Username for 'https://github.com'`.

### چرخه‌ی روزانه با GitHub

<div dir="ltr">

```text
git pull  →  edit  →  git status / git diff  →  git add  →  git commit  →  git push
```

</div>

---

## ۸. سه اشتباه رایج

**۱. رمز یا توکن در مخزن.** فایل `ncbi_api_key.txt` یا توکن GitHub در یک اسکریپت، و مخزن عمومی است. حتی اگر commit بعدی پاکش کند، در تاریخچه می‌ماند و ربات‌ها مخزن‌های عمومی را برای همین می‌گردند. **راه:** از روز اول در `.gitignore`؛ اگر رخ داد، **نخست کلید را باطل کنید** (در سایت سرویس) و کلید تازه بسازید.

‏**۲. ‏`git push --force` روی شاخه‌ی مشترک.** تاریخچه‌ی GitHub را با نسخه‌ی شما **جایگزین** می‌کند و کار همکاران پاک می‌شود. پس از `--amend` روی commitی که push شده، Git `push` معمولی را رد می‌کند (`rejected … non-fast-forward`) و وسوسه‌ی `--force` پیش می‌آید. **راه:** برای commitهای push‌شده `revert`، نه `amend`.

**۳. پاک کردن نشانه‌های تضاد را فراموش کردن.** اگر `<<<<<<<` یا `=======` در فایل بماند و commit کنید، اسکریپت دیگر اجرا نمی‌شود. پیش از `git add` پس از تضاد: `grep -n "<<<<<<<\|>>>>>>>" فایل` باید **هیچ** خروجی ندهد.

---

## 📘 برای کنجکاوها

- ‏**‏Pull Request:** در کار گروهی، به‌جای ادغام مستقیم، شاخه را push می‌کنید و در GitHub «درخواست ادغام» می‌دهید؛ همکار تغییرها را می‌بیند، نظر می‌دهد و سپس ادغام می‌کند.
- ‏**‏DOI برای کد:** یک **Release** در GitHub بسازید و آن را به **Zenodo** وصل کنید تا کد مقاله یک DOI همیشگی بگیرد (منابع).
- ‏**‏`git stash`:** تغییرهای commit‌نشده را موقتاً کنار می‌گذارد تا بتوانید شاخه عوض کنید؛ با `git stash pop` برمی‌گردند.

---

## جمع‌بندی

- شاخه = خط کار موازی برای آزمایش: `git switch -c نام`؛ برگشت: `git switch main`.
- ‏`git merge نام` شاخه را در شاخه‌ی کنونی ادغام می‌کند؛ تضاد = تصمیم شما؛ پس از ویرایش `add` و `commit`.
- ‏tag برچسب ثابت نسخه‌ی مقاله یا پایان‌نامه است.
- ‏`--amend` تنها پیش از push؛ `revert` همیشه امن است.
- ‏`clone` / `pull` / `push` با GitHub؛ احراز هویت با توکن یا SSH؛ رمزها هرگز در مخزن.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
git branch                          # list branches (* = current)
git switch -c new-branch            # create and go
git switch main                     # go back
git log --oneline --graph --all     # picture of all branches
git merge other-branch              # merge into current branch
git merge --abort                   # give up a conflicted merge
grep -n "<<<<<<<\|>>>>>>>" file     # leftover conflict markers?
git branch -d other-branch          # delete a merged branch
git tag -a v1.0 -m "message"        # fixed label for a version
git commit --amend -m "new message" # fix last commit (NOT pushed yet)
git revert --no-edit <hash>         # undo a commit with a new commit
git clone <url>                     # copy a repository with history
git remote add origin <url>         # connect to GitHub (once)
git push -u origin main             # first push; later just: git push
git push origin v1.0                # push a tag
git pull                            # get changes from GitHub
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنی |
| :--- | :--- |
| شاخه (*branch*) | خط کار موازی؛ برچسبی متحرک روی آخرین commit خود |
| ادغام (*merge*) | یکی کردن تغییرهای دو شاخه |
| تضاد (*conflict*) | دو شاخه یک جا را جور دیگری عوض کرده‌اند؛ تصمیم با شما |
| ‏tag | برچسب ثابت روی یک commit (نسخه‌ی مقاله) |
| ‏remote / origin | نسخه‌ی مخزن روی سرور / نام پیش‌فرض آن |
| ‏clone / push / pull | گرفتن کل مخزن / فرستادن / گرفتن تغییرها |
| ‏Personal Access Token | رمز ویژه برای احراز هویت Git در GitHub |
| ‏amend / revert | جایگزینی آخرین commit / خنثی کردن با commit تازه |

---

## منابع

**مقاله و مستند**
- Perez-Riverol Y, et al. (2016). *Ten Simple Rules for Taking Advantage of Git and GitHub.* PLoS Comput Biol 12(7):e1004947. https://doi.org/10.1371/journal.pcbi.1004947
- ‏Chacon S, Straub B. *Pro Git*، فصل ۳ «Git Branching»: https://git-scm.com/book/en/v2
- GitHub Docs, *Managing your personal access tokens*: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
- ‏GitHub Docs, *Referencing and citing content* (Zenodo و DOI): https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Version Control with Git* (Atlassian)، ماژول‌های branching و remote: https://www.coursera.org/learn/version-control-with-git
- edX: *Git and GitHub Basics* (IBM): https://www.edx.org/learn/github/ibm-git-and-github-basics
- YouTube: *How Git Works: Explained in 4 Minutes* (ByteByteGo): https://www.youtube.com/watch?v=e9lnsKot_SQ
- YouTube: *Reproducible Research 2026, 02: Version Control with Git* (Bioinformatics.ca): https://www.youtube.com/watch?v=S0kw9OB2Tf0

<sub>نشانی‌های YouTube در 2026-10-13 وارسی شدند. نشانی‌های Coursera و edX از نمایه‌ی جست‌وجو در 2026-10-21 گرفته شدند؛ وارسی مستقیم همه‌ی نشانی‌ها در پایان دوره انجام می‌شود.</sub>

</div>
