
import pandas as pd

def string_standardize(text):
    text = str(text)
    text = text.strip()
    text = re.sub(r'\s\s+', ' ', text, re.MULTILINE)
    return text


def input_excel(excel_path, sheet_name):
    df = pd.read_excel(excel_path, 
            sheet_name=sheet_name, 
            header=0, 
            na_values='N/A',
            keep_default_na=False)

    # strip all strings from excel database
    df.replace(r'(^\s+|\s+$)', '', regex=True, inplace=True)
    df.replace(r'(\s+)', ' ', regex=True, inplace=True)
    df.replace(r'(\s*\,\s*)', ',', regex=True, inplace=True)
    return df


class Data():
    teachers = input_excel('data.xlsx', 'teachers')
    teachers['improper_class_names'] = teachers['improper_class_names'].apply(lambda x: x.split(',') if x.split(',')!=[''] else [])
    teachers['predefined_days_off'] = teachers['predefined_days_off'].apply(lambda x: x.split(',') if x.split(',')!=[''] else [])
    classes = input_excel('data.xlsx', 'classes')
    classes['time_frames'] = classes['time_frames'].apply(lambda x: x.split(',') if x.split(',')!=[''] else [])
    
'''
data = Data()
print((data.teachers['predefined_days_off']))
print((data.teachers.loc[0, 'predefined_days_off']))
'''