import os
import glob
import json

from text_analyzer import TextAnalyzer
from language_evaluator import TextLanguageEvaluator

def main():
    evaluator = TextLanguageEvaluator()
    # Get the absolute path of the current executing file.
    current_file_path = os.path.abspath(__file__)
    # Determine the root directory of the project
    project_root = os.path.dirname(current_file_path)

    json_model_path = os.path.join(project_root, "data", "reference_models")

    evaluator.read_json_folder(json_model_path)

    evaluator.initialize_results()

    test_data_path = os.path.join(project_root, "data", "corpus_multi", "*", "test", "*")

    test_file_list = glob.glob(test_data_path)

    correct_predictions_count = 0

    for file_path in test_file_list:

        dossiers = file_path.split("/")
        if len(dossiers) < 3:
            continue

        actual_language = dossiers[-3]

        raw_text = evaluator.read_file(file_path)
        clean_text = raw_text.replace(" ", "").replace("\n", "").replace("\t", "")
   

        bigrams = [clean_text[i:i+2] for i in range(len(clean_text) - 1)]

        bigram_frequencies = {}
        for bg in bigrams:
            bigram_frequencies[bg] = bigram_frequencies.get(bg, 0) + 1

        sorted_bigrams = sorted([[freq, ''.join(bg)] for bg, freq in bigram_frequencies.items()])
        top_10_bigrams = sorted_bigrams[-10:]
        most_frequent_bigrams = set([bg for freq, bg in top_10_bigrams])

        predictions = evaluator.calculate_intersection(most_frequent_bigrams)

        if predictions:
            # sorted predictions ex [5, "en"], [2, "fr"] ...
            arrangement = sorted(predictions, reverse=True)
            best_prediction = arrangement[0][1]

            evaluator.update_metrics(best_prediction, actual_language)

            if best_prediction == actual_language:
                correct_predictions_count += 1
    if len(test_file_list) > 0:

        accuracy = correct_predictions_count / len(test_file_list)

    else:
        accuracy = 0.0

    print("             EVALUATION REPORT             ")
    print("\n")
    print(f"Total Test Files : {len(test_file_list)}")
    print(f"Correct Answers  : {correct_predictions_count}")
    print(f"Accuracy Score   : {accuracy:.4f} ({accuracy * 100 / 1:.1f}%)")
    print("\n")
    print("Detailed Metrics (TP, FP, FN) per Language:")
    print(json.dumps(evaluator.evaluation_results, indent=2))
    print("-"*40)

if __name__ == "__main__":
    main()