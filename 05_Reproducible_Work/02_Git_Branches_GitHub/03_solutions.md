<div dir="rtl">

# پاسخ تشریحی: شاخه، ادغام و GitHub

خروجی‌ها از اجرای واقعی در 2026-10-21 (git 2.43) گرفته شده‌اند. hashهای commitهای تازه‌ی شما فرق می‌کنند؛ بقیه‌ی خروجی‌ها باید یکسان باشند.

---

## پاسخ ۱: شاخه‌ای که تنها جلو رفت

<div dir="ltr">

```bash
git switch -c readme
printf '# E. coli gene counts\nUsage: bash scripts/count_genes.sh ecoli_k12.gff\n' > README.md
git add README.md
git commit -m "Add README"
git switch main
git merge readme
git log --oneline --graph -3
```

</div>

<div dir="ltr">

```text
Switched to a new branch 'readme'
[readme 81dd627] Add README
 1 file changed, 2 insertions(+)
 create mode 100644 README.md
Switched to branch 'main'
Updating ae3f591..81dd627
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)
 create mode 100644 README.md
* 81dd627 Add README
* ae3f591 Revert "Add usage note"
* ed406c5 Add usage note
```

</div>

- (الف) پس از ساختن `readme`، در `main` هیچ commit تازه‌ای نبود. پس `main` تنها باید **جلو برود** تا به `81dd627` برسد: این **‏fast-forward** است. چیزی برای ادغام یا تضاد نبود و commit ادغامی هم لازم نشد.
- (ب) یک خط راست، بی شاخه‌ی جدا؛ گویی کار از آغاز در `main` بوده است.

---

## پاسخ ۲: ادغام بی‌تضاد

<div dir="ltr">

```bash
git switch -c sort-numeric
sed -i 's/sort | uniq -c/sort | uniq -c | sort -k1,1nr/' scripts/count_genes.sh
git commit -qam "Sort by count"
git switch -q main
printf 'Data: NCBI RefSeq NC_000913.3\n' >> README.md
git commit -qam "Document data source"
git merge --no-edit sort-numeric
git log --oneline --graph -5
bash scripts/count_genes.sh $GFF
cat README.md
```

</div>

<div dir="ltr">

```text
Switched to a new branch 'sort-numeric'
Merge made by the 'ort' strategy.
 scripts/count_genes.sh | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)
*   fbdb5db Merge branch 'sort-numeric'
|\  
| * 5095f5d Sort by count
* | eb07d4e Document data source
|/  
* 81dd627 Add README
* ae3f591 Revert "Add usage note"
     49 NC_000913.3	+
     37 NC_000913.3	-
# E. coli gene counts
Usage: bash scripts/count_genes.sh ecoli_k12.gff
Data: NCBI RefSeq NC_000913.3
```

</div>

‏`Merge made by the 'ort' strategy` (`ort` نام روش ادغام خودکار Git است) و یک commit ادغام (`fbdb5db`) با پیام پیش‌فرض `Merge branch 'sort-numeric'`. هر دو شاخه کار کرده بودند، ولی روی **فایل‌های جدا**، پس Git خودش ادغام کرد. هر دو تغییر هستند: اسکریپت تازه (`sort -k1,1nr`) و خط Data در README. (چون ۴۹ از ۳۷ بزرگ‌تر است، ترتیب خروجی پیش و پس از `sort -k1,1nr` یکی است.)

---

## پاسخ ۳: تضاد در README

<div dir="ltr">

```bash
git switch -q -c title
sed -i '1s/.*/# E. coli K-12: tRNA genes per strand/' README.md
git commit -qam "Clarify title"
git switch -q main
sed -i '1s/.*/# Gene counts (E. coli)/' README.md
git commit -qam "Shorter title"
git merge title
cat README.md
```

</div>

<div dir="ltr">

```text
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
<<<<<<< HEAD
# Gene counts (E. coli)
=======
# E. coli K-12: tRNA genes per strand
>>>>>>> title
Usage: bash scripts/count_genes.sh ecoli_k12.gff
Data: NCBI RefSeq NC_000913.3
```

</div>

با `nano README.md`، خط‌های `<<<<<<< HEAD`، `# Gene counts (E. coli)`، `=======` و `>>>>>>> title` را پاک کنید (اینجا عنوان شاخه‌ی `title` را نگه داشتیم، چون می‌گوید tRNA و رشته). وارسی و ثبت:

<div dir="ltr">

```bash
grep -c "<<<<<<<\|>>>>>>>" README.md
cat README.md
git add README.md
git commit -qm "Merge title: keep the clearer title"
git log --oneline --graph -4
```

</div>

<div dir="ltr">

```text
0
# E. coli K-12: tRNA genes per strand
Usage: bash scripts/count_genes.sh ecoli_k12.gff
Data: NCBI RefSeq NC_000913.3
*   15e330e Merge title: keep the clearer title
|\  
| * c8e8dfd Clarify title
* | 8ecae17 Shorter title
|/  
```

</div>

‏`grep -c` = **۰**: نشانه‌ای نمانده. (با `grep -n` به‌جای `-c`، هیچ خطی چاپ نمی‌شود.) هر دو پاسخ «درست» است اگر آگاهانه برگزیده باشید؛ می‌توانستید دو عنوان را هم با هم ترکیب کنید.

---

## پاسخ ۴: نسخه‌ی پایان‌نامه در برابر امروز

<div dir="ltr">

```bash
bash <(git show v1.0-thesis-ch2:scripts/count_genes.sh) $GFF
git diff v1.0-thesis-ch2 -- scripts/count_genes.sh | tail -2
```

</div>

<div dir="ltr">

```text
     49 NC_000913.3	+
     37 NC_000913.3	-
-awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f1,7 | sort | uniq -c
+awk -F'\t' '$3=="gene" && $9 ~ /gene_biotype=tRNA/' "$1" | cut -f1,7 | sort | uniq -c | sort -k1,1nr
```

</div>

- (الف) ۴۹ و ۳۷؛ همان عددهای درس.
- (ب) تنها `| sort -k1,1nr` (ترتیب خروجی بر پایه‌ی شمار) افزوده شده. **عددها عوض نمی‌شوند**؛ تنها ترتیب سطرها شاید عوض شود. با `git diff <tag>` همیشه می‌توانید بگویید از نسخه‌ی مقاله تا امروز دقیقاً چه عوض شده است.

---

## پاسخ ۵: GitHub ساختگی روی کامپیوتر خودتان

<div dir="ltr">

```bash
cd ~/git_ex02
git init --bare -b main fake_github.git
cd ecoli_project
git remote add origin ../fake_github.git
git push -u origin main
git push origin v1.0-thesis-ch2
```

</div>

<div dir="ltr">

```text
Initialized empty Git repository in /home/you/git_ex02/fake_github.git/
To ../fake_github.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.
To ../fake_github.git
 * [new tag]         v1.0-thesis-ch2 -> v1.0-thesis-ch2
```

</div>

همکار:

<div dir="ltr">

```bash
cd ~/git_ex02
git clone fake_github.git colleague
cd colleague
git config user.name "Colleague"; git config user.email "colleague@example.org"
echo "Contact: colleague@example.org" >> README.md
git commit -qam "Add contact"
git push
```

</div>

<div dir="ltr">

```text
Cloning into 'colleague'...
done.
...
   15e330e..cc4be45  main -> main
```

</div>

‏(`git config` بی `--global` = تنها برای این مخزن؛ تا commitها نام همکار را بگیرند.) و شما:

<div dir="ltr">

```bash
cd ~/git_ex02/ecoli_project
git pull
tail -1 README.md
```

</div>

<div dir="ltr">

```text
From ../fake_github
   15e330e..cc4be45  main       -> origin/main
Updating 15e330e..cc4be45
Fast-forward
 README.md | 1 +
 1 file changed, 1 insertion(+)
Contact: colleague@example.org
```

</div>

خط همکار رسید. ‏`git pull` یک **fast-forward** بود (همانند تمرین ۱): در این فاصله شما commit تازه‌ای نداشتید. اگر داشتید، `pull` یک ادغام واقعی می‌کرد و شاید تضاد. **روی GitHub واقعی** تنها نشانی `origin` فرق می‌کند (`https://github.com/...`)؛ بقیه‌ی دستورها همین‌اند.

---

## پاسخ ۶: amend پس از push

<div dir="ltr">

```bash
echo "Licence: CC-BY 4.0" >> README.md
git commit -qam "Add licence"
git push -q
git commit -q --amend -m "Add license (CC-BY 4.0)"
git push
```

</div>

<div dir="ltr">

```text
To ../fake_github.git
 ! [rejected]        main -> main (non-fast-forward)
error: failed to push some refs to '../fake_github.git'
hint: Updates were rejected because the tip of your current branch is behind
hint: its remote counterpart. If you want to integrate the remote changes,
hint: use 'git pull' before pushing again.
```

</div>

- (الف) **رد شد** (`rejected … non-fast-forward`). commit کهنه (`Add licence`) روی سرور است؛ `--amend` آن را **در کامپیوتر شما** با commit تازه‌ای جایگزین کرد. حالا دو تاریخچه از هم جدا شده‌اند.

<div dir="ltr">

```bash
git pull --no-rebase --no-edit
git log --oneline --graph -4
git push
```

</div>

<div dir="ltr">

```text
Merge made by the 'ort' strategy.
*   4cce0fe Merge branch 'main' of ../fake_github
|\  
| * a7462b2 Add licence
* | cd5dd4c Add license (CC-BY 4.0)
|/  
* cc4be45 Add contact
   a7462b2..4cce0fe  main -> main
```

</div>

- (ب) کار درست شد، ولی تاریخچه حالا **دو commit با یک کار** و یک commit ادغام بی‌معنا دارد. راه بهتر: پس از push، پیام را **رها کنید** (یک غلط تایپی در پیام آسیبی ندارد) یا اگر محتوا اشتباه بود، `git revert`. **‏`--amend` تنها پیش از push.** (و هرگز `git push --force` روی مخزن مشترک: کار همکار از سرور پاک می‌شود.)

---

## پاسخ ۷ (فکری): توکن در مخزن عمومی

به ترتیب:
1. **کلید را همین حالا در سایت سرویس باطل کنید** (برای NCBI: در تنظیمات حساب، کلید را پاک کنید) و کلید تازه بسازید. این مهم‌ترین گام است: کلید پیش‌تر **عمومی** بوده و شاید کسی (یا رباتی) آن را برداشته باشد.
2. کلید تازه را **بیرون از مخزن** نگه دارید (برای نمونه در `~/.ncbi_key` یا یک متغیر محیطی، بخش ۰۱)، و اسکریپت آن را از آن‌جا بخواند. نام فایل کلید را در `.gitignore` بگذارید.
3. اسکریپت بی‌کلید را commit و push کنید. اگر لازم است کلید کهنه از **تاریخچه** هم پاک شود، ابزارهای ویژه‌ای هست (راهنمای GitHub: *Removing sensitive data from a repository*)؛ ولی این کار جای گام ۱ را نمی‌گیرد.

چرا commit تازه بس نیست؟ چون کلید در **commit دیروز** می‌ماند و هر کسی با `git log -p` یا `git show <hash>:فایل` (ماژول ۰۱) آن را می‌بیند. هر کپی (clone) مخزن هم آن را دارد.

</div>
