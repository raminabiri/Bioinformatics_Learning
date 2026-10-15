# محیط‌های نرم‌افزاری دوره

## راه اصلی: Conda/Mamba
```bash
mamba env create -f envs/bioinfo_course.yml     # یا conda env create
conda activate bioinfo_course
```
`bioinfo_course.yml` ابزارهای بخش‌های ۰۰، ۰۱ و ۰۳ (ماژول‌های ۰۱ و ۰۲) را با نسخه‌ی تست‌شده دارد. برای بخش‌های بعدی، هر بخش فایل محیط خودش را می‌گیرد، چون مثلاً QIIME 2 و GROMACS با بقیه سازگار نیستند و نباید در یک محیط باشند.

تنظیم پیشنهادی کانال‌ها (طبق مستندات Bioconda):
```bash
conda config --add channels bioconda
conda config --add channels conda-forge
conda config --set channel_priority strict
```

## راه جایگزین: وقتی `conda.anaconda.org` در دسترس نیست
در تاریخ 2026-10-12 دسترسی به مخزن conda از سرور دوره قطع یا بسیار کند بود. ابزارهای ماژول QC از منبع رسمی هر ابزار نصب شدند. همین روش برای شما هم کار می‌کند:

```bash
mkdir -p ~/opt/course_tools/bin && cd ~/opt/course_tools

# fastp 0.23.4 — باینری استاتیک رسمی
curl -L -o bin/fastp http://opengene.org/fastp/fastp.0.23.4 && chmod +x bin/fastp

# FastQC 0.12.1 — نیاز به Java 11+ دارد
curl -L -o fastqc.zip https://www.bioinformatics.babraham.ac.uk/projects/fastqc/fastqc_v0.12.1.zip
unzip -q fastqc.zip && chmod +x FastQC/fastqc && ln -sf ../FastQC/fastqc bin/fastqc

# Bowtie2 2.5.4 — باینری رسمی از GitHub
curl -L -o bt2.zip https://github.com/BenLangmead/bowtie2/releases/download/v2.5.4/bowtie2-2.5.4-linux-x86_64.zip
unzip -q bt2.zip && for b in bowtie2-2.5.4-linux-x86_64/bowtie2*; do ln -sf ../$b bin/; done

# MultiQC 1.25.1 — از PyPI در یک venv
python3 -m venv mqc && mqc/bin/pip install --timeout 60 --retries 10 multiqc==1.25.1 && ln -sf ../mqc/bin/multiqc bin/multiqc

# فعال‌سازی (به ~/.bashrc هم اضافه کنید)
export PATH=~/opt/course_tools/bin:$PATH
```
seqkit و samtools را می‌توانید از هر محیط conda موجود (یا از صفحه‌ی Releases در GitHub هر ابزار) لینک کنید. `datasets` (NCBI) از https://www.ncbi.nlm.nih.gov/datasets/docs/v2/command-line-tools/download-and-install/ قابل دریافت است.

**نسخه‌هایی که درس‌ها با آن‌ها تست شده‌اند:** FastQC 0.12.1، fastp 0.23.4، MultiQC 1.25.1، Bowtie2 2.5.4، seqkit 2.13.0، samtools 1.20 و wgsim 1.20 (از محیط `snippy_env`)، NCBI datasets 18.38.0، jq 1.7.
