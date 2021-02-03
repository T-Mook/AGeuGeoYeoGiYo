# -*- coding:utf-8 -*-
# import os, sys
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # Add parent folder reference
import pandas as pd

class excel:

    def __init__(self):
        print('=== [Complete] Excel Class Init...' + ('=' * 50))

    def lists_to_dataframes_list(self, target_lists):
        
        df_list = []
        for target_list in target_lists:
            df = pd.DataFrame(
                data=target_list,
                columns=['제목', '요약', '제공자', '주소'])
            df_list.append(df)
        
        print('[ Count DataFrame Number in list ] :' + str(len(df_list)))
        return df_list

    def dataframe_to_excelfile_multisheets(self, df_list, sheet_names_list, xlxs_dir):
        ''' df_list and sheet_names_list that match each other are saved
        in each sheet of excel file. There should be df_list and sheet_names_list
        with the same content count. '''

        if len(df_list) != len(sheet_names_list):
            print('[ ERROR ] : The number of df_list and sheet_names_list must be consumed')
            return

        # ref : https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.ExcelWriter.html
        # ref : https://rfriend.tistory.com/466
        with pd.ExcelWriter(xlxs_dir) as writer:
            for df, sheet_name in zip(df_list, sheet_names_list):
                df.to_excel(
                    writer,
                    sheet_name = sheet_name,
                    index = True,
                    index_label = "순서",
                    startrow=0,
                    startcol=0,
                    freeze_panes = (1, 0)) # (2, 0) 틀 고정

if __name__ == '__main__':
    import time
    import os
    
    ### [ Basic Settings ] ===============================================
    base_dir = "C:/Users/TMook/Documents/My Work/EASYTREND/results"
    file_basic_name = "test_search_results" # file name
    
    # [ Set Save dir and file name ] ===================================
    time_string = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
    file_name = file_basic_name + "_" + time_string + ".xlsx"
    xlxs_dir = os.path.join(base_dir, file_name)

    ### [ Test Run ] ===================================
    target_lists = [
        [[1, 2, 3], ['a', 'b', 'c']],
        [[3, 4, 5], ['a', 'b', 'c']]
    ]
    sheet_names_list = ['테스트1', '테스트2']

    excelWriter = excel()
    df_list = excelWriter.lists_to_dataframes_list(target_lists= target_lists)
    excelWriter.dataframe_to_excelfile_multisheets(
        df_list= df_list, sheet_names_list= sheet_names_list, xlxs_dir= xlxs_dir
    )
    