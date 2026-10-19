# 指定基底映像檔
FROM python:3.10-slim

# 設定容器內的工作目錄
WORKDIR /app

# 先複製 requirements.txt 到容器內
COPY requirements.txt .

# 安裝套件
RUN pip install --no-cache-dir -r requirements.txt

# 把原始碼複製一份放進容器裡
COPY . .

# 對外容器開放的 Port
EXPOSE 8000

# 7. 啟動伺服器的指令 (不再用 --reload，因為這是正式部署模式)
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]