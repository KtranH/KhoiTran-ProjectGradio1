import pyodbc
import pandas as pd
from typing import List, Dict, Any, Optional

class DatabaseConnection:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.conn = None
        self.cursor = None

    def connect(self):
        try:
            self.conn = pyodbc.connect(self.connection_string)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Lỗi kết nối database: {str(e)}")
            return False

    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()

    def execute_query(self, query: str) -> Optional[List[Dict[str, Any]]]:
        try:
            if not self.conn or not self.cursor:
                if not self.connect():
                    return None

            self.cursor.execute(query)
            columns = [column[0] for column in self.cursor.description]
            results = []
            
            for row in self.cursor.fetchall():
                results.append(dict(zip(columns, row)))
            
            return results
        except Exception as e:
            print(f"Lỗi thực thi truy vấn: {str(e)}")
            return None

    def get_table_schema(self, table_name: str) -> Optional[List[Dict[str, str]]]:
        try:
            if not self.conn or not self.cursor:
                if not self.connect():
                    return None

            # Lấy thông tin schema của bảng
            self.cursor.execute(f"""
                SELECT COLUMN_NAME, DATA_TYPE
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = '{table_name}'
            """)
            
            schema = []
            for row in self.cursor.fetchall():
                schema.append({
                    "column_name": row[0],
                    "data_type": row[1]
                })
            
            return schema
        except Exception as e:
            print(f"Lỗi lấy schema: {str(e)}")
            return None

    def format_results_as_text(self, results: List[Dict[str, Any]]) -> str:
        if not results:
            return "Không tìm thấy kết quả."
        
        df = pd.DataFrame(results)
        return df.to_string(index=False) 