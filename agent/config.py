import os

# 大模型配置
LLM_CONFIG = {
    "MODEL_NAME": "qwen3.7-max",
    "BASE_URL": "https://dashscope.aliyuncs.com/compatible-mode/v1",
    "API_KEY": "你的千问api key"
}

# 数据目录配置
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

# 结果目录配置
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")

# 杜邦分析指标配置
DUPONT_CONFIG = {
    "NET_PROFIT_RATIO": "销售净利率",
    "ASSET_TURNOVER": "总资产周转率",
    "EQUITY_MULTIPLIER": "权益乘数",
    "ROE": "净资产收益率"
}

# Excel表头映射
EXCEL_MAPPING = {
    "资产负债表": {
        "资产总计": ["资产总计"],
        "负债合计": ["负债合计"],
        "股东权益合计": ["股东权益合计", "所有者权益合计"],
        "归属于母公司股东权益": ["归属于母公司股东权益总计"],
        "流动资产合计": ["流动资产合计"],
        "非流动资产合计": ["非流动资产合计"],
        "存货": ["存货"],
        "应收账款": ["应收账款", "应收票据及应收账款"],
        "货币资金": ["货币资金"]
    },
    "利润表": {
        "营业总收入": ["营业总收入", "营业收入"],
        "营业收入": ["营业收入"],
        "净利润": ["净利润"],
        "归属于母公司所有者的净利润": ["归属于母公司所有者的净利润", "归属于母公司股东的净利润"],
        "营业成本": ["营业成本"],
        "销售费用": ["销售费用"],
        "管理费用": ["管理费用"],
        "财务费用": ["财务费用"]
    }
}
