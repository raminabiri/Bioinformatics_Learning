**پاسخ‌نامه تمرین‌های جلسه اول**

**پاسخ تمرین ۱:**
```bash
# استفاده از سوئیچ -p برای ساخت همزمان مسیرهای تو در تو
mkdir -p bio_project/data
cd bio_project/data
# برای چاپ مسیر فعلی:
pwd
# استفاده از علامت > برای ساخت فایل و ریختن خروجی در آن
echo ">protein_mutant" > sample.fasta
# استفاده از علامت >> برای اضافه کردن به انتهای فایل (بدون پاک شدن خطوط قبل)
echo "MKTAYIAKQRQISF" >> sample.fasta
cat sample.fasta
mv sample.fasta protein_final.fasta
# ابزار less برای خواندن فایل‌های حجیم بدون اشغال بیش از حد رم استفاده می‌شود
less protein_final.fasta
tail -n 10 genome.fasta
# سوئیچ -c در اینجا کار شمارش (count) را انجام می‌دهد
# علامت ^ یعنی جستجو فقط در ابتدای خطوط انجام شود
grep -c "^>" protein_final.fasta
# ابتدا با grep -o الگوها جدا می‌شوند و با | (پایپ) خروجی به wc -l داده می‌شود تا شمرده شوند
grep -o "ATG" genome.fasta | wc -l
