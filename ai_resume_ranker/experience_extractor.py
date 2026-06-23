import re
from datetime import datetime

def estimate_experience(text):

    years = re.findall(r"20\d{2}", text)

    if len(years) < 2:
        return 0

    years = [int(y) for y in years]

    start_year = min(years)

    current_year = datetime.now().year

    experience = current_year - start_year

    return max(experience, 0)