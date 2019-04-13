import pandas as pd
import urllib.request
import requests
import zipfile
import io
import os
from datetime import datetime
import sys
import tkinter as tk
from tkinter import ttk

x = datetime.now()
DateTimeSTR = '{}{}{}'.format(x.year, str(x.month).zfill(2) if len(str(x.month)) < 2 else str(x.month),
                              str(x.day).zfill(2) if len(str(x.day)) < 2 else str(x.day))

try:
    url = 'https://www.fda.gov/downloads/Drugs/InformationOnDrugs/UCM163762.zip'
    req = requests.get(url)
    ContentDisposition = req.headers['Content-Disposition']
    zipfileName = ContentDisposition[ContentDisposition.find('=') + 1:].replace('"', '')
    check = zipfileName.replace('EOBZIP', '').replace('_', '').replace('.zip', '')
    path = './{}_OrangeBook'.format(check)
    if not os.path.isdir(path):
        os.mkdir(path)
        os.chdir(path)

    else:
        os.chdir(path)
    app = tk.Tk()
    app.geometry('200x200')
    labelTop = tk.Label(app, text="選擇副檔名")
    labelTop.grid(column=0, row=0, sticky="n")

    comboExample = ttk.Combobox(app, values=[
        "csv",
        "json",
        "xlsx",
        # "h5",
        "msgpack",
    ])
    comboExample.grid(column=0, row=1, sticky="n")
    comboExample.current(0)


    def filetypesSelect(filedf, fileName, filetypesStr, check):
        if 'csv' in filetypesStr:
            filedf.to_csv('{}_{}.csv'.format(check, fileName), index=False)
        elif 'json' in filetypesStr:
            filedf.to_json('{}_{}.json'.format(check, fileName), orient="records")
        elif 'xlsx' in filetypesStr:
            filedf.to_excel('{}_{}.xlsx'.format(check, fileName), index=False)
        elif 'h5' in filetypesStr:
            with pd.HDFStore('{}_{}.h5'.format(check, fileName)) as store:
                store["{}_{}".format(check, fileName)] = filedf
        elif 'msgpack' in filetypesStr:
            filedf.to_msgpack("{}_{}.msg".format(check, fileName))
        else:
            pass
    def change_label_number():
        global url
        global zipfileName
        global comboExample
        comboExampleget = comboExample.get()
        print(comboExampleget)
        urllib.request.urlretrieve(url, zipfileName)
        print('Downloads Orange Book Data.')
        with zipfile.ZipFile(zipfileName, 'r') as zipFile:
            products = pd.read_csv(io.StringIO(zipFile.read('products.txt').decode('utf-8')), sep='~', encoding='utf-8')
            patent = pd.read_csv(io.StringIO(zipFile.read('patent.txt').decode('utf-8')), sep='~', encoding='utf-8')
            exclusivity = pd.read_csv(io.StringIO(zipFile.read('exclusivity.txt').decode('utf-8')), sep='~',
                                      encoding='utf-8')
        # 計算三份檔案資料筆數
        OrangeBookDataCounts = ''
        OrangeBookDataCounts += 'products count: {}\n'.format(len(products))
        OrangeBookDataCounts += 'patent count: {}\n'.format(len(patent))
        OrangeBookDataCounts += 'exclusivity count: {}\n'.format(len(exclusivity))
        with open('OrangeBook_DataCounts.txt', 'w') as txt:
            txt.write(OrangeBookDataCounts)
        print('Loading Orange Book Data to Excel file.')

        # filetypesSelect(filetypes, fileName, check)
        filetypesSelect(products, 'products', comboExampleget, check)
        filetypesSelect(patent, 'patent', comboExampleget, check)
        filetypesSelect(exclusivity, 'exclusivity', comboExampleget, check)
        # products.to_csv('{}_products_{}.csv'.format("OB", check), index=False)
        # patent.to_csv('{}_patent_{}.csv'.format("OB", check), index=False)
        # exclusivity.to_csv('{}_exclusivity_{}.csv'.format("OB", check), index=False)
        app.quit()


    buttonExample = tk.Button(app, text="儲存", command=change_label_number)
    buttonExample.grid(column=0, row=2)
    app.mainloop()


except Exception:
    error_Text = ''
    e_type, e_value, e_traceback = sys.exc_info()
    error_Text += f'''錯誤訊息如下：
            Errortype ==> {e_type.__name__}
            ErrorInfo ==> {e_value}
            ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
            ErrorLineOn ==> {e_traceback.tb_lineno}
            ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
    with open('errorFileLog.log', 'w+') as errorFileLog:
        errorFileLog.write(error_Text)
    print(e_type, e_value, e_traceback)
finally:
    pass
