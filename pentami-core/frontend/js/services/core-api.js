export async function sendChat({ query, sessionId, persona = 'serious', tenantId = 'tenant_penta_default' }) {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query, session_id: sessionId, persona, tenant_id: tenantId })
  });

  if (!response.ok) {
    throw new Error(`chat request failed: ${response.status}`);
  }

  return response.json();
}
