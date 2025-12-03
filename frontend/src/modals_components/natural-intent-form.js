import React, { useState } from "react";
import "./group-forms.css";

function NaturalIntentForm({ mode, closeNaturalModal }) {
  const [inputType, setInputType] = useState("");
  const [inputText, setInputText] = useState("");
  const [convertedResult, setConvertedResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (inputType !== "text") {
      alert("Please select TEXT as input type first.");
      return;
    }

    if (!inputText.trim()) {
      alert("Please enter your intent.");
      return;
    }

    try {
      const response = await fetch("http://127.0.0.1:8000/api/NaturalIntent/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          user: "frontend_test",
          intent: inputText,
          timestamp: new Date().toISOString(),
        }),
      });

      if (response.ok) {
        const data = await response.json();
        setConvertedResult(JSON.stringify(data, null, 2));
      } else {
        alert("Failed to convert intent.");
      }
    } catch (error) {
      console.error(error);
      alert("Server connection failed.");
    }
  };

  return (
    <div style={{ margin: "20px" }}>
      <h3>Natural Language Intent</h3>

      {/* Input type selection → dropdown */}
      <div style={{ marginBottom: "20px" }}>
        <label style={{ display: "block", marginBottom: "8px" }}>
          Select input type:
        </label>

        <select
          value={inputType}
          onChange={(e) => setInputType(e.target.value)}
          style={{
            width: "200px",
            height: "20px",
            fontSize: "16px",
          }}
        >
          <option value="">Choose Input Type</option>
          <option value="text">Text</option>
          <option value="voice" disabled>
            Voice (coming soon)
          </option>
        </select>
      </div>

      <form onSubmit={handleSubmit}>
        {inputType === "text" && (
          <div style={{ marginBottom: "15px" }}>
            <label>Text Intent</label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="e.g., 'Continuously monitor the position of SDV_001'"
              style={{ width: "100%", height: "120px" }}
            />
          </div>
        )}

        <footer className="footer">
          <button
            type="submit"
            className={mode === "dark" ? "dark-button" : "light-button"}
            style={{ marginTop: "20px" }}
          >
            Submit
          </button>
        </footer>
      </form>

      {convertedResult && (
        <div className="converted-output">
          <h3>Converted Output</h3>
          <pre
            style={{
              background: "#eee",
              padding: "15px",
              borderRadius: "8px",
              marginTop: "20px",
              maxWidth: "800px",

              whiteSpace: "pre-wrap",
              wordBreak: "break-word",
            }}
          >
            {convertedResult}
          </pre>
        </div>
      )}
    </div>
  );
}
export default NaturalIntentForm;