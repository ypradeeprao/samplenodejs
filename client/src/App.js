import React, { useEffect, useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [num1, setNum1] = useState("");
  const [num2, setNum2] = useState("");
  const [operator, setOperator] = useState("+");
  const [calcResult, setCalcResult] = useState("");

  useEffect(() => {
    // Fetch welcome message
    fetch("http://localhost:5000/api/message")
      .then(res => res.json())
      .then(data => setMessage(data.message))
      .catch(err => console.error("Error fetching message:", err));

    // Send test prompt to AI
    fetch("http://localhost:5000/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt: "What is the capital of France?" })
    })
      .then(res => res.json())
      .then(data => setAiResponse(data.response))
      .catch(err => console.error("Error calling AI:", err));
  }, []);

 const handleCalculate = () => {
  fetch("http://localhost:5000/api/calculate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      num1,
      num2,
      operator
    })
  })
    .then(res => res.json())
    .then(data => {
      if (data.result !== undefined) {
        setCalcResult(`Result: ${data.result}`);
        setAiResponse(data.explanation); // 🧠 update AI explanation section
      } else {
        setCalcResult(`Error: ${data.error}`);
        setAiResponse(""); // clear previous explanation
      }
    })
    .catch(err => {
      setCalcResult("Error: " + err.message);
      setAiResponse("");
    });
};

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <h1>React + Flask (venv)</h1>
      <p>{message}</p>

      <h2>🔮 AI Response:</h2>
      <p>{aiResponse}</p>

      <h2>🧮 Calculator</h2>
      <div>
        <input
          type="number"
          value={num1}
          onChange={e => setNum1(e.target.value)}
          placeholder="Number 1"
        />
        <select value={operator} onChange={e => setOperator(e.target.value)}>
          <option value="+">+</option>
          <option value="-">−</option>
          <option value="*">×</option>
          <option value="/">÷</option>
        </select>
        <input
          type="number"
          value={num2}
          onChange={e => setNum2(e.target.value)}
          placeholder="Number 2"
        />
        <button onClick={handleCalculate}>Calculate</button>
      </div>
      <p>{calcResult}</p>
    </div>
  );
}

export default App;
