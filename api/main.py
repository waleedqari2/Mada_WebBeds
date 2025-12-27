from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional, Literal
import os
import json
import uuid

from scraping import config
from scraping.hotels_config import HOTELS, ALL_HOTELS_KEY
from scraping.hotel_scraper import (
    generate_night_ranges,
    scrape_full_stay_for_hotels,
    scrape_night_by_night_for_hotels,
)
from scraping.storage import save_results_to_excel

app = FastAPI(title="Mada WebBeds Scraper API")


class SearchRequest(BaseModel):
    mode: Literal["full_stay", "night_by_night"]
    date_from: str  # "01/02/2026"
    date_to: str    # "05/02/2026"
    hotels: List[str]  # أسماء الفنادق أو ["ALL"]


@app.post("/cookies")
async def upload_cookies(file: UploadFile = File(...)):
    if not file.filename.endswith(".json"):
        raise HTTPException(status_code=400, detail="الملف يجب أن يكون JSON")

    content = await file.read()
    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="ملف JSON غير صالح")

    with open(config.COOKIES_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {"status": "ok", "message": "تم حفظ الكوكيز بنجاح"}


@app.post("/search")
def search(request: SearchRequest):
    # تحديد الفنادق المستخدمة
    if ALL_HOTELS_KEY in request.hotels:
        selected_hotels = HOTELS
    else:
        selected_hotels = {
            name: url for name, url in HOTELS.items() if name in request.hotels
        }
        if not selected_hotels:
            raise HTTPException(status_code=400, detail="لا توجد فنادق مطابقة للأسماء المرسلة")

    # تنفيذ البحث
    if request.mode == "full_stay":
        results = scrape_full_stay_for_hotels(selected_hotels)
    else:
        night_ranges = generate_night_ranges(request.date_from, request.date_to)
        results = scrape_night_by_night_for_hotels(selected_hotels, night_ranges)

    # حفظ النتائج في Excel
    job_id = str(uuid.uuid4())
    excel_path = os.path.join(config.OUTPUT_DIR, f"results_{job_id}.xlsx")
    save_results_to_excel(results, excel_path)

    return {
        "job_id": job_id,
        "results_count": len(results),
        "excel_path": excel_path,
    }


@app.get("/results/{job_id}/excel")
def download_excel(job_id: str):
    excel_path = os.path.join(config.OUTPUT_DIR, f"results_{job_id}.xlsx")
    if not os.path.exists(excel_path):
        raise HTTPException(status_code=404, detail="الملف غير موجود")
    return FileResponse(
        excel_path,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        filename=f"results_{job_id}.xlsx",
    )