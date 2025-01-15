from datetime import datetime

def validate_date(value):
    try:
        date_obj = datetime.strptime(value, "%d/%m/%Y")
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        pass

    try:
        date_obj = datetime.strptime(value, "%Y/%m/%d")
        return date_obj.strftime("%Y-%m-%d")  # Converte para "YYYY-MM-DD" e retorna
    except ValueError:
        raise ValueError(f"{value} is not a valid date format. Use either 'DD/MM/YYYY' or 'YYYY/MM/DD'.")