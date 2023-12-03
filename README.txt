Healthcare Quality Measures
This package provides a toolkit for evaluating various healthcare quality measures in a standardized, scalable way.

Contents:
abstract_quality_measure.py: Contains AbstractQualityMeasure superclass with base functionality
sar_quality_measure.py: Contains SARQualityMeasure concrete subclass for Stroke-after-Rehabilitation (SAR) measure
run_system.py: Runtime script to evaluate sample data using SAR measure
sample_data.csv: Sample input data
"Technical Assessment Classification Key.xlsx": Classification key data
results.json: Output results from sample data run

Before running, I use pandas.read_excel() therefore I would recommend running:
pip3 install openpyxl

I also used Python 3.11.4 64-bit

Execute run_system.py script:
python run_system.py

Output is written to results.json
I'll leave the last json result but feel free to delete it and run the system again to make sure it creates the json
The predictions are returned in this format:
{
  "1": {
    "matches_product_line": true,
    "matches_age_requirements": true,
    "is_enrolled_through": true,
    "is_excluded": true,
    "has_event": true,
    "is_denominator": true,
    "is_numerator": true
  },
  "2": {
    "matches_product_line": true,
    "matches_age_requirements": false,
    "is_enrolled_through": true,
    "is_excluded": true,
    "has_event": true,
    "is_denominator": false,
    "is_numerator": true
  },
  ...