from app.predictor import HeartRiskPredictor
import pandas as pd
import numpy as np

# Создаем тестовые данные с ВСЕМИ необходимыми признаками
test_data = pd.DataFrame({
    'id': [1, 2],  # Обязательная колонка
    'age': [0.45, 0.60],
    'cholesterol': [0.190, 0.240],
    'heart_rate': [0.72, 0.88],
    'diabetes': [1, 0],
    'family_history': [1, 0],
    'smoking': [0, 1],
    'obesity': [0, 1],
    'alc_consump': [0, 1],
    'diet': ['1', '2'],  # Категориальный признак
    'medication_use': [0, 1],
    'sedentary_hours': [0.5, 0.2],
    'income': [0.7, 0.8],
    'bmi': [0.1, 0.5],
    'triglycerides': [0.3, 0.6],
    'phys_activity_days': ['3.0', '2.0'],  # Категориальный признак
    'sleep_hours': [0.5, 0.7],
    'troponin': [0.1, 0.5],
    'systolic_pressure': [0.7, 0.6]
})

# Инициализация и предсказание
predictor = HeartRiskPredictor()
result = predictor.predict(test_data)
print(result)