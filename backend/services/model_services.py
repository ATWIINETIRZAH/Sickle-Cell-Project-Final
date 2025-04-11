

import pickle
import tensorflow as tf
import numpy as np
import os

class ModelService:
    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        pkl_path = os.path.join(base_dir, "models", "random_forest_model2.pkl")
        h5_path = os.path.join(base_dir, "models", "lstm_model2.h5")

        try:
            with open(pkl_path, "rb") as f:
                loaded_data = pickle.load(f)
                print(f"Type of loaded pkl data: {type(loaded_data)}")
                
                if isinstance(loaded_data, dict) and 'model' in loaded_data:
                    self.pkl_model = loaded_data['model']
                else:
                    self.pkl_model = loaded_data
        except Exception as e:
            print(f"Error loading pkl model: {str(e)}")
            self.pkl_model = None
        
        try:
            
            def mse(y_true, y_pred):
                return tf.reduce_mean(tf.square(y_true - y_pred))
            
            custom_objects = {'mse': mse}
            self.h5_model = tf.keras.models.load_model(h5_path, custom_objects=custom_objects)
        except Exception as e:
            print(f"Error loading H5 model: {str(e)}")
            self.h5_model = None
    
    def predict_with_pkl(self, data):
        if self.pkl_model is None:
            return {"error": "PKL model failed to load"}
            
        input_data = self._preprocess_for_pkl(data)
        print(input_data.dtype)
        prediction = self.pkl_model.predict(input_data)
        return prediction.tolist() if isinstance(prediction, np.ndarray) else prediction
    
    def predict_with_h5(self, data):
        if self.h5_model is None:
            return {"error": "H5 model failed to load"}
            
        input_data = self._preprocess_for_h5(data)
        prediction = self.h5_model.predict(input_data)
        return prediction.tolist()
    
    def _preprocess_for_pkl(self, data):
        preprocessed_data = {
            'WBC': data.get('WBC'),
            'HGB': data.get('HGB'),
            'LYmp': data.get('LYmp'),
            'NEUTp': data.get('NEUTp')
        }
        
        for key, value in preprocessed_data.items():
            if value is None:
                raise ValueError(f"Missing required field: {key}")
        
        features = np.array([[
            preprocessed_data['WBC'],
            preprocessed_data['HGB'],
            preprocessed_data['LYmp'],
            preprocessed_data['NEUTp']
        ]])
        
        return features

    def _preprocess_for_h5(self, data):
        preprocessed_data = {
            'RBC': data.get('RBC'),
            'WBC': data.get('WBC'),
            'HGB': data.get('HGB'),
            'PLT': data.get('PLT')
        }

        for key, value in preprocessed_data.items():
            if value is None:
                raise ValueError(f"Missing required field: {key}")
        
        
        features = np.array([
            preprocessed_data['RBC'],
            preprocessed_data['WBC'],
            preprocessed_data['HGB'],
            preprocessed_data['PLT']
        ])
        
        features = np.tile(features, (10, 1))  
        features = np.expand_dims(features, axis=0)  
        
        return features