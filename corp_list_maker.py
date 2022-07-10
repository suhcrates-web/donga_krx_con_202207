import requests, json
from database import cursor, db


cursor.execute(
    f"""
    CREATE TABLE IF NOT EXISTS krx_stuffs.corps_list(
    ISU_CD varchar(14) PRIMARY KEY,
    ISU_SRT_CD varchar(6),
    ISU_NM varchar(50),
    ISU_ABBRV varchar(50),
    LIST_DD date,
    MKT_TP_NM varchar(10),
    KIND_STKCERT_TP_NM varchar(10),
    LIST_SHRS bigint
    );
    """
)

url = 'http://data.krx.co.kr/comm/bldAttendant/getJsonData.cmd'
header = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'ko,en-US;q=0.9,en;q=0.8,ko-KR;q=0.7',
    'Connection': 'keep-alive',
    'Content-Length': '129',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Cookie': '__smVisitorID=5lIgCqzecYa; JSESSIONID=IJvDPaWhobYYYScZC9eQrluJDy960IwzaglgfMxi1UKxpMQjJ4DyLx5jahwqs8iI.bWRjX2RvbWFpbi9tZGNvd2FwMi1tZGNhcHAwMQ==',
    'Host': 'data.krx.co.kr',
    'Origin': 'http://data.krx.co.kr',
    'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020301',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'
}

data = {
'bld': 'dbms/MDC/STAT/standard/MDCSTAT01901',
'locale': 'ko_KR',
'mktId': 'ALL',
'share': '1',
'csvxls_isNo': 'false'
    }

temp = requests.post(url, data=data, headers=header)
temp = json.loads(temp.content.decode('utf-8'))['OutBlock_1']
for corp in temp:
    cursor.execute(
        f"""
    insert into krx_stuffs.corps_list values(
    "{corp['ISU_CD']}","{corp['ISU_SRT_CD']}","{corp['ISU_NM']}","{corp['ISU_ABBRV']}","{corp['LIST_DD']}","{corp['MKT_TP_NM']}","{corp['KIND_STKCERT_TP_NM']}","{corp['LIST_SHRS'].replace(',','')}"
    )
    """
    )

db.commit()