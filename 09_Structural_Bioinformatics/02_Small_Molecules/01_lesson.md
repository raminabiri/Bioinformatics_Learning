<div dir="rtl">

# درس: مولکول‌های کوچک؛ PubChem، ChEMBL و RDKit

**بخش:** `09_Structural_Bioinformatics` · **ماژول:** `02_Small_Molecules` · **پیش‌نیاز:** ماژول [۰۱](../01_Protein_Structure/)؛ `curl`، `sed` و حلقه‌ی `for` از بخش [۰۱](../../01_Linux/)؛ پایتون (بخش ۰۳) · **زمان:** حدود ۵۰ دقیقه · **ابزار:** PubChem PUG REST، ChEMBL API، RDKit 2026.03.1 · **آخرین بازبینی:** 2026-10-24

> ✅ **وضعیت: اجرا شده.** همه‌ی خروجی‌ها واقعی‌اند (2026-10-24؛ اسکریپت RDKit دو ثانیه و ۸۸ مگابایت). سایت ZINC به سرور ما پاسخ نداد؛ بخش ZINC تنها از مستندات است.

---

## در یک نگاه

**در پایان این درس می‌توانید:**
1. یک مولکول را با **SMILES** بنویسید و بخوانید، و قالب‌های SDF، MOL2 و PDBQT را بشناسید.
2. ساختار و ویژگی‌های چند دارو را با `curl` از **PubChem** بگیرید.
3. سازوکار و وضعیت بالینی یک دارو را از **ChEMBL** بخوانید.
4. با **RDKit** ویژگی‌های دارو-مانندی (قاعده‌ی پنج Lipinski) و **شباهت Tanimoto** را حساب کنید.
5. توضیح دهید چرا ریفامپیسین قاعده‌ی Lipinski را می‌شکند ولی دارویی خوراکی است.

<div dir="ltr">

```bash
conda activate structural
cd ~/struct
P=~/Bioinformatics_Learning-main/09_Structural_Bioinformatics/99_scripts_data
```

</div>

---

## ۱. داستان

در ماژول ۰۱ دیدید ریفامپیسین در جایگاهش در RNAP چگونه می‌نشیند. ولی ریفامپیسین تنها نیست: ریفابوتین، ریفاپنتین و ریفاکسیمین هم از همین خانواده‌اند (**ریفامایسین‌ها**). پیش از اینکه آن‌ها را در ماژول ۰۳ داک کنیم، باید بدانیم این مولکول‌ها چه شکلی‌اند، چقدر بزرگ‌اند، و چقدر به هم شبیه‌اند. همه‌ی این‌ها را می‌توان از چند پایگاه عمومی و چند خط پایتون به دست آورد.

---

## ۲. مفهوم به زبان ساده

### ۲.۱ نوشتن یک مولکول با حروف: SMILES

‏**SMILES** یک مولکول را در یک سطر متن می‌نویسد: اتم‌ها با نمادشان (`C`، `N`، `O`)، پیوند دوگانه `=`، شاخه در پرانتز، و حلقه با شماره. برای نمونه اتانول `CCO` است و بنزن `c1ccccc1` (حروف کوچک = حلقه‌ی آروماتیک). نشانه‌های `@`، `/` و `\` **فضاآرایی** را نشان می‌دهند (کدام سو، کدام ایزومر).

| قالب | چه دارد | کاربرد |
| :--- | :--- | :--- |
| ‏SMILES | پیوندها، بی مختصات | جست‌وجو، جدول، شباهت |
| ‏SDF / MOL | اتم‌ها **با مختصات** دوبعدی یا سه‌بعدی و پیوندها؛ چند مولکول در یک فایل | ورودی بیشتر ابزارها |
| ‏MOL2 | مانند MOL، با نوع اتم و بار | برخی ابزارهای داکینگ |
| ‏PDBQT | ‏PDB + بار جزئی (Q) + نوع اتم AutoDock (T) + پیوندهای چرخان | ورودی AutoDock Vina (ماژول ۰۳) |

### ۲.۲ پایگاه‌ها

- ‏**PubChem** (NCBI): بیش از صد میلیون ترکیب، با یک **CID** برای هر کدام؛ یک API ساده (PUG REST) دارد.
- ‏**ChEMBL** (EMBL-EBI): ترکیب‌ها **همراه با فعالیت زیستی** (IC₅₀، Ki) و سازوکار و وضعیت بالینی داروها.
- ‏**ZINC** (UCSF): میلیاردها ترکیب **خریدنی** با ساختار سه‌بعدی آماده برای غربالگری مجازی.

### ۲.۳ دارو-مانندی و قاعده‌ی پنج Lipinski

‏Lipinski (۱۹۹۷) دید بیشتر داروهای **خوراکی** این چهار شرط را دارند؛ همه مضرب ۵‌اند، برای همین «قاعده‌ی پنج» نام گرفت:

| ویژگی | مرز |
| :--- | :--- |
| وزن مولکولی (MW) | ≤ ۵۰۰ دالتون |
| ‏cLogP (چربی‌دوستی) | ≤ ۵ |
| دهنده‌ی پیوند هیدروژنی (HBD) | ≤ ۵ |
| پذیرنده‌ی پیوند هیدروژنی (HBA) | ≤ ۱۰ |

بیش از یک تخلف = جذب خوراکی شاید بد باشد. این یک **قاعده‌ی سرانگشتی** است، نه قانون؛ به‌ویژه برای **فراورده‌های طبیعی** (مانند ریفامایسین‌ها) و داروهایی که با ناقل جذب می‌شوند.

### ۲.۴ شباهت مولکولی

یک **fingerprint** (اثر انگشت) مولکول را به یک رشته‌ی بیت بدل می‌کند: هر بیت = بودن یا نبودن یک تکه‌ی کوچک ساختار. ‏**Morgan fingerprint** (همان ECFP) تکه‌ها را از هر اتم تا شعاع معینی (این‌جا ۲ پیوند) می‌سازد. **ضریب Tanimoto** = (بیت‌های روشن مشترک) ÷ (بیت‌های روشن در هر کدام)، از ۰ (هیچ شباهت) تا ۱ (یکسان). **تشبیه:** دو کیسه‌ی تکه‌های لگو؛ Tanimoto می‌گوید چند درصد تکه‌ها در هر دو کیسه هست.

> 📺 **فیلم:** *Chemistry with Python – an Introduction to RDKit*: https://youtube.com/watch?v=9Z9XM9xamDU · *Molecular Strings and Fingerprints (RDKit tutorial)*: https://www.youtube.com/watch?v=kBk8HbjWwCw
> 📄 **مرجع:** Weininger D (1988). *SMILES, a chemical language and information system.* Journal of Chemical Information and Computer Sciences 28:31–36. https://doi.org/10.1021/ci00057a005 · Lipinski CA, Lombardo F, Dominy BW, Feeney PJ (2001). *Experimental and computational approaches to estimate solubility and permeability in drug discovery and development settings.* Advanced Drug Delivery Reviews 46:3–26. https://doi.org/10.1016/S0169-409X(00)00129-0

---

## ۳. گام ۱: گرفتن ساختارها از PubChem

‏PUG REST نشانی‌ای با این بخش‌ها دارد: `.../compound/name/<نام>/property/<ویژگی‌ها>/<قالب>`. برای هر دارو یک درخواست می‌فرستیم و نتیجه را در یک CSV جمع می‌کنیم. افزون بر پنج ریفامایسین، سه آنتی‌بیوتیک دیگر را هم برای سنجش برمی‌داریم.

<div dir="ltr">

```bash
PUG=https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name
echo "name,CID,SMILES,MolecularFormula" > rif.csv
for n in rifampicin rifabutin rifapentine rifaximin "rifamycin SV" ciprofloxacin trimethoprim ampicillin; do
  q=${n// /%20}
  curl -s "$PUG/$q/property/SMILES,MolecularFormula/CSV" | tail -n +2 | sed "s/^/\"$n\",/" >> rif.csv
  sleep 0.3
done
cut -c1-70 rif.csv
```

</div>

**تکه‌به‌تکه:**

| بخش | کار |
| :--- | :--- |
| ‏`q=${n// /%20}` | جای فاصله را در نام با `%20` پر می‌کند، چون نشانی وب فاصله نمی‌پذیرد («rifamycin SV») |
| ‏`property/SMILES,MolecularFormula/CSV` | دو ویژگی، در قالب CSV؛ PubChem خودش ستون `CID` را هم می‌افزاید |
| ‏`tail -n +2` | سطر نام ستون‌های PubChem را برمی‌دارد |
| ‏`sed "s/^/\"$n\",/"` | نام دارو را در آغاز سطر می‌گذارد |
| ‏`sleep 0.3` | میان درخواست‌ها کمی درنگ؛ PubChem بیش از ۵ درخواست در ثانیه را نمی‌پذیرد |

**خروجی واقعی** (هر سطر تا ۷۰ نویسه بریده شده):

<div dir="ltr">

```
name,CID,SMILES,MolecularFormula
"rifampicin",135398735,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(=C2O)C(=C(C
"rifabutin",135415564,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C3=C(C4=C(C(=C3O)C)
"rifapentine",135403821,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C(=C3C(=C2O)C(=C(
"rifaximin",6436173,"C[C@H]1/C=C/C=C(\C(=O)NC2=C(C3=C(C4=C(C(=C3O)C)O[
"rifamycin SV",6324616,"C[C@H]1/C=C/C=C(\C(=O)NC2=CC(=C3C(=C2O)C(=C(C4
"ciprofloxacin",2764,"C1CC1N2C=C(C(=O)C3=CC(=C(C=C32)N4CCNCC4)F)C(=O)O
"trimethoprim",5578,"COC1=CC(=CC(=C1OC)OC)CC2=CN=C(N=C2N)N","C14H18N4O
"ampicillin",6249,"CC1([C@@H](N2[C@H](S1)[C@@H](C2=O)NC(=O)[C@@H](C3=C
```

</div>

**توضیح خروجی:** هر پنج ریفامایسین با یک تکه‌ی یکسان آغاز می‌شوند (`C[C@H]1/C=C/C=C(\C(=O)N...`): همان حلقه‌ی بزرگ ansa. ‏SMILES ریفامپیسین ۱۶۴ نویسه است؛ ‏SMILES سیپروفلوکساسین ۴۸. فرمول ریفامپیسین C₄₃H₅₈N₄O₁₂ است، همان ۵۹ اتم سنگینی که در بلور دیدیم.

> 📺 **فیلم:** *Autodock molecular docking* (فهرست پخش؛ بخشی از آن کار با PubChem است): https://www.youtube.com/playlist?list=PLs_nni5HZu9aPJ8ATT2lD4wmpNi1lz9R2
> 📄 **مرجع:** Kim S, et al. (2023). *PubChem 2023 update.* Nucleic Acids Research 51:D1373–D1380. https://doi.org/10.1093/nar/gkac956 · راهنمای PUG REST: https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest

---

## ۴. گام ۲: سازوکار و وضعیت بالینی از ChEMBL

<div dir="ltr">

```bash
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule.json?pref_name__iexact=rifampin" | python3 -c "
import sys, json
m = json.load(sys.stdin)['molecules'][0]
print(m['molecule_chembl_id'], m['pref_name'], 'max_phase', m['max_phase'], 'first_approval', m['first_approval'], 'ATC', m['atc_classifications'], 'oral', m['oral'])
p = m['molecule_properties']
print({k: p[k] for k in ['full_mwt', 'alogp', 'hbd', 'hba', 'rtb', 'psa', 'num_ro5_violations']})"
curl -s "https://www.ebi.ac.uk/chembl/api/data/mechanism.json?molecule_chembl_id=CHEMBL374478" | python3 -c "
import sys, json
for x in json.load(sys.stdin)['mechanisms']:
    print(x['mechanism_of_action'], x['target_chembl_id'], x['action_type'])"
```

</div>

‏ChEMBL نام آمریکایی **rifampin** را به کار می‌برد. پاسخ JSON است و با ماژول `json` پایتون (بخش ۰۳) خوانده می‌شود.

**خروجی واقعی** (پاسخ ChEMBL چند ثانیه طول می‌کشد):

<div dir="ltr">

```
CHEMBL374478 RIFAMPIN max_phase 4.0 first_approval 1971 ATC ['J04AB02'] oral True
{'full_mwt': '822.95', 'alogp': '4.34', 'hbd': 6, 'hba': 15, 'rtb': 4, 'psa': '220.15', 'num_ro5_violations': 3}
Bacterial DNA-directed RNA polymerase inhibitor CHEMBL2364672 INHIBITOR
```

</div>

**توضیح خروجی:** ‏`max_phase 4` یعنی داروی تأییدشده؛ نخستین تأیید ۱۹۷۱؛ ‏ATC ‏`J04AB02` یعنی «آنتی‌بیوتیک ضد سل»؛ ‏`oral True` یعنی خوراکی. سازوکار: **مهارکننده‌ی RNA پلیمراز باکتری**، همان چیزی که در ماژول ۰۱ دیدیم. **سه تخلف از قاعده‌ی پنج**، ولی داروی خوراکی است.

> 📄 **مرجع:** Zdrazil B, et al. (2024). *The ChEMBL Database in 2023: a drug discovery platform spanning multiple bioactivity data types and time periods.* Nucleic Acids Research 52:D1180–D1192. https://doi.org/10.1093/nar/gkad1004 · ChEMBL web services: https://chembl.gitbook.io/chembl-interface-documentation/web-services

---

## ۵. گام ۳: دارو-مانندی و شباهت با RDKit

‏**RDKit** پرکاربردترین کتابخانه‌ی آزاد شیمی‌انفورماتیک در پایتون است. اسکریپت `mol_props.py` برای هر مولکول CSV:
- وزن، cLogP (روش Crippen)، HBD، HBA، پیوندهای چرخان (RotB) و **TPSA** (مساحت سطح قطبی) را حساب می‌کند،
- تخلف‌های قاعده‌ی پنج را می‌شمارد،
- ‏Tanimoto را با Morgan fingerprint (شعاع ۲، ‏۲۰۴۸ بیت) نسبت به یک مولکول مرجع می‌سنجد،
- و (اگر نام فایل سوم را بدهید) برای هر مولکول یک ساختار **سه‌بعدی** می‌سازد (ETKDG، سپس بهینه‌سازی با میدان نیروی MMFF) که در ماژول ۰۳ به کار می‌آید.

<div dir="ltr">

```bash
python3 $P/02_Small_Molecules/scripts/mol_props.py rif.csv rifampicin rif3d.sdf | column -t -s$'\t'
```

</div>

**خروجی واقعی:**

<div dir="ltr">

```
name           MW     cLogP  HBD  HBA  RotB  TPSA   Ro5_violations  Tanimoto_to_rifampicin
rifampicin     823.0  4.34   6    15   4     220.1  3               1.00
rifabutin      847.0  4.75   5    14   4     209.0  2               0.66
rifapentine    877.0  5.65   6    15   5     220.1  4               0.87
rifaximin      785.9  6.16   5    12   2     198.4  3               0.65
rifamycin SV   697.8  4.75   6    12   2     201.3  3               0.70
ciprofloxacin  331.3  1.58   2    4    3     74.6   0               0.09
trimethoprim   290.3  1.26   2    7    5     105.5  0               0.05
ampicillin     349.4  0.32   3    5    4     112.7  0               0.10
```

</div>

**توضیح خروجی:**

1. **همه‌ی ریفامایسین‌ها ۲ تا ۴ تخلف دارند** (وزن بالای ۷۰۰، HBA بالای ۱۰، و برای برخی cLogP بالای ۵). سه آنتی‌بیوتیک دیگر هیچ تخلفی ندارند. ریفامپیسین، ریفابوتین و ریفاپنتین با این همه خوراکی‌اند: نمونه‌ی خوب **«فراسوی قاعده‌ی پنج»** (beyond Rule of 5). مولکول‌های بزرگ و انعطاف‌پذیر گاهی پیوندهای هیدروژنی درونی می‌سازند و سطح قطبی خود را از غشا پنهان می‌کنند. ریفاکسیمین برعکس، عمداً از روده **جذب نمی‌شود** و برای عفونت‌های روده به کار می‌رود.
2. **عددهای RDKit با ChEMBL یکی‌اند** (وزن ۸۲۳٫۰ در برابر ۸۲۲٫۹۵، cLogP ‏۴٫۳۴، HBD ‏۶، HBA ‏۱۵، RotB ‏۴، ‏TPSA ‏۲۲۰٫۱، تخلف ۳). دو ابزار مستقل یک نتیجه دادند.
3. **شباهت:** ریفاپنتین (۰٫۸۷) نزدیک‌ترین است؛ تنها گروه متیل روی پیپرازین را با یک حلقه‌ی سیکلوپنتیل عوض کرده. ریفابوتین و ریفاکسیمین (۰٫۶۵ تا ۰٫۶۶) حلقه‌ی دیگری به هسته افزوده‌اند. سه داروی دیگر (۰٫۰۵ تا ۰٫۱۰) هیچ شباهتی ندارند؛ هدف‌های دیگری هم دارند.
4. ‏**RotB تنها ۴** برای مولکولی به این بزرگی: بیشتر پیوندهای ریفامپیسین درون **حلقه‌ی بزرگ**‌اند و RDKit پیوندهای حلقه را چرخان نمی‌شمارد. این در داکینگ (ماژول ۰۳) مهم می‌شود.

<details>
<summary>✋ امتحان کن: چرا Tanimoto ریفاپنتین با ریفامپیسین ۰٫۸۷ است و نه ۱، در حالی که تنها یک گروه فرق دارد؟</summary>

چون Morgan fingerprint با شعاع ۲، هر اتم را با همسایه‌هایش تا دو پیوند دورتر می‌بیند. عوض شدن متیل با سیکلوپنتیل، تکه‌های تازه‌ای می‌سازد (اتم‌های حلقه‌ی پنج‌تایی) و چند تکه‌ی پیرامون نیتروژن پیپرازین را هم تغییر می‌دهد. پس چند بیت روشن یا خاموش می‌شوند و مخرج Tanimoto بزرگ‌تر می‌شود.

</details>

‏**ZINC (از مستندات):** برای غربالگری مجازی (داکینگ هزاران یا میلیون‌ها ترکیب)، **ZINC-22** ترکیب‌های خریدنی را با ساختار سه‌بعدی و پروتونه‌شده (در pH معین) آماده دارد؛ ابزار جست‌وجوی وب آن **CartBlanche** است (https://cartblanche22.docking.org). سایت ZINC در 2026-10-24 از سرور ما پاسخ نداد؛ برای همین در این درس با PubChem کار کردیم.

> 📺 **فیلم:** *RDKit Lecture: Reading Molecules [SDF Files]*: https://www.youtube.com/watch?v=0vjqVxYTge8
> 📄 **مرجع:** RDKit: https://www.rdkit.org/docs · Rogers D, Hahn M (2010). *Extended-connectivity fingerprints.* Journal of Chemical Information and Modeling 50:742–754. https://doi.org/10.1021/ci100050t · Doak BC, Over B, Giordanetto F, Kihlberg J (2014). *Oral druggable space beyond the rule of 5: insights from drugs and clinical candidates.* Chemistry & Biology 21:1115–1142. https://doi.org/10.1016/j.chembiol.2014.08.013 · Tingle BI, et al. (2023). *ZINC-22 — a free multi-billion-scale database of tangible compounds for ligand discovery.* J Chem Inf Model 63:1166–1176. https://doi.org/10.1021/acs.jcim.2c01253

---

## ۶. سه اشتباه رایج

1. **کنار گذاشتن یک ترکیب تنها به خاطر قاعده‌ی پنج.** ریفامپیسین سه تخلف دارد و یکی از مهم‌ترین داروهای جهان است. قاعده برای غربال اولیه‌ی ترکیب‌های **سنتزی** ساخته شده.
2. ‏**SMILES بی فضاآرایی.** ریفامپیسین ۹ مرکز کایرال و چند پیوند دوگانه‌ی cis/trans دارد (تمرین ۴)؛ اگر `@` و `/` را بیندازید، مولکول دیگری را داک می‌کنید.
3. **یکی گرفتن «شبیه» با «همان فعالیت».** دو مولکول با Tanimoto ‏۰٫۶۵ شاید فعالیت بسیار متفاوتی داشته باشند (activity cliff)، و دو مولکول با ساختار متفاوت شاید یک هدف را مهار کنند.

---

## 📘 برای کنجکاوها

- ‏RDKit مولکول‌ها را می‌کشد: `from rdkit.Chem import Draw; Draw.MolToFile(mol, 'rif.png')`.
- ‏PubChem برای هر ترکیب ساختار سه‌بعدی هم دارد (`/record/SDF?record_type=3d`)، ولی برای مولکول‌های بسیار انعطاف‌پذیر یا بزرگ گاهی نه.
- ‏**QED** (Quantitative Estimate of Drug-likeness) یک عدد پیوسته‌ی ۰ تا ۱ به جای شمردن تخلف‌هاست: `from rdkit.Chem import QED`.

---

## جمع‌بندی

- ‏SMILES مولکول را در یک سطر می‌نویسد؛ SDF مختصات دارد؛ PDBQT برای Vina است.
- ‏PubChem (ساختار، CID)، ChEMBL (فعالیت، سازوکار، وضعیت بالینی) و ZINC (ترکیب‌های خریدنی سه‌بعدی) سه پایگاه اصلی‌اند.
- ریفامایسین‌ها ۲ تا ۴ تخلف از قاعده‌ی پنج دارند ولی چندتایشان خوراکی‌اند؛ RDKit و ChEMBL عددهای یکسان دادند.
- ‏Tanimoto روی Morgan fingerprint: ریفاپنتین ۰٫۸۷، دیگر آنتی‌بیوتیک‌ها کمتر از ۰٫۱.

---

## کارت دستورهای این درس

<div dir="ltr">

```bash
curl -s "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/NAME/property/SMILES,MolecularFormula/CSV"
curl -s "https://www.ebi.ac.uk/chembl/api/data/molecule.json?pref_name__iexact=NAME"
python3 mol_props.py compounds.csv REFERENCE out3d.sdf
```

</div>

---

## واژه‌نامه‌ی درس

| واژه | معنا |
| :--- | :--- |
| ‏SMILES | نوشتن ساختار مولکول در یک سطر متن |
| ‏SDF / MOL2 / PDBQT | قالب‌های فایل مولکول با مختصات |
| ‏CID | شناسه‌ی ترکیب در PubChem |
| فضاآرایی (stereochemistry) | آرایش فضایی اتم‌ها؛ ایزومرهای آینه‌ای و cis/trans |
| قاعده‌ی پنج Lipinski | چهار مرز ساده برای دارو-مانندی خوراکی |
| ‏cLogP | لگاریتم ضریب توزیع اکتانول/آب، برآوردشده؛ معیار چربی‌دوستی |
| ‏TPSA | مساحت سطح قطبی مولکول |
| ‏fingerprint | نمایش مولکول با رشته‌ای از بیت‌ها |
| ضریب Tanimoto | شباهت دو fingerprint، از ۰ تا ۱ |
| فراورده‌ی طبیعی | ترکیبی که یک موجود زنده می‌سازد (ریفامایسین از باکتری *Amycolatopsis*) |

---

## منابع

**مقاله و مستند**
- Weininger D (1988). *SMILES.* J Chem Inf Comput Sci 28:31–36. https://doi.org/10.1021/ci00057a005
- Lipinski CA, et al. (2001). Adv Drug Deliv Rev 46:3–26. https://doi.org/10.1016/S0169-409X(00)00129-0
- Doak BC, et al. (2014). *Oral druggable space beyond the rule of 5.* Chem Biol 21:1115–1142. https://doi.org/10.1016/j.chembiol.2014.08.013
- Rogers D, Hahn M (2010). *Extended-connectivity fingerprints.* J Chem Inf Model 50:742–754. https://doi.org/10.1021/ci100050t
- Kim S, et al. (2023). *PubChem 2023 update.* Nucleic Acids Res 51:D1373–D1380. https://doi.org/10.1093/nar/gkac956
- Zdrazil B, et al. (2024). *The ChEMBL Database in 2023.* Nucleic Acids Res 52:D1180–D1192. https://doi.org/10.1093/nar/gkad1004
- Tingle BI, et al. (2023). *ZINC-22.* J Chem Inf Model 63:1166–1176. https://doi.org/10.1021/acs.jcim.2c01253
- RDKit documentation: https://www.rdkit.org/docs

**کتاب**
- ‏Leach AR, Gillet VJ (2007). *An Introduction to Chemoinformatics*, revised ed. Springer. (فصل‌های نمایش مولکول، توصیفگرها و شباهت)
- ‏Leach AR (2001). *Molecular Modelling: Principles and Applications*, 2nd ed. Pearson. (فصل طراحی دارو)

**فیلم و دوره‌ی آموزشی**
- ‏Coursera: *Drug Discovery* (UC San Diego): https://www.coursera.org/learn/drug-discovery
- ‏edX: *Introduction to Drug Discovery* (EPFLx؛ روش‌های ligand-based): https://www.edx.org/learn/biology-life-sciences/ecole-polytechnique-federale-de-lausanne-introduction-to-drug-discovery
- ‏edX: *Medicinal Chemistry: The Molecular Basis of Drug Discovery* (Davidson College): https://www.edx.org/learn/medicine/davidson-college-medicinal-chemistry-the-molecular-basis-of-drug-di
- ‏YouTube: *Chemistry with Python – an Introduction to RDKit*: https://youtube.com/watch?v=9Z9XM9xamDU
- ‏YouTube: *Molecular Strings and Fingerprints (RDKit tutorial)*: https://www.youtube.com/watch?v=kBk8HbjWwCw
- ‏YouTube: *RDKit Lecture: Reading Molecules [SDF Files]*: https://www.youtube.com/watch?v=0vjqVxYTge8

<sub>داده‌های PubChem و ChEMBL در 2026-10-24 گرفته شدند. نشانی‌های فیلم از جست‌وجوی وب‌اند و در وارسی پایان دوره سنجیده می‌شوند.</sub>

</div>
