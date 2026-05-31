import json
import os
import glob
import matplotlib.pyplot as plt


class TextAnalyzer:
    def __init__(self):
        self.word_list = []
        self.length_dict = {}
        self.frequency_list = []

    def read_file(self, path):
        with open(path, encoding="utf-8") as f:
            return f.read() 
    
    def split_string(self, text): 
        clean_text = text.replace(" ", "").replace("\n", "").replace("\t", "").replace("\r", "")
        
        self.word_list = [clean_text[i:i+2] for i in range(len(clean_text) - 1)]
        
        print(f"The text contains {len(self.word_list)} character bigrams in total")
        return self.word_list

    def calculate_length (self):
        for word in self.word_list: 
            length = len(word)
            if length not in self.length_dict:
                self.length_dict[length]=1 
            else:
                self.length_dict[length]+=1
        return self.length_dict

    def calculate_frequency(self):
        total_words = len(self.word_list)
        self.frequency_list = []
        for length in range(30):
            if length in self.length_dict:
                self.frequency_list.append(self.length_dict[length]/ total_words)
            else:
                self.frequency_list.append(0)

        return self.frequency_list
    
    def get_words_top10(self):

        self.word_counts = {}
        for word in self.word_list:
            self.word_counts[word] = self.word_counts.get(word, 0) + 1

        
        top10 = [[count, word] for word, count in self.word_counts.items()]
        sorted_top10 = sorted(top10)[-10:]


        return [word for count, word in sorted_top10]
    
    def read_json_folder(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Error : The path '{folder_path}' does not exist.")
            return []
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith('.json')]

        print(f"\nFound {len(json_files)} JSON files in {folder_path}:")
        print(json_files)

        self.json_data = []
        for filename in json_files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding = 'utf-8') as f:
                content = json.load(f)
                print(f"Loaded JSON from {filename}: {content}")
                self.json_data.append(content)
        return self.json_data