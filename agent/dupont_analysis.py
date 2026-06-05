import numpy as np

class DupontAnalyzer:
    """杜邦分析计算器"""
    
    def __init__(self):
        pass
    
    def calculate_net_profit_ratio(self, net_profit, revenue):
        """计算销售净利率 = 净利润 / 营业收入"""
        if revenue is None or revenue == 0:
            return None
        if net_profit is None:
            return None
        return net_profit / revenue
    
    def calculate_asset_turnover(self, revenue, avg_total_assets):
        """计算总资产周转率 = 营业收入 / 平均总资产"""
        if avg_total_assets is None or avg_total_assets == 0:
            return None
        if revenue is None:
            return None
        return revenue / avg_total_assets
    
    def calculate_equity_multiplier(self, avg_total_assets, avg_equity):
        """计算权益乘数 = 平均总资产 / 平均股东权益"""
        if avg_equity is None or avg_equity == 0:
            return None
        if avg_total_assets is None:
            return None
        return avg_total_assets / avg_equity
    
    def calculate_roe(self, net_profit_ratio, asset_turnover, equity_multiplier):
        """计算ROE = 销售净利率 × 总资产周转率 × 权益乘数"""
        if None in [net_profit_ratio, asset_turnover, equity_multiplier]:
            return None
        return net_profit_ratio * asset_turnover * equity_multiplier
    
    def calculate_average(self, current, previous):
        """计算平均值"""
        if current is None or previous is None:
            return current
        return (current + previous) / 2
    
    def analyze_company(self, company_data):
        """分析单个公司的杜邦指标（三层拆解）"""
        if not company_data:
            return None
        
        periods = company_data['periods']
        balance = company_data['balance_sheet']
        income = company_data['income_statement']
        
        # 获取第一层数据
        total_assets = balance.get('资产总计', [None] * len(periods))
        equity = balance.get('股东权益合计', [None] * len(periods))
        liabilities = balance.get('负债合计', [None] * len(periods))
        revenue = income.get('营业总收入', [None] * len(periods))
        net_profit = income.get('净利润', [None] * len(periods))
        
        # 如果净利润为空，尝试获取归属于母公司股东的净利润
        if all(v is None for v in net_profit):
            net_profit = income.get('归属于母公司所有者的净利润', [None] * len(periods))
        
        # 如果营业总收入为空，尝试获取营业收入
        if all(v is None for v in revenue):
            revenue = income.get('营业收入', [None] * len(periods))
        
        # 获取第二层详细数据（用于三层拆解）
        cost = income.get('营业成本', [None] * len(periods))
        sales_expense = income.get('销售费用', [None] * len(periods))
        admin_expense = income.get('管理费用', [None] * len(periods))
        finance_expense = income.get('财务费用', [None] * len(periods))
        
        # 获取资产负债表详细数据
        current_assets = balance.get('流动资产合计', [None] * len(periods))
        non_current_assets = balance.get('非流动资产合计', [None] * len(periods))
        cash = balance.get('货币资金', [None] * len(periods))
        receivables = balance.get('应收账款', [None] * len(periods))
        inventory = balance.get('存货', [None] * len(periods))
        
        results = []
        
        for i, period in enumerate(periods):
            # 当前期数据
            current_assets_val = total_assets[i]
            current_equity = equity[i]
            current_revenue = revenue[i]
            current_net_profit = net_profit[i]
            current_liabilities = liabilities[i]
            
            # 详细财务数据
            current_cost = cost[i] if i < len(cost) else None
            current_sales_expense = sales_expense[i] if i < len(sales_expense) else None
            current_admin_expense = admin_expense[i] if i < len(admin_expense) else None
            current_finance_expense = finance_expense[i] if i < len(finance_expense) else None
            current_current_assets = current_assets[i] if i < len(current_assets) else None
            current_non_current_assets = non_current_assets[i] if i < len(non_current_assets) else None
            current_cash = cash[i] if i < len(cash) else None
            current_receivables = receivables[i] if i < len(receivables) else None
            current_inventory = inventory[i] if i < len(inventory) else None
            
            # 上一期数据（用于计算平均值）
            prev_assets_val = total_assets[i+1] if i+1 < len(total_assets) else None
            prev_equity = equity[i+1] if i+1 < len(equity) else None
            
            # 计算平均值
            avg_assets = self.calculate_average(current_assets_val, prev_assets_val)
            avg_equity_val = self.calculate_average(current_equity, prev_equity)
            
            # 计算杜邦指标
            net_profit_ratio = self.calculate_net_profit_ratio(current_net_profit, current_revenue)
            asset_turnover = self.calculate_asset_turnover(current_revenue, avg_assets)
            equity_multiplier = self.calculate_equity_multiplier(avg_assets, avg_equity_val)
            roe = self.calculate_roe(net_profit_ratio, asset_turnover, equity_multiplier)
            
            # 计算第二层指标（用于三层拆解）
            gross_profit = None
            gross_profit_ratio = None
            if current_revenue and current_cost:
                gross_profit = current_revenue - current_cost
                gross_profit_ratio = gross_profit / current_revenue if current_revenue != 0 else None
            
            operating_profit = None
            operating_profit_ratio = None
            if gross_profit and current_sales_expense is not None and current_admin_expense is not None:
                operating_profit = gross_profit - current_sales_expense - current_admin_expense
                operating_profit_ratio = operating_profit / current_revenue if current_revenue != 0 else None
            
            # 资产负债率
            asset_ratio = None
            if current_assets_val and current_liabilities:
                asset_ratio = current_liabilities / current_assets_val if current_assets_val != 0 else None
            
            results.append({
                'period': period,
                'roe': roe,
                'net_profit_ratio': net_profit_ratio,
                'asset_turnover': asset_turnover,
                'equity_multiplier': equity_multiplier,
                # 第二层指标
                'gross_profit': gross_profit,
                'gross_profit_ratio': gross_profit_ratio,
                'operating_profit': operating_profit,
                'operating_profit_ratio': operating_profit_ratio,
                'asset_ratio': asset_ratio,
                # 原始数据（用于详细展示）
                'raw_data': {
                    # 基础数据
                    'total_assets': current_assets_val,
                    'equity': current_equity,
                    'liabilities': current_liabilities,
                    'revenue': current_revenue,
                    'net_profit': current_net_profit,
                    'avg_assets': avg_assets,
                    'avg_equity': avg_equity_val,
                    # 利润表详细数据
                    'cost': current_cost,
                    'sales_expense': current_sales_expense,
                    'admin_expense': current_admin_expense,
                    'finance_expense': current_finance_expense,
                    'gross_profit': gross_profit,
                    'operating_profit': operating_profit,
                    # 资产负债表详细数据
                    'current_assets': current_current_assets,
                    'non_current_assets': current_non_current_assets,
                    'cash': current_cash,
                    'receivables': current_receivables,
                    'inventory': current_inventory,
                    # 比率数据
                    'gross_profit_ratio': gross_profit_ratio,
                    'operating_profit_ratio': operating_profit_ratio,
                    'asset_ratio': asset_ratio
                }
            })
        
        return results
    
    def analyze_industry(self, industry_data):
        """分析整个行业的杜邦指标"""
        industry_results = {}
        
        for company_name, company_data in industry_data.items():
            company_results = self.analyze_company(company_data)
            if company_results:
                industry_results[company_name] = company_results
        
        return industry_results
    
    def calculate_growth_rate(self, current, previous):
        """计算增长率"""
        if previous is None or previous == 0:
            return None
        if current is None:
            return None
        return (current - previous) / abs(previous)
    
    def get_period_comparison(self, company_results, period1, period2):
        """获取两个周期的对比数据"""
        result1 = None
        result2 = None
        
        for res in company_results:
            if res['period'] == period1:
                result1 = res
            elif res['period'] == period2:
                result2 = res
        
        if not result1 or not result2:
            return None
        
        return {
            'period1': result1,
            'period2': result2,
            'growth_rates': {
                'roe': self.calculate_growth_rate(result1['roe'], result2['roe']),
                'net_profit_ratio': self.calculate_growth_rate(result1['net_profit_ratio'], result2['net_profit_ratio']),
                'asset_turnover': self.calculate_growth_rate(result1['asset_turnover'], result2['asset_turnover']),
                'equity_multiplier': self.calculate_growth_rate(result1['equity_multiplier'], result2['equity_multiplier'])
            }
        }
    
    def get_industry_period_data(self, industry_results, period):
        """获取行业在特定周期的数据"""
        period_data = {}
        
        for company_name, results in industry_results.items():
            for res in results:
                if res['period'] == period:
                    period_data[company_name] = res
                    break
        
        return period_data
    
    def get_industry_summary(self, industry_results):
        """获取行业汇总统计"""
        if not industry_results:
            return None
        
        # 获取所有周期
        periods = []
        for results in industry_results.values():
            for res in results:
                if res['period'] not in periods:
                    periods.append(res['period'])
        
        summary = {}
        
        for period in periods:
            period_data = self.get_industry_period_data(industry_results, period)
            if not period_data:
                continue
            
            roes = [data['roe'] for data in period_data.values() if data['roe'] is not None]
            net_profit_ratios = [data['net_profit_ratio'] for data in period_data.values() if data['net_profit_ratio'] is not None]
            asset_turnovers = [data['asset_turnover'] for data in period_data.values() if data['asset_turnover'] is not None]
            equity_multipliers = [data['equity_multiplier'] for data in period_data.values() if data['equity_multiplier'] is not None]
            
            summary[period] = {
                'count': len(period_data),
                'roe_avg': np.mean(roes) if roes else None,
                'roe_max': max(roes) if roes else None,
                'roe_min': min(roes) if roes else None,
                'roe_std': np.std(roes) if len(roes) > 1 else None,
                'net_profit_ratio_avg': np.mean(net_profit_ratios) if net_profit_ratios else None,
                'asset_turnover_avg': np.mean(asset_turnovers) if asset_turnovers else None,
                'equity_multiplier_avg': np.mean(equity_multipliers) if equity_multipliers else None,
                'companies': period_data
            }
        
        return summary

# 测试代码
if __name__ == '__main__':
    from data_reader import ExcelDataReader
    
    reader = ExcelDataReader()
    analyzer = DupontAnalyzer()
    
    test_file = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\data\食品饮料\SH600519_贵州茅台.xlsx"
    data = reader.parse_financial_data(test_file)
    
    if data:
        results = analyzer.analyze_company(data)
        print("杜邦分析结果:")
        for res in results:
            print(f"周期: {res['period']}")
            print(f"  ROE: {res['roe']:.2%}")
            print(f"  销售净利率: {res['net_profit_ratio']:.2%}")
            print(f"  总资产周转率: {res['asset_turnover']:.4f}")
            print(f"  权益乘数: {res['equity_multiplier']:.2f}")
            if 'raw_data' in res:
                print(f"  营业收入: {res['raw_data']['revenue']}")
                print(f"  净利润: {res['raw_data']['net_profit']}")
                print(f"  资产总计: {res['raw_data']['total_assets']}")
                print(f"  股东权益: {res['raw_data']['equity']}")
            print()
