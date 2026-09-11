const sessionId = sessionStorage.getItem('penta_session_id') || `sess_${crypto.randomUUID()}`;
sessionStorage.setItem('penta_session_id', sessionId);

export const state = {
  installed: new Set(),
  drawerOpen: false,
  chatOpen: false,
  sessionId
};
