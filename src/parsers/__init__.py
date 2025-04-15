"""
Module with parsers for different types of medical data.

This module provides parsers for:
- Patient data (demographic, medical history)
- Hospitalization data (admissions, diagnoses)
- Ward/department data
- Laboratory test results
- Final medical reports
"""

# Base parser functionality
from src.parsers.base_parser import get_full_path, SUB_PATH

# Patient data parsers
from src.parsers.patient_parser import (
    get_sex,
    get_age,
    get_amnez_d,
    get_amnez_life,
    get_condition,
    parse_conditions_as_key_value,
    get_structured_condition
)

# Hospitalization data parsers
from src.parsers.hosp_parser import get_gosp_info, get_diagnosis

# Ward/department data parsers
from src.parsers.ward_parser import (
    get_ward_table,
    get_ward_list,
    get_ward_name,
    get_research_list,
    get_research_name,
    get_research_table,
    compute_full_wards
)

# Final report parsers
from src.parsers.final_parser import get_final_table1, get_final_table2

# Laboratory data parsers
from src.parsers.lab_parser import get_table_1 