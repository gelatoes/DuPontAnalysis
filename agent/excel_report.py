import os
import pandas as pd
from datetime import datetime

class ExcelReportGenerator:
    """Excel报告生成器"""
    
    def __init__(self):
        pass
    
    def format_percent(self, value):
        """格式化百分比"""
        if value is None:
            return '-'
        return f"{value * 100:.2f}%"
    
    def format_number(self, value):
        """格式化数字"""
        if value is None:
            return '-'
        return f"{value:.4f}"
    
    def set_column_width(self, worksheet, column, width):
        """设置列宽"""
        worksheet.column_dimensions[column].width = width
    
    def generate_company_dupont_sheet(self, writer, company_name, company_data):
        """生成单个公司的杜邦分析表"""
        if not company_data:
            return
        
        # 准备数据
        periods = []
        roes = []
        net_profit_ratios = []
        asset_turnovers = []
        equity_multipliers = []
        
        for period_data in company_data:
            periods.append(period_data['period'])
            roes.append(self.format_percent(period_data['roe']))
            net_profit_ratios.append(self.format_percent(period_data['net_profit_ratio']))
            asset_turnovers.append(self.format_number(period_data['asset_turnover']))
            equity_multipliers.append(self.format_number(period_data['equity_multiplier']))
        
        # 创建DataFrame
        df = pd.DataFrame({
            '周期': periods,
            '净资产收益率 (ROE)': roes,
            '销售净利率': net_profit_ratios,
            '总资产周转率': asset_turnovers,
            '权益乘数': equity_multipliers
        })
        
        # 写入Sheet
        df.to_excel(writer, sheet_name=company_name[:31], index=False)
        
        # 设置列宽
        worksheet = writer.sheets[company_name[:31]]
        self.set_column_width(worksheet, 'A', 12)
        self.set_column_width(worksheet, 'B', 16)
        self.set_column_width(worksheet, 'C', 16)
        self.set_column_width(worksheet, 'D', 16)
        self.set_column_width(worksheet, 'E', 16)
    
    def generate_vertical_analysis_sheet(self, writer, industry_results):
        """生成纵向分析Sheet"""
        all_data = []
        
        for company_name, company_data in industry_results.items():
            for period_data in company_data:
                all_data.append({
                    '公司名称': company_name,
                    '周期': period_data['period'],
                    'ROE': period_data['roe'],
                    '销售净利率': period_data['net_profit_ratio'],
                    '总资产周转率': period_data['asset_turnover'],
                    '权益乘数': period_data['equity_multiplier']
                })
        
        if not all_data:
            return
        
        df = pd.DataFrame(all_data)
        
        # 按公司和周期排序
        df = df.sort_values(['公司名称', '周期'], ascending=[True, False])
        
        # 写入Sheet
        df.to_excel(writer, sheet_name='纵向分析', index=False)
        
        # 设置列宽
        worksheet = writer.sheets['纵向分析']
        self.set_column_width(worksheet, 'A', 20)
        self.set_column_width(worksheet, 'B', 12)
        self.set_column_width(worksheet, 'C', 14)
        self.set_column_width(worksheet, 'D', 14)
        self.set_column_width(worksheet, 'E', 14)
        self.set_column_width(worksheet, 'F', 14)
    
    def generate_horizontal_analysis_sheet(self, writer, industry_results):
        """生成横向分析Sheet"""
        # 获取所有周期
        periods = []
        for results in industry_results.values():
            for res in results:
                if res['period'] not in periods:
                    periods.append(res['period'])
        
        periods.sort(reverse=True)
        
        # 为每个周期创建横向对比
        for period in periods:
            period_data = []
            
            for company_name, results in industry_results.items():
                for res in results:
                    if res['period'] == period:
                        period_data.append({
                            '公司名称': company_name,
                            'ROE': res['roe'],
                            '销售净利率': res['net_profit_ratio'],
                            '总资产周转率': res['asset_turnover'],
                            '权益乘数': res['equity_multiplier']
                        })
                        break
            
            if period_data:
                df = pd.DataFrame(period_data)
                df = df.sort_values('ROE', ascending=False)
                df['排名'] = df['ROE'].rank(ascending=False, method='min')
                
                # 重新排列列顺序
                df = df[['排名', '公司名称', 'ROE', '销售净利率', '总资产周转率', '权益乘数']]
                
                sheet_name = f'{period.replace(":", "-")}_横向对比'[:31]
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                
                # 设置列宽
                worksheet = writer.sheets[sheet_name]
                self.set_column_width(worksheet, 'A', 8)
                self.set_column_width(worksheet, 'B', 20)
                self.set_column_width(worksheet, 'C', 14)
                self.set_column_width(worksheet, 'D', 14)
                self.set_column_width(worksheet, 'E', 14)
                self.set_column_width(worksheet, 'F', 14)
    
    def generate_summary_sheet(self, writer, industry_results):
        """生成汇总Sheet"""
        # 获取所有周期
        periods = []
        for results in industry_results.values():
            for res in results:
                if res['period'] not in periods:
                    periods.append(res['period'])
        
        periods.sort(reverse=True)
        
        summary_data = []
        
        for period in periods:
            period_roes = []
            period_net_profit = []
            period_asset_turnover = []
            period_equity_multiplier = []
            
            for company_name, results in industry_results.items():
                for res in results:
                    if res['period'] == period:
                        if res['roe'] is not None:
                            period_roes.append(res['roe'])
                        if res['net_profit_ratio'] is not None:
                            period_net_profit.append(res['net_profit_ratio'])
                        if res['asset_turnover'] is not None:
                            period_asset_turnover.append(res['asset_turnover'])
                        if res['equity_multiplier'] is not None:
                            period_equity_multiplier.append(res['equity_multiplier'])
                        break
            
            if period_roes:
                summary_data.append({
                    '周期': period,
                    '公司数量': len(period_roes),
                    'ROE平均值': self.format_percent(sum(period_roes) / len(period_roes)),
                    'ROE最大值': self.format_percent(max(period_roes)),
                    'ROE最小值': self.format_percent(min(period_roes)),
                    '平均销售净利率': self.format_percent(sum(period_net_profit) / len(period_net_profit)) if period_net_profit else '-',
                    '平均总资产周转率': f"{sum(period_asset_turnover) / len(period_asset_turnover):.4f}" if period_asset_turnover else '-',
                    '平均权益乘数': f"{sum(period_equity_multiplier) / len(period_equity_multiplier):.4f}" if period_equity_multiplier else '-'
                })
        
        if summary_data:
            df = pd.DataFrame(summary_data)
            df.to_excel(writer, sheet_name='行业汇总', index=False)
            
            # 设置列宽
            worksheet = writer.sheets['行业汇总']
            self.set_column_width(worksheet, 'A', 12)
            self.set_column_width(worksheet, 'B', 10)
            self.set_column_width(worksheet, 'C', 14)
            self.set_column_width(worksheet, 'D', 14)
            self.set_column_width(worksheet, 'E', 14)
            self.set_column_width(worksheet, 'F', 14)
            self.set_column_width(worksheet, 'G', 14)
            self.set_column_width(worksheet, 'H', 14)
    
    def generate_report(self, industry_results, industry_name, output_path):
        """生成完整的Excel报告"""
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 创建Excel writer
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # 生成汇总Sheet
            self.generate_summary_sheet(writer, industry_results)
            
            # 生成纵向分析Sheet
            self.generate_vertical_analysis_sheet(writer, industry_results)
            
            # 生成横向分析Sheet
            self.generate_horizontal_analysis_sheet(writer, industry_results)
            
            # 生成各公司杜邦分析Sheet
            for company_name, company_data in industry_results.items():
                self.generate_company_dupont_sheet(writer, company_name, company_data)
        
        print(f"Excel报告已生成: {output_path}")
        return output_path

# 测试代码
if __name__ == '__main__':
    from data_reader import ExcelDataReader
    from dupont_analysis import DupontAnalyzer
    
    reader = ExcelDataReader()
    analyzer = DupontAnalyzer()
    excel_generator = ExcelReportGenerator()
    
    industry_path = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\data\食品饮料"
    industry_data = reader.parse_industry_data(industry_path)
    industry_results = analyzer.analyze_industry(industry_data)
    
    output_path = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\results\test_report.xlsx"
    excel_generator.generate_report(industry_results, '食品饮料', output_path)
