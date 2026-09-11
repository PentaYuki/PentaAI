import { storeApps } from './config/catalog.js';
import { elements } from './core/dom.js';
import { state } from './core/state.js';
import { initChat, setChatOpen } from './features/chat.js';
import { renderHomeGrid } from './features/desktop.js';
import { renderStoreGrid } from './features/store.js';

function updateClock() {
  const now = new Date();
  let hour = now.getHours() % 12 || 12;
  const minute = now.getMinutes().toString().padStart(2, '0');
  const period = now.getHours() >= 12 ? 'PM' : 'AM';
  if (elements.clock) elements.clock.textContent = `${hour}:${minute} ${period}`;
}

function setDrawerOpen(open) {
  state.drawerOpen = open;
  elements.drawer?.classList.toggle('open', open);
  elements.scrim?.classList.toggle('show', open);
  elements.dockStore?.setAttribute('aria-expanded', String(open));
  elements.dockDrawer?.setAttribute('aria-expanded', String(open));
}

function renderDesktop() {
  renderHomeGrid(storeApps, () => setDrawerOpen(true));
  renderStoreGrid(storeApps, renderDesktop);
}

function initNavigation() {
  elements.dockStore?.addEventListener('click', () => setDrawerOpen(true));
  elements.dockDrawer?.addEventListener('click', () => setDrawerOpen(!state.drawerOpen));
  elements.drawerClose?.addEventListener('click', () => setDrawerOpen(false));
  elements.scrim?.addEventListener('click', () => setDrawerOpen(false));
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape') {
      setDrawerOpen(false);
      setChatOpen(false);
    }
  });
}

function init() {
  updateClock();
  setInterval(updateClock, 1000);
  initNavigation();
  initChat();
  renderDesktop();
}

init();
