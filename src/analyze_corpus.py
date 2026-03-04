import pandas as pd
import numpy as np

# I ran each function one by one.
# Steps:
# 1. Obtain HADM_IDs and SUBJECT_IDs present in ScAN
# 2. Filter Admissions and Patient data based on the IDs to only include the data present in ScAN
# 2. Merge tables and only keep columns relevant to demographic src
# 3. Display values and counts for each column. These values were then used to generate the pie charts.
# For some columns, values were consolidated into a bucket/category. This is applicable to: religion, ethnicity, age
# the corpus file pattern is subject ID_HADM ID

OUTPUT_DIR = '../get_data/outputs/'
DEMOGRAPHICS_CSV = OUTPUT_DIR + 'final_demographics.csv'

HADM_ID_COL = 'HADM_ID' # hospital admission id
SUBJECT_ID_COL = 'SUBJECT_ID' # patient id


def print_counts_for_field(df, col):
    print(col)
    for key, val in df[col].value_counts().items():
        print('{}:{}'.format(key, val))
    print('\n')


def get_counts_for_religion(df):
    col = 'RELIGION'
    none = "NOT SPECIFIED/UNOBTAINABLE"
    christian_other = "CHRISTIAN - OTHER"

    df[col] = df[col].fillna(none)
    df[col] = df[col].replace({
        "UNOBTAINABLE": none,
        "NOT SPECIFIED": none,
        "UNITARIAN-UNIVERSALIST": "OTHER"
    })

    df[col] = df[col].replace({
        "EPISCOPALIAN": christian_other,
        "7TH DAY ADVENTIST": christian_other,
        "ROMANIAN EAST. ORTH": christian_other,
        "CHRISTIAN SCIENTIST": christian_other,
        "GREEK ORTHODOX": christian_other,
        "JEHOVAH'S WITNESS": christian_other,
    })

    print_counts_for_field(df, col)


def get_counts_for_age(df):
    col = 'AGE'
    bins = [18, 24, 34, 44, 54, 64, 74, 350]  # Age ranges
    labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65-74', '75 and up']
    df[col] = df[col].fillna(0)
    df[col] = pd.cut(df[col], bins=bins, labels=labels, right=False)
    print_counts_for_field(df, col)


def get_counts_for_ethnicity(df):
    col = 'ETHNICITY'
    other = 'UNKNOWN/OTHER/DECLINED'
    asian = 'ASIAN'
    hispaniclatino = 'HISPANIC OR LATINO'
    european = 'EUROPEAN'
    df[col] = df[col].replace({
        "UNKNOWN/NOT SPECIFIED": other,
        "UNABLE TO OBTAIN": other,
        "OTHER": other,
        "PATIENT DECLINED TO ANSWER": other,
        "ASIAN - JAPANESE": asian,
        "ASIAN - VIETNAMESE": asian,
        "ASIAN - CHINESE": asian,
        "WHITE - BRAZILIAN": "SOUTH AMERICAN",
        "HISPANIC/LATINO - PUERTO RICAN": hispaniclatino,
        "HISPANIC/LATINO - DOMINICAN": hispaniclatino,
        "WHITE - RUSSIAN": european,
        "WHITE - OTHER EUROPEAN": european,
        "PORTUGUESE": european,
    })
    print_counts_for_field(df, col)


def get_counts_for_death(df):
    exp_col = 'EXPIRE_FLAG'
    hexp_col = 'HOSPITAL_EXPIRE_FLAG'
    conditions = [
        (df[exp_col] == 1) & (df[hexp_col] == 0),  # dead but not here
        (df[hexp_col] == 1),  # dead here
        (df[exp_col] == 0)  # alive
    ]

    choices = ['DIED BUT NOT DURING THIS HOSPITAL VISIT', 'DIED DURING THIS HOSPITAL VISIT', 'ALIVE']
    df['DEATH_STATUS'] = np.select(conditions, choices, default='unknown')

    print_counts_for_field(df, 'DEATH_STATUS')


demographics_df = pd.read_csv(DEMOGRAPHICS_CSV)
basic_fields = ['GENDER', 'INSURANCE', 'MARITAL_STATUS', 'LANGUAGE'] # fields that don't need special processing
for field in basic_fields:
    print_counts_for_field(demographics_df, field)

get_counts_for_religion(demographics_df)
get_counts_for_age(demographics_df)
get_counts_for_ethnicity(demographics_df)
get_counts_for_death(demographics_df)