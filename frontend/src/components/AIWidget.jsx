/**
 * AIWidget.jsx — Production version
 *
 * Chat tab  → calls FastAPI locally (http://127.0.0.1:8000/api/v1/chat)
 * RAG tab   → calls FastAPI locally (http://127.0.0.1:8000/api/v1/qa)
 * Agent tab → calls API Gateway + Lambda + AgentCore with Cognito JWT auth
 *
 * Drop-in replacement for the original AIWidget.jsx.
 * Requires useAuth.js and LoginModal.jsx in the same folder.
 * Requires VITE_API_URL in frontend/.env
 */

import { useState } from "react";
import { useAuth } from "./useAuth";
import LoginModal from "./LoginModal";

// ── Endpoints ────────────────────────────────────────────────────────────────
const LOCAL_API = "http://127.0.0.1:8000/api/v1";           // FastAPI (Chat + RAG)
const AGENT_API = import.meta.env.VITE_API_URL + "/agent";   // API Gateway → Lambda → AgentCore

export default function AIWidget() {
  const [open, setOpen] = useState(false);
  const [tab, setTab]   = useState("chat");
  const [input, setInput] = useState("");

  const [chatMessages,  setChatMessages]  = useState([]);
  const [ragMessages,   setRagMessages]   = useState([]);
  const [agentMessages, setAgentMessages] = useState([]);

  const [loading, setLoading]     = useState(false);
  const [showLogin, setShowLogin] = useState(false);

  const { user, login, logout, getIdToken } = useAuth();

  // ── Message state routing (identical pattern to original) ─────────────────
  const messages =
    tab === "chat"  ? chatMessages  :
    tab === "rag"   ? ragMessages   :
                      agentMessages;

  const setMessages =
    tab === "chat"  ? setChatMessages  :
    tab === "rag"   ? setRagMessages   :
                      setAgentMessages;

  // ── Tab click handler — Agent tab requires login ──────────────────────────
  const handleTabClick = (newTab) => {
    setTab(newTab);
    if (newTab === "agent" && !user) {
      setShowLogin(true);
    }
  };

  // ── Send message ──────────────────────────────────────────────────────────
  const sendMessage = async () => {
    if (!input.trim()) return;

    // Block Agent tab usage if not logged in
    if (tab === "agent" && !user) {
      setShowLogin(true);
      return;
    }

    const userText = input;
    setInput("");
    setMessages((prev) => [...prev, { role: "user", text: userText }]);
    setLoading(true);

    try {
      let res;

      if (tab === "agent") {
        // ── Production path: API Gateway + Cognito JWT ─────────────────────
        // getIdToken() automatically refreshes if near-expired
        const idToken = await getIdToken();

        res = await fetch(AGENT_API, {
          method: "POST",
          headers: {
            "Content-Type":  "application/json",
            "Authorization": `Bearer ${idToken}`,
          },
          body: JSON.stringify({ message: userText }),
        });

      } else {
        // ── Local FastAPI path (Chat + RAG) ────────────────────────────────
        const endpoint = tab === "chat" ? "/chat" : "/qa";

        res = await fetch(LOCAL_API + endpoint, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ message: userText }),
        });
      }

      if (!res.ok) {
        const errBody = await res.json().catch(() => ({}));
        throw new Error(errBody.error || `HTTP ${res.status}`);
      }

      const data  = await res.json();
      const reply = data.reply || data.response || "No response received";

      setMessages((prev) => [...prev, { role: "bot", text: reply }]);

    } catch (error) {
      console.error(error);

      // Show login modal again on auth errors
      if (error.message.includes("401") || error.message.includes("Not authenticated")) {
        setShowLogin(true);
        setMessages((prev) => [...prev, { role: "bot", text: "⚠️ Session expired — please sign in again." }]);
      } else {
        setMessages((prev) => [...prev, { role: "bot", text: `⚠️ ${error.message}` }]);
      }
    }

    setLoading(false);
  };

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <>
      {/* Login modal — only mounts when needed */}
      {showLogin && (
        <LoginModal
          onLogin={async (email, password) => {
            await login(email, password);
            setShowLogin(false);
          }}
          onClose={() => setShowLogin(false)}
        />
      )}

      {/* Floating Action Button */}
      <button className="fab" onClick={() => setOpen(true)}>
        🤖
      </button>

      {open && (
        <div className="overlay" onClick={() => setOpen(false)}>
          <div className="panel" onClick={(e) => e.stopPropagation()}>

            {/* ── Header ── */}
            <div className="header">
              <div className="tabs">
                <button
                  className={tab === "chat" ? "active" : ""}
                  onClick={() => handleTabClick("chat")}
                >
                  Chat
                </button>

                <button
                  className={tab === "rag" ? "active" : ""}
                  onClick={() => handleTabClick("rag")}
                >
                  RAG
                </button>

                <button
                  className={tab === "agent" ? "active" : ""}
                  onClick={() => handleTabClick("agent")}
                >
                  Agent
                </button>
              </div>

              <div className="header-right">
                {/* Show signed-in user + logout when on Agent tab */}
                {tab === "agent" && user && (
                  <div className="user-info">
                    <span className="user-email">{user.email}</span>
                    <button className="logout-btn" onClick={logout}>
                      Sign out
                    </button>
                  </div>
                )}

                {/* Show login prompt on Agent tab when not signed in */}
                {tab === "agent" && !user && (
                  <button
                    className="login-prompt"
                    onClick={() => setShowLogin(true)}
                  >
                    Sign in
                  </button>
                )}

                <button className="close" onClick={() => setOpen(false)}>
                  ✕
                </button>
              </div>
            </div>

            {/* ── Messages ── */}
            <div className="messages">
              {messages.length === 0 && (
                <div className="welcome">
                  {tab === "chat"
                    ? "Ask anything to VoltStream AI"
                    : tab === "rag"
                    ? "Ask questions from your PDF knowledge base"
                    : user
                    ? "Control smart devices using AI Agent"
                    : "🔒 Sign in to use the AI Agent"}
                </div>
              )}

              {messages.map((m, i) => (
                <div key={i} className={`msg ${m.role}`}>
                  {m.text}
                </div>
              ))}

              {loading && (
                <div className="msg bot">Thinking...</div>
              )}
            </div>

            {/* ── Input ── */}
            <div className="inputBox">
              <input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder={
                  tab === "chat"          ? "Ask anything..."         :
                  tab === "rag"           ? "Ask from PDF..."          :
                  !user                   ? "Sign in to use agent..."  :
                                            "Turn off Refrigerator..."
                }
                onKeyDown={(e) => e.key === "Enter" && sendMessage()}
                disabled={tab === "agent" && !user}
              />

              <button
                onClick={tab === "agent" && !user
                  ? () => setShowLogin(true)
                  : sendMessage}
              >
                {tab === "agent" && !user ? "Login" : "Send"}
              </button>
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
          box-shadow: 0 0 20px rgba(0,194,255,.4);
        }

        .overlay {
          position: fixed;
          inset: 0;
          background: rgba(0,0,0,.7);
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
        }

        .header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          padding: 14px;
          border-bottom: 1px solid #1f2937;
        }

        .header-right {
          display: flex;
          align-items: center;
          gap: 8px;
        }

        .user-info {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .user-email {
          font-size: 11px;
          color: #94a3b8;
        }

        .logout-btn {
          font-size: 11px;
          color: #ef4444;
          background: none;
          border: none;
          cursor: pointer;
          padding: 0;
        }

        .login-prompt {
          font-size: 12px;
          color: #00c2ff;
          background: none;
          border: 1px solid #00c2ff44;
          border-radius: 6px;
          padding: 4px 10px;
          cursor: pointer;
        }

        .tabs button {
          margin-right: 8px;
          padding: 8px 14px;
          border: none;
          border-radius: 8px;
          background: #1f2937;
          color: white;
          cursor: pointer;
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
          margin-top: 30px;
        }

        .msg {
          padding: 10px 14px;
          border-radius: 12px;
          max-width: 80%;
          word-wrap: break-word;
        }

        .user {
          align-self: flex-end;
          background: #2563eb;
        }

        .bot {
          align-self: flex-start;
          background: #374151;
        }

        .inputBox {
          display: flex;
          border-top: 1px solid #1f2937;
        }

        .inputBox input {
          flex: 1;
          border: none;
          outline: none;
          padding: 14px;
          background: #0f172a;
          color: white;
        }

        .inputBox input:disabled {
          opacity: 0.4;
          cursor: not-allowed;
        }

        .inputBox button {
          border: none;
          padding: 14px 18px;
          background: #00c2ff;
          color: black;
          cursor: pointer;
          font-weight: 600;
        }
      `}</style>
    </>
  );
}
