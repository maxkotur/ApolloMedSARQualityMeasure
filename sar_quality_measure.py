from abstract_quality_measure import AbstractQualityMeasure

class SARQualityMeasure(AbstractQualityMeasure):

    def __init__(self):
        super().__init__()
    
    # Returns the dict of booleans based on the criteria of the member
    def get_result(self, member_data, code_groups):
        
        # Gets default result dict
        result = super().get_result()
        
        # Checks each criteria for the member
        result["matches_product_line"] = self.matches_product_line(member_data)
        result["matches_age_requirements"] = self.matches_age_requirements(member_data) 
        result["is_enrolled_through"] = self.is_enrolled_through(member_data)
        result["is_excluded"] = self.is_excluded(member_data, code_groups)    
        result["has_event"] = self.has_event(member_data, code_groups)
        
        # Checks if is_denominator is True
        if (result["matches_product_line"] 
            and result["matches_age_requirements"] 
            and result["is_enrolled_through"]
            and result["has_event"]
            and result["is_excluded"]):
            result["is_denominator"] = True  
        
        # Checks if is_numerator is True
        result["is_numerator"] = self.has_stroke_after_rehab(member_data, code_groups)
        
        return result
