import pandas as pd


def save_results_to_excel(rows: list, excel_path: str):
    if not rows:
        df = pd.DataFrame(columns=["hotel_name", "room_name", "price", "currency", "stay_from", "stay_to"])
    else:
        df = pd.DataFrame(rows)
    df.to_excel(excel_path, index=False)