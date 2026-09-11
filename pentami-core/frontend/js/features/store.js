import { elements } from '../core/dom.js';
import { state } from '../core/state.js';
import { showToast } from '../ui/toast.js';

export function renderStoreGrid(storeApps, onChanged) {
  if (!elements.storeGrid) return;
  elements.storeGrid.replaceChildren();

  storeApps.forEach(app => {
    const installed = state.installed.has(app.id);
    const card = document.createElement('div');
    card.className = 'store-card';
    const badgeHtml = app.icon ? `<img src="${app.icon}" alt="${app.name}" class="store-card-icon-img">` : app.mono;
    card.innerHTML = `
      <div class="store-card-badge">${badgeHtml}</div>
      <div class="store-card-info">
        <div class="store-card-name">${app.name}</div>
        <div class="store-card-desc">${app.desc}</div>
      </div>
      <div class="store-card-action"><button class="btn-store-action ${installed ? 'btn-installed' : 'btn-install'}" type="button">${installed ? '✓ Đã cài' : '+ Tải về'}</button></div>
    `;

    card.querySelector('.btn-store-action').addEventListener('click', () => {
      if (state.installed.has(app.id)) {
        state.installed.delete(app.id);
        showToast(`Đã gỡ ${app.name} khỏi màn hình chính`);
      } else {
        state.installed.add(app.id);
        showToast(`Đã tải & ghim ${app.name} ra màn hình chính`);
      }
      onChanged();
    });

    elements.storeGrid.appendChild(card);
  });
}
