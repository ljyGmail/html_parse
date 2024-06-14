import oracledb

con = oracledb.connect(user="od", password="odod123#", dsn="10.205.100.209:1521/DEVDB")
cursor = con.cursor()

cursor.execute('select * from tbl_tmp_column')
lst = cursor.fetchall()

for i in lst:  # NO, XPATH, COLUMN_NM, RPT_ID
    sql = f"""
    SELECT A.RPT_ID
          , A.EXT_NO
          , B.TBL_NM
          , C.COL_NM
          , C.COL_TP
          , C.EXT_TP
          , C.EXT_PATH
    FROM TBL_EXT_200 A
       ,TBL_EXT_201 B
       ,TBL_EXT_202 C
        ,USER_TAB_COLUMNS D
    WHERE 1=1
    AND A.EXT_NO  = B.EXT_NO
    AND B.EXT_NO = C.EXT_NO
    AND A.RPT_ID IN ( {i[3]} )
     AND A.VER = ( SELECT MAX(VER) FROM TBL_EXT_200 WHERE RPT_ID = {i[3]}  )
     AND C.EXT_PATH  LIKE '%{i[1]}%'
    AND C.COL_NM = '{i[2]}'
    AND B.TBL_NM  = D.TABLE_NAME
    AND C.COL_NM = D.COLUMN_NAME
    """
    # print(sql)

    # select
    cursor.execute(sql)
    out_data = cursor.fetchall()
    print("====>", out_data)
    for item in out_data:
        # print("****>", item[2], '@@@', item[3])
        # item[2] 테이블 명  item[3]컬럼명
        select_sql = f"select {item[3]} from {item[2]} where {item[3]} is not null and rownum = 1"
        print(select_sql)
        cursor.execute(select_sql)
        select_result = cursor.fetchone()

        if select_result is not None:
            # print('%%%%> ',select_result)
            if select_result[0] is not None:
                insert_sql = f"""
                INSERT INTO TBL_TMP_TABLE (NO, TABLE_NO, XPATH, VAL) 
                VALUES ({i[0]}, '{item[2]}', '{item[6]}', '{select_result[0]}')"""
            else:
                insert_sql = f"""
                INSERT INTO TBL_TMP_TABLE (NO, TABLE_NO, XPATH, ETC) 
                VALUES ({i[0]}, '{item[2]}', '{item[6]}', 'No Result2')"""
        else:
            insert_sql = f"""
            INSERT INTO TBL_TMP_TABLE (NO, TABLE_NO, XPATH, ETC) 
            VALUES ({i[0]}, '{item[2]}', '{item[6]}', 'No Result1')"""

        print(insert_sql)
        cursor.execute(insert_sql)
con.commit()
con.close()
