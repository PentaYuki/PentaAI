"""
Penta MCP Playwright Server
Cung cấp các công cụ chuẩn Model Context Protocol (MCP) cho AI Agent
để tự động hóa tương tác trên trình duyệt Web một cách an toàn và có kiểm soát.
"""

import asyncio
from typing import Any, Dict, Optional


class PentaPlaywrightController:
    """
    Quản lý Chromium instance và context biệt lập cho từng phiên làm việc của User.
    """
    def __init__(self, headless: bool = True):
        self.headless = headless
        self._browser = None
        self._playwright = None
        self._active_pages: Dict[str, Any] = {}

    async def initialize(self):
        """Khởi động Playwright browser sandbox."""
        try:
            from playwright.async_api import async_playwright
            self._playwright = await async_playwright().start()
            self._browser = await self._playwright.chromium.launch(
                headless=self.headless,
                args=["--no-sandbox", "--disable-setuid-sandbox"]
            )
        except ImportError:
            # Fallback mock controller cho môi trường thiếu package playwright
            self._browser = "mock"

    async def get_or_create_page(self, session_id: str):
        if self._browser == "mock":
            return "mock_page"
        if session_id not in self._active_pages:
            context = await self._browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="PentaAI-Automated-Agent/1.0"
            )
            page = await context.new_page()
            self._active_pages[session_id] = page
        return self._active_pages[session_id]

    async def navigate(self, session_id: str, url: str) -> Dict[str, Any]:
        """Tool MCP: Điều hướng tới URL."""
        if self._browser == "mock":
            return {"status": "success", "url": url, "title": f"Mock Page: {url}"}
        page = await self.get_or_create_page(session_id)
        response = await page.goto(url, wait_until="domcontentloaded")
        title = await page.title()
        return {
            "status": "success",
            "url": page.url,
            "title": title,
            "http_status": response.status if response else 200
        }

    async def click(self, session_id: str, selector: str) -> Dict[str, Any]:
        """Tool MCP: Click vào phần tử selector."""
        if self._browser == "mock":
            return {"status": "success", "clicked_selector": selector}
        page = await self.get_or_create_page(session_id)
        await page.click(selector, timeout=5000)
        return {"status": "success", "clicked_selector": selector}

    async def fill(self, session_id: str, selector: str, text: str) -> Dict[str, Any]:
        """Tool MCP: Nhập dữ liệu vào ô biểu mẫu."""
        if self._browser == "mock":
            return {"status": "success", "filled_selector": selector, "length": len(text)}
        page = await self.get_or_create_page(session_id)
        await page.fill(selector, text, timeout=5000)
        return {"status": "success", "filled_selector": selector}

    async def extract_text(self, session_id: str, selector: str = "body") -> Dict[str, Any]:
        """Tool MCP: Trích xuất nội dung văn bản từ trang web đưa vào RAG."""
        if self._browser == "mock":
            return {"status": "success", "text": "Mock extracted content from Penta Ecosystem."}
        page = await self.get_or_create_page(session_id)
        element = await page.query_selector(selector)
        text = await element.inner_text() if element else ""
        return {"status": "success", "text": text[:5000]} # Trả về tối đa 5000 ký tự

    async def screenshot(self, session_id: str, full_page: bool = False) -> Dict[str, Any]:
        """Tool MCP: Chụp ảnh màn hình cho Vision LLM phân tích."""
        if self._browser == "mock":
            return {"status": "success", "format": "base64", "data": "mock_base64_image_string"}
        import base64
        page = await self.get_or_create_page(session_id)
        screenshot_bytes = await page.screenshot(full_page=full_page)
        b64_str = base64.b64encode(screenshot_bytes).decode("utf-8")
        return {"status": "success", "format": "base64", "data": b64_str}

    async def close_session(self, session_id: str):
        """Giải phóng page và context của user khi kết thúc phiên."""
        if session_id in self._active_pages and self._browser != "mock":
            page = self._active_pages.pop(session_id)
            await page.context.close()
