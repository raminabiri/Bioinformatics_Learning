#!/usr/bin/env bash
# "Gene tour": follow one gene (E. coli K-12 rpoB) across major public databases
# using only their official command-line tools / REST APIs.
# Requires: curl, jq, datasets (NCBI Datasets CLI).
# Usage: bash gene_tour.sh [GENE] [TAXID] ["PUBMED TERM"]
# Note: the UniProt/KEGG steps are fixed to E. coli K-12 (UniProt organism 83333, KEGG "eco").
set -euo pipefail
GENE=${1:-rpoB}
TAXID=${2:-511145}   # Escherichia coli str. K-12 substr. MG1655
TERM=${3:-"rifampicin resistance"}
TERM_Q=${TERM// /+}

echo "== 1. NCBI Taxonomy"
datasets summary taxonomy taxon "$TAXID" --as-json-lines \
  | jq -r '.taxonomy | "taxid=\(.tax_id)  name=\(.current_scientific_name.name)"'

echo "== 2. NCBI Genome (reference assembly)"
datasets summary genome taxon "$TAXID" --reference --as-json-lines \
  | jq -r '"\(.accession)  \(.assembly_info.assembly_level)  length=\(.assembly_stats.total_sequence_length)  GC=\(.assembly_stats.gc_percent)%  genes=\(.annotation_info.stats.gene_counts.total)"'

echo "== 3. NCBI Gene"
datasets summary gene symbol "$GENE" --taxon "$TAXID" --as-json-lines \
  | jq -r '"GeneID=\(.gene_id)  symbol=\(.symbol)  locus_tag=\(.locus_tag)  \(.description)"'

echo "== 4. UniProtKB (reviewed / Swiss-Prot)"
UP_TSV=$(curl -s "https://rest.uniprot.org/uniprotkb/search?query=gene_exact:${GENE}+AND+organism_id:83333+AND+reviewed:true&fields=accession,length,protein_name,ec&format=tsv")
echo "$UP_TSV"
UNIPROT=$(echo "$UP_TSV" | awk -F'\t' 'NR==2{print $1}')

echo "== 5. KEGG (via UniProt cross-reference)"
KEGG=$(curl -s "https://rest.uniprot.org/uniprotkb/${UNIPROT}.json" | jq -r '.uniProtKBCrossReferences[] | select(.database=="KEGG") | .id' | grep '^eco:' | head -1)
curl -s "https://rest.kegg.jp/get/${KEGG}" | grep -E '^(ENTRY|ORTHOLOGY|PATHWAY)'

echo "== 6. AlphaFold DB"
curl -s "https://alphafold.ebi.ac.uk/api/prediction/${UNIPROT}" \
  | jq -r '.[0] | "model=\(.entryId)  mean_pLDDT=\(.globalMetricValue)"'

echo "== 7. PDB (experimental structures that contain this UniProt sequence)"
Q='{"query":{"type":"terminal","service":"text","parameters":{"attribute":"rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession","operator":"exact_match","value":"'"$UNIPROT"'"}},"return_type":"entry"}'
curl -s -X POST https://search.rcsb.org/rcsbsearch/v2/query -H 'Content-Type: application/json' -d "$Q" \
  | jq -r '"entries=\(.total_count)  first: \([.result_set[:5][].identifier] | join(", "))"'

echo "== 8. PubMed (literature)"
curl -s "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term=${GENE}+AND+${TERM_Q}&retmode=json" \
  | jq -r '"PubMed hits for \"'"$GENE AND $TERM"'\": \(.esearchresult.count)"'

echo "Run date: $(date +%F)"
