<div dir="rtl">

# درس ۱: Entrez و E-utilities با `curl`؛ از نام ژن تا توالی پروتئین

**بخش:** `11_V2_NCBI_Databases` · **ماژول:** `01_Entrez_EDirect` · **پیش‌نیاز:** ماژول [02/03](../../02_BioLinux/03_Annotation_Formats/) (نخستین `efetch` با `curl`)؛ `grep`، `cut` و `awk` از بخش [۰۱](../../01_Linux/) · **زمان:** حدود ۷۵ دقیقه · **ابزار:** curl 8.20.0 · **آخرین بازبینی:** 2026-10-27

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-27). هر درخواست کمتر از یک ثانیه. شمارها (شمار رکورد، شمار مقاله) هر روز کمی بالا می‌روند؛ شمار شما شاید با این درس یکی نباشد، ولی شناسه‌ها و مختصات همین‌اند.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. بگویید Entrez چیست و چرا پایگاه‌های NCBI به هم «پیوند» دارند.
2. فرق **UID** (شناسه‌ی عددی) و **accession.version** را بگویید.
3. پنج ابزار اصلی E-utilities را با `curl` به کار ببرید: `einfo`، `esearch`، `esummary`، `elink`، `efetch`.
4. با **برچسب فیلد** (`[gene]`، `[preferred symbol]`، `[Organism:noexp]`) جست‌وجوی دقیق بنویسید.
5. با **سرور تاریخچه** (History server) چند گام را بی جابه‌جا کردن فهرست شناسه‌ها به هم بچسبانید.
6. قاعده‌ی سرعت (۳ درخواست در ثانیه) و **کلید API** را بشناسید.

**پیش از آغاز:**

<div dir="ltr">

```bash
mkdir -p ~/ncbi/m01 && cd ~/ncbi/m01
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
```

</div>

‏`B` تنها برای کوتاه شدن دستورهاست: نشانی پایه‌ی همه‌ی E-utilities.

---

## ۱. داستان

در ماژول 02/03 یک تکه از ژنوم *E. coli* را با یک نشانی بلند گرفتید: `efetch.fcgi?db=nuccore&id=NC_000913.3&…&seq_start=4181245&seq_stop=4185273`. ولی این عددها را از کجا آوردیم؟ ما از پیش می‌دانستیم *rpoB* کجاست. در کار واقعی پرسش وارونه است: **«ژن *rpoB* در سویه‌ی K-12 کجاست، پروتئین‌اش چیست و چند مقاله درباره‌اش هست؟»** پاسخ این پرسش در سه پایگاه جداست (Gene، Protein، PubMed). در این درس یاد می‌گیرید از یک نام ژن آغاز کنید و با چند درخواست کوچک به هر سه برسید، و همه را در یک اسکریپت تکرارپذیر بنویسید، نه با کلیک در مرورگر.

---

## ۲. مفهوم به زبان ساده

### ‏۲.۱ ‏Entrez: یک موتور جست‌وجو روی ۳۸ پایگاه

‏**Entrez** سامانه‌ی جست‌وجوی NCBI است. ‏PubMed، Gene، Protein، Nucleotide، SRA، GEO و… هر کدام یک **پایگاه** (database) در Entrez‌اند. نیروی Entrez در **پیوندها**ست: هر رکورد Gene به پروتئین‌هایش، به توالی‌اش، به مقاله‌هایش و… پیوند دارد. **تشبیه:** یک کتابخانه‌ی بزرگ با چند تالار (پایگاه)؛ برگه‌ی هر کتاب نشان می‌دهد کتاب‌های وابسته در کدام تالار و کدام قفسه‌اند.

### ۲.۲ دو گونه شناسه

| شناسه | نمونه | ویژگی |
| :--- | :--- | :--- |
| ‏**UID** (شناسه‌ی Entrez) | ‏`948488` (ژن rpoB)، `16131817` (پروتئین) | تنها یک عدد؛ درون **یک پایگاه** یکتاست. Gene ID همان UID پایگاه Gene است |
| ‏**accession.version** | ‏`NP_418414.1`، `NC_000913.3` | نام پایدار رکورد توالی؛ پس از `.` **نسخه** می‌آید و با هر دگرگونی توالی یکی بالا می‌رود |

‏E-utilities در درون با UID کار می‌کنند؛ `efetch` برای پایگاه‌های توالی accession را هم می‌پذیرد. **در گزارش و مقاله همیشه accession.version بنویسید**، چون می‌گوید دقیقاً کدام نسخه‌ی توالی را به کار برده‌اید.

### ۲.۳ ابزارهای E-utilities

‏**E-utilities** رابط برنامه‌نویسی (API) Entrez است: هر ابزار یک نشانی وب است که با `curl` صدا زده می‌شود و پاسخ را (بیشتر XML) برمی‌گرداند.

| ابزار | کار | پرسش |
| :--- | :--- | :--- |
| ‏`einfo` | آگاهی درباره‌ی پایگاه‌ها | «چه پایگاه‌هایی هست؟ این پایگاه چه فیلدهایی دارد؟» |
| ‏`esearch` | جست‌وجو → فهرست UID | «کدام رکوردها با این پرسش جورند؟» |
| ‏`esummary` | ‏UID → خلاصه‌ی رکورد | «این رکورد در چند خط چیست؟» |
| ‏`elink` | ‏UID در یک پایگاه → UIDهای وابسته در پایگاه دیگر | «پروتئین/مقاله‌های این ژن کدام‌اند؟» |
| ‏`efetch` | ‏UID یا accession → رکورد کامل (FASTA، GenBank، …) | «خود رکورد را بده» |

چند ابزار دیگر هم هست (`epost`، `egquery`، `espell`، `ecitmatch`) که در این درس به کارشان نمی‌گیریم.

> 📺 **فیلم:** *E-Utilities Introduction* (National Library of Medicine): https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** Sayers E. *A General Introduction to the E-utilities.* In: Entrez Programming Utilities Help. NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK25497/ · Sayers EW, et al. (2025). *Database resources of the National Center for Biotechnology Information in 2025.* Nucleic Acids Res 53(D1):D20–D29. https://doi.org/10.1093/nar/gkae979

---

## ۳. گام ۱: `einfo`؛ چه پایگاه‌هایی هست؟

**چرا؟** پیش از جست‌وجو باید بدانید نام دقیق پایگاه چیست (`gene`، نه `genes`) و چه فیلدهایی دارد.

<div dir="ltr">

```bash
curl -sS "$B/einfo.fcgi" > einfo.xml
grep -c '<DbName>' einfo.xml
grep -o '<DbName>[^<]*' einfo.xml | cut -d'>' -f2 | head -8 | tr '\n' ' '; echo
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`curl -sS` | بی نوار پیشرفت (`-s`) ولی اگر خطایی بود نشانش بده (`-S`) |
| ‏`"$B/einfo.fcgi"` | ‏`einfo` بی هیچ پارامتر: فهرست همه‌ی پایگاه‌ها |
| ‏`grep -o '<DbName>[^<]*'` | تنها تکه‌ی `<DbName>نام` را از هر سطر بیرون بکش (`[^<]*` = هر چیز تا پیش از `<` بعدی) |
| ‏`cut -d'>' -f2` | ‏`<DbName>` را دور بریز، نام بماند |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
38
pubmed protein nuccore ipg nucleotide structure genome gap
```

</div>

‏**۳۸** پایگاه. حالا آگاهی یک پایگاه، پایگاه Gene:

<div dir="ltr">

```bash
curl -sS "$B/einfo.fcgi?db=gene" > einfo_gene.xml
grep -oE '<(Count|LastUpdate|Description)>[^<]*' einfo_gene.xml | head -3
grep -c '<Field>' einfo_gene.xml
grep -c '<Link>' einfo_gene.xml
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Description>Gene database
<Count>101280616
<LastUpdate>2026/10/26 09:28
36
33
```

</div>

**توضیح خروجی:**
- پایگاه Gene بیش از **۱۰۱ میلیون** ژن دارد و روز پیش به‌روز شده است.
- ‏**۳۶ فیلد جست‌وجو** دارد (مانند `GENE` = نام ژن، `PREF` = preferred symbol، `ORGN` = جاندار) و **۳۳ گونه پیوند** به پایگاه‌های دیگر (مانند `gene_protein`، `gene_pubmed`).
- ‏`?db=gene` یعنی پارامتر `db` را برابر `gene` بگذار. ‏`?` پارامترها را از نشانی جدا می‌کند و `&` پارامترها را از هم.

<details>
<summary>✋ امتحان کن: نام کوتاه فیلد «preferred symbol» در einfo پایگاه Gene چیست؟</summary>

<div dir="ltr">

```bash
grep -A2 '<Name>PREF</Name>' einfo_gene.xml
```

</div>

‏`PREF`، با `<FullName>Preferred Symbol</FullName>`. هر فیلد یک نام کوتاه و یک نام کامل دارد؛ در پرسش هر دو کار می‌کنند (`rpoB[PREF]` همان `rpoB[preferred symbol]` است). **دام:** `PFN` شبیه است ولی یعنی *Protein Full Name*؛ نام کوتاه را همیشه در einfo بسنجید، نه با حدس.

</details>

---

## ۴. گام ۲: `esearch`؛ از نام ژن به UID

**چرا؟** هر کار با Entrez با یک جست‌وجو آغاز می‌شود. خروجی `esearch` فهرست UIDهاست.

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" \
     --data-urlencode "db=gene" \
     --data-urlencode "term=rpoB[gene] AND Escherichia coli K-12[orgn]" > s1.xml
grep -oE '<Count>[^<]*' s1.xml | head -1
grep -o '<Id>[^<]*' s1.xml | cut -d'>' -f2 | tr '\n' ' '; echo
grep -o '<QueryTranslation>[^<]*' s1.xml
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`-G` | پارامترهای `--data-urlencode` را با `?` و `&` به پایان نشانی بچسبان (درخواست GET) |
| ‏`--data-urlencode "term=…"` | فاصله، `[` و `]` را به شکل امن نشانی درآور (`%20`، `%5B`، `%5D`). اشتباه رایج ۱ را ببینید |
| ‏`rpoB[gene]` | ‏`rpoB` را تنها در فیلد **نام ژن** بجوی |
| ‏`Escherichia coli K-12[orgn]` | تنها در جاندار *E. coli* K-12 (و همه‌ی زیرسویه‌هایش) |
| ‏`head -1` | نخستین `<Count>` شمار کل است؛ `<Count>`های بعدی شمار هر بخش پرسش‌اند |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>6
948488 14968024 12934478 7952368 7436037 6058462
<QueryTranslation>rpoB[gene] AND "Escherichia coli K-12"[Organism]
```

</div>

**توضیح خروجی:**
- **شش** ژن، نه یکی! چون «*E. coli* K-12» یک **گروه** در رده‌بندی است و زیرسویه‌های MG1655، W3110، DH10B، MDS42 و BW2952 همه زیر آن‌اند. هر زیرسویه‌ای که ژنومش در NCBI هست رکورد Gene جدا دارد.
- ‏`QueryTranslation` نشان می‌دهد Entrez پرسش شما را چگونه فهمید: `[orgn]` به `[Organism]` برگردانده شد. **همیشه این سطر را ببینید**؛ اگر Entrez پرسش را جور دیگری فهمیده باشد، این‌جا پیداست.

برای یک زیرسویه‌ی **تنها** (MG1655، سویه‌ی مرجع) از شناسه‌ی رده‌بندی آن (TaxID ‏`511145`) و `noexp` کار بکشید:

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode "db=gene" \
     --data-urlencode "term=rpoB[gene] AND txid511145[Organism:noexp]" | grep -oE '<(Count|Id)>[^<]*'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>1
<Id>948488
<Count>22433
<Count>4672
```

</div>

‏**۱** ژن: Gene ID ‏`948488`. دو `<Count>` بعدی شمار هر بخش جداگانه‌اند: ‏`rpoB[gene]` در همه‌ی جانداران ۲۲٬۴۳۳ ژن و `txid511145` روی هم ۴٬۶۷۲ ژن.

| برچسب | معنا |
| :--- | :--- |
| ‏`txid511145[Organism]` | این TaxID **و همه‌ی شاخه‌های زیر آن** (explode، پیش‌فرض) |
| ‏`txid511145[Organism:noexp]` | **تنها** خود این TaxID (no explode) |

<details>
<summary>✋ امتحان کن: اگر برچسب `[gene]` را بردارید (`rpoB AND txid511145[Organism:noexp]`) چند ژن می‌آید؟</summary>

**۸** ژن (2026-10-27). بی برچسب، Entrez واژه را در **همه‌ی فیلدها** می‌جوید: در نام‌های دیگر ژن‌ها، در خلاصه‌ی متنی‌شان و… ژن‌هایی که در شرح‌شان به rpoB اشاره شده هم می‌آیند. تمرین ۲ همین را با gyrA می‌کاود.

</details>

> 📺 **فیلم:** *E-Utilities Introduction* (NLM)، بخش ESearch: https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** Sayers E. *The E-utilities In-Depth: Parameters, Syntax and More* (ESearch). NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK25499/ · Brown GR, et al. (2015). *Gene: a gene-centered information resource at NCBI.* Nucleic Acids Res 43(D1):D36–D42. https://doi.org/10.1093/nar/gku1055

---

## ۵. گام ۳: `esummary`؛ ژن کجای ژنوم است؟

**چرا؟** UID تنها یک عدد است. ‏`esummary` نام، شرح، نام‌های دیگر و **جای ژن روی کروموزوم** را می‌دهد.

<div dir="ltr">

```bash
curl -sS "$B/esummary.fcgi?db=gene&id=948488" > sum.xml
grep -oE '<(Name|Description|OtherAliases|ChrAccVer|ChrStart|ChrStop)>[^<]*' sum.xml
grep -oE '<(ScientificName|TaxID)>[^<]*' sum.xml
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Name>rpoB
<Description>RNA polymerase subunit beta
<OtherAliases>b3987, ECK3978, ftsR, groN, nitB, rif, ron, sdgB, stl, stv, tabD
<ChrAccVer>NC_000913.3
<ChrStart>4181244
<ChrStop>4185272
<ChrStart>999999999
<ScientificName>Escherichia coli str. K-12 substr. MG1655
<TaxID>511145
```

</div>

**توضیح خروجی:**
- ‏`OtherAliases`: ‏**۱۱ نام دیگر** برای همین ژن؛ `b3987` شماره‌ی locus در MG1655 است و `rif` («ریفامپیسین») نام قدیمی‌اش. این نام‌ها در گام بعد و درس ۲ دردسر می‌سازند.
- ‏`ChrAccVer` ‏`NC_000913.3`: همان کروموزوم مرجعی که در بخش‌های پیشین دیدید.
- ‏`ChrStart` و `ChrStop`: **از صفر شمرده می‌شوند** (0-based). در GenBank و در ماژول 02/03 همین ژن `4181245..4185273` است؛ **به هر دو یک بیفزایید**. ‏`ChrStart` کوچک‌تر از `ChrStop` است، پس ژن روی رشته‌ی **مثبت** است. طول: `4185272 − 4181244 + 1 = 4029` باز.
- **یک `ChrStart` دوم با `999999999`!** این جای ژن نیست؛ فیلدی برای مرتب‌سازی در صفحه‌ی وب است که هم‌نام از آب درآمده. ‏`grep` نمی‌داند هر فیلد درون کدام بخش XML است و همه را می‌آورد. در درس ۲ با `xtract` این گرفتاری را درست حل می‌کنیم.

<details>
<summary>✋ امتحان کن: طول پروتئین rpoB را از طول ژن پیش‌بینی کنید.</summary>

‏۴۰۲۹ باز = ۱۳۴۳ کُدون. کُدون پایانی اسید آمینه نمی‌سازد، پس **۱۳۴۲** اسید آمینه. در گام ۵ همین عدد را می‌بینیم.

</details>

---

## ۶. گام ۴: `elink`؛ از ژن به پروتئین و مقاله

**چرا؟** ‏UID ژن را داریم؛ پروتئین‌اش در پایگاه دیگری است (`protein`). ‏`elink` پل میان پایگاه‌هاست.

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&id=948488" > link.xml
grep -oE '<LinkName>[^<]*' link.xml
curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&id=948488&linkname=gene_protein_refseq" | grep -o '<Id>[^<]*'
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`dbfrom=gene&db=protein` | از پایگاه Gene به پایگاه Protein |
| ‏`id=948488` | ژن آغاز |
| ‏`linkname=gene_protein_refseq` | از میان گونه‌های پیوند، تنها پیوند به پروتئین‌های **RefSeq** |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<LinkName>gene_protein
<LinkName>gene_protein_refseq
<Id>948488
<Id>16131817
```

</div>

**توضیح خروجی:**
- دو گونه پیوند: `gene_protein` (همه‌ی پروتئین‌ها؛ **۱۳** رکورد) و `gene_protein_refseq` (تنها RefSeq؛ **۱** رکورد).
- چرا ۱۳؟ همان پروتئین rpoB از MG1655 بارها ثبت شده است: یک بار در RefSeq (`NP_…`)، یک بار با ژنوم اصلی GenBank (`AAC…`)، و در چند پروژه‌ی تعیین توالی دوباره‌ی MG1655. برای کار بیوانفورماتیک **RefSeq** را برمی‌داریم: یک رکورد بازبینی‌شده و بی‌تکرار برای هر پروتئین (ماژول 11/02 RefSeq را می‌کاود).
- **دام:** نخستین `<Id>` (`948488`) پروتئین نیست؛ شناسه‌ی **ژن آغاز** است که `elink` در پاسخ برمی‌گرداند. پروتئین تنها `16131817` است. پس **شمار پیوندها = شمار `<Id>` منهای یک**.

همین برای مقاله‌ها:

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=pubmed&id=948488&linkname=gene_pubmed" | grep -c '<Id>'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
351
```

</div>

‏۳۵۱ − ۱ = **۳۵۰** مقاله در PubMed به ژن rpoB در MG1655 پیوند دارند.

> 📺 **فیلم:** *E-Utilities Introduction* (NLM)، بخش ELink: https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** ‏ELink و فهرست نام پیوندها در *The E-utilities In-Depth*: https://www.ncbi.nlm.nih.gov/books/NBK25499/ (بخش ELink)

---

## ۷. گام ۵: `efetch`؛ خود توالی

**چرا؟** تا این‌جا تنها شناسه داشتیم. ‏`efetch` رکورد کامل را می‌دهد.

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=protein&id=16131817&rettype=fasta&retmode=text" > rpoB.faa
head -2 rpoB.faa
grep -v '>' rpoB.faa | tr -d '\n' | wc -c
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`rettype=fasta&retmode=text` | قالب FASTA، متن ساده |
| ‏`grep -v '>'` | سطر سرخط را کنار بگذار |
| ‏`tr -d '\n' \| wc -c` | سطرهای توالی را به هم بچسبان و نویسه‌ها را بشمار |

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
>NP_418414.1 RNA polymerase subunit beta [Escherichia coli str. K-12 substr. MG1655]
MVYSYTEKKRIRKDFGKRPQVLDVPYLLSIQLDSFQKFIEQDPEGQYGLEAAFRSVFPIQSYSGNSELQY
1342
```

</div>

‏UID ‏`16131817` همان **`NP_418414.1`** است، با **۱۳۴۲** اسید آمینه؛ درست همان پیش‌بینی گام ۳. همین را با accession هم می‌توانید بگیرید (`id=NP_418414.1`)؛ نتیجه یکی است.

---

## ۸. گام ۶: سرور تاریخچه؛ چند گام در یک زنجیر

**چرا؟** در گام‌های ۲ تا ۵ هر بار شناسه را با چشم خواندیم و در دستور بعدی گذاشتیم. برای ۲ ژن مشکلی نیست؛ برای ۲۰۰۰ ژن نشدنی است. **سرور تاریخچه** نتیجه‌ی هر گام را **روی سرور NCBI** نگه می‌دارد و شما تنها یک «برگه‌ی امانت» (WebEnv) و یک شماره (QueryKey) به گام بعد می‌دهید.

**تشبیه:** به جای بردن ۲۰۰۰ کتاب از این تالار به آن تالار، تنها شماره‌ی قفسه را به کتابدار می‌دهید.

### ۸.۱ جست‌وجو با `usehistory=y`

<div dir="ltr">

```bash
curl -sS -G "$B/esearch.fcgi" --data-urlencode "db=gene" --data-urlencode "usehistory=y" \
     --data-urlencode "term=(rpoB[preferred symbol] OR gyrA[preferred symbol]) AND txid511145[Organism:noexp]" > h1.xml
grep -oE '<(Count|QueryKey|WebEnv)>[^<]*' h1.xml | head -3
WE=$(grep -o '<WebEnv>[^<]*' h1.xml | cut -d'>' -f2)
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>2
<QueryKey>1
<WebEnv>MCID_6ae070d59501553bbc059500
```

</div>

دو ژن (rpoB و gyrA) روی سرور، با `QueryKey=1` در «پرونده»ی `WebEnv`. ‏`WE=$(…)` همان کار بخش ۰۱ است: خروجی یک دستور را در یک متغیر بریز. **WebEnv شما با این یکی فرق دارد** و تنها چند ساعت زنده است.

### ۸.۲ پیوند روی سرور: `cmd=neighbor_history`

<div dir="ltr">

```bash
curl -sS "$B/elink.fcgi?dbfrom=gene&db=protein&linkname=gene_protein_refseq&cmd=neighbor_history&query_key=1&WebEnv=$WE" \
     | grep -oE '<(LinkName|QueryKey)>[^<]*'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<LinkName>gene_protein_refseq
<QueryKey>2
```

</div>

‏`elink` این بار شناسه‌ها را چاپ نکرد؛ پروتئین‌ها را روی سرور با `QueryKey=2` نگه داشت.

### ۸.۳ دریافت از سرور

<div dir="ltr">

```bash
curl -sS "$B/efetch.fcgi?db=protein&query_key=2&WebEnv=$WE&rettype=fasta&retmode=text" > two.faa
awk '/^>/{if(h)print h, n; h=$1; n=0; next}{n+=length($0)} END{print h, n}' two.faa
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
>NP_418414.1 1342
>NP_416734.1 875
```

</div>

دو پروتئین RefSeq: rpoB (۱۳۴۲) و **gyrA** (`NP_416734.1`، ۸۷۵ اسید آمینه)، بی آنکه حتی یک UID را دست زده باشید. دستور `awk` همان شمارنده‌ی طول بخش ۰۱ است: در هر سرخط طول پیشین را چاپ کن و از نو بشمار.

| پارامتر | معنا |
| :--- | :--- |
| ‏`usehistory=y` | نتیجه را روی سرور نگه دار و WebEnv بده |
| ‏`cmd=neighbor_history` | پیوندها را روی سرور نگه دار، چاپ نکن |
| ‏`query_key` + `WebEnv` | به جای `id=`: «همان فهرست شماره‌ی ۲ در آن پرونده» |

<details>
<summary>✋ امتحان کن: اگر `WebEnv` را درست بدهید ولی `query_key=3` چه می‌شود؟</summary>

در این پرونده تنها دو فهرست هست. ‏`curl` هیچ خطایی نشان نمی‌دهد، ولی درون فایل به جای FASTA این است (2026-10-27):

<div dir="ltr">

```
<eFetchResult>
	<ERROR>Unable to obtain query #3</ERROR>
</eFetchResult>
```

</div>

پس همیشه پس از `efetch` شمار رکوردها را بسنجید، و با `grep -c '^>'` (تنها `>` در **آغاز** سطر): همین فایل خطا با `grep -c '>'` عدد **۵** می‌دهد، چون هر برچسب XML هم `>` دارد؛ با `'^>'` درست **۰**.

</details>

> 📺 **فیلم:** *E-Utilities Introduction* (NLM)، بخش History server: https://www.youtube.com/watch?v=BCG-M5k-gvE
> 📄 **مرجع:** «Using the Entrez History Server» در *A General Introduction to the E-utilities*: https://www.ncbi.nlm.nih.gov/books/NBK25497/

---

## ۹. گام ۷: مرز سرعت و کلید API

**چرا؟** سرورهای NCBI میان همه‌ی جهان بخش می‌شوند. قاعده:
- **بی کلید:** بیشینه **۳ درخواست در ثانیه** از هر نشانی IP.
- **با کلید API:** تا **۱۰ درخواست در ثانیه**.
- کارهای بزرگ (بیش از ۱۰۰ درخواست) را شب‌ها یا آخر هفته (به وقت آمریکا) بفرستید.

ببینیم اگر ۱۲ درخواست هم‌زمان بفرستیم چه می‌شود (`seq 1 12` عددهای ۱ تا ۱۲ را می‌دهد، `&` هر دستور را در پس‌زمینه اجرا می‌کند (بخش 01/10) و `wait` تا پایان همه می‌ایستد):

<div dir="ltr">

```bash
for i in $(seq 1 12); do curl -s "$B/einfo.fcgi?db=gene&retmode=json" -o rate_$i.txt & done; wait
cat rate_*.txt | grep -o '"error":"[^"]*"' | sort | uniq -c
grep -h -m1 -o '{"error[^}]*}' rate_*.txt | head -1
rm rate_*.txt
```

</div>

**خروجی واقعی (2026-10-27؛ نشانی IP پوشانده شده):**

<div dir="ltr">

```
      9 "error":"API rate limit exceeded"
{"error":"API rate limit exceeded","api-key":"<نشانی IP شما>","count":"4","limit":"3"}
```

</div>

**توضیح خروجی:**
- تنها **۳** درخواست پذیرفته شد و **۹** تا با `API rate limit exceeded` رد شدند. ‏`"limit":"3"` همان مرز بی‌کلید است.
- بی کلید، NCBI شما را با **نشانی IP** می‌شناسد (فیلد `api-key`). اگر کلاس ۲۰ نفره پشت یک IP باشد، مرز ۳ درخواست برای **همه با هم** است.
- **بدتر از رد شدن:** درخواست رد شده خطای HTTP نمی‌دهد که `curl` آن را ببیند؛ فایل خروجی تنها همین یک سطر JSON است. اسکریپتی که خروجی را نسنجد، با داده‌ی تهی جلو می‌رود.

**کلید API:** پس از ساخت حساب NCBI، در بخش «Account settings» یک کلید (۳۶ نویسه) بسازید. **هرگز کلید را در اسکریپت، در Git یا در گزارش ننویسید.** آن را تنها در `~/.bashrc` بگذارید:

<div dir="ltr">

```bash
echo 'export NCBI_API_KEY="کلید_شما"' >> ~/.bashrc     # once; then open a new terminal
curl -sS "$B/esearch.fcgi?db=gene&term=rpoB%5Bgene%5D&api_key=$NCBI_API_KEY" | grep -m1 -o '<Count>[^<]*'
```

</div>

**خروجی واقعی (2026-10-27):**

<div dir="ltr">

```
<Count>22433
```

</div>

آزمون درخواست‌های هم‌زمان را با کلید و **۸** درخواست (زیر مرز ۱۰) تکرار کردیم: **هیچ‌کدام** رد نشد.

در دستورها تنها نام متغیر `$NCBI_API_KEY` دیده می‌شود، نه خود کلید. ‏EDirect (درس ۲) و Biopython این متغیر را خودشان می‌خوانند.

> 📺 **فیلم:** ‏NLM، *Downloading NCBI Biological Data and Creating Custom Reports Using the Command Line* (ضبط کارگاه، 2023): https://www.nlm.nih.gov/ncbi/workshops/2023-04_custom-reports/workshop-video.html
> 📄 **مرجع:** *New API Keys for the E-utilities* (NCBI Insights، 2017): https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/ · بخش «Usage Guidelines and Requirements» در https://www.ncbi.nlm.nih.gov/books/NBK25497/

---

## ۱۰. سه اشتباه رایج

1. **کروشه و فاصله در نشانی.** ‏`curl` در نشانی، `[` و `]` را «بازه» می‌فهمد:

   <div dir="ltr">

   ```bash
   curl -sS "$B/esearch.fcgi?db=gene&term=rpoB[gene]"
   ```

   </div>

   **خروجی واقعی:**

   <div dir="ltr">

   ```
   curl: (3) bad range in URL position 78:
   https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=rpoB[gene]
                                                                                ^
   ```

   </div>

   راه درست: `-G --data-urlencode "term=…"` (گام ۲)، یا نوشتن `%5B` و `%5D` به جای کروشه‌ها و `+` به جای فاصله (گام ۷).
2. **جست‌وجو بی برچسب فیلد.** ‏`rpoB AND txid511145[Organism:noexp]` ‏۸ ژن می‌دهد، نه یکی. همیشه `[gene]` یا `[preferred symbol]` بگذارید و `QueryTranslation` را ببینید.
3. **فراموش کردن 0-based بودن مختصات Gene.** ‏`ChrStart=4181244` در GenBank `4181245` است. اگر این عدد را بی افزودن یک به `seq_start` بدهید، توالی یک باز جابه‌جا می‌شود و ترجمه‌اش بی‌معنا. تمرین ۳ همین را می‌آزماید.

---

## 📘 برای کنجکاوها

- ‏**JSON به جای XML:** بیشتر ابزارها `retmode=json` را می‌پذیرند (`esearch`، `esummary`، `elink`، `einfo`)؛ ‏`efetch` نه. JSON را با `jq` یا پایتون آسان‌تر می‌خوانید.
- ‏**POST برای فهرست‌های بلند:** اگر هزاران `id=` دارید، نشانی خیلی بلند می‌شود. ‏`curl -X POST -d "db=gene&id=…"` همان کار را بی مرز طول انجام می‌دهد؛ ‏EDirect خودش همین را می‌کند.
- ‏**`tool` و `email`:** NCBI می‌خواهد در کارهای بزرگ پارامترهای `tool=نام_برنامه` و `email=نشانی_شما` را هم بفرستید تا اگر برنامه‌تان بار سنگینی ساخت، پیش از بستن دسترسی با شما تماس بگیرند.
- ‏**`retmax` و `retstart`:** ‏`esearch` به گونه‌ی پیش‌فرض تنها ۲۰ UID نخست را برمی‌گرداند (`Count` شمار کل است). برای بیشتر، `retmax` را بالا ببرید یا بهتر، سرور تاریخچه را به کار ببرید.

---

## جمع‌بندی

- ‏Entrez ‏۳۸ پایگاه پیوسته است؛ E-utilities نشانی‌های وبی‌اند که با `curl` صدا زده می‌شوند.
- ‏`esearch` → UID، ‏`esummary` → خلاصه، ‏`elink` → رکوردهای وابسته در پایگاه دیگر، ‏`efetch` → رکورد کامل.
- برچسب فیلد (`[gene]`، `[Organism:noexp]`) شش نتیجه را به یکی رساند. ‏`QueryTranslation` را همیشه ببینید.
- ‏*rpoB* در MG1655: Gene ID ‏`948488`، ‏`NC_000913.3` ‏4181245..4185273 (پس از افزودن یک)، رشته‌ی مثبت، پروتئین `NP_418414.1` با ۱۳۴۲ اسید آمینه، ۳۵۰ مقاله.
- سرور تاریخچه (`usehistory`، `WebEnv`، `query_key`) گام‌ها را بی جابه‌جایی شناسه‌ها به هم می‌چسباند.
- مرز سرعت ۳ درخواست در ثانیه بی کلید و ۱۰ با کلید؛ کلید تنها در متغیر محیطی.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
B=https://eutils.ncbi.nlm.nih.gov/entrez/eutils
curl -sS "$B/einfo.fcgi?db=DB"                                             # databases / fields / links
curl -sS -G "$B/esearch.fcgi" --data-urlencode "db=DB" --data-urlencode "term=QUERY"
curl -sS "$B/esummary.fcgi?db=DB&id=UID"
curl -sS "$B/elink.fcgi?dbfrom=DB1&db=DB2&id=UID&linkname=DB1_DB2_xxx"   # first <Id> = source
curl -sS "$B/efetch.fcgi?db=DB&id=UID_OR_ACC&rettype=fasta&retmode=text"
# history: esearch usehistory=y -> WebEnv; elink cmd=neighbor_history; efetch query_key=N&WebEnv=$WE
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏Entrez | سامانه‌ی جست‌وجوی یکپارچه‌ی NCBI روی همه‌ی پایگاه‌هایش |
| ‏E-utilities | رابط برنامه‌نویسی Entrez؛ چند نشانی وب برای جست‌وجو، خلاصه، پیوند و دریافت |
| ‏UID | شناسه‌ی عددی یک رکورد درون یک پایگاه Entrez |
| ‏accession.version | نام پایدار رکورد توالی همراه با شماره‌ی نسخه |
| برچسب فیلد (field tag) | ‏`[gene]`، `[orgn]` و… که می‌گوید واژه در کدام فیلد جست‌وجو شود |
| ‏TaxID | شناسه‌ی عددی یک جاندار در رده‌بندی NCBI |
| ‏explode / noexp | با / بی همه‌ی شاخه‌های زیر یک گروه رده‌بندی |
| پیوند (link) | رابطه‌ی ثبت‌شده میان رکوردهای دو پایگاه (مانند ژن → پروتئین) |
| ‏RefSeq | مجموعه‌ی توالی‌های مرجع بازبینی‌شده و بی‌تکرار NCBI |
| سرور تاریخچه (History server) | نگه‌داری نتیجه‌ی هر گام روی سرور NCBI |
| ‏WebEnv / QueryKey | شناسه‌ی پرونده روی سرور / شماره‌ی هر فهرست درون آن |
| 0-based | شمارش جایگاه از صفر؛ GenBank از یک می‌شمارد |
| مرز سرعت (rate limit) | بیشینه‌ی درخواست در ثانیه که سرور می‌پذیرد |
| کلید API | رشته‌ی شخصی که مرز سرعت را بالا می‌برد و شما را می‌شناساند |

---

## منابع

**مقاله و مستند**
- ‏Sayers EW, et al. (2025). *Database resources of the National Center for Biotechnology Information in 2025.* Nucleic Acids Res 53(D1):D20–D29. https://doi.org/10.1093/nar/gkae979
- ‏Brown GR, et al. (2015). *Gene: a gene-centered information resource at NCBI.* Nucleic Acids Res 43(D1):D36–D42. https://doi.org/10.1093/nar/gku1055
- ‏Sayers E. *A General Introduction to the E-utilities.* Entrez Programming Utilities Help, NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK25497/
- ‏Sayers E. *The E-utilities In-Depth: Parameters, Syntax and More.* NCBI Bookshelf: https://www.ncbi.nlm.nih.gov/books/NBK25499/
- *New API Keys for the E-utilities.* NCBI Insights (2017): https://ncbiinsights.ncbi.nlm.nih.gov/2017/11/02/new-api-keys-for-the-e-utilities/

**کتاب**
- ‏Pevsner J (2015). *Bioinformatics and Functional Genomics*, 3rd ed. Wiley-Blackwell. (فصل ۲: دسترسی به داده‌ی توالی و ادبیات؛ Entrez، accession و RefSeq)
- ‏Baxevanis AD, Bader GD, Wishart DS (eds.) (2020). *Bioinformatics*, 4th ed. Wiley. (فصل‌های پایگاه‌های داده‌ی زیستی و NCBI)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Access Bioinformatics Databases with Biopython* (پروژه‌ی راهنمادار، Entrez و PubMed): https://www.coursera.org/projects/access-bioinformatics-databases-with-biopython
- ‏edX: *Introduction to Genomic Data Science* (UC San Diego؛ پایگاه‌های داده‌ی ژنومی): https://www.edx.org/learn/bioinformatics/the-university-of-california-san-diego-introduction-to-genomic-data-science
- ‏YouTube: *E-Utilities Introduction* (National Library of Medicine): https://www.youtube.com/watch?v=BCG-M5k-gvE
- ‏NLM: *Downloading NCBI Biological Data and Creating Custom Reports Using the Command Line* (ضبط کارگاه): https://www.nlm.nih.gov/ncbi/workshops/2023-04_custom-reports/workshop-video.html

<sub>همه‌ی دستورها در 2026-10-27 روی سرور دوره اجرا شدند. DOIها با doi.org، و صفحه‌های NCBI و Coursera با درخواست مستقیم (HTTP 200) وارسی شدند؛ عنوان فیلم YouTube با noembed وارسی شد. نشانی IP در خروجی گام ۷ پوشانده شد.</sub>

</div>
