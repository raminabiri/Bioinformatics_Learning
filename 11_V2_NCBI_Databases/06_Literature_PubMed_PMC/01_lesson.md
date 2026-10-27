<div dir="rtl">

# درس: PubMed، MeSH، PMC و PubTator3؛ جست‌وجوی دقیق و خواندن ماشینی ادبیات

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `06_Literature_PubMed_PMC` · **پیش‌نیاز:** ماژول [11/01](../01_Entrez_EDirect/) (E-utilities، EDirect، `xtract`)؛ ماژول [09/01](../../09_Structural_Bioinformatics/01_Protein_Structure/) (جهش‌های S531L، H526Y، D516V و شماره‌گذاری *E. coli* و *M. tuberculosis*) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** curl 8.20.0، EDirect 24.0، jq، Literature Citation Exporter، PMC ID Converter، PubTator3 API · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). شمار مقاله‌ها هر روز بالا می‌رود.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. ببینید PubMed پرسش شما را چگونه **ترجمه** می‌کند (Automatic Term Mapping) و چرا املای یک واژه شمار نتیجه را سه برابر می‌کند.
2. با **MeSH** (واژگان کنترل‌شده‌ی NLM) و برچسب‌های `[tiab]`، `[MeSH Terms]`، `[MeSH Major Topic]` و `[pt]` جست‌وجوی دقیق بسازید.
3. صدها رکورد را بگیرید و با `xtract` جدول کنید (سال، مجله).
4. فهرست منابع را خودکار در قالب **RIS** یا **AMA/APA** بگیرید.
5. از PubMed به **PMC** (متن کامل) بروید و متن را بکاوید.
6. با **PubTator3** ژن‌ها، جهش‌ها، داروها و جانداران نام‌برده در یک مقاله را بیرون بکشید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m06 && cd ~/ncbi/m06
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
P3=https://www.ncbi.nlm.nih.gov/research/pubtator3-api
```

</div>

---

## ۱. داستان

در ماژول 09/01 ساختار 5UAC را از مقاله‌ی Molodtsov و همکاران (۲۰۱۷) دیدید و سه جهش مقاومت به ریفامپیسین (S531L، H526Y، D516V) را روی آن یافتید. حالا می‌خواهید یک **مرور ادبیات** بنویسید: «جهش‌های rpoB و مقاومت به ریفامپیسین در *E. coli*». در PubMed می‌نویسید `rifampicin resistance` و **۱۷٬۱۶۹** مقاله می‌گیرید. نمی‌شود همه را خواند. در این درس یاد می‌گیرید پرسش را دقیق کنید، بدانید PubMed چه کرده است، نتیجه را جدول کنید، و حتی بگذارید یک ابزار متن‌کاوی جهش‌ها را از مقاله‌ها برایتان بیرون بکشد. **پاسخ معلوم:** مقاله‌ی Molodtsov باید همان سه جهش را نشان دهد.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏PubMed، MEDLINE و PMC

| | چیست | چه دارد |
| :--- | :--- | :--- |
| ‏**PubMed** | موتور جست‌وجوی ادبیات زیست‌پزشکی | نزدیک به ۴۰ میلیون رکورد: عنوان، چکیده، نویسندگان |
| ‏**MEDLINE** | بخش اصلی PubMed | رکوردهایی که کتابداران NLM با **MeSH** نمایه کرده‌اند |
| ‏**PMC** | بایگانی **متن کامل** | مقاله‌های آزاد و دست‌نوشته‌های پژوهش‌های با بودجه‌ی NIH |

### ‏۲.۲ ‏MeSH: یک نام برای هر مفهوم

نویسندگان یک دارو را «rifampicin»، «rifampin» یا «RIF» می‌نامند. کتابداران NLM به هر مقاله‌ی MEDLINE چند **سرعنوان MeSH** (Medical Subject Headings) می‌دهند؛ هر مفهوم یک نام و یک شناسه دارد (Rifampin = ‏`D012293`)، هر چه نویسنده نوشته باشد. سرعنوان‌ها در **درخت** چیده شده‌اند (دارو → آنتی‌بیوتیک → ریفامایسین‌ها → Rifampin). نشان `*` روی یک سرعنوان یعنی **موضوع اصلی** مقاله (Major Topic)؛ و پس از `/` یک **زیرسرعنوان** می‌آید (`Rifampin/pharmacology`).

**تشبیه:** MeSH برچسب‌های قفسه‌ی کتابخانه است؛ هر کتاب، هر عنوانی داشته باشد، زیر یک برچسب استاندارد می‌رود.

> 📺 **فیلم:** *This MeSH tutorial will dramatically improve your literature search on PubMed* (EvidentiaSystems): https://www.youtube.com/watch?v=7fWFupz0LVA
> 📄 **مرجع:** ‏MeSH (NLM): https://www.nlm.nih.gov/mesh/meshhome.html · راهنمای PubMed: https://pubmed.ncbi.nlm.nih.gov/help/

---

## ۳. گام ۱: PubMed پرسش شما را چگونه می‌فهمد؟

<div dir="ltr">

```bash
for q in 'rifampicin resistance' 'rifampicin' \
         '"Rifampin"[MeSH Terms] AND "Drug Resistance, Bacterial"[MeSH Terms]' \
         '"Rifampin/pharmacology"[MeSH Terms] AND rpoB[tiab]' \
         'rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms]' \
         'rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms] AND review[pt]'; do
  r=$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode "term=$q")
  echo "$(echo "$r" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2) | $q"
  echo "   -> $(echo "$r" | grep -oE '<QueryTranslation>[^<]*' | cut -d'>' -f2 | cut -c1-250)"
  sleep 0.4
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
17169 | rifampicin resistance
   -> ("rifampicins"[All Fields] OR "rifampin"[Supplementary Concept] OR "rifampin"[All Fields] OR "rifampicin"[All Fields] OR "rifampin"[MeSH Terms] OR "rifampicine"[All Fields]) AND ("resist"[All Fields] OR "resistance"[All Fields] OR "resistances"[All F
38849 | rifampicin
   -> "rifampicins"[All Fields] OR "rifampin"[Supplementary Concept] OR "rifampin"[All Fields] OR "rifampicin"[All Fields] OR "rifampin"[MeSH Terms] OR "rifampicine"[All Fields]
2938 | "Rifampin"[MeSH Terms] AND "Drug Resistance, Bacterial"[MeSH Terms]
   -> "Rifampin"[MeSH Terms] AND "drug resistance, bacterial"[MeSH Terms]
1025 | "Rifampin/pharmacology"[MeSH Terms] AND rpoB[tiab]
   -> "rifampin/pharmacology"[MeSH Terms] AND "rpoB"[Title/Abstract]
83 | rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms]
   -> "rpoB"[Title/Abstract] AND "rifampicin"[Title/Abstract] AND "Escherichia coli"[MeSH Terms]
1 | rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms] AND review[pt]
   -> "rpoB"[Title/Abstract] AND "rifampicin"[Title/Abstract] AND "Escherichia coli"[MeSH Terms] AND "review"[Publication Type]
```

</div>

**توضیح خروجی:**
- ‏**Automatic Term Mapping (ATM):** برای «rifampicin» بی برچسب، PubMed شش جست‌وجو را با `OR` به هم بسته است: املای‌های گوناگون، سرعنوان MeSH (`"rifampin"[MeSH Terms]`) و «Supplementary Concept». «resistance» هم به «resist» و «resistances» گسترده شده. برای نگاه نخست خوب است؛ برای جست‌وجوی دقیق و تکرارپذیر نه.
- ‏`[MeSH Terms]`: تنها مقاله‌هایی که کتابدار آن مفهوم را برایشان گذاشته است: ‏**۲۹۳۸** به جای ۱۷٬۱۶۹. مقاله‌هایی که تنها گذرا به مقاومت اشاره کرده‌اند بیرون می‌روند.
- ‏`[tiab]` = عنوان یا چکیده. ‏`[pt]` = گونه‌ی انتشار (review، clinical trial، …).
- با سه برچسب به **۸۳** رسیدیم؛ یک عدد خواندنی.

### ۳.۱ دام املای واژه

<div dir="ltr">

```bash
for q in 'rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms]' \
         'rpoB[tiab] AND rifampin[tiab] AND "Escherichia coli"[MeSH Terms]' \
         'rpoB[tiab] AND (rifampicin[tiab] OR rifampin[tiab]) AND "Escherichia coli"[MeSH Terms]' \
         'rpoB[tiab] AND "Rifampin"[MeSH Terms] AND "Escherichia coli"[MeSH Terms]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode "term=$q" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2) | $q"
  sleep 0.4
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
83 | rpoB[tiab] AND rifampicin[tiab] AND "Escherichia coli"[MeSH Terms]
33 | rpoB[tiab] AND rifampin[tiab] AND "Escherichia coli"[MeSH Terms]
115 | rpoB[tiab] AND (rifampicin[tiab] OR rifampin[tiab]) AND "Escherichia coli"[MeSH Terms]
84 | rpoB[tiab] AND "Rifampin"[MeSH Terms] AND "Escherichia coli"[MeSH Terms]
```

</div>

**توضیح خروجی:**
- ‏«rifampicin» (املای اروپایی) **۸۳** و «rifampin» (املای آمریکایی) **۳۳**؛ با هم **۱۱۵** (تنها یک مقاله هر دو را دارد). اگر تنها یکی را بنویسید، نزدیک به یک‌سوم یا دوسوم مقاله‌ها را از دست می‌دهید.
- سرعنوان MeSH (۸۴) هر دو املا را می‌پوشاند ولی تنها روی رکوردهای **نمایه‌شده**؛ مقاله‌های تازه که هنوز MeSH نگرفته‌اند (چند ماه تا یک سال) بیرون می‌مانند.
- **راه درست برای مرور:** هر دو: `(MeSH OR همه‌ی املاها[tiab])`. در این درس با ۱۱۵ ادامه می‌دهیم.

> 📺 **فیلم:** *This MeSH tutorial will dramatically improve your literature search on PubMed*: https://www.youtube.com/watch?v=7fWFupz0LVA
> 📄 **مرجع:** راهنمای PubMed، بخش‌های «Automatic Term Mapping» و «Search Field Descriptions and Tags»: https://pubmed.ncbi.nlm.nih.gov/help/

---

## ۴. گام ۲: پایگاه MeSH

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=mesh&id=68012293&version=2.0" > mesh.xml
grep -oE '<(DS_YearIntroduced|DS_ScopeNote)>[^<]{0,200}' mesh.xml
grep -oE '<string>[^<]*' mesh.xml | head -7 | tr '\n' ' '; echo
grep -oE '<TreeNum>[^<]*' mesh.xml
```

</div>

‏UID پایگاه `mesh` برای سرعنوان `D012293` عدد **68012293** است: `68` + شماره (همان قاعده‌ی گونه‌ای که در GEO دیدید).

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<DS_YearIntroduced>1973
<DS_ScopeNote>A semisynthetic antibiotic produced from Streptomyces mediterranei. It has a broad antibacterial spectrum, including activity against several forms of Mycobacterium. In susceptible organisms it inhibits DNA-depe
<string>Rifampin <string>Benemycin <string>Rifampicin <string>Rifadin <string>Rimactane <string>Tubocin <string>Rimactan
<TreeNum>D03.633.400.811.700
<TreeNum>D04.345.295.750.700
```

</div>

**توضیح خروجی:**
- از **۱۹۷۳** سرعنوان MeSH است؛ شرح می‌گوید RNA پلیمراز وابسته به DNA را باز می‌دارد (همان سازوکار 09/01).
- **نام‌های هم‌ارز** (entry terms): Rifampicin، Rifadin، Rimactane، … . جست‌وجوی `"Rifampin"[MeSH Terms]` همه را می‌پوشاند.
- دو **شماره‌ی درخت**: `D03…` (ترکیب‌های هتروسیکلیک) و `D04…` (ترکیب‌های چندحلقه‌ای). یک مفهوم می‌تواند در چند شاخه باشد. جست‌وجوی MeSH به گونه‌ی پیش‌فرض **همه‌ی زیرشاخه‌ها** را هم می‌آورد (explode).

---

## ۵. گام ۳: ۱۱۵ مقاله در یک جدول

<div dir="ltr">

```bash
Q='rpoB[tiab] AND (rifampicin[tiab] OR rifampin[tiab]) AND "Escherichia coli"[MeSH Terms]'
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode usehistory=y --data-urlencode "term=$Q" > h.xml
WE=$(grep -o '<WebEnv>[^<]*' h.xml | cut -d'>' -f2)
curl -sS "$B/efetch.fcgi?db=pubmed&query_key=1&WebEnv=$WE&retmode=xml&retmax=200" > pm.xml
ls -la pm.xml
xtract -input pm.xml -mixed -pattern PubmedArticle -element MedlineCitation/PMID \
       -block PubDate -element Year -block MedlineJournalInfo -element MedlineTA > pm.tsv
wc -l < pm.tsv; head -3 pm.tsv
cut -f3 pm.tsv | sort | uniq -c | sort -rn | head -5
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`retmax=200` | تا ۲۰۰ رکورد در یک درخواست (پیش‌فرض ۲۰) |
| ‏`xtract -input pm.xml` | ‏`xtract` به جای لوله، یک فایل را بخواند |
| ‏`-mixed` | ‏XML پابمد درون متن برچسب دارد (`<i>`، `<sup>` برای نام گونه و نمایه)؛ بی این گزینه `xtract` برای هر کدام خطای `UNEXPECTED MIXED CONTENT` می‌دهد (ما ۴۴ کیلوبایت از این خطا گرفتیم) |
| ‏`MedlineCitation/PMID` | ‏`PMID` درون `MedlineCitation`؛ چون PMIDهای دیگری (منابع مقاله) هم در رکورد هست |
| ‏`MedlineTA` | نام کوتاه مجله |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
-rw-rw-r-- 1 ubuntu ubuntu 1602613 Oct 27 14:54 pm.xml
115
41748027	2026	J Food Prot
41412349	2026	J Glob Antimicrob Resist
40729517	2025	Mol Biol Evol
     19 J Bacteriol
     15 Mol Gen Genet
      9 Antimicrob Agents Chemother
      4 Proc Natl Acad Sci U S A
      4 J Mol Biol
```

</div>

**توضیح خروجی:**
- ‏۱۱۵ مقاله، ۱٫۶ مگابایت XML (با چکیده‌ها و فهرست منابع).
- مجله‌های اصلی: *J Bacteriol* و *Mol Gen Genet* (ژنتیک کلاسیک باکتری‌ها). تمرین ۳ نشان می‌دهد بیشتر این مقاله‌ها از **دهه‌ی ۱۹۸۰**‌اند: ژنتیک rpoB در *E. coli* پیش از دوران تعیین توالی ژنوم کاویده شد.

---

## ۶. گام ۴: فهرست منابع خودکار

**چرا؟** نوشتن دستی فهرست منابع پر از خطاست. ‏NCBI دو راه دارد:

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=pubmed --data-urlencode "term=10.1016/S0092-8674(01)00286-0[doi]" | grep -oE '<Id>[^<]*'
curl -sS "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=ris&id=11290327" | head -10
curl -sS "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=citation&id=11290327" | jq -r '.ama.orig'
curl -sS "$B/efetch.fcgi?db=pubmed&id=11290327&rettype=medline&retmode=text" | grep -E '^(PMID|DP  |TA  |MH  )' | head -9
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Id>11290327
TY  - JOUR
DB  - PubMed
AU  - Campbell, E A
AU  - Korzheva, N
AU  - Mustaev, A
AU  - Murakami, K
AU  - Nair, S
AU  - Goldfarb, A
AU  - Darst, S A
T1  - Structural mechanism for rifampicin inhibition of bacterial rna polymerase
Campbell EA, Korzheva N, Mustaev A, et al. Structural mechanism for rifampicin inhibition of bacterial rna polymerase. Cell. 2001;104(6):901-912. doi:10.1016/s0092-8674(01)00286-0
PMID- 11290327
DP  - 2001 Mar 23
TA  - Cell
MH  - Amino Acid Sequence
MH  - Binding Sites
MH  - Crystallography, X-Ray
MH  - DNA-Directed RNA Polymerases/*antagonists & inhibitors/*chemistry/genetics
MH  - Escherichia coli/enzymology
MH  - Kinetics
```

</div>

**توضیح خروجی:**
- ‏`[doi]`: از DOI مقاله‌ی Campbell (منبع درس 09/01) به PMID رسیدیم.
- ‏**RIS** را Zotero، Mendeley و EndNote مستقیم می‌خوانند. ‏`format=citation` سبک‌های **AMA**، **APA** و **MLA** را در JSON می‌دهد؛ `jq` یکی را برمی‌دارد.
- قالب **MEDLINE**: هر سطر با برچسبی دوحرفی. ‏`MH` سرعنوان‌های MeSH همین مقاله‌اند؛ `*` = موضوع اصلی، `/` = زیرسرعنوان (`antagonists & inhibitors`، `chemistry`). این برای یافتن سرعنوان درست برای جست‌وجوی بعدی‌تان بسیار سودمند است: یک مقاله‌ی خوب بیابید و MeSHهایش را ببینید.

> 📄 **مرجع:** ‏Literature Citation Exporter API: https://api.ncbi.nlm.nih.gov/lit/ctxp/

---

## ۷. گام ۵: PMC؛ متن کامل

<div dir="ltr">

```bash
for p in 28009073 11290327; do
  echo "$p -> pmc: $(curl -sS "$B/elink.fcgi?dbfrom=pubmed&db=pmc&id=$p&linkname=pubmed_pmc" | grep -o '<Id>[^<]*' | cut -d'>' -f2 | tail -n +2)"
  sleep 0.4
done
curl -sS "https://pmc.ncbi.nlm.nih.gov/tools/idconv/api/v1/articles/?ids=28009073,11290327&format=json&tool=course&email=your.name@example.org" | jq -c '.records[]'
curl -sS "$B/efetch.fcgi?db=pmc&id=5344776" > pmc.xml
ls -la pmc.xml
grep -oE '<title>[^<]{3,80}' pmc.xml | sed -n '6,10p'
sed 's/<[^>]*>/ /g' pmc.xml | grep -oE '\b[A-Z][0-9]{3}[A-Z]\b' | sort | uniq -c | sort -rn | head -6
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`linkname=pubmed_pmc` | پیوند PubMed → PMC (اگر متن کامل در PMC هست) |
| ‏ID Converter | تبدیل PMID، PMCID و DOI به هم؛ نشانی تازه روی `pmc.ncbi.nlm.nih.gov` |
| ‏`efetch db=pmc` | متن کامل در قالب XML (استاندارد JATS) |
| ‏`sed 's/<[^>]*>/ /g'` | همه‌ی برچسب‌های XML را بردار؛ متن بماند |
| ‏`\b[A-Z][0-9]{3}[A-Z]\b` | الگوی نام جهش: یک حرف، سه رقم، یک حرف (S531L) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
28009073 -> pmc: 5344776
11290327 -> pmc:
{"doi":"10.1111/mmi.13606","pmcid":"PMC5344776","pmid":28009073,"requested-id":"28009073"}
{"pmid":11290327,"requested-id":"11290327","status":"error","errmsg":"Identifier not found in PMC"}
-rw-rw-r-- 1 ubuntu ubuntu 102310 Oct 27 14:57 pmc.xml
<title>Structural basis of the RIF resistance by the S531L mutation
<title>Structural basis of the RIF resistance by the H526Y mutation
<title>Structural basis of the RIF resistance by the D516V mutation
<title>DISCUSSION
<title>MATERIALS AND METHODS
     36 S531L
     34 H526Y
     21 D516V
      3 S450L
      3 H445Y
      3 D435V
```

</div>

**توضیح خروجی:**
- مقاله‌ی Molodtsov در PMC هست (`PMC5344776`)؛ مقاله‌ی Campbell (۲۰۰۱، *Cell*) **نیست**: همه‌ی مقاله‌ها متن کامل آزاد ندارند.
- **پاسخ معلوم برقرار است:** سه بخش نتایج، یکی برای هر جهش؛ و S531L ‏۳۶ بار، H526Y ‏۳۴ و D516V ‏۲۱ بار.
- ‏**S450L، H445Y و D435V** هم هر کدام ۳ بار آمده‌اند: همان سه جهش با **شماره‌گذاری M. tuberculosis** (درس 09/01: S531 در *E. coli* = S450 در *M. tuberculosis*). متن‌کاوی که تنها یکی از دو شماره‌گذاری را بجوید، نیمی از ادبیات سل را از دست می‌دهد.

> 📄 **مرجع:** ‏PMC ID Converter: https://pmc.ncbi.nlm.nih.gov/tools/idconv/ · Comeau DC, et al. (2019). *PMC text mining subset in BioC: about three million full-text articles and growing.* Bioinformatics 35:3533–3535. https://doi.org/10.1093/bioinformatics/btz070

---

## ۸. گام ۶: PubTator3؛ بگذارید ماشین بخواند

**چرا؟** ‏`grep` بالا تنها الگوی «حرف-عدد-حرف» را می‌شناخت. ‏**PubTator3** (NCBI) با یادگیری ماشین **ژن، جهش، دارو، بیماری و جاندار** را در همه‌ی PubMed و بخشی از PMC یافته و هر کدام را به شناسه‌ی استاندارد پیوند داده است.

<div dir="ltr">

```bash
curl -sS "$P3/publications/export/biocjson?pmids=28009073" > pt.json
jq -r '.PubTator3[0].passages[] | .annotations[] | "\(.infons.type)\t\(.text)\t\(.infons.identifier // "-")"' pt.json \
  | sort | uniq -c | sort -k2,2 -k1,1nr
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`export/biocjson?pmids=…` | برچسب‌های یک یا چند مقاله در قالب BioC-JSON |
| ‏`.passages[]` | بخش‌های متن (عنوان، چکیده، …) |
| ‏`.annotations[]` | هر نام‌بُرد شناخته‌شده: گونه (`type`)، متن، شناسه |
| ‏`// "-"` | اگر شناسه نبود، `-` بنویس |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
      3 Chemical	RIF	MESH:D012293
      3 Chemical	RMP	MESH:D012293
      1 Chemical	Rifampin	MESH:D012293
      1 Chemical	Rifamycin-	-
      1 Chemical	rifamycin	MESH:C023808
      1 Chemical	Rifamycin	MESH:D012294
      1 Chemical	RIFs	MESH:D012293
      3 Disease	TB	MESH:D014376
      1 Disease	RIFR TB	MESH:D018088
      1 Disease	tuberculosis	MESH:D014376
      4 Gene	RpoB	888164
      1 Species	Escherichia coli	562
      1 Species	Mycobacterium tuberculosis	1773
      4 Variant	S531L	tmVar:p|SUB|S|531|L;HGVS:p.S531L;VariantGroup:0;CorrespondingGene:888164;CorrespondingSpecies:83332
      2 Variant	D516V	tmVar:p|SUB|D|516|V;HGVS:p.D516V;VariantGroup:1;CorrespondingGene:888164;CorrespondingSpecies:83332
      2 Variant	H526Y	tmVar:p|SUB|H|526|Y;HGVS:p.H526Y;VariantGroup:2;CorrespondingGene:888164;CorrespondingSpecies:83332
```

</div>

**توضیح خروجی:**
- ‏«RIF»، «RMP»، «RIFs» و «Rifampin» **همه** به یک شناسه رسیده‌اند: `MESH:D012293` (گام ۲). این همان کاری است که MeSH برای کل مقاله می‌کند، ولی این‌جا برای **هر نام‌بُرد** در متن.
- سه جهش پاسخ معلوم پیدا شدند، با نام HGVS پروتئینی (`p.S531L`).
- **دام:** ژن `RpoB` به **888164** پیوند خورده است: Gene ID ژن rpoB در ***M. tuberculosis* H37Rv** (TaxID 83332)، نه 948488 (*E. coli*، 11/01). ولی شماره‌های 531، 526 و 516 شماره‌گذاری **E. coli**‌اند. ابزار جهش را به گونه‌ای پیوند داده که موضوع اصلی مقاله است، با شماره‌گذاری‌ای که مقاله برگزیده است. متن‌کاوی خودکار ابزار جست‌وجوست، نه داور نهایی.

همین برای همه‌ی ادبیات:

<div dir="ltr">

```bash
curl -sS "$P3/search/?text=rpoB%20S531L&page=1" | jq -r '.count, (.results[0:3][] | "\(.pmid)\t\(.title[0:70])")'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
379
33397543	Evaluation of the frequency of mutation genes in multidrug-resistant t
34676224	Cell Wall Proteomics Reveal Phenotypic Adaption of Drug-Resistant Myco
40392805	Genotypic analysis of drug-resistant tuberculosis in Ghana: Insights i
```

</div>

‏**۳۷۹** مقاله «rpoB S531L» را نام برده‌اند؛ بیشترشان درباره‌ی سل.

> 📺 **فیلم:** *PubTator 3.0: The Ultimate Tool for Biomedical Literature Annotation & Mining* (Moving Guide): https://www.youtube.com/watch?v=P4e4KWJU0NQ
> 📄 **مرجع:** Wei CH, et al. (2024). *PubTator 3.0: an AI-powered literature resource for unlocking biomedical knowledge.* Nucleic Acids Res 52(W1):W540–W546. https://doi.org/10.1093/nar/gkae235

---

## ۹. سه اشتباه رایج

1. **اعتماد به ATM برای مرور سیستماتیک.** ترجمه‌ی خودکار با به‌روزرسانی PubMed دگرگون می‌شود؛ پرسش را با برچسب‌ها بنویسید، `QueryTranslation` و تاریخ اجرا را در روش کار بیاورید.
2. **یک املا.** ‏rifampicin/rifampin، tumour/tumor، haemoglobin/hemoglobin: هر دو را با `OR`، یا سرعنوان MeSH به‌اضافه‌ی `[tiab]` برای مقاله‌های تازه.
3. **پذیرفتن خروجی متن‌کاوی بی وارسی.** ‏PubTator ژن *E. coli* را به rpoB سل پیوند داد. پیش از ساختن جدول از چنین داده‌ای، چند رکورد را با چشم بسنجید.

---

## 📘 برای کنجکاوها

- ‏**`[MeSH Major Topic]`** (یا `[majr]`) تنها مقاله‌هایی را می‌آورد که آن مفهوم **موضوع اصلی**‌شان است (نشان `*` در گام ۴): تمرین ۲.
- ‏**PMC Open Access و مجوز:** همه‌ی متن‌های PMC برای متن‌کاوی آزاد نیستند؛ رکورد Molodtsov در BioC برچسب `author_manuscript` دارد (دست‌نوشته‌ی پذیرفته‌شده‌ی پژوهش با بودجه‌ی NIH). پیش از ساختن پیکره‌ی بزرگ، مجوز هر مقاله را ببینید.
- ‏**LitSense و LitVar:** دو ابزار دیگر NCBI؛ LitVar همه‌ی مقاله‌های یک واریانت (مانند rs113993960، 11/05) را گرد می‌آورد.

---

## جمع‌بندی

- ‏PubMed پرسش بی برچسب را با ATM گسترش می‌دهد؛ `QueryTranslation` را ببینید.
- ‏MeSH (Rifampin = ‏D012293) همه‌ی املاها را می‌پوشاند ولی تنها رکوردهای نمایه‌شده را؛ `[tiab]` را با هر دو املا کنارش بگذارید. ۸۳ + ۳۳ → ۱۱۵.
- ‏`efetch` + `xtract -mixed` → جدول PMID، سال و مجله.
- ‏RIS و AMA/APA از Citation Exporter؛ MeSHهای یک مقاله‌ی خوب از قالب MEDLINE.
- ‏PMC: متن کامل Molodtsov سه جهش را با هر دو شماره‌گذاری دارد؛ PubTator3 آن‌ها را یافت ولی به ژن سل پیوند داد.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
curl … esearch db=pubmed term="QUERY" | grep -oE '<(Count|QueryTranslation)>[^<]*'
curl -sS "$B/esummary.fcgi?db=mesh&id=68xxxxxx&version=2.0"            # MeSH Dxxxxxx
curl … efetch db=pubmed query_key=1 WebEnv=… retmode=xml retmax=200 > pm.xml
xtract -input pm.xml -mixed -pattern PubmedArticle -element MedlineCitation/PMID -block PubDate -element Year
curl -sS "https://api.ncbi.nlm.nih.gov/lit/ctxp/v1/pubmed/?format=ris&id=PMID"
curl -sS "$B/efetch.fcgi?db=pubmed&id=PMID&rettype=medline&retmode=text" | grep '^MH'
curl -sS "$B/efetch.fcgi?db=pmc&id=PMCNUMBER" > full.xml
curl -sS "$P3/publications/export/biocjson?pmids=PMID" | jq …
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏PubMed / MEDLINE / PMC | موتور جست‌وجو / بخش نمایه‌شده با MeSH / بایگانی متن کامل |
| ‏MeSH | واژگان کنترل‌شده‌ی NLM برای نمایه‌سازی |
| سرعنوان (descriptor) | یک مفهوم MeSH با یک نام و شناسه |
| زیرسرعنوان (subheading) | جنبه‌ای از سرعنوان (`/pharmacology`) |
| موضوع اصلی (Major Topic) | سرعنوانی که مقاله بیشتر درباره‌ی آن است (`*`) |
| ‏ATM | گسترش خودکار پرسش در PubMed |
| ‏RIS | قالب استاندارد تبادل منابع برای نرم‌افزارهای مدیریت منابع |
| ‏JATS | استاندارد XML متن کامل مقاله‌ها |
| متن‌کاوی (text mining) | بیرون کشیدن خودکار دانش از متن |
| نام‌بُرد (mention) | یک بار آمدن یک موجودیت (ژن، دارو) در متن |
| ‏BioC | قالب ساده‌ی متن و برچسب برای متن‌کاوی |

---

## منابع

**مقاله و مستند**
- ‏Wei CH, et al. (2024). *PubTator 3.0: an AI-powered literature resource for unlocking biomedical knowledge.* Nucleic Acids Res 52(W1):W540–W546. https://doi.org/10.1093/nar/gkae235
- ‏Comeau DC, et al. (2019). *PMC text mining subset in BioC: about three million full-text articles and growing.* Bioinformatics 35:3533–3535. https://doi.org/10.1093/bioinformatics/btz070
- ‏Sayers EW, et al. (2025). *Database resources of the National Center for Biotechnology Information in 2025.* Nucleic Acids Res 53(D1):D20–D29. https://doi.org/10.1093/nar/gkae979
- ‏Molodtsov V, et al. (2017). Mol Microbiol 103:1034–1045. https://doi.org/10.1111/mmi.13606 (پاسخ معلوم)
- راهنمای PubMed: https://pubmed.ncbi.nlm.nih.gov/help/ · MeSH: https://www.nlm.nih.gov/mesh/meshhome.html · Citation Exporter: https://api.ncbi.nlm.nih.gov/lit/ctxp/ · PubTator3: https://www.ncbi.nlm.nih.gov/research/pubtator3/

**کتاب**
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲: دسترسی به ادبیات؛ PubMed و MeSH)
- ‏Higgins JPT, et al. (eds.) (2023). *Cochrane Handbook for Systematic Reviews of Interventions*, version 6.4. Cochrane. (فصل ۴: جست‌وجو و گزینش مطالعه‌ها) https://training.cochrane.org/handbook

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Access Bioinformatics Databases with Biopython* (PubMed با Entrez): https://www.coursera.org/projects/access-bioinformatics-databases-with-biopython
- ‏edX: *Essentials of Genomics and Biomedical Informatics* (IsraelX): https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics
- ‏YouTube: *This MeSH tutorial will dramatically improve your literature search on PubMed* (EvidentiaSystems): https://www.youtube.com/watch?v=7fWFupz0LVA
- ‏YouTube: *PubTator 3.0: The Ultimate Tool for Biomedical Literature Annotation & Mining* (Moving Guide): https://www.youtube.com/watch?v=P4e4KWJU0NQ

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند. نشانی پیشین PMC OA Service (`/pmc/utils/oa/oa.fcgi`) از سرور ۴۰۴ داد و ID Converter به `pmc.ncbi.nlm.nih.gov` رفته است. DOIها با doi.org و صفحه‌ها با درخواست مستقیم وارسی شدند؛ فیلم‌ها با noembed.</sub>

</div>
