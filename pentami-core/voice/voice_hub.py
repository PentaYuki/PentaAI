"""
Penta Realtime Voice Hub
Điều phối luồng âm thanh đàm thoại 2 chiều với độ trễ siêu thấp:
- STT: Deepgram Nova-2 Streaming WebSocket (~200ms latency)
- TTS: ElevenLabs Streaming WebSocket (~300ms latency)
"""

import asyncio
from typing import AsyncGenerator, Callable, Optional


class VoiceHubConfig:
    def __init__(
        self,
        deepgram_api_key: str = "",
        elevenlabs_api_key: str = "",
        elevenlabs_voice_id: str = "21m00Tcm4TlvDq8ikWAM", # Default voice
        sample_rate: int = 16000,
        language: str = "vi" # Tiếng Việt
    ):
        self.deepgram_api_key = deepgram_api_key
        self.elevenlabs_api_key = elevenlabs_api_key
        self.elevenlabs_voice_id = elevenlabs_voice_id
        self.sample_rate = sample_rate
        self.language = language


class RealtimeVoiceSession:
    """
    Quản lý 1 phiên đàm thoại giọng nói thời gian thực giữa User và AI Avatar.
    """
    def __init__(self, session_id: str, config: VoiceHubConfig):
        self.session_id = session_id
        self.config = config
        self.is_active = False

    async def start(self):
        """Khởi động kết nối WebSocket tới Deepgram và ElevenLabs."""
        self.is_active = True

    async def stream_audio_input(self, audio_chunk: bytes) -> Optional[str]:
        """
        Nhận gói PCM audio từ Micro của User và gửi tới Deepgram WebSocket.
        Trả về interim transcript hoặc final transcript khi nhận diện xong từ.
        """
        # Giả lập pipeline stream âm thanh
        return None

    async def stream_tts_output(self, text_generator: AsyncGenerator[str, None]) -> AsyncGenerator[bytes, None]:
        """
        Nhận token text từ LLM theo dạng streaming, đẩy ngay sang ElevenLabs
        và trả về các chunk âm thanh nhị phân (PCM / MP3) để Client phát loa ngay lập tức.
        """
        async for phrase in text_generator:
            if phrase.strip():
                # Stream chunk âm thanh về client
                yield b"\x00" * 320 # Binary audio chunk placeholder
                await asyncio.sleep(0.02)

    async def stop(self):
        """Đóng phiên đàm thoại."""
        self.is_active = False
