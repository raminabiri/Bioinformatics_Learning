# PROGRESS — Bioinformatics course (Persian, MSc/PhD level)

## 1. Current goal
(Status legend added 2026-10-15: ✍️ = written + commands checked against docs, heavy steps not run; STYLE_GUIDE §5.1.)
Rebuild the whole course to the standard in `STYLE_GUIDE.md`: every lesson tested on real course data with real outputs, exercises + detailed solutions, verified live references + videos at the end. Work part by part; user says "ادامه" to continue.
User rules: ask before heavy downloads (state what/size/time); course is introductory (practice data/DBs, and lessons must say real work needs the full DB).

## 2. Done so far (2026-10-14)
- ✅ **00_Orientation**: 01 Landscape, 02 Databases (+ `scripts/gene_tour.sh`, `scripts/project_summary.sh`).
- ✅ **01_Computing_Foundations**, all 5 modules rewritten and tested:
  - 01 Bash: E. coli data via `data/download.sh`, plus `scripts/fasta_stats.sh`.
  - 02 Conda: offline env test, plus `scripts/record_versions.sh`.
  - 03 Formats: `scripts/make_examples.sh` builds real FASTA/FASTQ/GFF/GB/BED/SAM/VCF and the wgsim truth file.
  - 04 Git: `scripts/git_demo.sh` with TZ-pinned dates, so hashes are reproducible.
  - 05 Workflows: `workflow/Snakefile`, `config.yaml`, `Snakefile_solution`.
- ✅ **03/01 Read QC** (`run_qc.sh`, `check.sh` 18/18).
- ✅ **03/02 Host removal** (wgsim spike-in, `make_spiked_sample.sh`, `run_host_removal.sh`, `check.sh` 8/8).
- 🟢 **03/03 Profiling**: Kraken2/Bracken with the PRACTICE DB (45 genomes) are tested; `evaluate_profile.py`; `check.sh` 4/4. The MetaPhlAn/HUMAnN section is intro only and untested.
- ✅ **02/01 Python/Biopython** (2026-10-14): lesson + 5 exercises + solutions; scripts `cds_table.py`, `gc_outliers.py`, `codon_usage.py`, `entrez_tour.py`. Fixed lesson error: `translate(table=11)` alone gives V for GTG starts; only `cds=True` gives M.
- ✅ **03/04 16S** (2026-10-15): lesson + 6 exercises + solutions + scripts, `check.sh` 14/14, links OK. Facts below kept for reference.
  - Done files: `README.md` (✅ text already written), `data/download.sh` (md5-checked, incl. SILVA V4 refs, user approved 20 MB), `scripts/{train_classifier.sh,run_16s.sh,check.sh}`. Outputs: `06_Metagenomics/work/04_16s/` (+ exploratory runs in `work/04_16s_explore/`, incl. `variants/`, `taxonomy-vsearch.qza`).
  - Env: `export PATH=/data/MicrobiomePipeline/qiime2_env/bin:$PATH` (QIIME 2 2026.7, framework "rachis", sklearn 1.7.1); `UNIFRAC_USE_GPU=N` needed (else `Accelerator Fatal Error … -acc=gpu` from `ssu`).
  - 2026.7 API changes: dada2 needs `--o-base-transition-stats`; `feature-table summarize` uses `--m-metadata-file` + `--o-feature-frequencies/--o-sample-frequencies/--o-summary`.
  - Old classifiers refused: `The scikit-learn version (1.4.2) used to generate this artifact does not match … (1.7.1)`. Species-level training hit 12.4 GB (killed: user's genomepipe H. pylori job shares RAM) → trained GENUS-level (67,689 → 8,415 classes; 8 min, 5.5 GB) = `data/db/silva-138-99-515-806-genus-nb.qza`.
  - Facts: demux 46,712/135,487 reads (34.5%) assigned; 60,234 unassigned have perfect barcodes (other studies on the run); 75 samples in metadata, 71 got reads (0–1,442). Quality: median Q33 at pos 1–11 vs 37–39 after; pos 151 median 25 → trim-left 13, trunc 150. Fragment 253 bp (vsearch merge 92%), overlap 47; trunc 120+120 → "No features remain".
  - DADA2 (trim13/trunc150): 46,712 → filt 41,834 → denoised 33,558 → merged 16,438 → nonchim 16,438; 414 ASVs, modal len 227. Low merge = low depth + 0 mismatch rule: mm2 19,871 (531 ASVs); pseudo 18,872 (466); pseudo+mm2 23,276 (739); trunc-r 130 19,672 (509); trunc 0 16,015 (386).
  - Taxonomy: NB genus 368/414 ASVs to genus (details still to extract); vsearch: 379 to genus, phyla Actinobacteriota 170, Proteobacteria 65, Chloroflexi 39, Acidobacteriota 28.
  - Diversity depth 150 seed 42 → 46/71 samples. Faith PD veg p=0.025 (H 5.01), Shannon veg p=0.036, observed p=0.13; transect all ns. UniFrac PERMANOVA veg F=3.77 p=0.001; transect F=1.57 p=0.058; Bray veg/transect p=0.001. PERMDISP veg p=0.842. Faith vs elevation Spearman 0.388 p=0.0077; vs pH −0.099 p=0.51. adonis elevation+vegetation: elevation R² 0.070 p=0.001, vegetation R² 0.030 p=0.092 → CONFOUNDING (vegetated sites all ≥2,687 m).
  - Videos verified live: QIIME 2 XIyZWpfcZ6U, PUsvtJgpNtE; Galaxy ISocxcJZEjw; Brown wV5_z7rR6yw; ISB ZFiZTZXhdJ4. Docs: amplicon-docs.qiime2.org/en/latest/, docs.qiime2.org/2024.10/tutorials/atacama-soils/.
- ✍️ **04/01 Assembly** (2026-10-15): lesson + 6 exercises (4 on labelled hypothetical data) + solutions + `scripts/repeat_report.py` (real: k-mer repeats 2.83% k21 / 1.79% k127; cutting at 7 rrn + 50 IS → 50 contigs, N50 173,810; IS alone N50 224,159, rRNA alone 2,497,193). SPAdes/Shovill/QUAST/CheckM2 NOT installed and not run; options checked against official READMEs/manuals. Links OK.
- ✍️ **04/02 Annotation** (2026-10-15): 3 lessons (prokaryote / phage+virus / eukaryote, per user: course is broad with microbial emphasis) + 7 exercises + solutions; scripts `light_annotation.sh`, `compare_genecalls.py`, `virus_demo.sh`, `yeast_demo.sh` (all light, real). Key real facts: Pyrodigal vs RefSeq E. coli 96.0% same stop, 230 start diffs, 171 missed (157 <100 aa), selenoproteins + dnaX slippage; barrnap 22/22 rRNA; tRNAscan 89 vs RefSeq 86 (extras = tRNA remnants at CP4-6/DLP12 borders + ssrA tmRNA); 12 cryptic prophages (GC 47.4%, 14% unknown vs 1.9%, 34/145 pseudogenes, integrases at borders); SARS-CoV-2: pp1ab missed, 284 nt of nsp12 uncovered, E/ORF7b/ORF10 missed; yeast chrI: 159 predicted vs 94 real, all 3 intron genes wrong. BRAKER3 is deprecated → BRAKER4 (Snakemake). PHROGs website unreachable from server (link removed). Not committed yet.
- ⚠️ **New rule (user, 2026-10-15):** we only teach — do NOT run heavy analyses/downloads ourselves. Write lessons completely and in detail. Light commands on existing small data are OK; heavy steps = commands + explanation, outputs only from cited official docs or clearly labelled as examples (never invented). Status for such modules: ✍️ نوشته‌شده. (The earlier approval to download isolate data for part 04 is no longer needed.)
- ⚪ Designed only (README with objectives and outline): 02/02, 02/03, 03/04 lesson, parts 04, 05, 06, 07.
- `_tools/`: `check_links.sh` (retries a 403 without the fake user-agent; sourceforge needs this) (YouTube oEmbed, Crossref, HTTP), `check_internal_links.py`, `yt_search.sh`.

## 3. Files changed (main)
- Root: `README.md` (roadmap + status), `STYLE_GUIDE.md`, `.gitignore`, `envs/bioinfo_course.yml`, `envs/README.md`, `_templates/module/*`, `_tools/*`.
- Every module folder follows: `README.md` + `01_lesson*.md`, `02_exercises.md`, `03_solutions.md` (+ `scripts/`).
- `06_Metagenomics/data/`: `download.sh` (incl. chr1 region), `ground_truth.tsv`, `ground_truth_species.tsv`, `README.md`.
- `06_Metagenomics/03_Taxonomic_Functional_Profiling/practice_db_genomes.tsv` + `scripts/{build_practice_db.sh,run_profile.sh,evaluate_profile.py,check.sh}`.
- `03_Python/02_Biopython/{01_lesson.md,scripts/cds_table.py}`.
- Removed: superseded `04_scripts.md` in 01/04 and 01/05 (the copy in 01/05 had the wrong content). Original course is in `/data/bioinformatics_learning_backup_2026-10-12.tar.gz`.
- Outside git (ignored): `work/`, `data/raw/`, `data/host/`, 01/01 `data/ecoli_k12.*`, 01/03 `data/`, 01/05 `results/ logs/ .snakemake/`.

## 4. Key decisions and rejected approaches
- **File naming:** `README.md` stays unnumbered so GitHub renders it; other files are `01_lesson`, `02_exercises`, `03_solutions` (user choice). Rejected `00_README.md` because GitHub would not render it.
- **Part order:** programming moved to 02, before the domain parts; Dify moved to 07/06.
- **Metagenomics data:** nf-core/test-datasets `mag` (simulated, known composition). Rejected the old data: SARS-CoV-2 amplicon mislabelled as gut (archived in `data/_archive_sarscov2_amplicon/`).
- **fastp:** `--cut_front --cut_tail`. Rejected `--cut_right`, which drops 10.8% of reads on minigut.
- **Host removal:** `samtools view -f 12 -F 256`. Rejected `--un-conc`, which leaks discordant pairs and single-mate pairs.
- **Kraken2:** custom practice DB (other strains + decoy species; Candida excluded on purpose). Rejected the Standard DB (8–80 GB; network ~150 KB/s).
- **Conda:** Miniforge + conda-forge > bioconda + strict, no `defaults` (Bioconda docs).
- **Tools:** conda.anaconda.org is unreachable, so tools were installed from official sources into `~/opt/course_tools/bin`:
  - fastqc, fastp, bowtie2, multiqc, kraken2, bracken
  - symlinks: seqkit, samtools, wgsim, bcftools, bgzip, tabix
- **Environments:**
  - Python: `genomepipe_tools` (Py 3.13, Bio 1.88, pandas 3.0.5, seaborn)
  - R: `deg_r` (R 4.6.1, ggplot2, dplyr, vegan); system R has DESeq2
  - Snakemake: `snakemake` (9.25.2)
  - QIIME 2 2026.7: `/data/MicrobiomePipeline/qiime2_env`
  - SILVA 138 and GG2 classifiers: `/data/MicrobiomePipeline/database/`

## 5. Known bugs / caveats (exact messages)
- `mamba env create -f envs/bioinfo_course.yml` fails: `Could not resolve host: conda.anaconda.org` / `SSL connect error … Operation too slow`.
- With `set -o pipefail`, `zcat … | head` exits **141** (SIGPIPE); fixed in `run_profile.sh` with `set +o pipefail` on that line.
- Snakemake 9.25.2: a deleted intermediate file, or a sample newly added to config, gives `Nothing to be done (all requested files are present and up to date).` while the final target is up to date. Request the file explicitly or use `--forcerun` (documented in 01/05).
- `datasets download genome accession --inputfile acc.txt` hangs at `Collecting 45 genome records … 0%`. Workaround: download one accession at a time (in `build_practice_db.sh`).
- `_tools/check_links.sh` sometimes reports `FAIL 000` for YouTube (timeouts); rerun gives 200.
- FastQC prints `application/gzip` lines; harmless.
- 85 empty `README.md` files inside `.git/` (pre-existing since 2026-10-04); untouched.
- Git: pushed 2026-10-15 as commit 3c7ead4 to origin/main (repo is PUBLIC). `advanced.odt` and `Bioinformatics_Course_ColorCoded.xlsx` deliberately left untracked (personal files, never tracked before). FIXED 2026-10-19: empty files `.git/refs/{,heads/,remotes/,tags/,remotes/origin/}README.md` made `git fetch` fail with `fatal: bad object refs/README.md`. They were moved (not deleted) to the session scratchpad. The user had pushed 270d160 (a web edit to old 00/01) on 2026-10-16; the batch-1 commit was rebased on it and pushed as 6834e1c.

- 🔁 **RESTRUCTURE (user-approved, 2026-10-19).** Strict prerequisite rule (STYLE_GUIDE §2.1): nothing is used before it is taught.
  - New parts: 00 Orientation (browser only) · 01_Linux · 02_BioLinux · 03_Python · 04_R_Statistics · 05_Reproducible_Work · 06_Metagenomics · 07_Bacterial_Genomics · 08_AMR_Virulence_Phylogeny · 09_Structural_Bioinformatics · 10_Advanced.
  - Old → new mapping:
    - 01_CF/01_Bash_Linux → 01_Linux/02_Bash
    - 01_CF/02 → 02_BioLinux/01_Conda_Bioconda
    - 01_CF/03 → 02_BioLinux/02_Bio_File_Formats
    - 00/02 lesson 2 + exercises 5–8 → 02_BioLinux/03_Data_Download
    - 02_PDA/01 → 03_Python/02_Biopython
    - 02_PDA/02 → 03_Python/03_Pandas
    - 02_PDA/03 → 04_R_Statistics/01_R_Stats
    - 01_CF/04 → 05_Reproducible_Work/01_Git_GitHub
    - 01_CF/05 → 05_Reproducible_Work/02_Workflows_Snakemake
    - 03..07 → 06..10
  - Scripts and data are in `<part>/99_scripts_data/<module>/`, because GitHub lists folders first. This is done for parts 00–05; parts 06/07 still keep `scripts/` inside each module, and these move when each module is rewritten.
  - New modules written:
    - 00/03_Web_Tools: ExPASy, Needle, Clustal Omega, BLAST, built on the RpoB RRDR story. Needle E. coli vs Mtb: 625/1451 (43.1%), score 2949.5. Biopython PairwiseAligner with BLOSUM62, gap 10/0.5, end gaps 0 reproduces Needle exactly. RRDR 507–533: 21/27 columns identical in 4 species; D516/H526/S531 conserved. Mtb UniProt S456 = clinical S450; S. aureus H481 ↔ E. coli H526.
    - 01_Linux/01_Setup_Computer: WSL/mac/Ubuntu/ssh, first commands, course ZIP via curl.
    - 03_Python/01_Python_Basics: README design only.
  - Bash data download now needs only curl. NCBI FTP + nf-core files have the same md5 as before. FASTQs are in `data/fastq`, with `R=fastq`, and ground_truth.tsv is copied into the Bash data folder.
  - Tools: `rename_paths.py` was one-off and was not committed (it is in the scratchpad).
  - Old-part refs ("بخش ۰۳"→"۰۶" etc.) were renumbered. Ambiguous refs to old parts ۰۱/۰۲ in not-yet-rewritten modules are still to be fixed at their rewrite.
  - Three decimals were wrongly changed by renumbering and were fixed (۴۰٫۰۵٪, ۰٫۰۴, ۱٫۰۵). All decimals in moved files were verified against HEAD.
  - ⚠️ I sent the user's email to the EBI REST API once (Needle job). Don't do this again; run tools locally or ask.
- ✅ **New-format rewrite, batch 1 (2026-10-19):**
  - 00/01, 00/02 (split into 01_lesson_browse + 02_lesson_download, 03_exercises, 04_solutions), and 01/01 Bash (split into 01_lesson_files, 02_lesson_text_tools, 03_lesson_scripts, 04_exercises, 05_solutions; new `scripts/count_reads.sh`).
  - All RTL-wrapped, Persian words applied, Coursera/edX/YouTube refs.
  - Tools added: `_tools/rtl_wrap.py` (idempotent; wraps file in div rtl and code fences in div ltr), `_tools/persian_words.py` (safe replacements + lists manual ones).
  - STYLE_GUIDE §1, §3, §4, §7 (RTL), §8 (word list) and checklist rewritten.
  - User rules: commit+push after every 3 modules. Technical/biological terms (بیوانفورماتیک، کامپیوتر، ژن، رید…) stay; معمولاً → در بسیاری از موارد.
  - Link facts: Coursera returns 451 from this server and from WebFetch, so its URLs are verified via WebSearch index. YouTube is unreachable 2026-10-19, so old oEmbed dates are kept. alphafold.ebi.ac.uk now gives 403 to curl/WebFetch. vincebuffalo.com timed out.
- 🔄 **FORMAT CHANGE (user, 2026-10-19):** user said lessons are not learnable (dense expert notes, jargon tables, test numbers, no intuition/examples). New audience: knows basic + molecular biology, NOT bioinformatics. New lesson format (pilot = 00/01, rewritten 2026-10-19): «در یک نگاه» goals → story (rifampicin-resistant E. coli, rpoB) → plain concepts + analogy → small worked example → «✋ امتحان کن» <details> boxes after each section → 3 common mistakes → «برای کنجکاوها» optional box → summary → glossary → refs. Exercises: strictly lesson-based, runnable (browser/calc), **راهنمایی right under each exercise title** (user request). Verification numbers go to solutions, not lesson body. WAITING for user feedback on pilot before updating STYLE_GUIDE §1/§3 and rewriting other lessons.

## 6. Next steps (priority order, one session each)
0. **Continue new-format rewrite, in course order, commit+push every 3 modules:** next 02_BioLinux/01_Conda_Bioconda, 02_BioLinux/02_Bio_File_Formats (its make_examples.sh depends on part-06 outputs, so fix the prerequisite), 03_Python/01_Python_Basics (new) → push; then 03_Python/02_Biopython, 03/03 Pandas (new), 04/01 R (new) → push; then 05/01 Git, 05/02 Snakemake (needs Python; workflow uses part-06 QC, so check the prerequisite), 06/01 → push; then 06/02–06/04, 07/01–07/02 (move scripts into 99_scripts_data and retest).
3. **04/03 MLST**, then 04/04 pan-genome, 04/05 Snippy — write-only per the new rule; for each topic add short non-bacterial sections where relevant (scope memory). Consider a short phage/virus/eukaryote note in 04/01 assembly.
4. **02/02 pandas:** fastp JSON, `cds_table.tsv`, Kraken vs truth plots.
5. **02/03 R/stats:** ggplot2, FDR simulation, vegan diversity on 16S output.
6. Then parts 05, 06, 07 (one module per session).
7. After each module: update the root `README.md` status table and run `_tools/check_links.sh` + `python3 _tools/check_internal_links.py`.
