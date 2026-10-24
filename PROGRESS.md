# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

## 1. Current goal
Rewrite the course part by part in the new step-by-step format (STYLE_GUIDE.md; memory: deep-explanation-style): dissect every command, real outputs only, strict prerequisites (nothing used before taught), exercises with a hint under each title + detailed solutions, refs (docs + Coursera + edX + YouTube), RTL. User says "ادامه" to continue. Commit+push every 3 modules.
**Now (2026-10-24):** part 08 COMPLETE (4 modules) and pushed. Next: part 09 = intro + a little practical (PDB/AlphaFold DB, small Vina docking, MD concepts as an entry to MD), written in a few weeks; then the two separate expert courses (structural bioinformatics, NGS + 3rd-gen; user has an expert reviewer). Part 10 → course v2. See memory course-roadmap-2026-10.
**Rules from user (2026-10-24):** run only commands needing < 1 GB RAM, otherwise code-only; word ضراوت → بیماری‌زایی (added to STYLE_GUIDE §8, replaced course-wide); a video URL + reference URL (📺/📄 lines) under EVERY technique section, plus the end-of-lesson list.

## 2. Done so far
- ✅ 00 Orientation, 01 Linux (10 modules), 02 BioLinux (5), 03 Python (6) — new format, pushed (b5afb1b and earlier).
- ✅ **04_R_Packages** (2026-10-20, pushed 87c221b). User decision: R language + statistics = SEPARATE course; no R/RStudio install lessons. Modules: 01_Install_Packages · 02_Run_Rscript · 03_Bioc_Examples (DESeq2 on simulated E. coli counts, seed 42, TP 88/FP 5/FN 12; vegan; ggtree woodmouse) · 04_R_in_Pipelines (run_all.sh, set -e, logs).
- ✅ **05_Reproducible_Work** (2026-10-21, pushed): 01_Git_Basics · 02_Git_Branches_GitHub (local bare repo as fake GitHub) · 03_Snakemake_First (count reads per accession = ground_truth.tsv) · 04_Snakemake_Pipeline (config.yaml, params/log, Python+R scripts, merge, check_truth; 7 exercises all run for real in scratchpad `p4/` and `doctor/`).
  - Real Snakemake 9 behavior found: inputs < 1 MB are checksummed (`--max-checksum-file-size`, default 1MB), so `touch names.tsv` triggers nothing; FASTQ (~3 MB) still follows mtime. Lesson 04 table + exercise 1 explain it.
  - `diversity.R` (part 04) silently treats any level ≠ genus as organism; exercise 04/4 teaches a `sys.exit` config check in the Snakefile instead of changing the part-04 script.
- ✅ **06_Metagenomics** (2026-10-21, pushed): rewritten in new format WITHOUT new runs; all outputs reused from the 2026-10-12..15 runs (work/ folder, gitignored) and verified by reading those files. Project layout for learners: ~/meta/{raw,qc,host,profile} (modules 01-03), ~/amplicon (module 04). Scripts moved to 06_Metagenomics/99_scripts_data/<module>/; shared data tables in 99_scripts_data/data. New env file envs/metagenomics.yml (not solved online). jq removed (not taught): fastp JSON read with Python json; DB build takes taxid from practice_db_genomes.tsv (verified identical to assembly reports). 06/01 has a Snakefile (workflow/) — not dry-run (no running); same structure as the 12-job workflow run on 2026-10-14. Module 03 and 04 split into 2 lessons each.
- ✍️ **07_Bacterial_Genomics** (2026-10-21, pushed): all 5 modules in new format, NOTHING run (user: no code, don't touch genomepipe/genomepipe_tools; removed the old `export PATH=…genomepipe_tools` line). 01 split into 2 lessons; 02 kept 3 lessons (restructured), files renamed 05_exercises/06_solutions; 03 MLST, 04 Panaroo, 05 Snippy written new from official docs (mlst README, Panaroo repo docs/, Snippy README fetched 2026-10-21); exercise tables labelled فرضی. ST10 (10-11-4-8-8-8-2) and ST131 (53-40-47-13-36-28-29) profiles verified via PubMLST REST API. Project folder ~/genomes; scripts in 07_Bacterial_Genomics/99_scripts_data/<module>/scripts (annotation scripts now write ./annotation and find part-01 data relative to the script). New envs/bacterial_genomics.yml (light tools; not solved online).
- ✅ **08_AMR_Virulence_Phylogeny** (2026-10-24, pushed). Rule: run only if < 1 GB RAM. All data = known-answer simulations on K-12 (part 01) or real public sequences; scripts in 08/99_scripts_data/<module>/scripts, small FASTA in 08/99_scripts_data/data. Real runs in scratchpad p08/{amr,phylo}.
  - 01 AMR: make_mock_isolates.py → isoA (gyrA S83L + pA blaCTX-M-15), isoB (parC S80I + pB blaNDM-1 + tet(A) 600 bp), isoC (K-12). AMRFinderPlus 4.2.7/DB 2026-08-07.1 found exactly the truth (tet(A) PARTIALX 50.38%); ~80 s, 183 MB. Lesson 2 RGI/ABRicate doc-only.
  - 02 virulence (ضراوت→بیماری‌زایی): make_virulence_isolates.py → isoD (eae gamma, stx2a operon from NCBI X07865 phage 933W, ehxA), isoE (papC, sat, cnf1, iutA + CTX-M-15). stxtyper: STX2A COMPLETE. VFDB setA (ABRicate repo copy, commit e2064df; VFDB site timed out) via makeblastdb/blastn: K-12 = 65 VF genes; ehxA=hlyA naming; papC split into 3 HSPs (missed at 80% cov); -max_target_seqs 5 trap. amr_vir_heatmap.R (ggplot2). Kleborate scores from docs/source/kpsc_modules.rst.
  - 03 MGE/CRISPR: isoF = K-12 + real plasmid pEK499 (EU935739.1, efetch): 12 core AMR genes; PlasmidFinder (ABRicate repo copy, 488 seqs; defaults 90/60 from README) → IncFIA + IncFII; gene_context.py: catB3 truncated by IS26 (2 bp), blaTEM next to IS1 (2 bp), CTX-M-15 73 bp from IS26; class 1 integron int-dfrA17-aadA5-qacEΔ1-sul1. find_crispr.py: K-12 array1 12 spacers next to cas operon (I-E), array2 6 spacers (0 exact repeats). MOB-suite/MinCED doc-only.
  - 04 phylo: ctxm_alleles.fna (13 CTX-M + KLUC-1 + TEM-1) → MAFFT L-INS-i (878 cols) → nj_tree.R (ape, TN93, 100 boot, root(edgelabel=TRUE)); 5 CTX-M groups 100%, KLUC-1 with group 1 (78). simulate_outbreak.py (seed 2026, 100 kb, infinite sites; STa H1→H2, STb H3, 9 sporadic, H2-05 KPC by plasmid) → outbreak_tree.R (SNP matrix, NJ, ggtree+gheatmap); NJ recovers exact branch lengths; RF 4 only from polytomies. IQ-TREE 3.1.4/Gubbins doc-only (iqtree/iqtree3 commands; +ASC; UFBoot≥95, SH-aLRT≥80).
  - New envs/amr.yml, envs/phylo.yml (not solved online).
- Old part-05 content (Snakemake QC workflow with fastp/FastQC/bowtie2, old Git lesson) backed up in scratchpad `old_part05/` and in git history; reuse QC workflow when rewriting 06/01.

## 3. Files changed
- Part 05 committed with composition.R 4th arg, 04/02 lesson+solutions, envs/workflow.yml, READMEs. Untracked user files left alone: `Bioinformatics_Course_ColorCoded.xlsx`, `advanced.odt`.

## 4. Key decisions and rejected approaches
- Part 05 Snakemake uses ONLY taught tools (Bash, seqkit, Python, R scripts of part 04). Rejected old fastp/FastQC/bowtie2 workflow: those tools are taught in part 06 (prereq rule).
- R scripts called via `shell: "Rscript …"`, not `script:` — so part-04 scripts stay usable outside Snakemake.
- `[.]` instead of `\.` in Snakefile regex (Python SyntaxWarning `"\." is an invalid escape sequence`); no `head` after `zcat` in rules (pipefail → exit 141).
- Part 04 env `envs/r_packages.yml` pins >= versions (unpinned solve picked bioconductor-ggtree 1.2.12).
- File naming: README.md unnumbered; 01_lesson, 02_exercises, 03_solutions; scripts/data in `<part>/99_scripts_data/<module>/`.
- Never send user's email to external APIs; heavy jobs/downloads are not run (write + cite docs, label hypothetical).

## 5. Known bugs / caveats (exact messages)
- Server AMRFinderPlus DB lacked nucleotide BLAST index: `The BLAST database for AMR_DNA-Escherichia.fa was not found.` Fixed in a scratchpad COPY (`p08/amrdb`, makeblastdb on AMR_DNA-*.fa) and run with `-d`; miniforge install untouched.
- YouTube unreachable from server on 2026-10-24 (`curl` 000) → video URLs taken from WebSearch.
- Running ABRicate from a git clone (with downloaded Path::Tiny/any2fasta) was denied by the auto-mode classifier ("Code from External"); ABRicate/RGI stay doc-only. Defaults minid/mincov 80 read from bin/abricate v1.4.0.
- `diff`/`column` not taught in part 01: exercises use `sort | uniq -u`; `column -t -s$'\t'` introduced in 08/01 lesson 1. Command-line BLAST (makeblastdb/blastn) first taught in 08/02 lesson 2.
- ape `root()` moves bootstrap labels unless `edgelabel = TRUE`; new root gets label "Root" (blanked in nj_tree.R). NJ can give negative branch lengths (CTX-M-3: -0.00033), explained in 08/04 lesson 1.
- VFDB site (mgc.ac.cn) timed out from the server; data files taken from the ABRicate GitHub repo (data only; running ABRicate from source was denied).
- conda.anaconda.org unreachable from server: `Could not resolve host: conda.anaconda.org`. Env files only dry-run solved with the offline cache.
- `envs/workflow.yml` with strict priority: `package snakemake-minimal-9.25.2-pyhdfd78af_0 is excluded by strict repo priority`; solves with `CONDA_CHANNEL_PRIORITY=flexible` (documented in yml + 05/03 lesson). With python=3.13: `pulp … requires python_abi =3.14` (offline cache).
- `envs/r_packages.yml` offline: `nothing provides r-aplot needed by bioconductor-ggtree-4.0.4` (cache gap; r-aplot exists on conda-forge).
- System R uses bspm/r2u: `install.packages("vegan")` installed r-cran-vegan + r-cran-permute system-wide via apt (2026-10-20).
- Snakemake shell + `zcat … | head` → exit 141 (SIGPIPE under pipefail).
- `_tools/check_links.sh` sometimes `FAIL 000` for YouTube (timeouts); rerun.
- Coursera returns 451 from server; URLs taken from WebSearch index. Full link check deferred to course end (user's VPN).
- In my shell grep=ugrep, awk=gawk, find=bfs: use /usr/bin/grep and /usr/bin/mawk for lesson outputs.

## 6. Next steps (priority order)
1. Part 09 (in a few weeks, with the user): intro + a little practical only — PDB/AlphaFold DB, a small Vina docking, MD concepts as an entry point to MD.
2. Separate full courses, planned with the user before writing: (a) structural bioinformatics at professional level (theory + practice; the 1 GB rule does not apply; heavy runs planned separately; the user will introduce an expert reviewer); (b) NGS + third-generation sequencing, wet lab + bioinformatics (topics of 10/02–10/04 move here).
3. Part 10 (Advanced) is NOT written now; it becomes course version 2 (much more complete). Mark it "نسخه‌ی ۲" in README when the user agrees on wording.
4. Verify env files online (r_packages, workflow, metagenomics, bacterial_genomics, amr, phylo) when conda is reachable; dry-run the 06/01 Snakefile.
5. At course end: full link check with user's VPN (`_tools/check_links.sh`), incl. YouTube links of 07/03-05 and all of part 08 (taken from WebSearch on 2026-10-24, YouTube unreachable from server). Re-search a YouTube video on CRISPR bacterial immunity for 08/03 lesson 2 (now only PBS NOVA "How CRISPR Works in Nature", not on YouTube).
