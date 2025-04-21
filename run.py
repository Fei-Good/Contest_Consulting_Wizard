import subprocess
import time
import os
import signal
import sys

def run_fastapi():
    print("启动FastAPI后端服务...")
    return subprocess.Popen(["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"])

def run_streamlit():
    print("启动Streamlit前端界面...")
    return subprocess.Popen(["streamlit", "run", "app.py"])

def main():
    # 启动服务
    fastapi_process = run_fastapi()
    time.sleep(2)  # 等待FastAPI启动
    streamlit_process = run_streamlit()
    
    try:
        # 保持程序运行
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n正在关闭服务...")
        fastapi_process.terminate()
        streamlit_process.terminate()
        sys.exit(0)

if __name__ == "__main__":
    main() 