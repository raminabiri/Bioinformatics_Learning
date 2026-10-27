<div dir="rtl">

# درس: dbSNP، ClinVar، dbVar، MedGen و GTR؛ یک جهش، پنج پایگاه

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `05_Variation_Clinical` · **پیش‌نیاز:** ماژول‌های [11/01](../01_Entrez_EDirect/) و [11/02](../02_Gene_RefSeq_Protein_Taxonomy/) (`NM_`/`NP_`، MANE، مختصات 0-based) · **زمان:** حدود ۹۰ دقیقه · **ابزار:** curl 8.20.0، EDirect 24.0، NCBI Variation Services API (v0)، jq · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). تنها درخواست وب.
>
> **مرز این درس:** این‌جا یاد می‌گیرید داده‌ی واریانت را **پیدا کنید و بخوانید**. تفسیر بالینی یک واریانت تازه (معیارهای ACMG/AMP) کار دوره‌ی جدای «ژنومیکس پزشکی و تفسیر بالینی واریانت» است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. شناسه‌های **rs** (dbSNP)، **VCV** (ClinVar)، **nsv** (dbVar) و **CUI** (MedGen) را بشناسید.
2. یک واریانت را به سه زبان بنویسید: **HGVS** (`c.`، `p.`، `g.`)، **SPDI** و مختصات کروموزوم؛ و میانشان با API تبدیل کنید.
3. قاعده‌ی **۳′** در HGVS را ببینید: دو نوشتار گوناگون، یک واریانت.
4. رده‌بندی ClinVar و **سطح بازبینی** (ستاره‌ها) را بخوانید.
5. از واریانت به بیماری (MedGen) و آزمون ژنتیکی (GTR) برسید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m05 && cd ~/ncbi/m05
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
V=https://api.ncbi.nlm.nih.gov/variation/v0
```

</div>

---

## ۱. داستان

**فیبروز کیستیک** (CF) شایع‌ترین بیماری ژنتیکی کشنده در جمعیت‌های اروپایی‌تبار است. در ۱۹۸۹ ژن آن، **CFTR**، یافته شد و همراهش شایع‌ترین جهش: حذف سه باز که یک **فنیل‌آلانین** را در جایگاه ۵۰۸ پروتئین برمی‌دارد، **F508del**. سی و چند سال بعد، همین یک جهش در پنج پایگاه NCBI شناسه دارد. یک آزمایشگاه ژنتیک، یک پزشک و یک پژوهشگر هر کدام از یکی از آن‌ها آغاز می‌کنند؛ شما باید بتوانید میانشان رفت‌وآمد کنید. این واریانت **پاسخ معلوم** ماست: بیماری‌زا، با بالاترین سطح بازبینی.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ پنج پایگاه

| پایگاه | چه دارد | شناسه | نمونه |
| :--- | :--- | :--- | :--- |
| ‏**dbSNP** | واریانت‌های کوچک (SNV، indel تا حدود ۵۰ باز) و فراوانی‌شان در جمعیت‌ها | ‏`rs` | ‏`rs113993960` |
| ‏**ClinVar** | رابطه‌ی واریانت با بیماری، به گزارش آزمایشگاه‌ها و کارشناسان | ‏`VCV` (و `RCV`، `SCV`) | ‏`VCV000007105` |
| ‏**dbVar** | واریانت‌های **ساختاری** (بزرگ‌تر از ۵۰ باز: حذف، مضاعف‌شدگی، وارونگی) | ‏`nsv` (و پژوهش `nstd`) | ‏`nsv7909578` |
| ‏**MedGen** | مفهوم‌های بیماری و فنوتیپ | ‏CUI (`C…`) | ‏`C0010674` |
| ‏**GTR** | آزمون‌های ژنتیکی آزمایشگاه‌ها | ‏GTR ID | — |

**تشبیه:** dbSNP شناسنامه‌ی واریانت است (کجاست، چقدر شایع است)؛ ClinVar پرونده‌ی پزشکی‌اش (چه بیماری‌ای می‌دهد، به گفته‌ی چه کسی)؛ MedGen دانشنامه‌ی بیماری؛ GTR فهرست آزمایشگاه‌هایی که می‌توانند آن را بیابند.

### ۲.۲ سه زبان برای یک واریانت

| زبان | ‏F508del در این زبان | ویژگی |
| :--- | :--- | :--- |
| ‏**HGVS** روی رونوشت | ‏`NM_000492.4:c.1521_1523del` | ‏`c.` = شماره‌ی باز در CDS (۱ = A کُدون آغاز). برای پزشک و آزمایشگاه |
| ‏**HGVS** روی پروتئین | ‏`NP_000483.3:p.Phe508del` | ‏`p.` = اسید آمینه |
| ‏**HGVS** روی ژنوم | ‏`NC_000007.14:g.117559592_117559594del` | ‏`g.` = شماره‌ی باز روی کروموزوم (از ۱) |
| ‏**SPDI** | ‏`NC_000007.14:117559590:TCTT:T` | توالی : جایگاه (**0-based**) : حذف‌شده : افزوده‌شده. برای رایانه |

> 📺 **فیلم:** *GenomeConnect and ClinVar Webinar* (ClinGen Resource): https://www.youtube.com/watch?v=Pty0vW9CkEE
> 📄 **مرجع:** den Dunnen JT, et al. (2016). *HGVS recommendations for the description of sequence variants: 2016 update.* Human Mutation 37:564–569. https://doi.org/10.1002/humu.22981 · Holmes JB, et al. (2020). *SPDI: data model for variants and applications at NCBI.* Bioinformatics 36:1902–1907. https://doi.org/10.1093/bioinformatics/btz856

---

## ۳. گام ۱: dbSNP؛ شناسنامه‌ی واریانت

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=snp&id=113993960" > snp.xml
grep -oE '<(SNP_CLASS|CHRPOS|CHRPOS_PREV_ASSM|SPDI|FXN_CLASS|CLINICAL_SIGNIFICANCE|CREATEDATE)>[^<]*' snp.xml
grep -oE 'NP_[0-9.]+:p\.[A-Za-z0-9]*' snp.xml | sort -u
```

</div>

‏در `db=snp` شناسه همان عدد پس از `rs` است.

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<CLINICAL_SIGNIFICANCE>risk-factor,pathogenic,likely-pathogenic,drug-response
<SPDI>NC_000007.14:117559590:TCTT:T,NC_000007.14:117559590:TCTT:TCTTCTT
<FXN_CLASS>intron_variant,inframe_deletion,inframe_insertion,coding_sequence_variant
<CREATEDATE>2010/07/08 12:50
<SNP_CLASS>delins
<CHRPOS>7:117559591
<CHRPOS_PREV_ASSM>7:117199645
NP_000483.3:p.Phe508del
NP_000483.3:p.Phe508dup
```

</div>

**توضیح خروجی:**
- **دو** آلل جایگزین زیر یک rs: حذف `CTT` (‏**Phe508del**) و **مضاعف‌شدگی** همان (‏Phe508dup، بسیار کم‌یاب). ‏dbSNP همه‌ی دگرگونی‌ها در یک جایگاه را زیر یک rs گروه می‌کند؛ پس «rs113993960» به‌تنهایی نمی‌گوید کدام آلل.
- ‏`CHRPOS` ‏7:117559591 روی GRCh38 و `CHRPOS_PREV_ASSM` ‏7:117199645 روی GRCh37: یک واریانت، دو مختصات در دو اسمبلی. **همیشه اسمبلی را بنویسید.**
- ‏`inframe_deletion`: سه باز حذف شده، پس چارچوب خواندن به هم نمی‌ریزد؛ تنها یک اسید آمینه کم می‌شود. ‏`intron_variant` از رونوشت‌های دیگری است که این‌جا اینترون دارند.
- ‏`CLINICAL_SIGNIFICANCE` خلاصه‌ای از **همه‌ی** گزارش‌های ClinVar برای این rs است (هر دو آلل، همه‌ی بیماری‌ها و پاسخ به دارو)؛ برای جزئیات به ClinVar بروید (گام ۳).

فراوانی در جمعیت‌ها و ژن‌ها، با `xtract`:

<div dir="ltr">

```bash
esummary -db snp -id 113993960 | xtract -pattern DocumentSummary -block MAF -element STUDY FREQ | tr '\t' '\n' | paste - -
esummary -db snp -id 113993960 | xtract -pattern DocumentSummary -block GENE_E -element NAME GENE_ID
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
1000Genomes	-=0.0039936/20
1000Genomes_30X	-=0.0039038/25
Estonian	-=0.0071429/32
ExAC	-=0.0067851/823
GnomAD_exomes	-=0.0124506/17428
GnomAD_genomes	-=0.0079298/1183
GoNL	-=0.0190381/19
NorthernSweden	-=0.01/6
PAGE_STUDY	-=0.0035453/279
TOPMED	-=0.0078507/2078
ALFA	T=0.003121/290
CFTR	1080	CFTR-AS1	111082987
```

</div>

**توضیح خروجی:**
- قالب `-=0.0124506/17428`: آلل `-` (حذف) با فراوانی **۱٫۲۵٪** در gnomAD exomes، از روی ۱۷٬۴۲۸ آلل. ‏`tr '\t' '\n' | paste - -` هر دو ستون را یک سطر کرد.
- بالاترین فراوانی در **GoNL** (هلند، ۱٫۹٪) و پایین‌ترین در 1000 Genomes و PAGE (جمعیت‌های گوناگون، ۰٫۴٪): F508del در اروپای شمالی شایع‌تر است. یک واریانت بیماری‌زای مغلوب با فراوانی ۱ تا ۲٪ یعنی حدود ۱ نفر از هر ۲۵ تا ۵۰ نفر **ناقل** است.
- ژن `CFTR` (Gene ID **1080**) و یک RNA ضدجهت (`CFTR-AS1`) روی همان ناحیه.

---

## ۴. گام ۲: تبدیل میان زبان‌ها با Variation Services

**چرا؟** آزمایشگاه `c.` می‌دهد، فایل VCF مختصات ژنوم دارد و پایگاه‌ها `rs`. ‏NCBI یک API برای تبدیل دارد:

<div dir="ltr">

```bash
curl -sS "$V/spdi/NC_000007.14:117559590:TCTT:T/hgvs"; echo
curl -sS "$V/hgvs/NM_000492.4:c.1521_1523del/contextuals"; echo
curl -sS "$V/spdi/NC_000007.14:117559590:TCTT:T/rsids"; echo
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
{"data":{"hgvs":"NC_000007.14:g.117559592_117559594del"}}
{"data":{"spdis":[{"seq_id":"NM_000492.4","position":1589,"deleted_sequence":"TCTT","inserted_sequence":"T"}],"input_hgvs_validity":"valid"}}
{"data":{"rsids":[113993960]}}
```

</div>

**توضیح خروجی:**
- ‏SPDI ژنومی → HGVS ژنومی؛ HGVS رونوشت → SPDI روی همان رونوشت (جایگاه ۱۵۸۹ از آغاز mRNA، نه از CDS)؛ SPDI → rs.
- چرا SPDI ‏`TCTT` → `T` است و نه `CTT` → هیچ؟ ‏SPDI یک باز پیش از حذف را هم نگه می‌دارد تا جایگاه یکتا باشد. ‏`117559590` (0-based) همان باز `T` پیش از حذف است؛ حذف از ۱۱۷۵۵۹۵۹۲ (1-based) آغاز می‌شود، همان HGVS.
- پاسخ JSON است؛ برای بیرون کشیدن یک فیلد از `jq` کار می‌کشیم (گام ۳).

### ۴.۱ قاعده‌ی ۳′: دو نوشتار، یک واریانت

توالی پیرامون جایگاه ۵۰۸ در CDS: ‏`…ATC ATC TTT GGT…` (Ile506، Ile507، Phe508، Gly509). حذف `CTT` و حذف `TCT` یک باز جلوتر، **یک توالی** می‌سازند. ‏HGVS می‌گوید آن را در **سوی ۳′‌ترین** جای ممکن بنویسید. بیازماییم:

<div dir="ltr">

```bash
for h in NM_000492.4:c.1520_1522del NM_000492.4:c.1519_1521del NM_000492.4:c.1521_1523delATC; do
  echo "== $h"
  r=$(curl -sS "$V/hgvs/$h/contextuals")
  echo "$r" | jq -r '.data.spdis[0] | "\(.seq_id):\(.position):\(.deleted_sequence):\(.inserted_sequence)"' 2>/dev/null
  echo "$r" | jq -r '.data.warnings[0].message // .error.message // "ok"' | cut -c1-110
  sleep 0.4
done
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`jq -r '.data.spdis[0] \| "…"'` | از JSON نخستین SPDI را بردار و چهار بخشش را با `:` بچسبان |
| ‏`.data.warnings[0].message // .error.message // "ok"` | اگر هشدار هست آن را، وگرنه پیام خطا، وگرنه «ok» |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
== NM_000492.4:c.1520_1522del
NM_000492.4:1589:TCTT:T
We detected that this HGVS could be represented with a more 3' location. Technically this does not conform to 
== NM_000492.4:c.1519_1521del
NM_000492.4:1585:ATCATC:ATC
ok
== NM_000492.4:c.1521_1523delATC
null:null:null:null
Error while processing 'NM_000492.4:c.1521_1523delATC': The submitted reference allele (ATC) does not agree wi
```

</div>

**توضیح خروجی:**
- ‏`c.1520_1522del`: **همان** SPDI ‏F508del (`1589:TCTT:T`)، با هشدار «می‌شد در جایگاه ۳′‌تر نوشت؛ با استاندارد HGVS جور نیست». یک واریانت، دو نوشتار؛ تنها `c.1521_1523del` درست است.
- ‏`c.1519_1521del`: SPDI دیگری (`1585:ATCATC:ATC`): یکی از دو **ATC** حذف شده، یعنی **Ile507del**، واریانت دیگری با rs دیگر (تمرین ۳).
- ‏`delATC` در جای `CTT`: **خطا**؛ API باز مرجع را با توالی واقعی می‌سنجد. پس `del` همراه توالی (`delCTT`) یک وارسی رایگان است.

> 📺 **فیلم:** *GenomeConnect and ClinVar Webinar* (ClinGen Resource): https://www.youtube.com/watch?v=Pty0vW9CkEE
> 📄 **مرجع:** ‏NCBI Variation Services API: https://api.ncbi.nlm.nih.gov/variation/v0/ · HGVS Nomenclature: https://hgvs-nomenclature.org/

---

## ۵. گام ۳: ClinVar؛ پرونده‌ی پزشکی واریانت

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=clinvar --data-urlencode "term=rs113993960" | grep -oE '<(Count|Id)>[^<]*' | head -3
esummary -db clinvar -id 7105,634837 \
  | xtract -pattern DocumentSummary -element accession title -block germline_classification -element description review_status last_evaluated
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>2
<Id>634837
<Id>7105
VCV000007105	NM_000492.3(CFTR):c.1521_1523del (p.Phe508del)	Pathogenic	practice guideline	2004/03/03 00:00
VCV000634837	NM_000492.3(CFTR):c.[1521_1523delCTT;3080T>C]	Pathogenic	reviewed by expert panel	2019/03/11 00:00
```

</div>

**توضیح خروجی:**
- ‏**VCV000007105**: خود F508del، **Pathogenic** (بیماری‌زا)، با سطح بازبینی **practice guideline**، یعنی بالاترین سطح (۴ ستاره): در یک رهنمود بالینی رسمی آمده است (تاریخ ارزیابی ۲۰۰۴).
- ‏**VCV000634837**: یک **هاپلوتایپ**: F508del همراه با جهش دوم `c.3080T>C` روی همان کروموزوم (`[ ; ]` در HGVS = دو دگرگونی روی یک آلل). کارشناسان (expert panel، ۳ ستاره) آن را جدا ارزیابی کرده‌اند.
- نام‌ها روی `NM_000492.3` نوشته شده‌اند، dbSNP روی `.4`: نسخه‌ی رونوشت بالا رفته ولی `c.` همان مانده است؛ API گام ۲ همین `c.1521_1523del` را روی `.4` پذیرفت. همیشه نسخه را ببینید و پیش از جابه‌جا کردن نسخه، با API بسنجید.

**ستاره‌های ClinVar (review status):**

| ستاره | سطح |
| :---: | :--- |
| ۴ | ‏practice guideline (رهنمود بالینی) |
| ۳ | ‏reviewed by expert panel (گروه کارشناسان، مانند ClinGen) |
| ۲ | ‏criteria provided, multiple submitters, no conflicts |
| ۱ | ‏criteria provided, single submitter (یا با ناسازگاری) |
| ۰ | ‏no assertion criteria provided |

یک واریانت «Pathogenic» با ۰ ستاره تنها ادعای یک آزمایشگاه بی معیار گفته‌شده است؛ با ۴ ستاره، اجماع بالینی.

### ۵.۱ همه‌ی واریانت‌های CFTR در یک نگاه

<div dir="ltr">

```bash
for q in 'CFTR[gene]' 'CFTR[gene] AND clinsig_pathogenic[prop]' 'CFTR[gene] AND clinsig_vus[prop]' \
         'CFTR[gene] AND clinsig_benign[prop]' 'CFTR[gene] AND clinsig_has_conflicts[prop]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=clinvar --data-urlencode "term=$q" \
          | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)  $q"; sleep 0.4
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
6529  CFTR[gene]
1295  CFTR[gene] AND clinsig_pathogenic[prop]
2591  CFTR[gene] AND clinsig_vus[prop]
112  CFTR[gene] AND clinsig_benign[prop]
408  CFTR[gene] AND clinsig_has_conflicts[prop]
```

</div>

‏**۶۵۲۹** رکورد برای CFTR؛ **۲۵۹۱** (۴۰٪) «**VUS**» (variant of uncertain significance، اهمیت نامعلوم) و ۴۰۸ با گزارش‌های **ناسازگار**. حتی برای پرپژوهش‌ترین ژن بیماری مغلوب، بیشتر واریانت‌ها هنوز تفسیر روشن ندارند. (شمارها با هم جمع نمی‌شوند: برخی رکوردها «likely» یا رده‌های دیگرند.)

> 📺 **فیلم:** *GenomeConnect and ClinVar Webinar*: https://www.youtube.com/watch?v=Pty0vW9CkEE
> 📄 **مرجع:** Landrum MJ, et al. (2018). *ClinVar: improving access to variant interpretations and supporting evidence.* Nucleic Acids Res 46(D1):D1062–D1067. https://doi.org/10.1093/nar/gkx1153 · راهنمای ستاره‌ها: https://www.ncbi.nlm.nih.gov/clinvar/docs/review_status/

---

## ۶. گام ۴: dbVar؛ واریانت‌های بزرگ

**چرا؟** همه‌ی جهش‌های بیماری‌زا چند باز نیستند؛ حذف یک یا چند **اگزون** کامل هم در CFTR هست.

<div dir="ltr">

```bash
for q in 'CFTR[gene_name]' 'CFTR[gene_name] AND "copy number loss"[vtype]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=dbvar --data-urlencode "term=$q" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)  $q"; sleep 0.4
done
curl -sS -G "$B/esearch.fcgi" --data-urlencode db=dbvar --data-urlencode "term=CFTR[gene_name]" --data-urlencode retmax=3 \
  | grep -o '<Id>[^<]*' | cut -d'>' -f2 | paste -sd, > dv.ids
esummary -db dbvar -id $(cat dv.ids) \
  | xtract -pattern DocumentSummary -element SV ST -block dbVarPlacement -if Assembly -starts-with GRCh38 -element Chr Chr_start Chr_end
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-block dbVarPlacement` | هر واریانت روی چند اسمبلی جا دارد؛ هر جا یک بلوک |
| ‏`-if Assembly -starts-with GRCh38` | تنها بلوکی که اسمبلی‌اش با GRCh38 آغاز می‌شود (`GRCh38`، `GRCh38.p12`، …) |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
1355  CFTR[gene_name]
267  CFTR[gene_name] AND "copy number loss"[vtype]
nsv7908318	nstd102	7	117667036	117667087
nsv7908449	nstd102	7	117642445	117642536
nsv7909578	nstd102	7	117501896	117519332
```

</div>

**توضیح خروجی:**
- ‏**۱۳۵۵** واریانت ساختاری روی CFTR، ۲۶۷ تا **کاهش شمار نسخه** (حذف).
- همه از پژوهش **nstd102**: مجموعه‌ای که dbVar از واریانت‌های ساختاری **ClinVar** ساخته است؛ پس این‌ها هم گزارش بالینی‌اند.
- ‏`nsv7909578`: ‏۱۷٬۴۳۷ باز (117501896 تا 117519332)؛ نزدیک به آغاز ژن CFTR. تمرین ۵ آن را می‌کاود.

> 📄 **مرجع:** Lappalainen I, et al. (2013). *dbVar and DGVa: public archives for genomic structural variation.* Nucleic Acids Res 41(D1):D936–D941. https://doi.org/10.1093/nar/gks1213

---

## ۷. گام ۵: MedGen و GTR؛ از واریانت به بیماری و آزمون

<div dir="ltr">

```bash
esearch -db medgen -query C0010674 | esummary | xtract -pattern DocumentSummary -element ConceptId Title | cut -f1,2
esearch -db medgen -query C0010674 | esummary | xtract -pattern DocumentSummary -block Names -element Name | tr '\t' '\n' | head -5
for q in 'CFTR[gene]' 'CFTR[gene] AND "Cystic fibrosis"[disname]'; do
  echo "$(curl -sS -G "$B/esearch.fcgi" --data-urlencode db=gtr --data-urlencode "term=$q" | grep -oE '<Count>[^<]*' | head -1 | cut -d'>' -f2)  $q"; sleep 0.4
done
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
C0010674	Cystic fibrosis
Cystic Fibrosis
Fibrosis, Cystic
CYSTIC FIBROSIS
CF
MUCOVISCIDOSIS
354  CFTR[gene]
239  CFTR[gene] AND "Cystic fibrosis"[disname]
```

</div>

**توضیح خروجی:**
- ‏**MedGen** هر بیماری را با یک **CUI** (از UMLS) نام می‌گذارد: `C0010674`، با همه‌ی نام‌های دیگرش (MUCOVISCIDOSIS نام قدیمی اروپایی است). همین CUI در ClinVar، GTR و OMIM به کار می‌رود و نام‌های گوناگون یک بیماری را به هم می‌رساند.
- ‏**GTR**: ‏۳۵۴ آزمون ژنتیکی که CFTR را می‌سنجند، ۲۳۹ تا با نام بیماری فیبروز کیستیک (بقیه بیشتر پنل‌های چندژنی‌اند که CFTR یکی از ژن‌هایشان است).

> 📄 **مرجع:** Rubinstein WS, et al. (2013). *The NIH genetic testing registry: a new, centralized database of genetic tests to enable access to comprehensive information and improve transparency.* Nucleic Acids Res 41(D1):D925–D935. https://doi.org/10.1093/nar/gks1173

---

## ۸. سه اشتباه رایج

1. ‏**‏rs = یک واریانت.** ‏`rs113993960` هم حذف است و هم مضاعف‌شدگی؛ همیشه آلل (یا SPDI/HGVS) را هم بنویسید.
2. **مختصات بی اسمبلی.** ‏117559591 (GRCh38) و 117199645 (GRCh37) یک جایگاه‌اند. آمیختن دو اسمبلی در یک جدول، واریانت‌ها را جابه‌جا می‌کند.
3. **خواندن رده‌بندی بی ستاره.** «Pathogenic» با ۰ ستاره و با ۴ ستاره یک ارزش ندارند؛ و VUS یعنی «نمی‌دانیم»، نه «احتمالاً بی‌خطر».

---

## 📘 برای کنجکاوها

- ‏**Variation Viewer** (https://www.ncbi.nlm.nih.gov/variation/view/) همه‌ی این لایه‌ها را روی یک نقشه‌ی ژنوم نشان می‌دهد: dbSNP، ClinVar، dbVar و ژن‌ها، با جابه‌جایی میان GRCh37 و GRCh38.
- ‏**RCV و SCV:** هر **SCV** گزارش یک آزمایشگاه است؛ **RCV** همه‌ی گزارش‌ها برای یک جفت «واریانت + بیماری»؛ **VCV** همه‌ی گزارش‌ها برای یک واریانت. ستاره‌های VCV از جمع SCVها می‌آیند.
- ‏**VCF و ClinVar:** فایل `clinvar.vcf.gz` همه‌ی ClinVar را در قالب VCF (بخش ۰۲) دارد و برای آنوتیشن یک فایل VCF به کار می‌رود؛ دوره‌ی ژنومیکس پزشکی همین را می‌کاود.

---

## جمع‌بندی

- ‏F508del: ‏`rs113993960` (dbSNP)، `VCV000007105` (ClinVar، Pathogenic، ۴ ستاره)، `NM_000492.4:c.1521_1523del`، `NP_000483.3:p.Phe508del`، `NC_000007.14:g.117559592_117559594del`، SPDI ‏`NC_000007.14:117559590:TCTT:T`.
- فراوانی ۰٫۴ تا ۱٫۹٪ در جمعیت‌های گوناگون (بیشترین در هلند).
- قاعده‌ی ۳′: ‏`c.1520_1522del` همان واریانت است ولی نادرست نوشته شده؛ `c.1519_1521del` واریانت دیگری است (Ile507del).
- ‏CFTR در ClinVar: ‏۶۵۲۹ رکورد، ۴۰٪ VUS. ‏dbVar: ‏۱۳۵۵ واریانت ساختاری. ‏MedGen: ‏C0010674. ‏GTR: ‏۳۵۴ آزمون.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=snp&id=RSNUMBER" | grep -oE '<(SPDI|CHRPOS|FXN_CLASS)>[^<]*'
esummary -db snp -id RSNUMBER | xtract -pattern DocumentSummary -block MAF -element STUDY FREQ
curl -sS "$V/hgvs/HGVS/contextuals"          # HGVS -> SPDI (+ warnings)
curl -sS "$V/spdi/SPDI/hgvs"                 # SPDI -> HGVS
curl -sS "$V/spdi/SPDI/rsids"                # SPDI -> rs
esummary -db clinvar -id UID | xtract -pattern DocumentSummary -element accession title -block germline_classification -element description review_status
curl … esearch db=clinvar term="GENE[gene] AND clinsig_pathogenic[prop]"
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏rs (RefSNP) | شناسه‌ی یک جایگاه واریانت در dbSNP |
| ‏VCV / RCV / SCV | رکورد ClinVar برای واریانت / واریانت + بیماری / گزارش یک آزمایشگاه |
| ‏HGVS | استاندارد نام‌گذاری واریانت (`c.`، `p.`، `g.`) |
| ‏SPDI | نمایش رایانه‌ای واریانت: توالی، جایگاه 0-based، حذف‌شده، افزوده‌شده |
| قاعده‌ی ۳′ | نوشتن واریانت در ۳′‌ترین جای ممکن |
| ‏inframe | حذف یا افزایشی که مضرب سه است و چارچوب خواندن را نمی‌شکند |
| هاپلوتایپ | چند واریانت روی یک کروموزوم |
| ناقل (carrier) | فردی با یک نسخه‌ی جهش‌یافته از ژن مغلوب، بی بیماری |
| سطح بازبینی (review status) | میزان پشتوانه‌ی یک رده‌بندی ClinVar، به ستاره |
| ‏VUS | واریانت با اهمیت نامعلوم |
| واریانت ساختاری | دگرگونی بزرگ‌تر از ۵۰ باز (حذف، مضاعف‌شدگی، وارونگی) |
| ‏CUI | شناسه‌ی مفهوم در UMLS و MedGen |

---

## منابع

**مقاله و مستند**
- ‏Riordan JR, et al. (1989). *Identification of the cystic fibrosis gene: cloning and characterization of complementary DNA.* Science 245:1066–1073. https://doi.org/10.1126/science.2475911
- ‏Sherry ST, et al. (2001). *dbSNP: the NCBI database of genetic variation.* Nucleic Acids Res 29:308–311. https://doi.org/10.1093/nar/29.1.308
- ‏Landrum MJ, et al. (2018). *ClinVar: improving access to variant interpretations and supporting evidence.* Nucleic Acids Res 46(D1):D1062–D1067. https://doi.org/10.1093/nar/gkx1153
- ‏Holmes JB, et al. (2020). *SPDI: data model for variants and applications at NCBI.* Bioinformatics 36:1902–1907. https://doi.org/10.1093/bioinformatics/btz856
- ‏den Dunnen JT, et al. (2016). *HGVS recommendations for the description of sequence variants: 2016 update.* Hum Mutat 37:564–569. https://doi.org/10.1002/humu.22981
- ‏Lappalainen I, et al. (2013). *dbVar and DGVa: public archives for genomic structural variation.* Nucleic Acids Res 41(D1):D936–D941. https://doi.org/10.1093/nar/gks1213
- ‏Rubinstein WS, et al. (2013). *The NIH genetic testing registry.* Nucleic Acids Res 41(D1):D925–D935. https://doi.org/10.1093/nar/gks1173

**کتاب**
- ‏Strachan T, Read A (2018). *Human Molecular Genetics*, 5th ed. CRC Press. (فصل‌های واریانت‌های بیماری‌زا و نام‌گذاری)
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲۱: بیماری‌های ژنتیکی انسان؛ dbSNP و پایگاه‌های بالینی)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Genomic Medicine Gets Personal* (Georgetown): https://www.coursera.org/learn/genomic-medicine
- ‏edX: *Essentials of Genomics and Biomedical Informatics* (IsraelX): https://www.edx.org/learn/medicine/israelx-essentials-of-genomics-and-biomedical-informatics
- ‏YouTube: *GenomeConnect and ClinVar Webinar* (ClinGen Resource): https://www.youtube.com/watch?v=Pty0vW9CkEE

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند. DOIها با doi.org، و صفحه‌ها با درخواست مستقیم وارسی شدند؛ فیلم با noembed.</sub>

</div>
