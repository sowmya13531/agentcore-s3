/**
 * AIWidget.jsx — Simple Version (No Auth)
 *
 * Chat tab  → FastAPI (http://127.0.0.1:8000/api/v1/chat)
 * RAG tab   → FastAPI (http://127.0.0.1:8000/api/v1/qa)
 * Agent tab → Lambda → AgentCore (direct call, no auth needed)
 */

import { useState } from "react";

const LOCAL_API = "http://127.0.0.1:8000/api/v1";
const AGENT_API = "https://kbvrs1wla4.execute-api.ap-south-1.amazonaws.com/prod/agent";

export default function AIWidget() {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState("agent"); // Default to Agent tab
  const [input, setInput] = useState("");

  const [chatMessages, setChatMessages] = useState([]);
  const [ragMessages, setRagMessages] = useState([]);
  const [agentMessages, setAgentMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);

  // Route messages by tab
  const messages =
    tab === "chat" ? chatMessages : tab === "rag" ? ragMessages : agentMessages;

  const setMessages =
    tab === "chat"
      ? setChatMessages
      : tab === "rag"
      ? setRagMessages
      : setAgentMessages;

  // Send message to appropriate endpoint
  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setLoading(true);

    try {
      let res;

      if (tab === "agent") {
  res = await fetch(AGENT_API, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: userText,
      sessionId: sessionId,
    }),
  });
} else {
  const endpoint = tab === "chat" ? "/chat" : "/qa";

  res = await fetch(LOCAL_API + endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      message: userText,
    }),
  });
}

      if (!res.ok) {
        throw new Error(`HTTP ${res.status}`);
      }
      const data = await res.json();

if (data.sessionId) {
  setSessionId(data.sessionId);
  console.log("Session ID:", data.sessionId);
}

if (data.requestId) {
  console.log("Request ID:", data.requestId);
}

const reply =
  data.reply ||
  data.response ||
  "No response received";

setMessages((prev) => [
  ...prev,
  {
    role: "bot",
    text: reply,
    sessionId: data.sessionId,
    requestId: data.requestId,
  },
]);
     
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: `⚠️ Error: ${error.message}` },
      ]);
    }

    setLoading(false);
  };

  return (
    <>
      {/* Floating Action Button */}
      <button className="fab" onClick={() => setOpen(true)}>
        🤖
      </button>

      {open && (
        <div className="overlay" onClick={() => setOpen(false)}>
          <div className="panel" onClick={(e) => e.stopPropagation()}>
            {/* Header */}
            <div className="header">
              <div className="tabs">
                <button
                  className={tab === "chat" ? "active" : ""}
                  onClick={() => setTab("chat")}
                >
                  Chat
                </button>
                <button
                  className={tab === "rag" ? "active" : ""}
                  onClick={() => setTab("rag")}
                >
                  RAG
                </button>
                <button
                  className={tab === "agent" ? "active" : ""}
                  onClick={() => setTab("agent")}
                >
                  Agent
                </button>
              </div>
              <button className="close" onClick={() => setOpen(false)}>
                ✕
              </button>
            </div>

            {/* Messages */}
            <div className="messages">
            {tab === "agent" && sessionId && (
  <div
    style={{
      padding: "8px",
      marginBottom: "10px",
      background: "#0f172a",
      borderRadius: "8px",
      fontSize: "11px",
      color: "#00c2ff",
      wordBreak: "break-all",
    }}
  >
    Session ID: {sessionId}
  </div>
)}
              {messages.length === 0 && (
                <div className="welcome">
                  {tab === "chat"
                    ? "💬 Ask anything to VoltStream AI"
                    : tab === "rag"
                    ? "📄 Ask questions from PDF knowledge base"
                    : "🏠 Control smart devices with AI Agent\n\nExample: 'Turn on the HVAC system'"}
                </div>
              )}

              {messages.map((m, i) => (
  <div key={i} className={`msg ${m.role}`}>
    <div>{m.text}</div>

    {m.sessionId && (
      <div
        style={{
          marginTop: "8px",
          fontSize: "11px",
          color: "#94a3b8",
          wordBreak: "break-all",
        }}
      >
        Session ID: {m.sessionId}
      </div>
    )}

    {m.requestId && (
      <div
        style={{
          fontSize: "11px",
          color: "#94a3b8",
          wordBreak: "break-all",
        }}
      >
        Request ID: {m.requestId}
      </div>
    )}
  </div>
))}

              {loading && <div className="msg bot">⏳ Thinking...</div>}
            </div>

            {/* Input */}
            <div className="inputBox">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  tab === "chat"
                    ? "Ask anything..."
                    : tab === "rag"
                    ? "Ask from PDF..."
                    : "Turn on HVAC, show all devices, energy tips..."
                }
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
              />
              <button onClick={sendMessage}>Send</button>
            </div>
          </div>
        </div>
      )}

      <style>{`
        .fab {
          position: fixed;
          right: 20px;
          bottom: 20px;
          width: 60px;
          height: 60px;
          border: none;
          border-radius: 50%;
          background: #00c2ff;
          color: black;
          font-size: 24px;
          cursor: pointer;
          z-index: 9999;
          box-shadow: 0 0 20px rgba(0, 194, 255, 0.4);
          transition: transform 0.2s;
        }

        .fab:hover {
          transform: scale(1.1);
        }

        .overlay {
          position: fixed;
          inset: 0;
          background: rgba(0, 0, 0, 0.7);
          display: flex;
          justify-content: center;
          align-items: center;
          z-index: 9998;
        }

        .panel {
          width: 450px;
          height: 650px;
          background: #111827;
          color: white;
          border-radius: 18px;
          display: flex;
          flex-direction: column;
          overflow: hidden;
          border: 1px solid #1f2937;
          box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 14px;
          border-bottom: 1px solid #1f2937;
          background: #0f172a;
        }

        .tabs {
          display: flex;
          gap: 8px;
        }

        .tabs button {
          padding: 8px 14px;
          border: none;
          border-radius: 8px;
          background: #1f2937;
          color: #94a3b8;
          cursor: pointer;
          font-size: 13px;
          font-weight: 500;
          transition: all 0.2s;
        }

        .tabs button:hover {
          background: #374151;
        }

        .tabs .active {
          background: #00c2ff;
          color: black;
          font-weight: 600;
        }

        .close {
          border: none;
          background: none;
          color: white;
          cursor: pointer;
          font-size: 18px;
          padding: 0;
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          border-radius: 6px;
          transition: background 0.2s;
        }

        .close:hover {
          background: rgba(255, 255, 255, 0.1);
        }

        .messages {
          flex: 1;
          overflow-y: auto;
          padding: 16px;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }

        .welcome {
          text-align: center;
          color: #94a3b8;
          margin-top: 40px;
          font-size: 14px;
          line-height: 1.6;
          white-space: pre-wrap;
        }

        .msg {
          padding: 12px 14px;
          border-radius: 12px;
          max-width: 85%;
          word-wrap: break-word;
          font-size: 14px;
          line-height: 1.5;
        }

        .msg.user {
          align-self: flex-end;
          background: #2563eb;
          color: white;
        }

        .msg.bot {
          align-self: flex-start;
          background: #374151;
          color: #e5e7eb;
        }

        .inputBox {
          display: flex;
          gap: 8px;
          border-top: 1px solid #1f2937;
          padding: 8px;
          background: #0f172a;
        }

        .inputBox input {
          flex: 1;
          border: 1px solid #374151;
          outline: none;
          padding: 12px;
          background: #1f2937;
          color: white;
          border-radius: 8px;
          font-size: 14px;
          transition: border 0.2s;
        }

        .inputBox input:focus {
          border-color: #00c2ff;
        }

        .inputBox input::placeholder {
          color: #6b7280;
        }

        .inputBox button {
          border: none;
          padding: 12px 18px;
          background: #00c2ff;
          color: black;
          cursor: pointer;
          font-weight: 600;
          border-radius: 8px;
          font-size: 14px;
          transition: all 0.2s;
        }

        .inputBox button:hover {
          background: #00d4ff;
          transform: translateY(-1px);
        }

        .inputBox button:active {
          transform: translateY(0);
        }

        /* Scrollbar styling */
        .messages::-webkit-scrollbar {
          width: 6px;
        }

        .messages::-webkit-scrollbar-track {
          background: #1f2937;
        }

        .messages::-webkit-scrollbar-thumb {
          background: #4b5563;
          border-radius: 3px;
        }

        .messages::-webkit-scrollbar-thumb:hover {
          background: #6b7280;
        }

        /* Responsive */
        @media (max-width: 600px) {
          .panel {
            width: 100%;
            height: 100%;
            border-radius: 0;
          }

          .msg {
            max-width: 90%;
          }
        }
      `}</style>
    </>
  );
}