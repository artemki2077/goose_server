from fastapi import FastAPI
from routing.data import router as data_router
import uvicorn


app = FastAPI(title="Гусь, ПО для сбора товаров с разных сайтов и анализа цен в одном месте")
app.include_router(data_router)

if __name__ == '__main__':
    uvicorn.run(app)