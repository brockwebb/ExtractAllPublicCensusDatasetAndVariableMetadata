# Extract All Public Census Dataset and Variable Metadata
- Script to generate data files containing the metadata of every dataset and table that is available on census.gov
- Some of the smaller data files are available in the data directory
- The full dataset (~900MB extracted) is available here: [CensusPublicMetadata](https://drive.google.com/file/d/1_0rXMtejU4e9XrqBOpZVFemQPIaI93RO/view?usp=sharing)

# Motivations for this
My goal is to see if I can:
1. create a knowledgegraph
2. train an LLM / graphRAG
3. make Census data more accessible to answer questions via natural language
4. Allow LLMs to write more accurate code/do analysis 

# Notes
- due to the number of variables (in the 3+ million range?) I broke up the files by decade
- About 3k variables wouldn't resolve, and got put into the unknown file... not bad though
- I used AI -- GPT 40, GPT 4o-1, Claude, and Gemini back and forth as I worked out issues
- There is a lot of logging and error handling... this was not an easy case, and there's a chance things still aren't perfect... such is life
