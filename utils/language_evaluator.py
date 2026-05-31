import os
import json
import glob

class TextLanguageEvaluator:
    def __init__(self):
        self.json_data = []
        self.reference_models = {}
        self.evaluation_results = {}
    
    def read_json_folder(self, folder_path):
        if not os.path.exists(folder_path):
            print(f"Error : The path '{folder_path} does not exist.'")
            return []
        file_list = os.listdir(folder_path)
        json_files = [file for file in file_list if file.endswith('.json')]

        self.json_data = []
        for filename in json_files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding = 'utf-8') as f:
                content = json.load(f)
                self.json_data.append(content)

            if isinstance(content, dict):
                self.reference_models.update(content)
        return self.json_data
    
    def read_file(self, file_path):
        with open(file_path, 'r', encoding = 'utf-8') as f:
            return f.read()
    
    def initialize_results(self):

        self.evaluation_results = {}

        for lang_ref in self.reference_models.keys():
            self.evaluation_results[lang_ref] = {"TP": 0, "FP": 0, "FN": 0}

        return self.evaluation_results
    
    def calculate_intersection(self, most_frequent_words):
        prediction_list = []

        for lang_ref, model in self.reference_models.items():

            common_words = set(model).intersection(most_frequent_words)
            prediction_list.append([len(common_words), lang_ref])
        
        prediction_list.sort()
        return prediction_list
    
    def update_metrics(self, predicted_language, actual_language):
        if predicted_language == actual_language:
            self.evaluation_results[predicted_language]['TP'] += 1
        else:
            if predicted_language in self.evaluation_results:
                self.evaluation_results[predicted_language]['FP'] += 1
            if actual_language in self.evaluation_results:
                self.evaluation_results[actual_language]['FN'] += 1