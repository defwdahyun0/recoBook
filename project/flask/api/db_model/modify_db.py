import sys
import re
import json
from tqdm import tqdm
from decouple import config
sys.path.append("./project/flask/")
sys.path.append("./project/flask/api/")
from api.db_model.mysql import conn_mysqldb
from api.utils.ColumnsFromDB import *

class ModifyDB:
    def __init__(self):
        self.conn = conn_mysqldb()
        self.cursor = self.conn.cursor()

    def get_db_data(self, column: str):
        # Book table에서 column data 가져오는 함수
        sql = f"SELECT {column} FROM Book"
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def refine_description(self, description):
        # description에서 특수문자를 제거하는 함수
        description = ModifyDB().get_db_data('description')
        refined_description = []
        regex = '[^ 0-9가-힣]'
        for i in range(len(description)):
            refined_description.append(re.sub(regex, '', description[i][0]))
        return refined_description

    def save_to_json(self, refined_description):
        # refined_description을 json 파일로 저장하는 함수
        title = ModifyDB().get_db_data('title')
        isbn = ModifyDB().get_db_data('isbn13')
        author = ModifyDB().get_db_data('author')
        dict = {}
        for n, (i, t, a, d) in enumerate(zip(isbn, title, author, refined_description)):
            dict[n] = {'isbn': i[0], 'title': t[0], 'author': a[0], 'description': d}
        with open('refined_description.json', 'w', encoding='utf-8') as f:
            json.dump(dict, f, ensure_ascii=False, indent=4)
        print('refined_description.json 파일 저장 완료')
        return dict

    def insert_value_into_db(self):
        sql = "SELECT isbn13 From Book"
        storage_url = config('NCP_URL') 
        self.cursor.execute(sql)
        isbn = self.cursor.fetchall()
        for i in tqdm(isbn):
            url = f"{storage_url}{i[0]}.jpg"
            sql = f"UPDATE Book SET resizedCover = '{url}'  WHERE isbn13 = '{i[0]}'"
            self.cursor.execute(sql)
            self.conn.commit()
        print('resizedCover 컬럼 업데이트 완료')


if __name__ == '__main__':
    # raw_description = ModifyDB().get_db_data('description')
    # print(len(raw_description))
    # refined_description = ModifyDB().refine_description(raw_description)
    # print(len(refined_description))
    # ModifyDB().save_to_json(refined_description)
    ModifyDB().insert_value_into_db()