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
    response: `☀️ It is sunnysunny todayy in ${city}.`,
    metadata: {
      city,
      forecast: "sunny",
      temperature: "28°C"
    }
  };

  res.json(response);
});


// Tool registry
const tools = {
  weather: {
    description: "Get current temperature for a city",
    parameters: { city: "string" },
    handler: (params) => {
      const { city } = params;
      // mock temperature
      return { city, temperature: 30, unit: "C" };
    },
  },
  sendEmail: {
    description: "Send a simple email (mock only)",
    parameters: { to: "string", message: "string" },
    handler: (params) => {
      console.log("Pretend sending email to:", params.to);
      return { success: true, sentTo: params.to };
    },
  },
};

// MCP metadata endpoint
app.get("/.well-known/mcp.json", (req, res) => {
  const metadata = Object.entries(tools).map(([name, tool]) => ({
    name,
    description: tool.description,
    parameters: tool.parameters,
  }));
  res.json({ tools: metadata });
});

// MCP tool call endpoint
app.post("/.well-known/mcp-call", (req, res) => {
  const { tool, parameters } = req.body;
  const selectedTool = tools[tool];
  if (!selectedTool) {
    return res.status(404).json({ error: "Tool not found" });
  }
  try {
    const result = selectedTool.handler(parameters);
    res.json({ result });
  } catch (err) {
    res.status(400).json({ error: "Tool failed", details: err.message });
  }
});

app.listen(port, '0.0.0.0', () => {
  console.log(`MCP Weather Tool running at http://0.0.0.0:${port}/weather`);
});
