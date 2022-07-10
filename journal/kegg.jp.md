# Notes on KEGG
These are notes on using the KEGG database and accompanying REST API.

- KEGG [REST API](https://www.kegg.jp/kegg/rest/keggapi.html) reference
- [This page](https://www.kegg.jp/pathway/cmos01110) shows secondary metabolic synthesis pathways for *Cucurbita Moschata*

## REST API examples
```bash
# Lists all organisms in the database
curl https://rest.kegg.jp/list/organism

# Shows the biosynthesis pathways in the database
curl https://rest.kegg.jp/list/pathway

# Grabs secondary metabolic synthesis pathways in the database
curl https://rest.kegg.jp/get/path01110

# Grabs secondary metabolic synthesis pathways for C. Moschata
curl https://rest.kegg.jp/get/cmos01110

# Grabs all metabolic synthesis pathways for C. Moschata
curl https://rest.kegg.jp/get/cmos01100
```

## API response structure
The REST API returns a series of paragraphs that are labeled.
The most common labels are `REL_PATHWAY`, `MODULE`, `COMPOUND`.
You want to traverse through the entries under `REL_PATHWAY` and `MODULE` to grab `COMPOUND` entries.
Those are names of pathway compounds, which are useful for Greenworld.