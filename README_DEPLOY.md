
# PentaAI Quick Start Guide

Đây là hướng dẫn chạy prototype backend hiện tại:

1. **Cài đặt thư viện:** 
   `pip install -r pentami-core/backend/requirements.txt`

2. **Khởi chạy hệ thống:**
   `./run_server.sh`

3. **Kiểm tra API:**
   - Health check: `curl http://127.0.0.1:8000/api/health`
   - Chat endpoint: `curl -X POST http://127.0.0.1:8000/api/chat -H 'Content-Type: application/json' -d '{"query": "Hello"}'`

Backend hiện chỉ có health, app catalog và chat echo. PostgreSQL, Redis và Qdrant là service local tùy chọn trong Compose, chưa được backend kết nối.
