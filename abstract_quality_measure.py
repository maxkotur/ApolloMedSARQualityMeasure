from abc import ABC, abstractmethod
from datetime import datetime as dt

class AbstractQualityMeasure(ABC):

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_result(self):
        # Returns a dictionary containing result info for quality reporting
        # Default is all are False
        result = {
            "matches_product_line": False,
            "matches_age_requirements": False, 
            "is_enrolled_through": False,
            "is_excluded": False,
            "has_event": False,
            "is_denominator": False,
            "is_numerator": False
        }
        
        return result

    # Methods that return boolean value of criteria
    
    # Returns if productLine is Medicare
    def matches_product_line(self, member_data):
        return member_data["productLine"] == "Medicare"
    
    # Returns if age is between 18-27
    def matches_age_requirements(self, member_data):
        age = int(member_data["age"])
        return age >= 18 and age <= 27

    # Returns if enrolled through date is December 31st 2023
    def is_enrolled_through(self, member_data):
        enrolled_end = member_data["enrolledEnd"]
        return enrolled_end == "12/31/2031"

    # Excludes if member had a Stroke Exclusion in 2023
    def is_excluded(self, member_data, code_groups):
        num_visits = int(member_data["visitNumber"])
        # Checks for each visit
        for i in range(num_visits):
            date_year = dt.strptime(member_data["visitDate"][i], "%m/%d/%Y").year
            # Checks for Stroke Exclusion in 2023
            if date_year == 2023 and member_data['visitCode'][i] in code_groups["Stroke Exclusion"]:
                return False
        return True

    # Returns if member had Rehabilitation in 2023
    def has_event(self, member_data, code_groups):
        num_visits = int(member_data["visitNumber"])
        # Checks for every visit
        for i in range(num_visits):
            date_year = dt.strptime(member_data["visitDate"][i], "%m/%d/%Y").year
            # Checks for Rehabilitation in 2023
            if date_year == 2023 and member_data['visitCode'][i] in code_groups["Rehabilitation"]:
                return True
        return False
    
    # Returns if member had a Stroke in 2023 within the first 7 days after Rehabilitation
    def has_stroke_after_rehab(self, member_data, code_groups):
        rehab_codes = code_groups['Rehabilitation']
        stroke_codes = code_groups['Stroke']
        
        rehab_dates = []
        stroke_dates = []
        
        # Gets each Rehabilition and Stroke date for the member
        for date_str, code in zip(member_data["visitDate"], member_data["visitCode"]):
            date = dt.strptime(date_str, "%m/%d/%Y").date()  
            if code in rehab_codes:
                rehab_dates.append(date)
            elif code in stroke_codes:
                stroke_dates.append(date)

        # For every Stroke in 2023, check for every Rehabilitation
        for stroke_date in stroke_dates:
            if stroke_date.year != 2023:
                continue
            
            # For every Rehabilitation, check if there are at most 7 days in between   
            for rehab_date in rehab_dates:
                delta = (stroke_date - rehab_date).days 
                if 0 <= delta <= 7:
                    return True

        return False
        