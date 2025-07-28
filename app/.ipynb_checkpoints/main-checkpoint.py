from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
import pandas as pd
import io
import logging
from typing import Dict
from app.predictor import HeartRiskPredictor

app = FastAPI(
    title="Heart Risk Prediction API",
    version="1.0",
    docs_url="/docs",
    redoc_url=None
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация предсказателя
predictor = HeartRiskPredictor()

@app.get("/")
async def root():
    return {"message": "Heart Risk Prediction API is running"}

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Проверка работоспособности сервиса"""
    return {"status": "OK"}
    
@app.post("/predict")
async def predict_csv(file: UploadFile = File(...)) -> StreamingResponse:
    """
    Обрабатывает CSV файл и возвращает предсказания
    
    Требования:
    - CSV файл с колонкой 'id'
    - Данные в UTF-8 кодировке
    
    Возвращает:
    - CSV с колонками: id, prediction
    """
    try:
        # 1. Проверка типа файла
        if not file.filename.lower().endswith('.csv'):
            raise HTTPException(400, detail="Только CSV файлы поддерживаются")
        
        # 2. Чтение данных
        contents = await file.read()
        try:
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        except UnicodeDecodeError:
            raise HTTPException(400, detail="Неверная кодировка файла (требуется UTF-8)")
        except pd.errors.EmptyDataError:
            raise HTTPException(400, detail="Файл пуст")
        except Exception as e:
            logger.error(f"Ошибка чтения CSV: {str(e)}")
            raise HTTPException(400, detail=f"Ошибка чтения CSV: {str(e)}")
        
        # 3. Проверка обязательных полей
        if 'id' not in df.columns:
            raise HTTPException(422, detail="Отсутствует обязательная колонка 'id'")
        
        # 4. Получение предсказаний
        try:
            result = predictor.predict(df)
        except ValueError as e:
            logger.error(f"Ошибка валидации данных: {str(e)}")
            raise HTTPException(422, detail=str(e))
        except Exception as e:
            logger.error(f"Ошибка модели: {str(e)}", exc_info=True)
            raise HTTPException(500, detail="Ошибка обработки данных моделью")
        
        # 5. Подготовка ответа
        stream = io.StringIO()
        result.to_csv(stream, index=False)
        
        return StreamingResponse(
            iter([stream.getvalue()]),
            media_type="text/csv",
            headers={
                "Content-Disposition": f"attachment; filename=predictions_{file.filename}",
                "X-API-Version": "1.0"
            }
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.exception("Непредвиденная ошибка сервера")
        raise HTTPException(500, detail="Внутренняя ошибка сервера")
