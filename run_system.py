import csv
import json
import pandas as pd

from sar_quality_measure import SARQualityMeasure

def main():

    # Load sample data
    data = []
    with open("sample_data.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)

    # Initialize SAR measure    
    sar = SARQualityMeasure()

    # Process data and get member data and code groups
    results = []
    member_data_dict = get_member_data(data)
    code_groups = classification_key()
    # For each member get their result
    for member_data in member_data_dict:
        result = sar.get_result(member_data_dict[member_data], code_groups)
        results.append(result)

    # Output results as a Dict
    predictions = {}
    for i, r in enumerate(results):
        predictions[i + 1] = r 
    
    # Create json and output results
    with open("results.json", "w") as f:
        json.dump(predictions, f, indent=2)

# Sorts out the members by memberId
# visitDate and visitCode are lists
# visitNumber gets replaced when encountering a larger number 
def get_member_data(data):
    members = {}

    # Main loop, sorts by memberId
    for row in data:
        member_id = row["memberId"]  
        
        if member_id not in members:
            members[member_id] = {}
        
        # Loop to store each value    
        for key, value in row.items():
            
            # visitDate and visitCode values stored in lists
            if key == "visitDate" or key == "visitCode":
                if key not in members[member_id]:
                    members[member_id][key] = [value] 
                else:
                    members[member_id][key].append(value)
            
            # visitNumber gets max visitNumber
            elif key == "visitNumber":
                if key not in members[member_id] or value > members[member_id][key]:
                    members[member_id][key] = value
            
            # Other values get stored
            else:
                if key not in members[member_id]: 
                    members[member_id][key] = value

    return members

# Loads the classification key data from excel
def classification_key():
    
    # Using read_excel from pandas
    classification_key = pd.read_excel('Technical Assessment Classification Key.xlsx')

    # Groups by classification key 
    # Values are stored in lists
    code_groups = {}
    for idx, row in classification_key.iterrows():
        group = row.iloc[0]
        code = row.iloc[1]
        
        if group not in code_groups:
            code_groups[group] = []
            
        if code not in code_groups[group]:
            code_groups[group].append(code)

    return code_groups

if __name__ == "__main__":
    main()