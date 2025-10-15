# pip install pandas openpyxl
import pandas as pd  
import datetime  
import json
  

def timestamp_to_date2(o, colname):
    if colname in o:
        o[colname] = timestamp_to_date(o[colname])


def timestamp_to_date(timestamp):  
    # 将毫秒戳转换为datetime对象  
    dt_object = datetime.datetime.fromtimestamp(timestamp/1000)  
      
    # 格式化为年月日  
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')  
      
    return formatted_date  
  
# JSON数据
io = open('json2excel.json',encoding='utf-8')
jsonstr = "".join([s.strip() for s in io.readlines()])
io.close()
json_data = json.loads(jsonstr)
list = []
# 第一行留空, 手写列头
#list.append({})
for x in json_data['list']:
  list.append(x)

#自动取列头
headers = []
if len(json_data['list']) > 0:
    row0 = json_data['list'][0]
    headers = row0.keys()

for o in list:
#     o['record_type'] = recordTypes[o['record_type']]
#     o['flow_status'] = flowStatus[o['flow_status']]
#     o['pay_status'] = payStatus[o['pay_status']]
    timestamp_to_date2(o,'create_time')

# 将JSON数据转换为pandas数据帧  
df = pd.DataFrame(list)

dt = datetime.datetime.now()
now = dt.strftime('%y%m%d_%H%M%S')
  
# 将数据帧导出为Excel XLSX文件  
df.to_excel(now+'_output.xlsx', index=False, header=headers)
# df.to_excel(now+'_output.xlsx', index=False, header=False)

