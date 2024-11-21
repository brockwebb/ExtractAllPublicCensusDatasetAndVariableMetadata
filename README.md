# WHY! 
> The purpose of this project is to democratize the use of all Public US Census Bureau data. The ability to ask questions in natural language and get an accurate response based on data would open up a whole new world of interest in using Census data, not to mention the evidence based decision making it could lead to. This could, in fact, expand and create a larger knowledgebase useing data from several statistical agencies (eg NCES, BLS, BEA, BJS, etc) to form a more robust and comprehensive view of the knowledge captured in our nations statistical data products.

# Notebooks
1. Extract All Public Census Dataset and Variable Metadata
  - Script to generate data files containing the metadata of every dataset and table that is available on census.gov
  - Some of the smaller data files are available in the data directory
2. Create KG
  - Programatically take the csv outputs from the extraction and build the KG
  - Modular to incorporate new survey data added to data.html
3. Enrich KG
  - Use LLMs to enrich the KG by using the rich metadata and relationships available
  - Create more concepts, increase the connectedness, discover hidden connections, improve use
     

# Motivations for this
My goal is to see if I can:
1. create a knowledgegraph
2. Create a hybrid-RAG application LLM RAG / graphRAG
3. make Census data more accessible to answer questions via natural language
4. Allow LLMs to write more accurate code/do analysis
5. Make Census data even more awesome!!! 

# Notes
- The first goal is to produce a set of tables that would locally mimic all the linkages and data that could be extracted from https://api.census.gov/data.html
- Once all the local CSV files are in place, we will programatically build the Knowledge Graph
- For modularity, if data.html was updated, we could just extract the difference, run it through the extractor, and add the additional nodes to the KG with the same methods (avoiding building the whole thing again)


# UPDATES
## 11/21/2024
- Realized that my initial extraction was problamatic and contained weird artifacts from attempted extraction from JSON
- Discovered a better file was available at https://api.census.gov/data.html ... this was created to be "machine readible" with all survey information.
- Starting over, I restructured everything more in line with best practices and a focus on modularity/reproducibility.
  
## 10/17/2024
- Added partially working graph rag using neo4j. [Census Public Metadat Graph RAG](https://github.com/brockwebb/ExtractAllPublicCensusDatasetAndVariableMetadata/blob/main/CensusPublicMetadataRAG.ipynb)
- Something isn't creating node relationships correctly...
- Requires installing neo4j, which isn't ideal (I started with graphRAG but gave up)
