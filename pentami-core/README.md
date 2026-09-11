# pentami-core

`pentami-core` là lõi FastAPI hiện có của workspace. Backend hiện ở `backend/main.py`; frontend tĩnh ở `frontend/`.

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
python -m pip install fastapi uvicorn pydantic
python pentami-core/backend/main.py
```

- UI: `http://127.0.0.1:8000/`
- OpenAPI: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`
- Chat: `POST http://127.0.0.1:8000/api/chat`

## Hợp đồng chat hiện tại

```json
{
  "query": "tìm file báo cáo tháng 8",
  "session_id": "sess_desktop_default",
  "persona": "serious",
  "tenant_id": "tenant_penta_default"
}
```

Router hiện là keyword matching trong process. Request chưa yêu cầu API key và chưa lưu session. Response là JSON đồng bộ, không phải stream.

## Test

```bash
python3 -m pytest pentami-core/tests/test_core_components.py -q
```

Test cần `pytest` và dependency embedding tương ứng. Repository hiện chưa có `requirements.txt` hoặc `pyproject.toml`, vì vậy dependency manifest là việc cần làm trước khi CI/production.
