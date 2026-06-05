import os
import sys
from datetime import datetime
from config import DATA_DIR, RESULTS_DIR
from data_reader import ExcelDataReader
from dupont_analysis import DupontAnalyzer
from report_generator import HTMLReportGenerator
from excel_report import ExcelReportGenerator

class DupontAgent:
    """杜邦分析Agent主类"""
    
    def __init__(self):
        self.reader = ExcelDataReader()
        self.analyzer = DupontAnalyzer()
        self.html_generator = HTMLReportGenerator()
        self.excel_generator = ExcelReportGenerator()
    
    def get_output_dir(self):
        """生成输出目录"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        output_dir = os.path.join(RESULTS_DIR, f'reports_{timestamp}')
        os.makedirs(output_dir, exist_ok=True)
        return output_dir
    
    def list_industries(self):
        """列出可用行业"""
        industries = self.reader.get_available_industries(DATA_DIR)
        if not industries:
            print("❌ 未找到任何行业数据")
            return None
        
        print("\n📊 可用行业列表：")
        for i, industry in enumerate(industries, 1):
            print(f"   {i}. {industry}")
        
        return industries
    
    def select_industry(self):
        """选择行业"""
        industries = self.list_industries()
        if not industries:
            return None
        
        while True:
            try:
                choice = input("\n请输入要分析的行业编号：")
                index = int(choice) - 1
                if 0 <= index < len(industries):
                    return industries[index]
                else:
                    print(f"❌ 无效输入，请输入1-{len(industries)}之间的数字")
            except ValueError:
                print("❌ 请输入有效的数字")
    
    def run_analysis(self, industry_name):
        """运行杜邦分析"""
        print(f"\n🔍 正在分析 {industry_name} 行业...")
        
        # 构建行业路径
        industry_path = os.path.join(DATA_DIR, industry_name)
        
        # 解析行业数据
        print("   正在读取财务数据...")
        industry_data = self.reader.parse_industry_data(industry_path)
        
        if not industry_data:
            print("❌ 未能读取到任何公司数据")
            return None
        
        print(f"   ✅ 成功读取 {len(industry_data)} 家公司的数据")
        
        # 执行杜邦分析
        print("   正在执行杜邦分析...")
        industry_results = self.analyzer.analyze_industry(industry_data)
        
        if not industry_results:
            print("❌ 分析失败")
            return None
        
        print("   ✅ 杜邦分析完成")
        
        # 生成输出目录
        output_dir = self.get_output_dir()
        
        # 生成HTML报告
        print("   正在生成HTML报告...")
        html_path = os.path.join(output_dir, f'{industry_name}_杜邦分析报告.html')
        self.html_generator.generate_report(industry_results, industry_name, html_path)
        
        # 生成Excel报告
        print("   正在生成Excel报告...")
        excel_path = os.path.join(output_dir, f'{industry_name}_杜邦分析报告.xlsx')
        self.excel_generator.generate_report(industry_results, industry_name, excel_path)
        
        print(f"\n🎉 分析完成！报告已保存到：")
        print(f"   📄 HTML报告: {html_path}")
        print(f"   📊 Excel报告: {excel_path}")
        
        return {
            'output_dir': output_dir,
            'html_path': html_path,
            'excel_path': excel_path,
            'industry_results': industry_results
        }
    
    def show_analysis_results(self, industry_results):
        """显示分析结果摘要"""
        print("\n📈 杜邦分析结果摘要：")
        
        for company_name, results in industry_results.items():
            print(f"\n--- {company_name} ---")
            for res in results[:3]:  # 只显示最近3个周期
                print(f"   周期: {res['period']}")
                print(f"     ROE: {self.format_percent(res['roe'])}")
                print(f"     销售净利率: {self.format_percent(res['net_profit_ratio'])}")
                print(f"     总资产周转率: {self.format_number(res['asset_turnover'])}")
                print(f"     权益乘数: {self.format_number(res['equity_multiplier'])}")
    
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
    
    def run(self):
        """运行Agent主流程"""
        print("=" * 60)
        print("          🎯 杜邦分析法智能分析系统")
        print("=" * 60)
        print("  支持功能：")
        print("    • 行业杜邦分析报告生成")
        print("    • 企业跨期对比分析（纵向）")
        print("    • 行业同期对比分析（横向）")
        print("    • 全面对比分析")
        print("=" * 60)
        
        while True:
            # 选择行业
            industry_name = self.select_industry()
            if not industry_name:
                print("退出程序")
                break
            
            # 运行分析
            result = self.run_analysis(industry_name)
            if result:
                # 显示结果摘要
                self.show_analysis_results(result['industry_results'])
                
                # 询问是否继续
                while True:
                    choice = input("\n是否继续分析其他行业？(y/n): ").strip().lower()
                    if choice in ['y', 'n']:
                        break
                    print("请输入 y 或 n")
                
                if choice == 'n':
                    print("\n👋 感谢使用杜邦分析法智能分析系统！")
                    break

def main():
    """主函数"""
    try:
        agent = DupontAgent()
        
        # 检查命令行参数
        if len(sys.argv) > 1:
            # 使用命令行参数指定行业
            industry_name = sys.argv[1]
            print(f"🎯 分析行业: {industry_name}")
            result = agent.run_analysis(industry_name)
            if result:
                agent.show_analysis_results(result['industry_results'])
        else:
            # 交互式模式
            agent.run()
    except KeyboardInterrupt:
        print("\n\n👋 用户中断，程序退出")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
