<div dir="rtl">

# پاسخ تشریحی: خانواده و دامنه‌ی پروتئین

همه‌ی خروجی‌ها واقعی‌اند (InterPro API ‏release 110.0، Pfam 38.2، HMMER 3.4، UniProt REST؛ روی سرور دوره، 2026-10-27).

---

## پاسخ ۱: سه بتالاکتاماز ناشناس

<div dir="ltr">

```bash
curl -sS "https://rest.uniprot.org/uniprotkb/accessions?accessions=P0AD64,Q48434,Q5U7L7&format=fasta" > three.faa
grep '>' three.faa | cut -c1-50
hmmscan --cut_ga --domtblout three.domtbl -o /dev/null mini_pfam.hmm three.faa
grep -v '^#' three.domtbl | awk '{split($4, q, "|"); printf "%-8s %-15s %-11s %9s %6s %5s-%-5s\n", q[2], $1, $2, $7, $14, $18, $19}'
for a in P0AD64 Q48434 Q5U7L7; do
  curl -sS "$I/entry/pfam/protein/uniprot/$a" \
    | jq -r --arg a $a '.results[] | [$a, .metadata.accession, (.proteins[0].entry_protein_locations[] | .fragments[] | "\(.start)-\(.end)")] | @tsv'
  sleep 1
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
>sp|P0AD64|BLA1_KLEPN Beta-lactamase SHV-1 OS=Kleb
>sp|Q48434|BLCY2_KLEPN Beta-lactamase CMY-2 OS=Kle
>sp|Q5U7L7|BLBV2_ECOLX Metallo-beta-lactamase VIM-
P0AD64   Beta-lactamase2 PF13354.13    3.6e-44  139.5    28-284  
P0AD64   Beta-lactamase  PF00144.30    3.8e-38  119.5    39-274  
Q48434   Beta-lactamase  PF00144.30    2.2e-98  318.0    32-380  
Q5U7L7   Lactamase_B     PF00753.34    1.7e-17   51.5    67-211  
P0AD64	PF13354	28-284
Q48434	PF00144	32-380
Q5U7L7	PF00753	67-211
```

</div>

- ‏**SHV-1:** رده‌ی **A** (PF13354). مانند سه آنزیم رده‌ی A درس، مدل رده‌ی C را هم با امتیاز ۱۱۹٫۵ گذراند.
- ‏**CMY-2:** رده‌ی **C** (PF00144، امتیاز ۳۱۸، مانند AmpC). ‏CMY-2 یک AmpC **پلاسمیدی** است: همان آنزیم کروموزومی، این‌بار روی پلاسمید و با بیان بالا.
- ‏**VIM-2:** رده‌ی **B** (متالوبتالاکتاماز، PF00753)، مانند NDM-1.

پاسخ PF00144 برای SHV-1 در InterPro **نیست**، چون PF13354 و PF00144 هم‌clan‌اند و Pfam تنها بهترین را نگه می‌دارد (درس، بخش ۵.۱). مرزها (۲۸–۲۸۴، ۳۲–۳۸۰، ۶۷–۲۱۱) درست همان InterPro است.

---

## پاسخ ۲: دو مرز برای یک دامنه

| بخش | ‏Pfam (درس) | CDD (11/07) |
| :--- | :--- | :--- |
| ‏GCR (بخش آغازی) | ‏PF02155: ‏۲۶–۴۰۱ | ‏pfam02155: ‏۲۶–۴۰۱ |
| ‏DBD (انگشت روی) | ‏PF00105 (zf-C4): ‏۴۲۰–۴۸۷ | ‏cd07172: ‏۴۱۷–۴۹۴ |
| ‏LBD | ‏PF00104 (Hormone_recep): ‏۵۵۸–۷۳۵ | ‏cd07076: ‏۵۳۱–۷۷۷ |

- ‏**GCR** درست یکسان است، چون CDD همان مدل Pfam را (با نام `pfam02155`) به کار می‌برد.
- ‏**DBD:** ‏CDD سه اسید آمینه پیش‌تر آغاز و هفت پس‌تر پایان می‌دهد. ‏**LBD:** ‏CDD ‏۲۷ زودتر آغاز می‌شود و تا پایان پروتئین (۷۷۷) می‌رود؛ Pfam ‏۴۲ اسید آمینه کوتاه‌تر.
- هیچ‌کدام «نادرست» نیست. مدل `cd…` ویژه‌ی **گیرنده‌های گلوکوکورتیکوئید و پروژسترون** است و از ساختار سه‌بعدی همین گروه ساخته شده؛ مدل Pfam برای **همه**‌ی گیرنده‌های هسته‌ای است و تنها هسته‌ی حفظ‌شده‌ی مشترک همه را می‌پوشاند. مرز دامنه یک **برآورد** است: برای کار با پروتئین (برش، بیان دامنه) از ساختار (PDB، 09/01) و چند منبع کمک بگیرید.

---

## پاسخ ۳: الگو در برابر HMM

<div dir="ltr">

```bash
cat query.faa three.faa > all9.faa
for a in P62593 P0AD64 A0A5R8T042 Q9F663; do
  r=$(curl -sS "$I/entry/prosite/protein/uniprot/$a" \
      | jq -r '[.results[]? | select(.metadata.accession == "PS00146") | .proteins[0].entry_protein_locations[0].fragments[0] | "\(.start)-\(.end)"] | join(",")')
  echo -e "$a\t${r:-none}"
  sleep 1
done
for a in P62593 P0AD64 A0A5R8T042 Q9F663; do
  s=$(awk -v a=$a '/^>/ {p = index($0, "|" a "|") > 0; next} p' all9.faa | tr -d '\n')
  m=$(echo "$s" | grep -boE 'S..K' | head -1 | cut -d: -f1)
  echo "$a  $(echo "$s" | cut -c$((m - 3))-$((m + 12)))"
done
curl -sS https://prosite.expasy.org/PS00146.txt | grep '^PA'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
P62593	64-79
P0AD64	62-77
A0A5R8T042	69-84
Q9F663	none
P62593  FPMMSTFKVLLCGAVL
P0AD64  FPMMSTFKVVLCGAVL
A0A5R8T042  FAMCSTSKVMAAAAVL
Q9F663  FPLCSSFKGFLAAAVL
PA   [FY]-x-[LIVMFY]-{E}-S-[TV]-x-K-x(3)-{T}-[AGLM]-{D}-{KA}-[LC].
```

</div>

برای KPC-2 سرور InterPro پاسخ **HTTP 204** (No Content) می‌دهد: «چیزی برای گزارش نیست»، با بدنه‌ی تهی. ‏`jq` چیزی چاپ نمی‌کند و `${r:-none}` (یعنی «اگر `r` تهی بود، `none`») آن را آشکار می‌کند. ‏`grep -b` جای **بایت** (از صفر) را می‌دهد؛ پس `m` جای `S` منهای یک است و `cut -c$((m - 3))-$((m + 12))` همان ۱۶ اسید آمینه از چهار پیش از `S` را می‌برد.

(الف) ‏**KPC-2** ‏PS00146 ندارد، در حالی که بتالاکتاماز رده‌ی A (و کارباپنماز مهم بالینی) است.

(ب) الگو را جایگاه‌به‌جایگاه بخوانید (`x` = هر چه، `[..]` = یکی از این‌ها، `{..}` = هر چه جز این‌ها):

| جایگاه | ۱ | ۲ | ۳ | ۴ | ۵ | **۶** | ۷ | ۸ |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| الگو | ‏[FY] | ‏x | ‏[LIVMFY] | ‏{E} | ‏S | **[TV]** | ‏x | ‏K |
| ‏TEM-1 | F | P | M | M | S | **T** | F | K |
| ‏KPC-2 | F | P | L | C | S | **S** ❌ | F | K |

جایگاه ششم باید T یا V باشد؛ KPC-2 در آن‌جا S دارد. **یک** اسید آمینه کل الگو را رد می‌کند. ولی HMMها KPC-2 را بی‌دشواری یافتند (درس: PF13354 با E ‏1.2e-49). الگو (PROSITE) یا هست یا نیست؛ HMM امتیاز همه‌ی جایگاه‌ها را با هم می‌سنجد و یک ناهمخوانی را با بقیه جبران می‌کند. پس **نبودِ** یک الگو گواه نبودِ خانواده نیست.

---

## پاسخ ۴: گیرنده‌ی هسته‌ای در باکتری؟

<div dir="ltr">

```bash
hmmfetch mini_pfam.hmm zf-C4 > zf.hmm
hmmsearch --cut_ga --tblout zf.tbl -o /dev/null zf.hmm ecoli.faa; grep -vc '^#' zf.tbl
hmmsearch --tblout zf_all.tbl -o /dev/null zf.hmm ecoli.faa; grep -vc '^#' zf_all.tbl
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
0
0
```

</div>

**هیچ** پروتئینی، حتی بی آستانه‌ی GA (با پیش‌فرض `hmmsearch`، ‏E ≤ 10). ✅ جور است: گیرنده‌های هسته‌ای تنها در **جانوران** هستند (فرادودمان Metazoa). باکتری‌ها ژن‌ها را با دستگاه‌های دیگری (مانند عامل‌های رونویسی دو بخشی و پروتئین‌های HTH) تنظیم می‌کنند. این یک **کنترل منفی** است: مدل درست، روی داده‌ای که نباید پاسخ دهد، پاسخ نمی‌دهد.

---

## پاسخ ۵: همسایه‌های بتالاکتاماز در clan

<div dir="ltr">

```bash
curl -sS "$I/set/pfam/CL0013" | jq -r '.metadata.relationships.nodes[] | [.accession, .short_name, .name] | @tsv'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
PF00905	Transpeptidase	Penicillin binding protein transpeptidase domain
PF04960	Glutaminase	Glutaminase
PF27310	HrcA_C_epsilon	HrcA C-terminal domain
PF06089	Asparaginase_II	L-asparaginase II
PF00144	Beta-lactamase	Beta-lactamase
PF13354	Beta-lactamase2	Beta-lactamase enzyme family
PF00768	Peptidase_S11	D-alanyl-D-alanine carboxypeptidase
PF02113	Peptidase_S13	D-Ala-D-Ala carboxypeptidase 3 (S13) family
```

</div>

**هشت** خانواده. تنها دو تا نام «بتالاکتاماز» دارند (و PF00905 بتالاکتامازهای رده‌ی D را هم در بر دارد). بقیه:
- ‏**Peptidase_S11 و S13، Transpeptidase:** آنزیم‌های دیواره‌ی سلولی (PBPها)؛ D-Ala-D-Ala را می‌برند یا پیوند می‌زنند. همان چیزی که پنی‌سیلین شبیه آن است.
- ‏**Glutaminase** و **Asparaginase_II:** آنزیم‌هایی که گلوتامین و آسپاراژین را می‌شکنند (آسپاراژیناز II باکتریایی دارویی برای سرطان خون است).
- ‏**HrcA_C_epsilon:** بخشی از یک پروتئین تنظیم‌کننده‌ی ژن‌های شوک گرمایی.

همه یک تاخوردگی و یک سازوکار سرینی کهن دارند، با کارهای بسیار گوناگون. همان درس گام ۴: clan خویشاوندی است، نه کار.

---

## پاسخ ۶: ‏GA یا E-value؟

<div dir="ltr">

```bash
hmmfetch mini_pfam.hmm Lactamase_B > b.hmm
grep '^GA' b.hmm
hmmsearch --tblout b_all.tbl -o /dev/null b.hmm ecoli.faa
grep -vc '^#' b_all.tbl
grep -v '^#' b_all.tbl | awk '{print $1, $5, $6}' | tail -4
grep -E '^>(NP_418516.1|NP_418613.2)' ecoli.faa | cut -c1-90
for g in phnP ulaG; do
  a=$(curl -sS -G "https://rest.uniprot.org/uniprotkb/search" --data-urlencode "query=gene_exact:$g AND organism_id:83333 AND reviewed:true" \
        --data-urlencode "fields=accession" --data-urlencode "format=tsv" | tail -1)
  printf "%s %s: " $g $a
  curl -sS "$I/entry/interpro/protein/uniprot/$a" | jq -r '[.results[] | "\(.metadata.accession) \(.metadata.name)"] | join("; ")'
  sleep 1
done
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
GA    22.70 21.90
8
NP_417190.1 6.3e-15 53.6
NP_416771.4 3.6e-08 31.5
NP_418516.1 0.0015 16.5
NP_418613.2 0.0049 14.8
>NP_418516.1 5-phospho-alpha-D-ribosyl 1,2-cyclic phosphate phosphodiesterase [Escherichia coli st
>NP_418613.2 L-ascorbate-6-phosphate lactonase [Escherichia coli str. K-12 substr. MG1655]
phnP P16692: IPR001279 Metallo-beta-lactamase; IPR017693 Phosphonate metabolism protein PhnP; IPR035682 Phosphonate metabolism protein, MBL domain; IPR036866 Ribonuclease Z/Hydroxyacylglutathione hydrolase-like
ulaG P39300: IPR023951 L-ascorbate-6-phosphate lactonase UlaG; IPR036866 Ribonuclease Z/Hydroxyacylglutathione hydrolase-like; IPR048021 UlaG-like, metallo-hydrolase domain; IPR050114 UPF0173/UPF0282/UlaG metal-dependent hydrolases
```

</div>

(الف) بی GA، **هشت** پاسخ به جای شش. دو پاسخ تازه، **PhnP** (فسفودی‌استراز، در سوخت‌وساز فسفونات) و **UlaG** (لاکتوناز در سوخت‌وساز ویتامین C)، امتیاز ۱۶٫۵ و ۱۴٫۸ دارند: **زیر** GA ‏(۲۲٫۷). ‏E-value آن‌ها (۰٫۰۰۱۵ و ۰٫۰۰۴۹) زیر ۰٫۰۱ است و با بسیاری از آستانه‌های رایج «معنادار» به شمار می‌آیند.

(ب) **بله.** InterPro هر دو را در ابرخانواده‌ی **IPR036866** (همان ابرخانواده‌ی NDM-1، تمرین ۱ درس) و PhnP را در IPR001279 «Metallo-beta-lactamase» هم گذاشته است، با مدل‌های پایگاه‌های دیگر. پس **GA محافظه‌کار است**: پاسخ‌های بالای آن کمابیش همیشه درست‌اند، ولی چند عضو دور واقعی را از دست می‌دهد. برای «فهرست مطمئن»، GA؛ برای «یافتن همه‌ی خویشاوندان ممکن»، E-value با نگاه دستی به پاسخ‌ها و سنجش با پایگاه‌های دیگر.

---

## پاسخ ۷ (فکری): ژن تازه روی یک پلاسمید

(الف) ‏PF00753 خانواده‌ای با بیش از ۱۸۷ هزار پروتئین است و در *E. coli* K-12 شش عضو دارد که **هیچ‌کدام** بتالاکتاماز نیستند (گلیوکسالاز، سولفاتاز، ریبونوکلئاز…؛ درس، گام ۴). امتیاز ۴۵ bit حتی از GloC (۱۴۲٫۵) کمتر است. پس «یک دامنه‌ی متالوبتالاکتاماز» تنها می‌گوید «این پروتئین در این ابرخانواده است».

(ب) گام‌های بعد:
1. **همه‌ی InterPro** (یا InterProScan): آیا مدل‌های **ویژه**‌تر، مانند NCBIfam «subclass B1 metallo-beta-lactamase» (همان که برای NDM-1 آمد: `NF033088`) یا CDD «NDM-1…» (`cd16300`)، پاسخ می‌دهند؟
2. **ابزار ویژه‌ی مقاومت:** AMRFinderPlus (08/01) با مدل‌ها و آستانه‌های ویژه‌ی خانواده‌های بتالاکتاماز؛ و BLAST در برابر پایگاه مرجع ژن‌های مقاومت NCBI (11/08) برای نزدیک‌ترین آنزیم شناخته‌شده و درصد یکسانی.
3. **جایگاه فعال:** آیا اسید آمینه‌های نگه‌دارنده‌ی روی (نقش‌های هیستیدین و آسپارتات زیرگروه B1) در هم‌ترازی با NDM-1 و VIM-2 بر جای خود هستند؟ بی آن‌ها آنزیم فلز نمی‌گیرد.
4. **آزمایش:** بیان ژن در یک سویه‌ی حساس و سنجش MIC کارباپنم‌ها (با و بی EDTA که روی را می‌گیرد)، یا آزمایش هیدرولیز (مانند Carba NP). تنها آزمایش «کارباپنماز» را ثابت می‌کند.

</div>
