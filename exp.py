import requests
import json
import ast

url = 'https://api.finance.naver.com/siseJson.naver'#?symbol=017670&requestType=1&startTime=20200831&endTime=20210504&timeframe=day'


datas = {
'symbol': '005930',
'requestType': '1',
'startTime': '20000504',
'endTime': '20210504',
'timeframe': 'day'
}


response = requests.post(url, data= datas)

temp = ast.literal_eval(response.text.replace('\n','').replace('\t',''))
print(temp)
