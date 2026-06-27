export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') return res.status(200).end();
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const { message } = req.body;
  if (!message) return res.status(400).json({ error: 'No message provided' });

  try {
    const response = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-api-key': process.env.ANTHROPIC_API_KEY,
        'anthropic-version': '2023-06-01'
      },
      body: JSON.stringify({
        model: 'claude-sonnet-4-6',
        max_tokens: 1000,
        system: 'You are CyberKavach AI — a friendly cybersecurity assistant for Indian users. Answer ONLY cybersecurity questions: phishing, OTP fraud, KYC fraud, UPI scams, lottery scams, job fraud, cyber hygiene. If asked anything else, politely redirect to cybersecurity. Support English, Bengali, Hindi — reply in the same language the user uses. Keep answers under 200 words. Always mention 1930 helpline or cybercrime.gov.in when relevant.',
        messages: [{ role: 'user', content: message }]
      })
    });

    const data = await response.json();
    const reply = data.content?.[0]?.text || 'Sorry, could not get a response.';
    res.status(200).json({ reply });
  } catch (err) {
    res.status(500).json({ error: 'Server error', details: err.message });
  }
}
