import requests, json, time
import pandas_datareader.data as web
from database import cursor, db
from datetime import date, timedelta
#### 투자자별

db_name = 'corps_naver'
table_name = '006400'  #여기선 corp_cd

##펑션구간
# 테이블 만들기
def make_table(db_name,table_name):
    cursor.execute(
        f"""
        CREATE TABLE IF NOT EXISTS {db_name}.{table_name}(
        date0 DATE PRIMARY KEY,
        open decimal(10,2),
        high decimal(10,2),
        low decimal(10,2),
        close decimal(10,2),
        vlolume bigint
        );
        """
    )


# from~end 까지 krx 데이터 받아서 sql에 저장
def naver_to_sql(from_when, end_when,db_name, table_name):
    ###  krx 헤더정보
    temp = web.DataReader(table_name, 'naver', from_when.strftime('%Y-%m-%d'), end_when.strftime('%Y-%m-%d')).to_dict('index')

    for line in temp.items():
        date0 = line[0]
        line = line[1]
        Open = line['Open'].replace(',','')
        High = line['High'].replace(',','')
        Low = line['Low'].replace(',','')
        Close = line['Close'].replace(',','')
        Volume = line['Volume'].replace(',','')

        cursor.execute(
            f"""
                INSERT INTO {db_name}.{table_name} VALUES("{date0}",{Open},{High},{Low},{Close},{Volume});
                """
        )
    db.commit()


# # 테이블 없으면 만들기


#####절차 ###
def corps_naver_go(corp_cd):
    db_name='corps_naver'
    table_name = corp_cd
    make_table(db_name, table_name)

    #### 기존데이터가 end_when보다 작으면 데이터 새로 뽑음 #####
    download0 = True
    while download0:
        cursor.execute(
            f"""
            SELECT MAX(date0) FROM {db_name}.{table_name};
            """
        )

        max_date = cursor.fetchall()[0][0]
        from_when = max_date + timedelta(days=1) if max_date != None else date(2001, 12, 1)
        end_when = date.today() - timedelta(days=1)

        if from_when == end_when:  # end_when이 오늘 이후면

            download0 = False
        else:
            # 테이블 충전
            print(f"{from_when} / {end_when}")
            naver_to_sql(from_when, end_when,db_name,  table_name)
            print(f"{from_when} / {end_when}  완료")
            time.sleep(5)

