import pandas as pd
import urllib.request
import requests
import zipfile
import io
import os
from datetime import datetime
import sys
import tkinter as tk

x = datetime.now()
DateTimeSTR = '{}{}{}'.format(x.year, str(x.month).zfill(2) if len(str(x.month)) < 2 else str(x.month),
                              str(x.day).zfill(2) if len(str(x.day)) < 2 else str(x.day))


def filetypesSelect(filedf, fileName, filetypesStr, check):
    if 'csv' in filetypesStr:
        filedf.to_csv('{}_{}.csv'.format(check, fileName), index=False, encoding='utf-8')
    elif 'json' in filetypesStr:
        filedf.to_json('{}_{}.json'.format(check, fileName), orient="records")
    elif 'xlsx' in filetypesStr:
        filedf.to_excel('{}_{}.xlsx'.format(check, fileName), index=False, encoding='utf-8')
    elif 'msgpack' in filetypesStr:
        filedf.to_msgpack("{}_{}.msg".format(check, fileName), encoding='utf-8')
    elif 'feather' in filetypesStr:
        filedf.to_feather('{}_{}.feather'.format(check, fileName))
    elif 'parquet' in filetypesStr:
        filedf.to_parquet('{}_{}.parquet'.format(check, fileName), engine='pyarrow', encoding='utf-8')
    elif 'pickle' in filetypesStr:
        filedf.to_pickle('{}_{}.pkl'.format(check, fileName))


def change_label_number():
    strLabel = tk.Label(window, text='處理中...')
    strLabel.pack(anchor='center')
    global url
    global zipfileName
    global comboExample
    comboExampleget = fileTypeListbox.get(fileTypeListbox.curselection())
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
    with open('OrangeBook_DataCounts.txt', 'w', encoding='utf-8') as txt:
        txt.write(OrangeBookDataCounts)
    print('Loading Orange Book Data to {}'.format(comboExampleget))
    try:
        filetypesSelect(products, 'products', comboExampleget, check)
        filetypesSelect(patent, 'patent', comboExampleget, check)
        filetypesSelect(exclusivity, 'exclusivity', comboExampleget, check)
        window.quit()
    except Exception:
        window2 = tk.Tk()
        window2.title('錯誤提示')
        window2.geometry('400x300')
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
        strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
        strLabel2.pack(anchor='center')
        window2.mainloop()

    finally:
        pass

window = tk.Tk()
window.title('請選擇輸出檔案格式(Select File Type)')
window.geometry('400x300')
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
    fileTypeVar = tk.StringVar()
    fileTypeVar.set(('csv', 'json', 'xlsx', 'msgpack', 'feather', 'parquet', 'pickle'))
    fileTypeListbox = tk.Listbox(window, listvariable=fileTypeVar)
    fileTypeListbox.pack(anchor='center')
    saveButton = tk.Button(window, text='儲存(Save)', command=change_label_number)
    saveButton.pack(anchor='center')
    window.mainloop()
except Exception:
    window2 = tk.Tk()
    window2.title('錯誤提示')
    window2.geometry('400x300')
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
    strLabel2 = tk.Label(window2, text='{}\n{}\n{}'.format(e_type, e_value, e_traceback))
    strLabel2.pack(anchor='center')
    window2.mainloop()
finally:
    pass
