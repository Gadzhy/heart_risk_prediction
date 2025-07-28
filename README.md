# Проект по предсказанию риска сердечного приступа по данным о пользователе

## Инструкция по запуску

### Предварительные требования

- Python 3.8+
- pip
### Установка

***Шаг 1: Клонирование репозитория***
```git clone https://github.com/yourusername/heart-risk-api.git
cd heart-risk-api
```
git clone — копирует проект с GitHub на локальную машину.
cd heart-risk-api — переходит в папку проекта.

***Шаг 2: Установка зависимостей***
`pip install -r requirements.txt`
Устанавливает все библиотеки, необходимые для работы API (FastAPI, pandas, scikit-learn и т.д.), которые перечислены в файле requirements.txt.

### Запуск сервиса

`uvicorn app.main:app --reload`
uvicorn — сервер для запуска FastAPI-приложений.
main:app — указывает, что приложение (app) находится в файле main.py.
--reload — включает автоматическую перезагрузку сервера при изменениях кода (удобно для разработки).
Сервер запустится по адресу: http://127.0.0.1:8000

## Проверка работоспособности

Запустите сервер по адресу: http://127.0.0.1:8000/docs
Найдите блок **"GET /health"** → нажмите **"Try it out"**
Нажмите **"Execute"**
Ожидаемый ответ:
json
{"status":"OK"}

## Как получить предсказания

1. Запустите сервер по адресу: http://127.0.0.1:8000/docs
2. Найдите блок **"POST /predict"** → нажмите **"Try it out"**

3. Нажмите **"Choose File"** и выберите ваш CSV-файл  

4. Нажмите **"Execute"**

5. **Результат** появится ниже в разделе "Response"  
   (CSV-файл с колонками `id, prediction`)
   
6. Скачайте файл

## Требования к CSV-файлу

**Названия колонок должны совпадать с перечисленными ниже вариантами:**
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

**Необходимые для предсказания признаки представлены ниже:**
        'age', 'cholesterol', 'heart_rate', 'diabetes', 'family_history',
        'smoking', 'obesity', 'alc_consump', 'diet', 'medication_use',
        'sedentary_hours', 'income', 'bmi', 'triglycerides',
        'phys_activity_days', 'sleep_hours', 'troponin', 'systolic_pressure'

**Обязательно наличие столбца id**

## Тестирование

### Тестовые данные

Пример тестовых данных находится в test_predictor.py:

test_data = pd.DataFrame({
    'id': [1, 2],
    'age': [0.45, 0.60],
    'cholesterol': [0.190, 0.240],
    # ... другие признаки ...
})

### Запуск тестов
Для запуска тестирования необходимо ввести команду:
`python test_predictor.py`

## Структура проекта

heart-risk-api/
├── app/
│   ├── main.py
│   ├── predictor.py
│   └── schemas.py
├── data/
├── models/
│   └── model.joblib
├── predictions.csv
├── test_predictor.py
├── requirements.txt
└── README.md




