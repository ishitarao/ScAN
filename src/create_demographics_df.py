import pandas as pd

RESOURCES_DIR = '../get_data/resources/'
OUTPUT_DIR = '../get_data/outputs/'

ADMISSIONS_CSV = RESOURCES_DIR + 'ADMISSIONS.csv'
PATIENTS_CSV = RESOURCES_DIR + 'PATIENTS.csv'
ID_CSV = '../get_data/id.csv'

FILTERED_ADMISSIONS_CSV = OUTPUT_DIR + 'filtered_admissions.csv'
FILTERED_PATIENTS_CSV = OUTPUT_DIR + 'filtered_patients.csv'
DEMOGRAPHICS_CSV = OUTPUT_DIR + 'final_demographics.csv'

HADM_ID_COL = 'HADM_ID' # hospital admission id
SUBJECT_ID_COL = 'SUBJECT_ID' # patient id

def get_ids(id_column):
    id_df = pd.read_csv(ID_CSV)
    return set(id_df[id_column].astype(str))

hadm_ids = get_ids(HADM_ID_COL)
subject_ids = get_ids(SUBJECT_ID_COL)


def filter_admissions_data():
    data_df = pd.read_csv(ADMISSIONS_CSV)
    filtered_df = data_df[data_df[HADM_ID_COL].astype(str).isin(hadm_ids)]
    filtered_df.to_csv(FILTERED_ADMISSIONS_CSV, index=False)


def filter_patients_data():
    data_df = pd.read_csv(PATIENTS_CSV)
    filtered_df = data_df[data_df[SUBJECT_ID_COL].astype(str).isin(subject_ids)]
    filtered_df.to_csv(FILTERED_PATIENTS_CSV, index=False)


def create_demographics_df():
    admissions_df = pd.read_csv(FILTERED_ADMISSIONS_CSV)
    patients_df = pd.read_csv(FILTERED_PATIENTS_CSV)
    admittime_col = "ADMITTIME"
    dob_col = "DOB"

    merged = pd.merge(admissions_df, patients_df, on=SUBJECT_ID_COL, how="inner")

    columns_to_keep = [SUBJECT_ID_COL, HADM_ID_COL, admittime_col, dob_col, "GENDER", "EXPIRE_FLAG", "HOSPITAL_EXPIRE_FLAG", "INSURANCE", "LANGUAGE", "RELIGION", "MARITAL_STATUS", "ETHNICITY"]
    filtered_df = merged[columns_to_keep]

    filtered_df[admittime_col] = pd.to_datetime(filtered_df[admittime_col])
    filtered_df[dob_col] = pd.to_datetime(filtered_df[dob_col])

    filtered_df['AGE'] = filtered_df[admittime_col].dt.year - filtered_df[dob_col].dt.year

    # Adjust if end date is before anniversary in that year
    filtered_df['AGE'] -= (
            (filtered_df[admittime_col].dt.month < filtered_df[dob_col].dt.month) |
            ((filtered_df[admittime_col].dt.month == filtered_df[dob_col].dt.month) &
             (filtered_df[admittime_col].dt.day < filtered_df[dob_col].dt.day))
    )

    filtered_df.to_csv(DEMOGRAPHICS_CSV, index=False)