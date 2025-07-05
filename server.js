const express = require('express');
const app = express();
const port = 3000;

app.use(express.json()); // Parse JSON bodies

app.get("/weather", (req, res) => {
  const city = req.query.city;
  if (!city) return res.status(400).json({ error: "Missing city" });

  res.json({
    city,
    temperature: 30,
    unit: "Celsius",
    condition: "Sunny"
  });
});

app.get("/openapi.yaml", (req, res) => {
  res.sendFile(__dirname + "/openapi.yaml");
});


app.listen(port, '0.0.0.0', () => {
  console.log(`MCP Weather Tool running at http://0.0.0.0:${port}/weather`);
});
