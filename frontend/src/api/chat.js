export async function chatWithDeepSeek(messages, userType = 'user') {
  const response = await fetch('/api/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ messages, userType })
  })
  const data = await response.json()
  if (data.success) {
    return data.reply
  }
  throw new Error(data.message || 'API Error')
} 