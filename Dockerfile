# 使用官方Python運行時作為母映像
FROM python:3.9-slim

# 設置工作目錄為/app
WORKDIR /app

# 將當前目錄內容複製到容器的/app
COPY . /app

# 安裝requirements.txt中列出的所有依賴
RUN pip install --no-cache-dir -r requirements.txt

# 讓世界可以訪問您的應用
EXPOSE 8080

# 定義環境變數
ENV NAME World

# 在容器啟動時運行app.py
CMD ["python", "app.py"]
