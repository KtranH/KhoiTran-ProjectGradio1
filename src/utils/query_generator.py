from typing import Optional, Dict, Any, List
import re

class QueryGenerator:
    def __init__(self, table_schemas: Dict[str, List[Dict[str, str]]]):
        """
        Khởi tạo với schema của các bảng trong database
        table_schemas: Dict[tên_bảng, List[Dict[tên_cột, kiểu_dữ_liệu]]]
        """
        self.table_schemas = table_schemas
        print(f"Đã tải schema cho các bảng: {', '.join(table_schemas.keys())}")

    def analyze_question(self, question: str) -> Optional[Dict[str, Any]]:
        """
        Phân tích câu hỏi và trả về thông tin cần thiết để tạo câu truy vấn
        """
        question = question.lower()
        
        # Xác định bảng cần truy vấn
        table_name = None
        for table in self.table_schemas.keys():
            # Tìm kiếm tên bảng trong câu hỏi
            table_variations = [
                table.lower(),
                table.lower().replace("_", " "),
                table.lower().replace("_", ""),
            ]
            if any(var in question for var in table_variations):
                table_name = table
                break
        
        if not table_name:
            # Thử tìm kiếm theo từ khóa
            keywords_to_tables = {
                "phòng": "rooms",
                "room": "rooms",
                "loại phòng": "room_types",
                "khách": "customers",
                "đặt phòng": "bookings",
                "booking": "bookings",
            }
            for keyword, table in keywords_to_tables.items():
                if keyword in question and table in self.table_schemas:
                    table_name = table
                    break
        
        if not table_name:
            return None
            
        # Xác định loại truy vấn
        query_type = "SELECT"
        count_keywords = ["bao nhiêu", "số lượng", "đếm", "count", "tổng số"]
        if any(keyword in question for keyword in count_keywords):
            query_type = "COUNT"
            
        # Xác định điều kiện
        conditions = []
        schema = self.table_schemas[table_name]
        
        # Mapping các từ khóa với điều kiện
        condition_mappings = {
            "trống": ("status", "=", "available"),
            "available": ("status", "=", "available"),
            "đã đặt": ("status", "=", "booked"),
            "booked": ("status", "=", "booked"),
        }
        
        # Thêm điều kiện từ mapping
        for keyword, (column, operator, value) in condition_mappings.items():
            if keyword in question:
                # Kiểm tra xem cột có tồn tại trong schema không
                if any(col["column_name"].lower() == column.lower() for col in schema):
                    conditions.append({
                        "column": column,
                        "operator": operator,
                        "value": value
                    })
        
        # Tìm các điều kiện khác từ schema
        for column in schema:
            col_name = column["column_name"].lower()
            if col_name in question:
                # Tìm giá trị cho điều kiện
                value_pattern = f"{col_name}\\s*(là|=|bằng|có giá trị|có giá|giá|có)\\s*([\\w\\s]+)"
                match = re.search(value_pattern, question)
                if match:
                    value = match.group(2).strip()
                    conditions.append({
                        "column": column["column_name"],
                        "operator": "=",
                        "value": value
                    })
        
        return {
            "table": table_name,
            "type": query_type,
            "conditions": conditions
        }

    def generate_sql_query(self, analysis: Dict[str, Any]) -> str:
        """
        Tạo câu truy vấn SQL dựa trên kết quả phân tích
        """
        if analysis["type"] == "COUNT":
            select_clause = "SELECT COUNT(*) as total"
        else:
            select_clause = "SELECT *"
            
        from_clause = f"FROM {analysis['table']}"
        
        where_clause = ""
        if analysis["conditions"]:
            conditions = []
            for cond in analysis["conditions"]:
                if isinstance(cond["value"], str):
                    value = f"'{cond['value']}'"
                else:
                    value = str(cond["value"])
                conditions.append(
                    f"{cond['column']} {cond['operator']} {value}"
                )
            where_clause = "WHERE " + " AND ".join(conditions)
        
        query_parts = [select_clause, from_clause]
        if where_clause:
            query_parts.append(where_clause)
            
        return " ".join(query_parts) 