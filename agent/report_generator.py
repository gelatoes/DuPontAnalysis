import os
from datetime import datetime

class HTMLReportGenerator:
    """HTML报告生成器"""
    
    def __init__(self):
        self.html_template = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>杜邦分析报告 - {title}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
            background-color: #f5f7fa;
            color: #333;
            line-height: 1.6;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        .tabs {{
            display: flex;
            justify-content: center;
            background-color: white;
            border-bottom: 2px solid #eee;
            position: sticky;
            top: 0;
            z-index: 100;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }}
        .tab {{
            padding: 12px 24px;
            cursor: pointer;
            border: none;
            background: none;
            font-size: 14px;
            font-weight: 500;
            color: #666;
            transition: all 0.3s;
            position: relative;
        }}
        .tab:hover {{
            color: #667eea;
        }}
        .tab.active {{
            color: #667eea;
        }}
        .tab.active::after {{
            content: '';
            position: absolute;
            bottom: -2px;
            left: 50%;
            transform: translateX(-50%);
            width: 60%;
            height: 3px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 2px;
        }}
        .content {{
            max-width: 1400px;
            margin: 20px auto;
            padding: 0 20px;
        }}
        .section {{
            background: white;
            border-radius: 12px;
            padding: 24px;
            margin-bottom: 20px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .section-title {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }}
        .table-container {{
            overflow-x: auto;
            margin-top: 10px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 14px;
        }}
        th, td {{
            padding: 12px 15px;
            text-align: center;
            border-bottom: 1px solid #eee;
        }}
        th {{
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            font-weight: 600;
            color: #555;
            white-space: nowrap;
        }}
        tr:hover {{
            background-color: #f9fafc;
        }}
        .highlight {{
            background-color: #fff3cd;
        }}
        .positive {{
            color: #28a745;
        }}
        .negative {{
            color: #dc3545;
        }}
        .kpi-card {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }}
        .card {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }}
        .card .label {{
            font-size: 14px;
            opacity: 0.9;
            margin-bottom: 8px;
        }}
        .card .value {{
            font-size: 28px;
            font-weight: 700;
        }}
        .card .change {{
            font-size: 12px;
            margin-top: 5px;
        }}
        .card.card-red {{
            background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
            box-shadow: 0 4px 15px rgba(220, 53, 69, 0.3);
        }}
        .card.card-yellow {{
            background: linear-gradient(135deg, #ffc107 0%, #e0a800 100%);
            box-shadow: 0 4px 15px rgba(255, 193, 7, 0.3);
        }}
        .card.card-blue {{
            background: linear-gradient(135deg, #007bff 0%, #0069d9 100%);
            box-shadow: 0 4px 15px rgba(0, 123, 255, 0.3);
        }}
        .card.card-green {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            box-shadow: 0 4px 15px rgba(40, 167, 69, 0.3);
        }}
        .card.green {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        }}
        .card.orange {{
            background: linear-gradient(135deg, #fd7e14 0%, #f09819 100%);
        }}
        .card.red {{
            background: linear-gradient(135deg, #dc3545 0%, #e85d75 100%);
        }}
        .chart-container {{
            min-height: 300px;
            margin: 20px 0 35px 0;
        }}
        .chart-bar {{
            display: flex;
            align-items: flex-end;
            height: 250px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }}
        .bar-group {{
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            height: 100%;
        }}
        .bar {{
            width: 40px;
            border-radius: 4px 4px 0 0;
            margin-bottom: 8px;
            transition: height 0.5s ease;
        }}
        .bar-label {{
            font-size: 11px;
            text-align: center;
            color: #666;
        }}
        .bar-value {{
            font-size: 10px;
            color: #888;
            margin-bottom: 4px;
        }}
        .period-selector {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .period-btn {{
            padding: 8px 16px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.3s;
        }}
        .period-btn:hover {{
            border-color: #667eea;
            color: #667eea;
        }}
        .period-btn.active {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-color: #667eea;
            color: white;
        }}
        .company-selector {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            flex-wrap: wrap;
        }}
        .company-btn {{
            padding: 8px 16px;
            border: 2px solid #ddd;
            background: white;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.3s;
        }}
        .company-btn:hover {{
            border-color: #28a745;
            color: #28a745;
        }}
        .company-btn.active {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            border-color: #28a745;
            color: white;
        }}
        .analysis-note {{
            background: #e7f3ff;
            border-left: 4px solid #2196F3;
            padding: 15px;
            margin-top: 20px;
            border-radius: 0 8px 8px 0;
            font-size: 14px;
            color: #336699;
        }}
        /* 图例样式 */
        .chart-legend {{
            display: flex;
            gap: 15px;
            margin-bottom: 15px;
            justify-content: center;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 13px;
            color: #666;
        }}
        .legend-color {{
            width: 16px;
            height: 16px;
            border-radius: 4px;
        }}
        /* 并列柱形图样式 */
        .chart-bar-grouped {{
            display: flex;
            gap: 20px;
            justify-content: center;
            align-items: flex-end;
            height: 300px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
        }}
        .grouped-bar-chart {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 10px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            padding: 10px;
        }}
        .grouped-bar-svg {{
            width: 100%;
            height: 360px;
        }}
        .line-chart-svg {{
            width: 100%;
            height: 360px;
        }}
        .chart-legend-rows {{
            display: grid;
            grid-template-columns: 1fr;
            gap: 8px;
            margin-bottom: 10px;
        }}
        .legend-row {{
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
        }}
        .legend-line {{
            width: 24px;
            height: 0;
            border-top: 3px solid #333;
        }}
        .legend-line.dashed {{
            border-top-style: dashed;
        }}
        .legend-line.dotdash {{
            border-top: none;
            height: 3px;
            background: repeating-linear-gradient(to right, #333 0 4px, transparent 4px 7px, #333 7px 10px, transparent 10px 14px);
        }}
        .bar-group-period {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 5px;
        }}
        .bar-item {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 3px;
        }}
        .bar-grouped {{
            width: 30px;
            border-radius: 4px 4px 0 0;
            min-height: 5px;
            transition: height 0.3s;
        }}
        .bar-grouped-label {{
            font-size: 10px;
            color: #666;
            white-space: nowrap;
        }}
        .bar-period-label {{
            font-size: 12px;
            color: #333;
            margin-top: 8px;
            white-space: nowrap;
        }}
        /* 折线图样式 */
        .line-chart {{
            display: flex;
            height: 250px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e9ecef;
            overflow: hidden;
        }}
        .y-axis {{
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            padding: 10px 5px;
            width: 30px;
            background: #e9ecef;
        }}
        .y-label {{
            font-size: 10px;
            color: #666;
            text-align: center;
        }}
        .chart-area {{
            flex: 1;
            position: relative;
            padding: 10px 0;
        }}
        .grid-lines {{
            position: absolute;
            top: 10px;
            left: 0;
            right: 0;
            bottom: 30px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}
        .grid-line {{
            height: 1px;
            background: #dee2e6;
        }}
        .trend-line {{
            position: absolute;
            top: 10px;
            left: 0;
            width: 100%;
            height: calc(100% - 40px);
        }}
        .x-axis {{
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 30px;
            display: flex;
            justify-content: space-around;
            align-items: center;
        }}
        .x-label {{
            font-size: 11px;
            color: #666;
            white-space: nowrap;
        }}
        .summary-box {{
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }}
        .summary-item {{
            flex: 1;
            min-width: 150px;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 8px;
            text-align: center;
        }}
        .summary-item .label {{
            font-size: 12px;
            color: #666;
            margin-bottom: 5px;
        }}
        .summary-item .value {{
            font-size: 18px;
            font-weight: 600;
            color: #333;
        }}
        /* 杜邦分析树状结构样式 */
        .dupont-tree {{
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 12px;
            min-height: 600px;
        }}
        .dupont-tree-map {{
            width: 100%;
            overflow-x: auto;
            padding: 10px 10px 20px 10px;
        }}
        .dupont-tree-map ul {{
            padding-top: 20px;
            position: relative;
            display: flex;
            justify-content: center;
            align-items: flex-start;
        }}
        .dupont-tree-map ul::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 50%;
            width: 0;
            height: 20px;
            border-left: 2px solid #667eea;
        }}
        .dupont-tree-map > ul::before {{
            display: none;
        }}
        .dupont-tree-map li {{
            list-style-type: none;
            text-align: center;
            position: relative;
            padding: 20px 18px 0 18px;
            min-width: 140px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .dupont-tree-map li::before,
        .dupont-tree-map li::after {{
            content: '';
            position: absolute;
            top: 0;
            width: 50%;
            height: 20px;
            border-top: 2px solid #667eea;
        }}
        .dupont-tree-map li::before {{
            right: 50%;
            border-right: 2px solid #667eea;
        }}
        .dupont-tree-map li::after {{
            left: 50%;
            border-left: 2px solid #667eea;
        }}
        .dupont-tree-map li:only-child::before,
        .dupont-tree-map li:only-child::after {{
            display: none;
        }}
        .dupont-tree-map li:only-child {{
            padding-top: 0;
        }}
        .dupont-tree-map li:first-child::before {{
            border: none;
        }}
        .dupont-tree-map li:last-child::after {{
            border: none;
        }}
        .dupont-node {{
            background: white;
            border: 2px solid #667eea;
            border-radius: 8px;
            padding: 12px 20px;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}
        .dupont-node:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 15px rgba(0,0,0,0.15);
        }}
        .dupont-node.main {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-color: #667eea;
        }}
        .dupont-node.level1 {{
            background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
            color: white;
            border-color: #28a745;
        }}
        .dupont-node.level2 {{
            background: linear-gradient(135deg, #fd7e14 0%, #f09819 100%);
            color: white;
            border-color: #fd7e14;
        }}
        .dupont-node.level3 {{
            background: white;
            color: #333;
            border-color: #dee2e6;
            font-size: 12px;
        }}
        .dupont-node.level4 {{
            background: #f8f9fa;
            color: #555;
            border-color: #ced4da;
            font-size: 11px;
            max-width: 220px;
        }}
        .dupont-node .label {{
            font-size: 12px;
            opacity: 0.8;
            margin-bottom: 4px;
        }}
        .dupont-node .value {{
            font-size: 18px;
            font-weight: 700;
        }}
        .dupont-node.main .value {{
            font-size: 24px;
        }}
        .dupont-node .formula-hint {{
            font-size: 10px;
            opacity: 0.8;
            margin-top: 4px;
            font-style: italic;
        }}
        .dupont-row {{
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-bottom: 30px;
        }}
        .dupont-connector {{
            width: 2px;
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
            height: 40px;
            margin: 0 auto;
        }}
        .dupont-connector-horizontal {{
            height: 2px;
            background: linear-gradient(90deg, transparent 0%, #667eea 50%, transparent 100%);
            margin: 10px 0;
        }}
        .dupont-subtree {{
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .dupont-section {{
            display: flex;
            gap: 40px;
            justify-content: center;
            align-items: flex-start;
        }}
        .dupont-section-title {{
            font-size: 14px;
            font-weight: 600;
            color: #666;
            margin-bottom: 15px;
            text-align: center;
        }}
        .dupont-formula {{
            font-size: 16px;
            color: #666;
            margin: 10px 0;
            font-family: monospace;
        }}
        /* 财务数据表格 */
        .financial-table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
        }}
        .financial-table th {{
            background: #f8f9fa;
            padding: 10px 12px;
            text-align: left;
            font-weight: 600;
        }}
        .financial-table td {{
            padding: 10px 12px;
            border-bottom: 1px solid #eee;
        }}
        .financial-table tr:hover {{
            background: #f9fafc;
        }}
        .financial-table .category {{
            font-weight: 600;
            background: #e9ecef;
        }}
        .financial-table .sub-item {{
            padding-left: 25px;
        }}
        /* 财务数据卡片样式 */
        .financial-cards {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            justify-content: center;
        }}
        .financial-card {{
            background: white;
            border: 2px solid #e9ecef;
            border-radius: 8px;
            padding: 10px 15px;
            min-width: 120px;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            transition: all 0.3s;
        }}
        .financial-card:hover {{
            border-color: #667eea;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
            transform: translateY(-2px);
        }}
        .financial-label {{
            font-size: 12px;
            color: #666;
            margin-bottom: 4px;
            font-weight: 500;
        }}
        .financial-value {{
            font-size: 16px;
            font-weight: 600;
            color: #333;
        }}
        .financial-section-title {{
            font-size: 13px;
            font-weight: 600;
            color: #666;
            margin-bottom: 10px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>杜邦分析报告</h1>
        <p>{subtitle}</p>
        <p style="font-size: 12px; opacity: 0.7; margin-top: 5px;">生成时间: {generate_time}</p>
    </div>

    <div class="tabs">
        {tabs_html}
    </div>

    <div class="content">
        {content_html}
    </div>

    <script>
        function showTab(tabName) {{
            document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-content').forEach(content => content.style.display = 'none');
            document.querySelector('[data-tab="' + tabName + '"]').classList.add('active');
            document.getElementById('content-' + tabName).style.display = 'block';
        }}
        
        // 杜邦分析树 - 全局状态
        var currentDupontPeriod = '';
        var currentDupontCompany = '';
        
        // 杜邦分析树 - 更新显示（同时满足公司和周期）
        function updateDupontTreeDisplay() {{
            var container = document.getElementById('content-dupont-tree');
            container.querySelectorAll('.dupont-tree-section').forEach(function(section) {{
                var matchCompany = !currentDupontCompany || section.dataset.company === currentDupontCompany;
                var matchPeriod = !currentDupontPeriod || section.dataset.period === currentDupontPeriod;
                if (matchCompany && matchPeriod) {{
                    section.style.display = 'block';
                }} else {{
                    section.style.display = 'none';
                }}
            }});
        }}
        
        // 杜邦分析树 - 按周期切换
        function showDupontTreeByPeriod(period) {{
            currentDupontPeriod = period;
            var formattedPeriod = period.split(' ')[0];
            var container = document.getElementById('content-dupont-tree');
            
            // 更新周期按钮状态
            container.querySelectorAll('.period-btn').forEach(function(btn) {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === formattedPeriod) {{
                    btn.classList.add('active');
                }}
            }});
            
            // 更新显示（同时满足公司和周期）
            updateDupontTreeDisplay();
        }}
        
        // 杜邦分析树 - 按公司切换
        function showDupontTreeByCompany(companyName) {{
            currentDupontCompany = companyName;
            var container = document.getElementById('content-dupont-tree');
            
            // 更新公司按钮状态
            container.querySelectorAll('.company-btn').forEach(function(btn) {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === companyName) {{
                    btn.classList.add('active');
                }}
            }});
            
            // 更新显示（同时满足公司和周期）
            updateDupontTreeDisplay();
        }}
        
        // 纵向分析 - 按公司切换
        function showVerticalByCompany(companyName) {{
            var container = document.getElementById('content-vertical');
            
            // 更新公司按钮状态
            container.querySelectorAll('.company-btn').forEach(function(btn) {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === companyName) {{
                    btn.classList.add('active');
                }}
            }});
            
            // 显示对应公司的数据
            container.querySelectorAll('.vertical-section').forEach(function(section) {{
                if (section.dataset.company === companyName) {{
                    section.style.display = 'block';
                }} else {{
                    section.style.display = 'none';
                }}
            }});
        }}
        
        // 横向分析 - 按周期切换
        function showHorizontalByPeriod(period) {{
            var formattedPeriod = period.split(' ')[0];
            var container = document.getElementById('content-horizontal');
            
            // 更新周期按钮状态
            container.querySelectorAll('.period-btn').forEach(function(btn) {{
                btn.classList.remove('active');
                if (btn.textContent.trim() === formattedPeriod) {{
                    btn.classList.add('active');
                }}
            }});
            
            // 显示对应周期的数据
            container.querySelectorAll('.horizontal-section').forEach(function(section) {{
                if (section.dataset.period === period) {{
                    section.style.display = 'block';
                }} else {{
                    section.style.display = 'none';
                }}
            }});
        }}
    </script>
</body>
</html>
        """
    
    def format_percent(self, value):
        """格式化百分比"""
        if value is None:
            return '-'
        return f"{value * 100:.2f}%"
    
    def format_number(self, value):
        """格式化数字"""
        if value is None:
            return '-'
        return f"{value:,.4f}"
    
    def format_currency(self, value):
        """格式化金额（单位：亿元）"""
        if value is None:
            return '-'
        if abs(value) >= 100000000:
            return f"{value / 100000000:.2f}亿"
        elif abs(value) >= 10000:
            return f"{value / 10000:.2f}万"
        return f"{value:.2f}"
    
    def generate_kpi_cards(self, data, title='关键指标'):
        """生成KPI卡片"""
        cards_html = f'<div class="section-title">{title}</div>'
        cards_html += '<div class="kpi-card">'
        
        if 'roe' in data:
            cards_html += f'''
            <div class="card card-red">
                <div class="label">净资产收益率 (ROE)</div>
                <div class="value">{self.format_percent(data['roe'])}</div>
            </div>
            '''
        
        if 'net_profit_ratio' in data:
            cards_html += f'''
            <div class="card card-yellow">
                <div class="label">销售净利率</div>
                <div class="value">{self.format_percent(data['net_profit_ratio'])}</div>
            </div>
            '''
        
        if 'asset_turnover' in data:
            cards_html += f'''
            <div class="card card-blue">
                <div class="label">总资产周转率</div>
                <div class="value">{self.format_number(data['asset_turnover'])}</div>
            </div>
            '''
        
        if 'equity_multiplier' in data:
            cards_html += f'''
            <div class="card card-green">
                <div class="label">权益乘数</div>
                <div class="value">{self.format_number(data['equity_multiplier'])}</div>
            </div>
            '''
        
        cards_html += '</div>'
        return cards_html
    
    def format_period(self, period_str):
        """格式化周期为 YYYY-MM-DD 格式"""
        if not period_str:
            return period_str
        # 去除时分秒部分
        if ' ' in period_str:
            return period_str.split(' ')[0]
        return period_str
    
    def generate_financial_cards(self, items):
        """生成财务数据按钮组件"""
        html = '<div class="financial-cards">'
        for label, value in items:
            if value and value != '-':
                html += f'''
                <div class="financial-card">
                    <div class="financial-label">{label}</div>
                    <div class="financial-value">{value}</div>
                </div>
                '''
        html += '</div>'
        return html
    
    def generate_dupont_tree(self, company_name, period_data):
        """生成经典杜邦分析树状结构（带清晰连接线）"""
        if not period_data or 'raw_data' not in period_data:
            return '<p>暂无数据</p>'
        
        raw = period_data['raw_data']
        roe = period_data['roe']
        net_profit_ratio = period_data['net_profit_ratio']
        asset_turnover = period_data['asset_turnover']
        equity_multiplier = period_data['equity_multiplier']
        asset_ratio = period_data.get('asset_ratio')
        total_asset_net_profit_ratio = period_data.get('total_asset_net_profit_ratio')
        
        # 准备财务数据按钮组件
        profit_items = [
            ('营业总收入', self.format_currency(raw['revenue'])),
            ('营业成本', self.format_currency(raw.get('cost'))),
            ('销售费用', self.format_currency(raw.get('sales_expense'))),
            ('管理费用', self.format_currency(raw.get('admin_expense'))),
            ('财务费用', self.format_currency(raw.get('finance_expense'))),
            ('净利润', self.format_currency(raw['net_profit']))
        ]
        
        asset_items = [
            ('货币资金', self.format_currency(raw.get('cash'))),
            ('应收账款', self.format_currency(raw.get('receivables'))),
            ('存货', self.format_currency(raw.get('inventory'))),
            ('流动资产', self.format_currency(raw.get('current_assets'))),
            ('非流动资产', self.format_currency(raw.get('non_current_assets'))),
            ('资产总计', self.format_currency(raw['total_assets']))
        ]
        
        liability_items = [
            ('流动负债', self.format_currency(raw.get('current_liabilities'))),
            ('非流动负债', self.format_currency(raw.get('non_current_liabilities'))),
            ('负债合计', self.format_currency(raw.get('liabilities'))),
            ('股东权益', self.format_currency(raw['equity'])),
            ('资产总计', self.format_currency(raw['total_assets']))
        ]
        
        html = f'''
        <div class="dupont-tree">
            <div class="dupont-tree-map">
                <ul>
                    <li>
                        <div class="dupont-node main">
                            <div class="label">第一层：净资产收益率 (ROE)</div>
                            <div class="value">{self.format_percent(roe)}</div>
                            <div class="formula-hint">= 总资产净利率 × 权益乘数</div>
                        </div>
                        <ul>
                            <li>
                                <div class="dupont-node level1">
                                    <div class="label">第二层：总资产净利率</div>
                                    <div class="value">{self.format_percent(total_asset_net_profit_ratio)}</div>
                                    <div class="formula-hint">= 销售净利率 × 总资产周转率</div>
                                </div>
                                <ul>
                                    <li>
                                        <div class="dupont-node level2">
                                            <div class="label">第三层：销售净利率</div>
                                            <div class="value">{self.format_percent(net_profit_ratio)}</div>
                                            <div class="formula-hint">= 净利润 / 营业收入</div>
                                        </div>
                                        <ul>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：净利润</div>
                                                    <div class="value">{self.format_currency(raw['net_profit'])}</div>
                                                    <div class="formula-hint">= 营业收入 - 成本 - 费用 - 税费</div>
                                                </div>
                                                <ul>
                                                    <li>
                                                        <div class="dupont-node level4">
                                                            <div class="label">第五层：利润表底层科目</div>
                                                            <div class="value">营收 - 成本 - 费用 - 税费等</div>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </li>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：营业收入</div>
                                                    <div class="value">{self.format_currency(raw['revenue'])}</div>
                                                </div>
                                            </li>
                                        </ul>
                                    </li>
                                    <li>
                                        <div class="dupont-node level2">
                                            <div class="label">第三层：总资产周转率</div>
                                            <div class="value">{self.format_number(asset_turnover)}</div>
                                            <div class="formula-hint">= 营业收入 / 期末总资产</div>
                                        </div>
                                        <ul>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：营业收入</div>
                                                    <div class="value">{self.format_currency(raw['revenue'])}</div>
                                                </div>
                                            </li>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：期末总资产</div>
                                                    <div class="value">{self.format_currency(raw['total_assets'])}</div>
                                                    <div class="formula-hint">= 流动资产 + 非流动资产</div>
                                                </div>
                                                <ul>
                                                    <li>
                                                        <div class="dupont-node level4">
                                                            <div class="label">第五层：资产负债表底层科目</div>
                                                            <div class="value">流动资产 + 非流动资产</div>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                            </li>
                            <li>
                                <div class="dupont-node level1">
                                    <div class="label">第二层：权益乘数</div>
                                    <div class="value">{self.format_number(equity_multiplier)}</div>
                                    <div class="formula-hint">= 1 / (1 - 资产负债率)</div>
                                </div>
                                <ul>
                                    <li>
                                        <div class="dupont-node level2">
                                            <div class="label">第三层：资产负债率</div>
                                            <div class="value">{self.format_percent(asset_ratio)}</div>
                                            <div class="formula-hint">= 总负债 / 总资产</div>
                                        </div>
                                        <ul>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：总负债合计</div>
                                                    <div class="value">{self.format_currency(raw['liabilities'])}</div>
                                                    <div class="formula-hint">= 流动负债 + 非流动负债</div>
                                                </div>
                                                <ul>
                                                    <li>
                                                        <div class="dupont-node level4">
                                                            <div class="label">第五层：资产负债表底层科目</div>
                                                            <div class="value">流动负债 + 非流动负债</div>
                                                        </div>
                                                    </li>
                                                </ul>
                                            </li>
                                            <li>
                                                <div class="dupont-node level3">
                                                    <div class="label">第四层：期末总资产</div>
                                                    <div class="value">{self.format_currency(raw['total_assets'])}</div>
                                                    <div class="formula-hint">= 流动资产 + 非流动资产</div>
                                                </div>
                                            </li>
                                        </ul>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                    </li>
                </ul>
            </div>
        </div>
        <div class="dupont-section" style="margin-top: 10px;">
            <div style="flex: 1;">
                <div class="dupont-section-title">盈利能力分析</div>
                <div class="financial-section-title">利润表关键项目</div>
                {self.generate_financial_cards(profit_items)}
            </div>
            <div style="flex: 1;">
                <div class="dupont-section-title">运营能力分析</div>
                <div class="financial-section-title">资产负债表-资产项</div>
                {self.generate_financial_cards(asset_items)}
            </div>
            <div style="flex: 1;">
                <div class="dupont-section-title">偿债能力分析</div>
                <div class="financial-section-title">负债与权益</div>
                {self.generate_financial_cards(liability_items)}
            </div>
        </div>
        '''
        return html
    

    def _build_grouped_bar_svg(self, categories, data_rows):
        metrics = [
            ('roe', '#dc3545', True),
            ('net_profit_ratio', '#ffc107', True),
            ('asset_turnover', '#007bff', False),
            ('equity_multiplier', '#28a745', False)
        ]

        left_values = []
        right_values = []
        for row in data_rows:
            for key, _, is_percent in metrics:
                value = row.get(key)
                if value is None:
                    continue
                if is_percent:
                    left_values.append(value * 100)
                else:
                    right_values.append(value)

        left_min = min(left_values + [0])
        left_max = max(left_values + [0])
        if left_min == left_max:
            left_min -= 1
            left_max += 1
        left_padding = (left_max - left_min) * 0.1
        left_min -= left_padding
        left_max += left_padding

        right_min = min(right_values + [0])
        right_max = max(right_values + [0])
        if right_min == right_max:
            right_min = 0
            right_max = right_max + 1
        right_max = max(right_max, 0)
        right_min = min(right_min, 0)

        svg_w = 1000
        svg_h = 360
        margin_left = 70
        margin_right = 70
        margin_top = 30
        margin_bottom = 60
        plot_w = svg_w - margin_left - margin_right
        plot_h = svg_h - margin_top - margin_bottom

        def left_y(value):
            return margin_top + (left_max - value) / (left_max - left_min) * plot_h

        baseline_y = left_y(0)
        baseline_y = max(margin_top, min(margin_top + plot_h, baseline_y))

        def right_y(value):
            if value >= 0:
                top_area = baseline_y - margin_top
                scale = right_max if right_max != 0 else 1
                return baseline_y - (value / scale) * top_area
            bottom_area = (margin_top + plot_h) - baseline_y
            scale = abs(right_min) if right_min != 0 else 1
            return baseline_y + (abs(value) / scale) * bottom_area

        group_count = len(categories) if categories else 1
        group_slot = plot_w / group_count
        group_width = group_slot * 0.75
        bar_width = group_width / 4 * 0.9
        gap = (group_width - bar_width * 4) / 3 if group_width > bar_width * 4 else 2

        svg_parts = [f'<svg class="grouped-bar-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">']

        svg_parts.append(f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#adb5bd" stroke-width="1"/>')
        svg_parts.append(f'<line x1="{svg_w - margin_right}" y1="{margin_top}" x2="{svg_w - margin_right}" y2="{margin_top + plot_h}" stroke="#adb5bd" stroke-width="1"/>')
        svg_parts.append(f'<line x1="{margin_left}" y1="{baseline_y}" x2="{svg_w - margin_right}" y2="{baseline_y}" stroke="#6c757d" stroke-width="1"/>')

        tick_count = 5
        for i in range(tick_count):
            value = left_min + (left_max - left_min) * (i / (tick_count - 1))
            y = left_y(value)
            svg_parts.append(f'<line x1="{margin_left}" y1="{y}" x2="{svg_w - margin_right}" y2="{y}" stroke="#e9ecef" stroke-width="1"/>')
            svg_parts.append(f'<text x="{margin_left - 8}" y="{y + 4}" text-anchor="end" font-size="10" fill="#666">{value:.1f}%</text>')

        for i in range(tick_count):
            value = right_min + (right_max - right_min) * (i / (tick_count - 1))
            if value >= 0:
                y = right_y(value)
            else:
                y = right_y(value)
            svg_parts.append(f'<text x="{svg_w - margin_right + 8}" y="{y + 4}" text-anchor="start" font-size="10" fill="#666">{value:.2f}</text>')

        for i, (category, row) in enumerate(zip(categories, data_rows)):
            group_start = margin_left + i * group_slot + (group_slot - group_width) / 2
            for idx, (key, color, is_percent) in enumerate(metrics):
                value = row.get(key) or 0
                if is_percent:
                    value_plot = value * 100
                    y_value = left_y(value_plot)
                else:
                    y_value = right_y(value)

                if y_value <= baseline_y:
                    y_top = y_value
                    height = baseline_y - y_value
                else:
                    y_top = baseline_y
                    height = y_value - baseline_y

                x = group_start + idx * (bar_width + gap)
                svg_parts.append(f'<rect x="{x}" y="{y_top}" width="{bar_width}" height="{height}" fill="{color}" rx="3" ry="3"/>')

                if is_percent:
                    display_value = f'{value * 100:.1f}%'
                else:
                    display_value = f'{value:.2f}'

                label_y = y_top - 6 if y_value <= baseline_y else y_top + height + 12
                svg_parts.append(f'<text x="{x + bar_width / 2}" y="{label_y}" text-anchor="middle" font-size="9" fill="#666">{display_value}</text>')

            label_x = group_start + group_width / 2
            svg_parts.append(f'<text x="{label_x}" y="{margin_top + plot_h + 30}" text-anchor="middle" font-size="10" fill="#666" transform="rotate(-25 {label_x} {margin_top + plot_h + 30})">{category}</text>')

        svg_parts.append('</svg>')
        return ''.join(svg_parts)

    def _build_metric_line_svg(self, periods, series, is_percent):
        all_values = []
        for item in series:
            for value in item['values']:
                if value is None:
                    continue
                all_values.append(value * 100 if is_percent else value)

        if not all_values:
            return ''

        min_val = min(all_values)
        max_val = max(all_values)
        if min_val == max_val:
            min_val -= 1
            max_val += 1
        padding = (max_val - min_val) * 0.1
        min_val -= padding
        max_val += padding

        svg_w = 1000
        svg_h = 360
        margin_left = 70
        margin_right = 30
        margin_top = 30
        margin_bottom = 60
        plot_w = svg_w - margin_left - margin_right
        plot_h = svg_h - margin_top - margin_bottom

        def y_pos(value):
            return margin_top + (max_val - value) / (max_val - min_val) * plot_h

        svg_parts = [f'<svg class="line-chart-svg" viewBox="0 0 {svg_w} {svg_h}" xmlns="http://www.w3.org/2000/svg">']
        svg_parts.append(f'<line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_h}" stroke="#adb5bd" stroke-width="1"/>')

        tick_count = 5
        for i in range(tick_count):
            value = min_val + (max_val - min_val) * (i / (tick_count - 1))
            y = y_pos(value)
            svg_parts.append(f'<line x1="{margin_left}" y1="{y}" x2="{svg_w - margin_right}" y2="{y}" stroke="#e9ecef" stroke-width="1"/>')
            label = f'{value:.1f}%' if is_percent else f'{value:.2f}'
            svg_parts.append(f'<text x="{margin_left - 8}" y="{y + 4}" text-anchor="end" font-size="10" fill="#666">{label}</text>')

        x_count = len(periods) if periods else 1
        x_step = plot_w / (x_count - 1) if x_count > 1 else 0
        x_positions = []
        for i, period in enumerate(periods):
            x = margin_left + i * x_step if x_count > 1 else margin_left + plot_w / 2
            x_positions.append(x)
            label = self.format_period(period)
            svg_parts.append(f'<text x="{x}" y="{margin_top + plot_h + 32}" text-anchor="middle" font-size="10" fill="#666" transform="rotate(-20 {x} {margin_top + plot_h + 32})">{label}</text>')

        extrema = []
        for item in series:
            for period, value in zip(periods, item['values']):
                if value is None:
                    continue
                extrema.append((period, value))

        max_point = max(extrema, key=lambda x: x[1]) if extrema else None
        min_point = min(extrema, key=lambda x: x[1]) if extrema else None

        for item in series:
            points = []
            for idx, value in enumerate(item['values']):
                if value is None:
                    points.append(None)
                    continue
                plot_value = value * 100 if is_percent else value
                points.append((x_positions[idx], y_pos(plot_value), value))

            path_points = [f'{p[0]},{p[1]}' for p in points if p is not None]
            if not path_points:
                continue
            svg_parts.append(f'<polyline points="{",".join(path_points)}" fill="none" stroke="{item["color"]}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')

            for p in points:
                if p is None:
                    continue
                svg_parts.append(f'<circle cx="{p[0]}" cy="{p[1]}" r="2.5" fill="{item["color"]}" stroke="white" stroke-width="1"/>')

        label_points = [max_point]
        if min_point and min_point != max_point:
            label_points.append(min_point)

        for label_point in label_points:
            if not label_point:
                continue
            period, value = label_point
            if period not in periods:
                continue
            x = x_positions[periods.index(period)]
            plot_value = value * 100 if is_percent else value
            y = y_pos(plot_value)
            display_value = f'{value * 100:.1f}%' if is_percent else f'{value:.2f}'
            offset = -10 if label_point == max_point else 12
            svg_parts.append(f'<text x="{x}" y="{y + offset}" text-anchor="middle" font-size="9" fill="#555">{display_value}</text>')

        svg_parts.append('</svg>')
        return ''.join(svg_parts)

    def generate_dupont_table(self, company_data, company_name):
        """生成杜邦分析表"""
        if not company_data:
            return '<p>暂无数据</p>'
        
        html = '<div class="table-container"><table>'
        html += '''
        <tr>
            <th>周期</th>
            <th>净资产收益率 (ROE)</th>
            <th>销售净利率</th>
            <th>总资产周转率</th>
            <th>权益乘数</th>
        </tr>
        '''
        
        for period_data in company_data:
            html += f'''
            <tr>
                <td>{period_data['period']}</td>
                <td>{self.format_percent(period_data['roe'])}</td>
                <td>{self.format_percent(period_data['net_profit_ratio'])}</td>
                <td>{self.format_number(period_data['asset_turnover'])}</td>
                <td>{self.format_number(period_data['equity_multiplier'])}</td>
            </tr>
            '''
        
        html += '</table></div>'
        return html
    
    def generate_vertical_analysis(self, company_data, company_name):
        """生成纵向分析（跨期对比）"""
        if not company_data or len(company_data) < 2:
            return '<p>数据不足，无法进行跨期对比</p>'
        
        html = ''
        
        categories = [self.format_period(d['period']) for d in company_data]
        data_rows = [
            {
                'roe': d.get('roe') or 0,
                'net_profit_ratio': d.get('net_profit_ratio') or 0,
                'asset_turnover': d.get('asset_turnover') or 0,
                'equity_multiplier': d.get('equity_multiplier') or 0
            }
            for d in company_data
        ]
        
        html += '<div class="chart-container">'
        html += '''
        <div class="chart-legend">
            <div class="legend-item"><span class="legend-color" style="background:#dc3545;"></span><span>ROE</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#ffc107;"></span><span>净利率</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#007bff;"></span><span>周转率</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#28a745;"></span><span>乘数</span></div>
        </div>
        <div class="grouped-bar-chart">
        '''
        html += self._build_grouped_bar_svg(categories, data_rows)
        html += '</div></div>'
        
        # 生成详细对比表
        html += '<div class="table-container"><table>'
        html += '''
        <tr>
            <th>指标</th>
            '''
        
        for period_data in company_data:
            html += f'<th>{period_data["period"]}</th>'
        
        html += '<th>变化率</th></tr>'
        
        metrics = [
            ('净资产收益率 (ROE)', 'roe'),
            ('销售净利率', 'net_profit_ratio'),
            ('总资产周转率', 'asset_turnover'),
            ('权益乘数', 'equity_multiplier')
        ]
        
        for name, key in metrics:
            html += f'<tr><td>{name}</td>'
            values = [d[key] for d in company_data]
            
            for v in values:
                if key in ['roe', 'net_profit_ratio']:
                    html += f'<td>{self.format_percent(v)}</td>'
                else:
                    html += f'<td>{self.format_number(v)}</td>'
            
            # 计算变化率
            if len(values) >= 2 and values[0] is not None and values[-1] is not None and values[-1] != 0:
                change = (values[0] - values[-1]) / abs(values[-1])
                change_color = 'positive' if change >= 0 else 'negative'
                html += f'<td class="{change_color}">{self.format_percent(change)}</td>'
            else:
                html += '<td>-</td>'
            
            html += '</tr>'
        
        html += '</table></div>'
        return html
    
    def generate_horizontal_analysis(self, industry_results, period):
        """生成横向分析（同期对比）"""
        period_data = {}
        for company_name, results in industry_results.items():
            for res in results:
                if res['period'] == period:
                    period_data[company_name] = res
                    break
        
        if not period_data:
            return '<p>该周期暂无数据</p>'
        
        # 按ROE排序
        sorted_companies = sorted(period_data.items(), key=lambda x: x[1]['roe'] or 0, reverse=True)
        
        html = '<div class="summary-box">'
        roes = [d['roe'] for d in period_data.values() if d['roe'] is not None]
        if roes:
            html += f'''
            <div class="summary-item">
                <div class="label">行业平均ROE</div>
                <div class="value">{self.format_percent(sum(roes)/len(roes))}</div>
            </div>
            <div class="summary-item">
                <div class="label">最高ROE</div>
                <div class="value">{self.format_percent(max(roes))}</div>
            </div>
            <div class="summary-item">
                <div class="label">最低ROE</div>
                <div class="value">{self.format_percent(min(roes))}</div>
            </div>
            <div class="summary-item">
                <div class="label">样本数量</div>
                <div class="value">{len(period_data)}</div>
            </div>
            '''
        html += '</div>'
        
        categories = [company_name[:8] for company_name, _ in sorted_companies]
        data_rows = [
            {
                'roe': data.get('roe') or 0,
                'net_profit_ratio': data.get('net_profit_ratio') or 0,
                'asset_turnover': data.get('asset_turnover') or 0,
                'equity_multiplier': data.get('equity_multiplier') or 0
            }
            for _, data in sorted_companies
        ]

        html += '<div class="chart-container">'
        html += '''
        <div class="chart-legend">
            <div class="legend-item"><span class="legend-color" style="background:#dc3545;"></span><span>ROE</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#ffc107;"></span><span>净利率</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#007bff;"></span><span>周转率</span></div>
            <div class="legend-item"><span class="legend-color" style="background:#28a745;"></span><span>乘数</span></div>
        </div>
        <div class="grouped-bar-chart">
        '''
        html += self._build_grouped_bar_svg(categories, data_rows)
        html += '</div></div>'
        
        # 生成详细对比表
        html += '<div class="table-container"><table>'
        html += '''
        <tr>
            <th>排名</th>
            <th>公司名称</th>
            <th>ROE</th>
            <th>销售净利率</th>
            <th>总资产周转率</th>
            <th>权益乘数</th>
        </tr>
        '''
        
        for i, (company_name, data) in enumerate(sorted_companies, 1):
            highlight = 'highlight' if i == 1 else ''
            html += f'''
            <tr class="{highlight}">
                <td>{i}</td>
                <td>{company_name}</td>
                <td>{self.format_percent(data['roe'])}</td>
                <td>{self.format_percent(data['net_profit_ratio'])}</td>
                <td>{self.format_number(data['asset_turnover'])}</td>
                <td>{self.format_number(data['equity_multiplier'])}</td>
            </tr>
            '''
        
        html += '</table></div>'
        
        # 添加分析注释
        best_company = sorted_companies[0][0] if sorted_companies else '暂无'
        html += f'''
        <div class="analysis-note">
            <strong>分析解读：</strong>
            通过横向对比，可以看出不同企业在同一时期的财务表现差异。
            ROE最高的企业在{best_company}，主要得益于较高的销售净利率和资产周转效率。
        </div>
        '''
        
        return html
    
    def generate_overall_analysis(self, industry_results, industry_name):
        """生成全面对比分析"""
        if not industry_results:
            return '<p>暂无数据</p>'
        
        # 获取所有周期
        periods = []
        for results in industry_results.values():
            for res in results:
                if res['period'] not in periods:
                    periods.append(res['period'])
        
        periods.sort(reverse=True)
        
        html = ''
        
        # 生成综合表格
        html += '<div class="table-container"><table>'
        html += '<tr><th>公司名称</th>'
        
        for period in periods:
            formatted_period = self.format_period(period)
            html += f'<th colspan="4">{formatted_period}</th>'
        
        html += '</tr>'
        
        html += '<tr><th></th>'
        for _ in periods:
            html += '<th>ROE</th><th>净利率</th><th>周转率</th><th>乘数</th>'
        html += '</tr>'
        
        for company_name, results in industry_results.items():
            html += f'<tr><td>{company_name}</td>'
            
            for period in periods:
                period_data = None
                for res in results:
                    if res['period'] == period:
                        period_data = res
                        break
                
                if period_data:
                    html += f'''
                    <td>{self.format_percent(period_data['roe'])}</td>
                    <td>{self.format_percent(period_data['net_profit_ratio'])}</td>
                    <td>{self.format_number(period_data['asset_turnover'])}</td>
                    <td>{self.format_number(period_data['equity_multiplier'])}</td>
                    '''
                else:
                    html += '<td>-</td><td>-</td><td>-</td><td>-</td>'
            
            html += '</tr>'
        
        html += '</table></div>'
        
        # 生成跨期间折线图（单画布）
        html += self.generate_trend_charts(industry_results, periods, industry_name)
        
        return html
    
    def generate_trend_charts(self, industry_results, periods, industry_name):
        """生成跨期间趋势折线图（按指标拆分）"""
        if not industry_results or not periods:
            return ''
        periods_sorted = sorted(periods)

        metrics = [
            ('roe', '净资产收益率 (ROE)', True),
            ('net_profit_ratio', '销售净利率', True),
            ('asset_turnover', '总资产周转率', False)
        ]

        company_colors = ['#dc3545', '#ffc107', '#007bff', '#28a745', '#667eea', '#fd7e14', '#17a2b8', '#6f42c1']

        charts_html = ''
        for metric_key, metric_name, is_percent in metrics:
            charts_html += f'<div class="section"><h3 class="section-title">{metric_name} - 跨期趋势</h3>'
            charts_html += '<div class="chart-container">'

            charts_html += '<div class="chart-legend" style="flex-wrap: wrap;">'
            for i, (company_name, _) in enumerate(industry_results.items()):
                charts_html += f'<div class="legend-item"><span class="legend-color" style="background:{company_colors[i % len(company_colors)]};"></span><span>{company_name}</span></div>'
            charts_html += '</div>'

            series = []
            for i, (company_name, results) in enumerate(industry_results.items()):
                values = []
                for period in periods_sorted:
                    value = None
                    for res in results:
                        if res['period'] == period:
                            value = res.get(metric_key)
                            break
                    values.append(value)
                series.append({
                    'name': company_name,
                    'color': company_colors[i % len(company_colors)],
                    'values': values
                })

            charts_html += self._build_metric_line_svg(periods_sorted, series, is_percent)
            charts_html += '</div></div>'

        return charts_html
    
    def generate_report(self, industry_results, industry_name, output_path):
        """生成完整报告"""
        generate_time = datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')
        
        # 获取所有周期
        periods = []
        for results in industry_results.values():
            for res in results:
                if res['period'] not in periods:
                    periods.append(res['period'])
        
        periods.sort(reverse=True)
        
        # 生成标签页
        tabs_html = ''
        content_html = ''
        
        # 标签1：行业概览
        tabs_html += '<button class="tab active" data-tab="overview" onclick="showTab(\'overview\')">行业概览</button>'
        
        overview_content = '<div id="content-overview" class="tab-content" style="display:block;">'
        overview_content += f'<div class="section"><h2 class="section-title">{industry_name}行业杜邦分析概览</h2>'
        
        # 显示最新周期的行业数据
        if periods:
            latest_period = periods[0]
            overview_content += f'<p style="color:#666; margin-bottom:15px;">数据周期：{latest_period}</p>'
            
            # 获取最新周期数据
            period_data = {}
            for company_name, results in industry_results.items():
                for res in results:
                    if res['period'] == latest_period:
                        period_data[company_name] = res
                        break
            
            if period_data:
                avg_roe = sum([d['roe'] for d in period_data.values() if d['roe'] is not None]) / len([d for d in period_data.values() if d['roe'] is not None])
                overview_content += self.generate_kpi_cards({
                    'roe': avg_roe,
                    'net_profit_ratio': sum([d['net_profit_ratio'] for d in period_data.values() if d['net_profit_ratio'] is not None]) / len([d for d in period_data.values() if d['net_profit_ratio'] is not None]),
                    'asset_turnover': sum([d['asset_turnover'] for d in period_data.values() if d['asset_turnover'] is not None]) / len([d for d in period_data.values() if d['asset_turnover'] is not None]),
                    'equity_multiplier': sum([d['equity_multiplier'] for d in period_data.values() if d['equity_multiplier'] is not None]) / len([d for d in period_data.values() if d['equity_multiplier'] is not None])
                }, title='行业平均指标')
        
        overview_content += '</div></div>'
        content_html += overview_content
        
        # 标签2：杜邦分析树（三层结构）
        tabs_html += '<button class="tab" data-tab="dupont-tree" onclick="showTab(\'dupont-tree\')">杜邦分析树</button>'
        
        dupont_tree_content = '<div id="content-dupont-tree" class="tab-content" style="display:none;">'
        # 添加周期选择器
        if periods:
            dupont_tree_content += '<div class="period-selector">'
            for i, period in enumerate(periods):
                active = 'active' if i == 0 else ''
                formatted_period = self.format_period(period)
                dupont_tree_content += f'<button class="period-btn {active}" onclick="showDupontTreeByPeriod(\'{period}\')">{formatted_period}</button>'
            dupont_tree_content += '</div>'
        
        # 添加公司选择器
        companies = list(industry_results.keys())
        dupont_tree_content += '<div class="company-selector">'
        for i, company_name in enumerate(companies):
            active = 'active' if i == 0 else ''
            dupont_tree_content += f'<button class="company-btn {active}" onclick="showDupontTreeByCompany(\'{company_name}\')">{company_name}</button>'
        dupont_tree_content += '</div>'
        
        # 为每个公司和周期创建杜邦分析树内容
        for company_name, company_data in industry_results.items():
            for period in periods:
                period_data = None
                for res in company_data:
                    if res['period'] == period:
                        period_data = res
                        break
                if period_data:
                    dupont_tree_content += f'<div class="section dupont-tree-section" data-company="{company_name}" data-period="{period}" style="display:none;">'
                    dupont_tree_content += f'<h2 class="section-title">{company_name} - {self.format_period(period)} 杜邦分析三层拆解</h2>'
                    dupont_tree_content += self.generate_dupont_tree(company_name, period_data)
                    dupont_tree_content += '</div>'
        
        # 显示默认内容（第一个公司和第一个周期）
        if companies and periods:
            dupont_tree_content += f'<script>currentDupontCompany = \'{companies[0]}\'; currentDupontPeriod = \'{periods[0]}\'; updateDupontTreeDisplay();</script>'
        dupont_tree_content += '</div>'
        content_html += dupont_tree_content
        
        # 标签3：纵向分析（跨期对比）
        tabs_html += '<button class="tab" data-tab="vertical" onclick="showTab(\'vertical\')">纵向分析</button>'
        
        vertical_content = '<div id="content-vertical" class="tab-content" style="display:none;">'
        # 添加公司选择器
        companies = list(industry_results.keys())
        vertical_content += '<div class="company-selector">'
        for i, company_name in enumerate(companies):
            active = 'active' if i == 0 else ''
            vertical_content += f'<button class="company-btn {active}" onclick="showVerticalByCompany(\'{company_name}\')">{company_name}</button>'
        vertical_content += '</div>'
        
        # 为每个公司创建纵向分析内容
        for company_name, company_data in industry_results.items():
            vertical_content += f'<div class="section vertical-section" data-company="{company_name}" style="display:none;">'
            vertical_content += f'<h2 class="section-title">{company_name} - 跨期对比分析</h2>'
            vertical_content += self.generate_vertical_analysis(company_data, company_name)
            vertical_content += '</div>'
        
        # 显示默认内容（第一个公司）
        if companies:
            vertical_content += f'<script>showVerticalByCompany(\'{companies[0]}\');</script>'
        vertical_content += '</div>'
        content_html += vertical_content
        
        # 标签5：横向分析（同期对比）
        tabs_html += '<button class="tab" data-tab="horizontal" onclick="showTab(\'horizontal\')">横向分析</button>'
        
        horizontal_content = '<div id="content-horizontal" class="tab-content" style="display:none;">'
        if periods:
            horizontal_content += '<div class="period-selector">'
            for i, period in enumerate(periods):
                active = 'active' if i == 0 else ''
                formatted_period = self.format_period(period)
                horizontal_content += f'<button class="period-btn {active}" onclick="showHorizontalByPeriod(\'{period}\')">{formatted_period}</button>'
            horizontal_content += '</div>'
            
            # 为每个周期创建横向分析内容
            for period in periods:
                horizontal_content += f'<div class="section horizontal-section" data-period="{period}" style="display:none;">'
                horizontal_content += f'<h2 class="section-title">{industry_name}行业 - {self.format_period(period)}同期对比</h2>'
                horizontal_content += self.generate_horizontal_analysis(industry_results, period)
                horizontal_content += '</div>'
            
            # 显示默认内容（第一个周期）
            horizontal_content += f'<script>showHorizontalByPeriod(\'{periods[0]}\');</script>'
        horizontal_content += '</div>'
        content_html += horizontal_content
        
        # 标签6：全面对比
        tabs_html += '<button class="tab" data-tab="overall-compare" onclick="showTab(\'overall-compare\')">全面对比</button>'
        
        overall_content = '<div id="content-overall-compare" class="tab-content" style="display:none;">'
        overall_content += f'<div class="section"><h2 class="section-title">{industry_name}行业 - 全面对比分析</h2>'
        overall_content += self.generate_overall_analysis(industry_results, industry_name)
        overall_content += '</div>'
        content_html += overall_content
        
        # 填充模板
        html = self.html_template.format(
            title=industry_name,
            subtitle=f'{industry_name}行业杜邦分析报告',
            generate_time=generate_time,
            tabs_html=tabs_html,
            content_html=content_html,
            industry_name=industry_name
        )
        
        # 确保目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        print(f"HTML报告已生成: {output_path}")
        return output_path

# 测试代码
if __name__ == '__main__':
    from data_reader import ExcelDataReader
    from dupont_analysis import DupontAnalyzer
    
    reader = ExcelDataReader()
    analyzer = DupontAnalyzer()
    generator = HTMLReportGenerator()
    
    industry_path = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\data\食品饮料"
    industry_data = reader.parse_industry_data(industry_path)
    industry_results = analyzer.analyze_industry(industry_data)
    
    output_path = r"d:\study\program\大信事务所合作\杜邦分析法与本量利分析\work\db\results\test_report.html"
    generator.generate_report(industry_results, '食品饮料', output_path)