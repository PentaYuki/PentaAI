# pentami-core

`pentami-core` là lõi FastAPI tối thiểu hiện có của workspace. Backend ở `backend/main.py`; frontend tĩnh ở `frontend/` nhưng chưa được backend mount.

## Cấu trúc thực tế

```text
pentami-core/
├── backend/
│   ├── main.py          # FastAPI entrypoint
│   ├── auth/            # helper/API-key code
│   ├── memory/          # memory implementations
│   ├── rag/             # embedding/vector helpers
│   ├── voice/           # voice-related code
│   └── tests/           # test backend
├── frontend/            # static frontend
├── config/              # prompts and configuration
└── dataset/             # sample datasets
```

Các thư mục `auth`, `memory`, `rag` và `voice` có code/helper riêng nhưng chưa đồng nghĩa với việc endpoint chính đã kết nối toàn bộ capability đó.

## Chạy backend

Từ thư mục gốc repository:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r pentami-core/backend/requirements.txt
./run_server.sh
```

- OpenAPI: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`
- Chat: `POST http://127.0.0.1:8000/api/chat`

## Hợp đồng chat hiện tại

```json
{"query": "tìm file báo cáo tháng 8"}
```

`/api/chat` hiện chỉ echo `query`. Request chưa yêu cầu API key, chưa lưu session và chưa định tuyến intent. Response là JSON đồng bộ, không phải stream.

## Test

```bash
python3 -m pytest pentami-core/tests/test_core_components.py -q
```

Test cần `pytest` và dependency embedding tương ứng; có thể cài từ `backend/requirements.txt`. Test hiện kiểm tra helper/protocol, chưa phải API integration test.
