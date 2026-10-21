<div dir="rtl">

# تمرین‌ها: شاخه، ادغام و GitHub

برای اینکه نقطه‌ی آغاز همه یکسان باشد، یک مخزن تازه با کل جلسه‌ی درس بسازید و در آن کار کنید:

<div dir="ltr">

```bash
GFF=~/Bioinformatics_Learning-main/01_Linux/99_scripts_data/data/ecoli_k12.gff
bash ~/Bioinformatics_Learning-main/05_Reproducible_Work/99_scripts_data/01_Git_Basics/scripts/git_demo.sh $GFF ~/git_ex02
cd ~/git_ex02/ecoli_project
git log --oneline -1          # ae3f591 Revert "Add usage note"
```

</div>

‏hashهای commitهای **تازه‌ی** شما با پاسخ‌نامه فرق می‌کنند (ماژول ۰۱، درس، بخش ۴).

---

## تمرین ۱: شاخه‌ای که تنها جلو رفت
> **راهنمایی:** درس، بخش‌های ۳ و ۴. در ادغام به واژه‌ی `Fast-forward` نگاه کنید.

یک شاخه به نام `readme` بسازید، در آن فایل `README.md` با دو خط زیر بنویسید و commit کنید. سپس به `main` برگردید و `readme` را ادغام کنید.

<div dir="ltr">

```text
# E. coli gene counts
Usage: bash scripts/count_genes.sh ecoli_k12.gff
```

</div>

(الف) چرا این بار تضادی نبود و حتی commit ادغام هم ساخته نشد؟ (ب) `git log --oneline --graph -3` چه شکلی دارد؟

---

## تمرین ۲: ادغام بی‌تضاد
> **راهنمایی:** درس، کادر «اگر ادغام بی‌تضاد باشد». `--no-edit` = پیام پیش‌فرض ادغام را بپذیر.

‏(الف) شاخه‌ی `sort-numeric` بسازید و در آن خروجی اسکریپت را بر پایه‌ی شمار مرتب کنید:

<div dir="ltr">

```bash
sed -i 's/sort | uniq -c/sort | uniq -c | sort -k1,1nr/' scripts/count_genes.sh
```

</div>

‏(ب) در `main` خط `Data: NCBI RefSeq NC_000913.3` را به پایان `README.md` بیفزایید و commit کنید. (ج) `sort-numeric` را با `git merge --no-edit` ادغام کنید. Git چه پیامی می‌دهد؟ گراف چه شکلی دارد؟ آیا هر دو تغییر در نتیجه هستند؟

---

## تمرین ۳: تضاد در README
> **راهنمایی:** درس، بخش ۴. نشانه‌های `<<<<<<<`، `=======`، `>>>>>>>` را با `nano` پاک کنید و با `grep -n` وارسی کنید که چیزی نمانده.

در شاخه‌ی `title` خط یکم README را به `# E. coli K-12: tRNA genes per strand` تغییر دهید و commit کنید؛ در `main` همان خط را به `# Gene counts (E. coli)`. ادغام کنید. تضاد را با نگه داشتن **عنوان روشن‌تر** (به نظر شما) حل کنید. پیش از commit، چه دستوری نشان می‌دهد هیچ نشانه‌ی تضادی نمانده؟

---

## تمرین ۴: نسخه‌ی پایان‌نامه در برابر امروز
> **راهنمایی:** درس، بخش ۵. `git diff <tag> -- فایل` تفاوت آن نسخه با نسخه‌ی کنونی را نشان می‌دهد.

(الف) نسخه‌ی `scripts/count_genes.sh` در tag `v1.0-thesis-ch2` را اجرا کنید. (ب) با `git diff v1.0-thesis-ch2 -- scripts/count_genes.sh` ببینید از آن نسخه تا امروز چه عوض شده است. آیا این تغییر **عددها**ی فصل ۲ را عوض می‌کند؟

---

## تمرین ۵: GitHub ساختگی روی کامپیوتر خودتان
> **راهنمایی:** درس، بخش ۷. یک مخزن `--bare` همان کاری را می‌کند که GitHub: جایی برای push و clone، بی پوشه‌ی کاری. همه‌ی دستورهای push/pull/clone درس روی آن کار می‌کنند، بی حساب و توکن.

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

حالا نقش **همکار** را بازی کنید: مخزن را در پوشه‌ی `~/git_ex02/colleague` با `git clone` بگیرید، در آن یک خط `Contact: colleague@example.org` به README بیفزایید، commit و push کنید. سپس به `ecoli_project` برگردید و `git pull` بزنید. آیا خط همکار رسید؟ `git pull` چه نوع ادغامی کرد؟

---

## تمرین ۶: amend پس از push
> **راهنمایی:** درس، بخش ۶ و اشتباه رایج ۲.

در `ecoli_project` (پس از تمرین ۵) خط `Licence: CC-BY 4.0` را به README بیفزایید، commit و **push** کنید. سپس پیام را با `git commit --amend -m "Add license (CC-BY 4.0)"` اصلاح و دوباره `git push` کنید. (الف) Git چه می‌گوید؟ (ب) با `git pull --no-rebase --no-edit` و سپس `git push` وضعیت را درست کنید و گراف را ببینید. چرا این تاریخچه «نازیبا» است و راه بهتر چه بود؟

---

## تمرین ۷ (فکری): توکن در مخزن عمومی
> **راهنمایی:** درس، اشتباه رایج ۱؛ ماژول ۰۱، تمرین ۷.

شما دیروز یک اسکریپت دانلود با یک **API key** درون آن به مخزن **عمومی** GitHub push کردید. امروز متوجه شدید. سه کار را به ترتیب اولویت بنویسید. چرا «پاک کردن کلید از اسکریپت و commit تازه» به‌تنهایی بس نیست؟

</div>
