const express = require('express');
const app = express();
const port = 3000;

app.use(express.json()); // Parse JSON bodies

app.post('/weather', (req, res) => {
  const { city } = req.body.args || {};

  if (!city) {
    return res.status(400).json({
      error: 'Missing "city" in args'
    });
  }

  // Simulated weather result
  const response = {
    response: `☀️ It is sunnysun today in ${city}.`,
    metadata: {
      city,
      forecast: "sunny",
      temperature: "28°C"
    }
  };

  res.json(response);
});

app.listen(port, '0.0.0.0', () => {
  console.log(`MCP Weather Tool running at http://0.0.0.0:${port}/weather`);
});
