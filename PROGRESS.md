# PROGRESS — Bioinformatics course (Persian, for biologists new to bioinformatics)

## 1. Current goal
Rewrite the course part by part in the new step-by-step format (STYLE_GUIDE.md; memory: deep-explanation-style): dissect every command, real outputs only, strict prerequisites (nothing used before taught), exercises with a hint under each title + detailed solutions, refs (docs + Coursera + edX + YouTube), RTL. User says "ادامه" to continue. Commit+push every 3 modules.
**Now:** parts 06 and 07 rewritten & pushed (2026-10-21). Next: part 08 (plan it with the user first).

## 2. Done so far
- ✅ 00 Orientation, 01 Linux (10 modules), 02 BioLinux (5), 03 Python (6) — new format, pushed (b5afb1b and earlier).
- ✅ **04_R_Packages** (2026-10-20, pushed 87c221b). User decision: R language + statistics = SEPARATE course; no R/RStudio install lessons. Modules: 01_Install_Packages · 02_Run_Rscript · 03_Bioc_Examples (DESeq2 on simulated E. coli counts, seed 42, TP 88/FP 5/FN 12; vegan; ggtree woodmouse) · 04_R_in_Pipelines (run_all.sh, set -e, logs).
- ✅ **05_Reproducible_Work** (2026-10-21, pushed): 01_Git_Basics · 02_Git_Branches_GitHub (local bare repo as fake GitHub) · 03_Snakemake_First (count reads per accession = ground_truth.tsv) · 04_Snakemake_Pipeline (config.yaml, params/log, Python+R scripts, merge, check_truth; 7 exercises all run for real in scratchpad `p4/` and `doctor/`).
  - Real Snakemake 9 behavior found: inputs < 1 MB are checksummed (`--max-checksum-file-size`, default 1MB), so `touch names.tsv` triggers nothing; FASTQ (~3 MB) still follows mtime. Lesson 04 table + exercise 1 explain it.
  - `diversity.R` (part 04) silently treats any level ≠ genus as organism; exercise 04/4 teaches a `sys.exit` config check in the Snakefile instead of changing the part-04 script.
- ✅ **06_Metagenomics** (2026-10-21, pushed): rewritten in new format WITHOUT new runs; all outputs reused from the 2026-10-12..15 runs (work/ folder, gitignored) and verified by reading those files. Project layout for learners: ~/meta/{raw,qc,host,profile} (modules 01-03), ~/amplicon (module 04). Scripts moved to 06_Metagenomics/99_scripts_data/<module>/; shared data tables in 99_scripts_data/data. New env file envs/metagenomics.yml (not solved online). jq removed (not taught): fastp JSON read with Python json; DB build takes taxid from practice_db_genomes.tsv (verified identical to assembly reports). 06/01 has a Snakefile (workflow/) — not dry-run (no running); same structure as the 12-job workflow run on 2026-10-14. Module 03 and 04 split into 2 lessons each.
- ✍️ **07_Bacterial_Genomics** (2026-10-21, pushed): all 5 modules in new format, NOTHING run (user: no code, don't touch genomepipe/genomepipe_tools; removed the old `export PATH=…genomepipe_tools` line). 01 split into 2 lessons; 02 kept 3 lessons (restructured), files renamed 05_exercises/06_solutions; 03 MLST, 04 Panaroo, 05 Snippy written new from official docs (mlst README, Panaroo repo docs/, Snippy README fetched 2026-10-21); exercise tables labelled فرضی. ST10 (10-11-4-8-8-8-2) and ST131 (53-40-47-13-36-28-29) profiles verified via PubMLST REST API. Project folder ~/genomes; scripts in 07_Bacterial_Genomics/99_scripts_data/<module>/scripts (annotation scripts now write ./annotation and find part-01 data relative to the script). New envs/bacterial_genomics.yml (light tools; not solved online).
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
- conda.anaconda.org unreachable from server: `Could not resolve host: conda.anaconda.org`. Env files only dry-run solved with the offline cache.
- `envs/workflow.yml` with strict priority: `package snakemake-minimal-9.25.2-pyhdfd78af_0 is excluded by strict repo priority`; solves with `CONDA_CHANNEL_PRIORITY=flexible` (documented in yml + 05/03 lesson). With python=3.13: `pulp … requires python_abi =3.14` (offline cache).
- `envs/r_packages.yml` offline: `nothing provides r-aplot needed by bioconductor-ggtree-4.0.4` (cache gap; r-aplot exists on conda-forge).
- System R uses bspm/r2u: `install.packages("vegan")` installed r-cran-vegan + r-cran-permute system-wide via apt (2026-10-20).
- Snakemake shell + `zcat … | head` → exit 141 (SIGPIPE under pipefail).
- `_tools/check_links.sh` sometimes `FAIL 000` for YouTube (timeouts); rerun.
- Coursera returns 451 from server; URLs taken from WebSearch index. Full link check deferred to course end (user's VPN).
- In my shell grep=ugrep, awk=gawk, find=bfs: use /usr/bin/grep and /usr/bin/mawk for lesson outputs.

## 6. Next steps (priority order)
1. Part 08 (AMR, virulence, phylogeny): agree a plan with the user (write-only like 07/03-05?), then write.
2. Parts 09, 10.
3. Verify env files online (r_packages, workflow, metagenomics, bacterial_genomics) when conda is reachable; dry-run the 06/01 Snakefile.
4. At course end: full link check with user's VPN (`_tools/check_links.sh`), incl. new YouTube links in 07/03-05.
