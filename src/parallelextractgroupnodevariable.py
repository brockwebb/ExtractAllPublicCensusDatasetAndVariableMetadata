import os
import pandas as pd
import json
import requests
import logging
from multiprocessing import Pool, cpu_count, current_process
from tqdm import tqdm
from datetime import datetime
from functools import partial

# Global logger setup
def setup_logging(output_folder):
    log_file = os.path.join(output_folder, f'processing_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(processName)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

# Worker function must be at module level
def worker_function(args):
    chunk_file, output_folder = args
    logger = logging.getLogger(f'worker_{current_process().name}')
    
    try:
        base_url = "https://api.census.gov"
        session = requests.Session()
        session.headers.update({
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        })
        
        logger.info(f"Starting processing of {chunk_file}")
        
        # Load the chunk
        df = pd.read_csv(chunk_file)
        
        # Rename and prepare columns
        df.rename(columns={'Name': 'Variable Name'}, inplace=True)
        
        # Create output paths
        os.makedirs(output_folder, exist_ok=True)
        chunk_name = os.path.splitext(os.path.basename(chunk_file))[0]
        output_file = os.path.join(output_folder, f"Processed_{chunk_name}.csv")
        error_log_file = os.path.join(output_folder, f"Errors_{chunk_name}.csv")
        
        # URL processing
        df['Variable Link'] = df['Variable Link'].apply(
            lambda x: f"{base_url}{x}" if isinstance(x, str) and x.startswith('/data') else x
        )
        df['Variable Link'] = df['Variable Link'].str.replace('.html', '.json')
        
        # Initialize columns
        for col in ['Attributes', 'Attribute Of', 'Attribute Type']:
            if col not in df.columns:
                df[col] = pd.Series(dtype='object')
        
        errors = []
        
        # Process each variable
        for i, row in df.iterrows():
            try:
                variable_url = row['Variable Link']
                if pd.isna(variable_url):
                    continue
                    
                response = session.get(variable_url, timeout=10)
                response.raise_for_status()
                variable_data = response.json()
                
                # Update columns
                df.at[i, 'Attributes'] = json.dumps(variable_data.get('attributes', 'na'))
                df.at[i, 'Attribute Of'] = variable_data.get('attribute of', 'na')
                df.at[i, 'Attribute Type'] = variable_data.get('attribute type', 'na')
                
            except Exception as e:
                logger.warning(f"Error processing row {i} in {chunk_file}: {str(e)}")
                errors.append({
                    "Chunk File": chunk_file,
                    "Index": i,
                    "Variable Name": row.get('Variable Name', 'na'),
                    "Variable Link": row.get('Variable Link', 'na'),
                    "Error": str(e)
                })
        
        # Save results
        column_order = [
            "SurveyID", "SurveyGroupID", "Group", "Variable Name", "Variable Link",
            "Label", "Concept", "Required", "Attributes", "Attribute Of", 
            "Attribute Type", "Limit", "Predicate Type"
        ]
        df = df[column_order]
        df.to_csv(output_file, index=False)
        
        if errors:
            pd.DataFrame(errors).to_csv(error_log_file, index=False)
            
        logger.info(f"Successfully processed {chunk_file}")
        return True
            
    except Exception as e:
        logger.error(f"Critical error processing {chunk_file}: {str(e)}")
        return False

def main():
    input_folder = "../data/data_extraction/GroupNodeChunks"
    output_folder = "../data/data_extraction/GroupNodesWithVariables"
    start_chunk = 0
    num_workers = 5

    # Setup logging
    logger = setup_logging(output_folder)
    
    try:
        all_files = sorted([
            f for f in os.listdir(input_folder) 
            if f.startswith("GroupNode_chunk_") and f.endswith(".csv")
        ], key=lambda x: int(x.split("_")[-1].split(".")[0]))
        
        files_to_process = [
            os.path.join(input_folder, f) for f in all_files
            if int(f.split("_")[-1].split(".")[0]) >= start_chunk
        ]
        
        logger.info(f"Found {len(files_to_process)} files to process")
        
        num_workers = min(num_workers or (cpu_count() - 1), len(files_to_process))
        logger.info(f"Using {num_workers} workers")
        
        # Create args list for worker function
        worker_args = [(f, output_folder) for f in files_to_process]
        
        with Pool(num_workers) as pool:
            with tqdm(total=len(files_to_process)) as pbar:
                for _ in pool.imap_unordered(worker_function, worker_args):
                    pbar.update()

    except Exception as e:
        logger.error(f"Critical error in main process: {str(e)}")

if __name__ == "__main__":
    main()
