@echo off
echo 正在启动杜邦分析法智能分析系统...
echo.

:: 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误：未找到Python，请先安装Python
    pause
    exit /b 1
)

:: 检查依赖是否安装
pip list | findstr pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
)

:: 运行主程序
python main.py

echo.
echo 程序已结束
pause
