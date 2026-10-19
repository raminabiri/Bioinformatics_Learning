# پاسخ تشریحی: Git و GitHub

> اجرا شده در 2026-10-13 با git 2.43، روی مخزن ساخته‌شده با `scripts/git_demo.sh`.

---

## تمرین ۱

1. ```text
   *   43ce93e Merge add-trna: tRNA genes per chromosome and strand
   |\
   | * a920e2b Count only tRNA genes
   * | 19a45e2 Also report chromosome
   |/
   * 31e9354 Count genes per strand
   * cc62ffa Add gene counting script and .gitignore
   ```
   hashها **یکسان‌اند**، چون hash هر commit تابعی از این‌هاست: محتوای همه‌ی فایل‌ها، نویسنده و ایمیل، تاریخ (با منطقه‌ی زمانی)، پیام، و hash commit(های) والد. اسکریپت همه‌ی این‌ها را ثابت کرده است. اگر فقط تاریخ یک ثانیه فرق کند، آن commit و **همه‌ی commitهای بعدی** hash دیگری می‌گیرند. همین زنجیره است که دست‌کاری پنهان تاریخچه را ناممکن می‌کند.
2. ```bash
   git log --oneline -1 HEAD~1   # 19a45e2 Also report chromosome     ← والد اول (شاخه‌ای که در آن merge کردیم: main)
   git log --oneline -1 HEAD^2   # a920e2b Count only tRNA genes      ← والد دوم (شاخه‌ی ادغام‌شده: add-trna)
   git log --oneline -1 HEAD~2   # 31e9354 Count genes per strand     ← والدِ والد اول
   ```
   `~n` همیشه روی **والد اول** n قدم عقب می‌رود. `^2` یعنی **والد دوم** همین commit.
3. ```text
    scripts/count_genes.sh | 2 +-
    1 file changed, 1 insertion(+), 1 deletion(-)
   ```
   از اول تا آخر فقط **خط سوم یک فایل** عوض شده است. `.gitignore` و دو خط اول اسکریپت تغییر نکرده‌اند.

---

## تمرین ۲

```bash
git status --short
git check-ignore -v results/table.tsv data/raw/b.fastq.gz notes.fastq.gz scripts/plot.R
```
```text
?? scripts/plot.R
.gitignore:3:results/	results/table.tsv
.gitignore:1:data/raw/	data/raw/b.fastq.gz
.gitignore:2:*.fastq.gz	notes.fastq.gz
```
1. فقط **`scripts/plot.R`** در `git status` ظاهر می‌شود. سه فایل دیگر نادیده گرفته شده‌اند.
2. `results/table.tsv` با خط ۳ (`results/`)، `data/raw/b.fastq.gz` با خط ۱ (`data/raw/`)، و `notes.fastq.gz` در ریشه با خط ۲ (`*.fastq.gz`، الگوی بدون `/` در هر پوشه‌ای اعمال می‌شود). `scripts/plot.R` در هیچ قانونی نیست و `check-ignore` برایش چیزی چاپ نمی‌کند.
3. ```bash
   printf '*.bam\n*.bai\n' >> .gitignore
   ```
   الگوی بدون `/` در همه‌ی زیرپوشه‌ها اعمال می‌شود. برای الگوی فقط در ریشه از `/*.bam` استفاده کنید.

---

## تمرین ۳

1. ```text
   ^cc62ffa (Student 2026-10-13 10:00:00 +0000 1) #!/usr/bin/env bash
   ^cc62ffa (Student 2026-10-13 10:00:00 +0000 2) set -euo pipefail
   43ce93ed (Student 2026-10-13 11:00:00 +0000 3) awk -F'\t' '$3=="gene" && ...
   ```
   خطوط ۱ و ۲ از اولین commit (`^` یعنی commit ریشه) هستند. خط ۳ آخرین بار در commit ادغام عوض شده است.
2. ```bash
   git log -p --format='%h %s' -- scripts/count_genes.sh | grep -E '^[0-9a-f]{7} |^\+awk'
   ```
   ```text
   43ce93e Merge add-trna: tRNA genes per chromosome and strand
   19a45e2 Also report chromosome
   +awk -F'\t' '$3=="gene"' "$1" | cut -f1,7 | sort | uniq -c
   a920e2b Count only tRNA genes
   +awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f7 | sort | uniq -c
   31e9354 Count genes per strand
   +awk -F'\t' '$3=="gene"' "$1" | cut -f7 | sort | uniq -c
   cc62ffa Add gene counting script and .gitignore
   +awk -F'\t' '$3=="gene"' "$1" | wc -l
   ```
   توجه: برای commit ادغام (`43ce93e`) `git log -p` به‌طور پیش‌فرض **diff نشان نمی‌دهد**. با `git log -p --cc` diff ترکیبی دیده می‌شود. نسخه‌ی نهایی خط سوم در خود فایل است: فیلتر tRNA به‌علاوه‌ی `cut -f1,7`.
3. ```bash
   bash <(git show 31e9354:scripts/count_genes.sh) ../../01_Bash_Linux/data/ecoli_k12.gff
   ```
   ```text
      2216 +
      2290 -
   ```

---

## تمرین ۴

```bash
git reset --hard HEAD~1             # فقط در مخزن تمرینی! commit ادغام را برمی‌دارد
git merge add-trna                  # CONFLICT
git checkout --ours scripts/count_genes.sh     # نسخه‌ی main (HEAD) را بپذیر
git add scripts/count_genes.sh
git commit -m "Merge add-trna: keep all genes (reject tRNA-only filter)"
bash scripts/count_genes.sh ../../01_Bash_Linux/data/ecoli_k12.gff
```
```text
awk -F'\t' '$3=="gene"' "$1" | cut -f1,7 | sort | uniq -c
   2216 NC_000913.3	+
   2290 NC_000913.3	-
```
2. همه‌ی ۴٬۵۰۶ ژن، به تفکیک کروموزوم و رشته.
3. **کسی که هدف علمی تحلیل را می‌داند.** از نظر Git هر دو تغییر معتبرند. اینکه «فقط tRNA» درست است یا «همه‌ی ژن‌ها» یک تصمیم علمی است که به سؤال پژوهش بستگی دارد. در کار تیمی، conflict را کسی حل می‌کند که branch را merge می‌کند، با مشورت نویسنده‌ی تغییر دیگر. پیام commit هم باید تصمیم را توضیح دهد، مثل «reject tRNA-only filter».

   `git reset --hard` تغییرات را **بازگشت‌ناپذیر** پاک می‌کند. فقط روی مخزن تمرینی یا commitهای push‌نشده استفاده کنید. در مخزن مشترک `git revert` امن است.

---

## تمرین ۵

```bash
echo "API_KEY=abc123" > secret.txt
git add secret.txt && git commit -m "oops add secret"
git rm --cached secret.txt && echo secret.txt >> .gitignore
git add .gitignore && git commit -m "Stop tracking secret.txt"
git show HEAD~1:secret.txt
git log --all --oneline -- secret.txt
```
```text
API_KEY=abc123
bfc32c6 Stop tracking secret.txt
9793cfb oops add secret
```
2. **خیر.** فایل از commit‌های **بعدی** حذف شده، ولی در commit `9793cfb` برای همیشه باقی است. هر کسی که مخزن را clone کند با یک دستور آن را می‌خواند.
3. **اول کلید یا رمز را باطل کنید و کلید جدید بسازید.** پاک کردن تاریخچه دوم است. مخزن عمومی ممکن است در چند دقیقه توسط ربات‌ها اسکن و کپی شده باشد، پس فرض کنید رمز لو رفته است. بعد از باطل کردن، می‌توانید تاریخچه را با ابزارهایی مثل `git filter-repo` پاک کنید. این کار تاریخچه را بازنویسی می‌کند و همه‌ی همکاران باید دوباره clone کنند. **همین منطق برای داده‌ی بیمار هم صادق است**، با این تفاوت که داده‌ی لو رفته را نمی‌شود «باطل» کرد. پس پیشگیری (`.gitignore` از روز اول) تنها راه واقعی است.

---

## تمرین ۶ (چالشی): فهرست بررسی

- [ ] `.gitignore` قبل از اولین commit: `data/raw/`، `*.fastq.gz`، `*.bam`، `results/` (اگر قابل بازتولید است)، `.Rhistory`، `__pycache__/`، `work/`
- [ ] `README.md`: هدف، پیش‌نیاز، `conda env create -f environment.yml`، اسکریپت دانلود داده، دستور اجرا، ساختار پوشه‌ها
- [ ] `environment.yml` با نسخه‌های پین‌شده (ماژول ۰۲)
- [ ] `data/download.sh` با شناسه‌های نسخه‌دار و md5 (مثل `06_Metagenomics/data/download.sh`)
- [ ] commitهای کوچک با پیام معنادار، مثلاً:
  - `Add data download script with md5 checks`
  - `Add gene counting script`
  - `Report counts per strand`
- [ ] `git tag -a v0.1 -m "..."` برای نسخه‌ای که در گزارش استفاده شد
- [ ] (اختیاری) `git push -u origin main && git push --tags`، ساخت Release در GitHub و اتصال به Zenodo برای DOI
- [ ] بررسی نهایی: `git status` تمیز باشد و `git ls-files` هیچ فایل داده‌ی حجیمی نشان ندهد.

نمونه‌ی کامل همین الگو خود این مخزن دوره است: `README.md`، `.gitignore`، `envs/`، و `data/download.sh` در هر بخش.
