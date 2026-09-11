import { elements } from '../core/dom.js';
import { state } from '../core/state.js';
import { showToast } from '../ui/toast.js';

const STORE_ICON = './assets/logo.png';

export function renderHomeGrid(storeApps, onOpenStore) {
  if (!elements.homeGrid) return;
  elements.homeGrid.replaceChildren();

  const storeTile = document.createElement('button');
  storeTile.className = 'tile';
  storeTile.title = 'Pentastore — Cửa hàng ứng dụng Penta Sys';
  storeTile.innerHTML = `<div class="mono-badge store-badge"><img src="${STORE_ICON}" alt="Pentastore Logo" class="tile-icon-img"></div><span class="tile-label">Pentastore</span>`;
  storeTile.addEventListener('click', onOpenStore);
  elements.homeGrid.appendChild(storeTile);

  storeApps.forEach(app => {
    if (!state.installed.has(app.id)) return;
    const tile = document.createElement('button');
    tile.className = 'tile';
    tile.title = `${app.name} (${app.category})`;
    const iconHtml = app.icon ? `<img src="${app.icon}" alt="${app.name}" class="tile-icon-img">` : app.mono;
    tile.innerHTML = `<div class="mono-badge">${iconHtml}</div><span class="tile-label">${app.name}</span>`;
    tile.addEventListener('click', () => showToast(`Mở ứng dụng: ${app.name}`));
    elements.homeGrid.appendChild(tile);
  });
}
