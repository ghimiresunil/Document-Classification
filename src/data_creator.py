import os
import pandas as pd 
from datareader import prepare_text

class DataCreation:
    '''
    Creates data for classification
    :param file_path :type str
    :return:dataframe    :type pandasdataframe

    '''
    def __init__(self):
        self.pwd = os.getcwd()

    def readdata(self,filepath):
        df = pd.DataFrame(columns=["Data","Category"]) 
        for files in os.listdir(filepath):
            file_type = os.path.basename(files)
            sub_dir = os.path.join(filepath, file_type)
            for files in os.listdir(sub_dir):
                full_path = os.path.join(sub_dir, files) 
                try:
                    cleaned_text = prepare_text(full_path,dolower=True)
                    print("Writing data ...")
                    df.loc[len(df.index)] = [cleaned_text,file_type]
                except Exception as e: 
                    print(e)
        df.to_csv(f"{self.pwd}/data/ResumeJobData.csv")
        return df

"""" <-------------- Testing ----------------> """
if __name__ == "__main__":          
    data_obj = DataCreation()
    datapath = "data/resume_job_other_data"
    csv_file = data_obj.readdata(datapath)
    print(csv_file)