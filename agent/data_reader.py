import os
import re
import pandas as pd
from config import EXCEL_MAPPING

class ExcelDataReader:
    """Excel财务数据读取器"""
    
    def __init__(self):
        self.pattern = re.compile(r'([\d\.]+)\s*(亿|万|元)?')
    
    def convert_value(self, value):
        """将财务数据字符串转换为数值"""
        if pd.isna(value) or value is None or str(value).strip() == '' or str(value).strip() == '--':
            return None
        
        value = str(value).strip()
        
        match = self.pattern.match(value)
        if match:
            num = float(match.group(1))
            unit = match.group(2)
            
            if unit == '亿':
                return num * 100000000
            elif unit == '万':
                return num * 10000
            else:
                return num
        
        try:
            return float(value)
        except ValueError:
            return None
    
    def read_excel_file(self, file_path):
        """读取单个Excel文件"""
        try:
            # 读取资产负债表
            df_balance = pd.read_excel(file_path, sheet_name='资产负债表', header=None)
            # 读取利润表
            df_income = pd.read_excel(file_path, sheet_name='利润表', header=None)
            
            return {
                'balance_sheet': df_balance,
                'income_statement': df_income
            }
        except Exception as e:
            print(f"读取Excel文件失败: {file_path}, 错误: {e}")
            return None
    
    def extract_periods(self, df):
        """提取时间周期"""
        if df is None or df.empty:
            return []
        
        # 获取第一行作为周期（从第二列开始）
        periods = []
        for col in range(1, df.shape[1]):
            period = str(df.iloc[0, col]).strip()
            if period and period != 'nan':
                periods.append(period)
        
        return periods
    
    def extract_value(self, df, target_names):
        """从DataFrame中提取指定项目的值"""
        if df is None or df.empty:
            return None
        
        for target_name in target_names:
            for row in range(df.shape[0]):
                cell_value = str(df.iloc[row, 0]).strip()
                if cell_value == target_name:
                    values = []
                    for col in range(1, df.shape[1]):
                        val = self.convert_value(df.iloc[row, col])
                        values.append(val)
                    return values
        
        return None
    
    def parse_financial_data(self, file_path):
        """解析财务数据"""
        data = self.read_excel_file(file_path)
        if not data:
            return None
        
        balance_df = data['balance_sheet']
        income_df = data['income_statement']
        
        periods = self.extract_periods(balance_df)
        
        # 提取资产负债表数据
        balance_data = {}
        for key, names in EXCEL_MAPPING['资产负债表'].items():
            values = self.extract_value(balance_df, names)
            if values:
                balance_data[key] = values
        
        # 提取利润表数据
        income_data = {}
        for key, names in EXCEL_MAPPING['利润表'].items():
            values = self.extract_value(income_df, names)
            if values:
                income_data[key] = values
        
        return {
            'periods': periods,
            'balance_sheet': balance_data,
            'income_statement': income_data
        }
    
    def parse_industry_data(self, industry_path):
        """解析整个行业的数据"""
        companies_data = {}
        
        if not os.path.isdir(industry_path):
            return {}
        
        for filename in os.listdir(industry_path):
            if filename.endswith('.xlsx'):
                file_path = os.path.join(industry_path, filename)
                company_name = filename.replace('.xlsx', '')
                
                try:
                    fin_data = self.parse_financial_data(file_path)
                    if fin_data:
                        companies_data[company_name] = fin_data
                        print(f"成功解析: {company_name}")
                    else:
                        print(f"解析失败: {company_name}")
                except Exception as e:
                    print(f"处理文件失败 {filename}: {e}")
        
        return companies_data
    
    def get_available_industries(self, data_dir):
        """获取可用的行业列表"""
        industries = []
        if os.path.isdir(data_dir):
            for item in os.listdir(data_dir):
                item_path = os.path.join(data_dir, item)
                if os.path.isdir(item_path):
                    industries.append(item)
        return industries

# 测试代码
if __name__ == '__main__':
    reader = ExcelDataReader()
    test_file = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\data\食品饮料\SH600519_贵州茅台.xlsx"
    result = reader.parse_financial_data(test_file)
    if result:
        print("周期:", result['periods'])
        print("资产负债表:", result['balance_sheet'])
        print("利润表:", result['income_statement'])
