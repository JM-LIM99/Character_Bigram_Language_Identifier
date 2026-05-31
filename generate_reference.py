import os
import glob
import json
import re 
from pathlib import Path
from text_analyzer import TextAnalyzer


def main():
    # Get the absolute path of the current executing file.
    current_file_path = os.path.abspath(__file__) 
    # Determine the root directory of the project
    project_root = os.path.dirname(current_file_path)

    raw_corpus_folder = os.path.join(project_root, "data", "corpus_multi")

    output_model_folder = os.path.join(project_root, "data", "reference_models")

    print(f"Scanning subdirectories in: {raw_corpus_folder}")

   
    if not os.path.exists(output_model_folder):
        os.makedirs(output_model_folder)
        print(f"Created target directory: {output_model_folder}")

    search_pattern = os.path.join(raw_corpus_folder, "**", "*")
    all_files = glob.glob(search_pattern, recursive=True)


    language_corpus = {}

    for file_path in all_files:
        # Skip if it's a directory or a hidden system file 
        if not os.path.isfile(file_path) or os.path.basename(file_path).startswith('.'):
            continue
            
        if not (file_path.endswith('.txt') or file_path.endswith('.html')):
            continue

        parts = file_path.split("/")
        # find a language code: ex) en (English)
        if len(parts) < 3:
            continue
        lang_code = parts[-3].lower() 

       
        analyzer = TextAnalyzer()
        try:
            file_content = analyzer.read_file(file_path)
            # Remove tags from text
            if file_path.endswith('.html'):
                file_content = re.sub(r'<[^>]+>', ' ', file_content)
                
            if lang_code not in language_corpus:
                language_corpus[lang_code] = ""
            language_corpus[lang_code] += " " + file_content
        except Exception as e:
            continue

    if not language_corpus:
        print("\n Error : No files found ")
        return

    for lang_code, combined_text in language_corpus.items():
        
        print(f"\n Analyzing consolidated text for [{lang_code}]...")

        analyzer = TextAnalyzer()
        analyzer.split_string(combined_text)
        
        
        top10_words = analyzer.get_words_top10()
        
        model_data = {
            lang_code: top10_words  
        }

       
        json_filename = f"{lang_code}.json"
        
        json_output_path = os.path.join(output_model_folder, json_filename)
        # Generate reference file
        with open(json_output_path, 'w', encoding='utf-8') as f:
            json.dump(model_data, f, ensure_ascii=False, indent=4)
            
        print(f"Successfully saved inside folder: {json_output_path}")

    print("\n All JSON files are safely stored inside './data/reference_models'")

if __name__ == "__main__":
    main()