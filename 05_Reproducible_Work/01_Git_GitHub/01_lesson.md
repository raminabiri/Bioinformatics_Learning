# درس: کنترل نسخه با Git و GitHub

**بخش:** `05_Reproducible_Work` · **ماژول:** `01_Git_GitHub` · **پیش‌نیاز:** 01_Bash_Linux · **زمان:** ۲ ساعت · **ابزار:** git 2.43 · **آخرین تست:** 2026-10-13

---

## ۱. مسئله

`analysis_final.R`، `analysis_final_v2.R`، `analysis_final_v2_REALLY_FINAL.R`... شش ماه بعد، داور می‌پرسد «شکل ۳ با کدام نسخه‌ی کد ساخته شد؟» و جوابی ندارید.

**Git** هر تغییر کد را با تاریخ، نویسنده و توضیح ثبت می‌کند. می‌توانید هر نسخه‌ی قبلی را بازیابی یا اجرا کنید و چند خط کار موازی (branch) داشته باشید. **GitHub** (یا GitLab و Codeberg) نسخه‌ی آنلاین مخزن است: پشتیبان، همکاری، و انتشار کد همراه مقاله.

> **Git برای کد و متن است، نه داده.** FASTQ، BAM و دیتابیس‌ها در git قرار نمی‌گیرند. فقط **اسکریپت دانلود آن‌ها** ثبت می‌شود. همین مخزن دوره این‌طور ساخته شده است (`.gitignore` ریشه را ببینید).

## ۲. مدل ذهنی: سه ناحیه

```text
 پوشه‌ی کاری (working tree) ──git add──► ناحیه‌ی آماده‌سازی (staging) ──git commit──► تاریخچه (repository)
        ▲                                                                              │
        └──────────────────────────── git restore / git switch ◄──────────────────────┘
```
- **commit** یک عکس کامل از پروژه در یک لحظه است و شناسه‌ی یکتای hash دارد (مثل `31e9354`).
- **branch** اشاره‌گری به یک خط commitهاست. `main` شاخه‌ی اصلی است.
- **remote** (معمولاً `origin`) نسخه‌ی مخزن روی سرور، مثلاً GitHub، است.

## ۳. کار عملی: یک پروژه‌ی کوچک از صفر

کل این جلسه در [scripts/git_demo.sh](../99_scripts_data/01_Git_GitHub/scripts/git_demo.sh) هست. تاریخ (با منطقه‌ی زمانی `+0000`) و نویسنده‌ی commitها در آن ثابت شده تا **hashها در هر کامپیوتری دقیقاً مثل این درس باشند**. hash به محتوا، نویسنده، تاریخ و commit والد بستگی دارد؛ اگر دستورها را دستی تایپ کنید، hashهای شما فرق می‌کند:
```bash
bash scripts/git_demo.sh ../01_Bash_Linux/data/ecoli_k12.gff /tmp/git_practice
```

### گام ۱: شروع و `.gitignore`
```bash
git init -b main ecoli_project && cd ecoli_project
git config user.name "Student"; git config user.email "student@example.org"   # فقط برای همین مخزن
mkdir -p data/raw results scripts
printf 'data/raw/\n*.fastq.gz\nresults/\n' > .gitignore
# ... scripts/count_genes.sh را می‌سازیم؛ یک فایل «داده‌ی حجیم» هم در data/raw می‌گذاریم
git status --short
```
```text
?? .gitignore
?? scripts/
```
`data/raw/a.fastq.gz` در فهرست نیست، چون `.gitignore` آن را نادیده گرفته است. **`.gitignore` را قبل از اولین commit بسازید.** فایلی که یک‌بار commit شود در تاریخچه می‌ماند، حتی اگر بعداً حذفش کنید.

### گام ۲: add، commit، diff
```bash
git add .gitignore scripts/count_genes.sh
git commit -m "Add gene counting script and .gitignore"
# تغییر اسکریپت: شمارش به تفکیک رشته
git diff
```
```text
-awk -F'\t' '$3=="gene"' "$1" | wc -l
+awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
```
```bash
git commit -am "Count genes per strand"     # -a: همه‌ی فایل‌های ردیابی‌شده‌ی تغییرکرده
```
**پیام commit خوب** می‌گوید **چه** و **چرا**، در زمان حال و کوتاه. «Count genes per strand» خوب است و «update» یا «changes» بد.

### گام ۳: branch و merge، و حل conflict
یک branch برای آزمایش تغییری می‌سازیم (فقط tRNAها را بشمار). هم‌زمان در `main` تغییر دیگری می‌دهیم (نام کروموزوم را هم گزارش کن). هر دو تغییر **یک خط** را عوض کرده‌اند:
```bash
git switch -c add-trna      # ... تغییر و commit
git switch main             # ... تغییر دیگر و commit
git merge add-trna
```
```text
Auto-merging scripts/count_genes.sh
CONFLICT (content): Merge conflict in scripts/count_genes.sh
Automatic merge failed; fix conflicts and then commit the result.
```
Git خودش تصمیم نمی‌گیرد و هر دو نسخه را در فایل علامت می‌زند:
```text
<<<<<<< HEAD
awk -F'\t' '$3=="gene"' "$1" | cut -f1,7 | sort | uniq -c
=======
awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f7 | sort | uniq -c
>>>>>>> add-trna
```
**حل conflict یعنی تصمیم علمی شما.** اینجا هر دو تغییر را می‌خواهیم: فقط tRNA، به تفکیک کروموزوم و رشته. فایل را ویرایش می‌کنیم، علامت‌ها را برمی‌داریم، بعد `git add` و `git commit`:
```bash
git log --oneline --graph --all
```
```text
*   43ce93e Merge add-trna: tRNA genes per chromosome and strand
|\
| * a920e2b Count only tRNA genes
* | 19a45e2 Also report chromosome
|/
* 31e9354 Count genes per strand
* cc62ffa Add gene counting script and .gitignore
```
```bash
bash scripts/count_genes.sh ../01_Bash_Linux/data/ecoli_k12.gff
```
```text
     49 NC_000913.3	+
     37 NC_000913.3	-
```
۸۶ tRNA، همان عدد تمرین ۲ ماژول 01/01.

### گام ۴: نسخه‌ی مقاله را علامت بزنید و نسخه‌ی قدیمی را اجرا کنید
```bash
git tag -a v1.0-thesis-ch2 -m "Version used for thesis chapter 2"
bash <(git show HEAD~2:scripts/count_genes.sh) ../01_Bash_Linux/data/ecoli_k12.gff
```
```text
   2216 +
   2290 -
```
`git show <commit>:<file>` محتوای یک فایل را **در آن commit** می‌دهد، بدون تغییر پوشه‌ی کاری. `HEAD~2` یعنی دو commit قبل در شاخه‌ی اصلی (`31e9354`). **این جواب سؤال داور است:** «شکل ۳ با `v1.0-thesis-ch2` ساخته شد. این tag، commit و دستور بازتولید آن است.»

### گام ۵: اشتباه کردم!
| وضعیت | دستور |
| :--- | :--- |
| تغییرات commit‌نشده‌ی یک فایل را دور بریز | `git restore file` |
| فایلی را از staging بیرون بیاور | `git restore --staged file` |
| آخرین commit را با commit جدیدی خنثی کن (امن، تاریخچه حفظ می‌شود) | `git revert HEAD` |
| پیام آخرین commit را اصلاح کن (فقط اگر هنوز push نشده) | `git commit --amend` |

## ۴. GitHub
```bash
git clone https://github.com/raminabiri/Bioinformatics_Learning.git    # همین دوره (مخزن عمومی)
cd Bioinformatics_Learning && git log --oneline | head
```
برای مخزن خودتان:
```bash
git remote add origin https://github.com/<your-user>/<repo>.git
git push -u origin main            # بار اول؛ بعد از آن فقط git push
git pull                           # دریافت تغییرات همکاران
git push origin v1.0-thesis-ch2    # tagها جداگانه push می‌شوند
```
- احراز هویت با رمز عبور حساب GitHub دیگر برای `git push` پذیرفته نمی‌شود. از **SSH key** یا **Personal Access Token** استفاده کنید (مستندات GitHub).
- **برای انتشار همراه مقاله:** یک **Release** در GitHub بسازید و آن را به **Zenodo** وصل کنید تا DOI دائمی بگیرد. لینک GitHub ممکن است تغییر کند ولی DOI می‌ماند (اصل F در FAIR، بخش 00/01).

## ۵. دام‌ها (Pitfalls)

| دام | چرا مشکل است | راه درست |
| :--- | :--- | :--- |
| commit کردن FASTQ، BAM یا دیتابیس | مخزن غول‌پیکر؛ GitHub فایل‌های بالای ۱۰۰ مگابایت را رد می‌کند؛ حذف از تاریخچه سخت است | `.gitignore` از روز اول؛ فقط اسکریپت دانلود |
| commit کردن رمز، توکن یا داده‌ی بیمار | حتی بعد از حذف در تاریخچه می‌ماند و عمومی می‌شود | `.gitignore` + فایل تنظیمات خارج از مخزن؛ اگر رخ داد، کلید را باطل کنید |
| commitهای غول‌پیکر با پیام «update» | تاریخچه بی‌فایده می‌شود | commitهای کوچک، یک تغییر منطقی در هر کدام |
| `git push --force` روی شاخه‌ی مشترک | کار همکاران پاک می‌شود | هرگز روی `main` مشترک |
| کار مستقیم روی `main` برای آزمایش‌ها | نسخه‌ی پایدار خراب می‌شود | branch برای هر آزمایش |
| ثبت نکردن نسخه‌ی کد در مقاله | تکرارپذیری ناممکن | tag + Release + DOI |

## ۶. جمع‌بندی
- چرخه‌ی روزانه: `git status` ← `git add` ← `git commit -m "..."` ← `git push`.
- branch برای آزمایش، merge برای ادغام. conflict یعنی شما تصمیم می‌گیرید.
- tag برای نسخه‌ی مقاله یا پایان‌نامه. `git show <commit>:<file>` برای اجرای نسخه‌ی قدیمی.
- داده در git نیست، فقط اسکریپت‌ها، فایل‌های محیط (ماژول ۰۲) و متن.

---

## منابع

### مقالات و مستندات
- Blischak JD, et al. (2016). A Quick Introduction to Version Control with Git and GitHub. *PLoS Comput Biol* 12(1):e1004668. https://doi.org/10.1371/journal.pcbi.1004668
- Perez-Riverol Y, et al. (2016). Ten Simple Rules for Taking Advantage of Git and GitHub. *PLoS Comput Biol* 12(7):e1004947. https://doi.org/10.1371/journal.pcbi.1004947
- کتاب رایگان *Pro Git*: https://git-scm.com/book/en/v2
- Software Carpentry — *Version Control with Git*: https://swcarpentry.github.io/git-novice/
- مستندات GitHub: https://docs.github.com/en/get-started
- اتصال GitHub به Zenodo برای DOI: https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content

### ویدیوهای آموزشی
- Bioinformatics.ca — *Reproducible Research 2026, 02: Version Control with Git*: https://www.youtube.com/watch?v=S0kw9OB2Tf0
- Riffomonas Project — *How to set up git for a bioinformatics project*: https://www.youtube.com/watch?v=DnwEaa5QtpI
- ByteByteGo — *How Git Works: Explained in 4 Minutes*: https://www.youtube.com/watch?v=e9lnsKot_SQ
- مکتب‌خونه — *آموزش گیت و گیت‌هاب ۲۰۲۶ با جادی، قسمت اول* (فارسی): https://www.youtube.com/watch?v=8RmjKD_YSlg
- Software Carpentry — *The Shell, Episode 1* (پیش‌نیاز کار با git در ترمینال): https://www.youtube.com/watch?v=U3iNcBtycaQ

> لینک‌ها در تاریخ 2026-10-13 بررسی شدند (`_tools/check_links.sh`).
