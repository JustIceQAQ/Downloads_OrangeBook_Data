import pandas as pd
import urllib.request
import requests
import zipfile
import io
import os
from datetime import datetime
import sys

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
    products.to_csv('OB_products_{}.csv'.format(check), index=False)
    patent.to_csv('OB_patent_{}.csv'.format(check), index=False)
    exclusivity.to_csv('OB_exclusivity_{}.csv'.format(check), index=False)
except Exception:
    mail_Text = ''
    e_type, e_value, e_traceback = sys.exc_info()
    mail_Text += f'''錯誤訊息如下：
        Errortype ==> {e_type.__name__}
        ErrorInfo ==> {e_value}
        ErrorFileName ==> {e_traceback.tb_frame.f_code.co_filename}
        ErrorLineOn ==> {e_traceback.tb_lineno}
        ErrorFunctionName ==> {e_traceback.tb_frame.f_code.co_name}'''
    with open('errorFileLog.log', 'w+') as errorFileLog:
        errorFileLog.write(errorFileLog)
    print(e_type, e_value, e_traceback)
finally:
    pass
