import joblib
import pandas as pd
from pathlib import Path
from typing import Dict, Optional

class HeartRiskPredictor:
    # Маппинг старых названий колонок к новым
    COLUMN_MAPPING = {
        'Age': 'age',
        'Cholesterol': 'cholesterol',
        'Heart rate': 'heart_rate',
        'Diabetes': 'diabetes',
        'Family History': 'family_history',
        'Smoking': 'smoking',
        'Obesity': 'obesity',
        'Alcohol Consumption': 'alc_consump',
        'Exercise Hours Per Week': 'exercise_hours',
        'Diet': 'diet',
        'Medication Use': 'medication_use',
        'Stress Level': 'stress_level',
        'Sedentary Hours Per Day': 'sedentary_hours',
        'Income': 'income',
        'BMI': 'bmi',
        'Triglycerides': 'triglycerides',
        'Physical Activity Days Per Week': 'phys_activity_days',
        'Sleep Hours Per Day': 'sleep_hours',
        'Blood sugar': 'blood_sugar',
        'CK-MB': 'ck-mb',
        'Troponin': 'troponin',
        'Gender': 'gender',
        'Systolic blood pressure': 'systolic_pressure',
        'Diastolic blood pressure': 'diastolic_pressure'
    }
    
    # Признаки, которые используются в финальной модели
    USED_FEATURES = [
        'age', 'cholesterol', 'heart_rate', 'diabetes', 'family_history',
        'smoking', 'obesity', 'alc_consump', 'diet', 'medication_use',
        'sedentary_hours', 'income', 'bmi', 'triglycerides',
        'phys_activity_days', 'sleep_hours', 'troponin', 'systolic_pressure'
    ]

    def __init__(self, model_path: Optional[str] = None):
        if model_path is None:
            model_path = Path(__file__).parent.parent / "models" / "model.joblib"
        self.model = joblib.load(model_path)
    
    def _preprocess_data(self, data: pd.DataFrame) -> pd.DataFrame:
        """Предобработка входных данных"""
        # Копируем данные чтобы не изменять оригинальный DataFrame
        processed = data.copy()
        
        # Переименовываем колонки если нужно
        processed.rename(columns=self.COLUMN_MAPPING, inplace=True)
        
        # Оставляем только нужные признаки
        required_cols = self.USED_FEATURES + ['id']
        available_cols = [col for col in required_cols if col in processed.columns]
        
        # Проверяем, что все нужные колонки присутствуют
        missing_cols = set(self.USED_FEATURES) - set(available_cols)
        if missing_cols:
            raise ValueError(f"Отсутствуют обязательные колонки: {missing_cols}")
            
        return processed[available_cols]

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Принимает DataFrame, возвращает предсказания"""
        # Предобработка данных
        processed_data = self._preprocess_data(data)
        
        # Проверяем наличие id
        if 'id' not in processed_data.columns:
            raise ValueError("Входные данные должны содержать колонку 'id'")
            
        # Получаем предсказания
        features = processed_data.drop("id", axis=1)
        predictions = self.model.predict(features)
        
        return pd.DataFrame({
            "id": processed_data["id"],
            "prediction": predictions
        })