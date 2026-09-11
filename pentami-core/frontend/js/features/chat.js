import { elements } from '../core/dom.js';
import { state } from '../core/state.js';
import { sendChat } from '../services/core-api.js';

export function setChatOpen(open) {
  state.chatOpen = open;
  if (!elements.kurumiChat || !elements.kurumiLauncher) return;
  elements.kurumiChat.classList.toggle('open', open);
  elements.kurumiChat.setAttribute('aria-hidden', String(!open));
  elements.kurumiLauncher.setAttribute('aria-expanded', String(open));
  if (open) elements.kurumiInput?.focus();
}

function appendMessage(text, role, route) {
  if (!elements.kurumiMessages) return;
  const message = document.createElement('div');
  message.className = `chat-message ${role === 'user' ? 'user-message' : 'assistant-message'}`;
  message.textContent = text;
  elements.kurumiMessages.appendChild(message);

  if (route) {
    const routeLabel = document.createElement('div');
    routeLabel.className = 'chat-route';
    routeLabel.textContent = `Đã định tuyến: ${route}`;
    elements.kurumiMessages.appendChild(routeLabel);
  }

  elements.kurumiMessages.scrollTop = elements.kurumiMessages.scrollHeight;
}

export async function sendMessage(query) {
  appendMessage(query, 'user');
  if (elements.kurumiRoute) elements.kurumiRoute.textContent = 'Đang phân tích và định tuyến...';

  try {
    const data = await sendChat({ query, sessionId: state.sessionId });
    appendMessage(data.reply_text, 'assistant', data.target_app);
    if (elements.kurumiRoute) elements.kurumiRoute.textContent = `Đang ở ${data.target_app}`;
  } catch {
    appendMessage('Penta Core chưa kết nối được lúc này. Hãy khởi động backend để tiếp tục phiên làm việc.', 'assistant');
    if (elements.kurumiRoute) elements.kurumiRoute.textContent = 'Chưa kết nối backend';
  }
}

export function initChat() {
  elements.kurumiSession && (elements.kurumiSession.textContent = state.sessionId.slice(-8));
  elements.kurumiLauncher?.addEventListener('click', () => setChatOpen(!state.chatOpen));
  elements.kurumiClose?.addEventListener('click', () => setChatOpen(false));
  elements.kurumiComposer?.addEventListener('submit', event => {
    event.preventDefault();
    const query = elements.kurumiInput?.value.trim();
    if (!query) return;
    elements.kurumiInput.value = '';
    sendMessage(query);
  });
}
