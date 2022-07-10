from database import db, cursor
from corps_naver import corps_naver_go

#코스피와 코스닥
cursor.execute(
    """
    select ISU_SRT_CD, ISU_ABBRV from krx_stuffs.corps_list where MKT_TP_NM = 'KOSDAQ' or MKT_TP_NM = 'KOSPI';
    """
)
corp_list = {k:v for k,v in cursor.fetchall()}

for corp_cd in corp_list:
    print(f"{corp_cd} : {corp_list[corp_cd]}")
    corps_naver_go(corp_cd)