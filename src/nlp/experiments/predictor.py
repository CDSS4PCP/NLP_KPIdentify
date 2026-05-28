import os
import spacy
from src.nlp.data.dataset import DatasetBuilder

def predict_kp(predict_data):
    builder = DatasetBuilder()
    
    # Try using scispacy model if available, else fallback to standard
    model_name = "en_core_sci_lg"
    if not spacy.util.is_package(model_name):
        # Using a basic model for runtime safety if scispacy isn't fully installed
        model_name = "en_core_web_sm"
        
    try:
        predict_data = builder.generate_predict_dataset(
            predict_data, 
            min_sentences=3, 
            filter_kp=False, 
            model_name=model_name
        )
    except Exception as e:
        print(f"Prediction error: {e}")
        predict_data[0]['keywords'] = []
    
    # In the refactored architecture, BiLSTM-CRF inference would be loaded here.
    # For now, we populate actual_keywords using the base NER results to ensure UI functionality.
    predict_data[0]['actual_keywords'] = predict_data[0].get('keywords', [])
    return predict_data
