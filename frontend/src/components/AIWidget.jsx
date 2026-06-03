import { useState } from "react";

export default function AIWidget() {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState("chat");
  const [input, setInput] = useState("");

  const [chatMessages, setChatMessages] = useState([]);
  const [ragMessages, setRagMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const API = "http://127.0.0.1:8000/api/v1";

  const messages = tab === "chat" ? chatMessages : ragMessages;
  const setMessages = tab === "chat" ? setChatMessages : setRagMessages;

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userText = input;
    setInput("");

    setMessages((prev) => [
      ...prev,
      { role: "user", text: userText },
    ]);

    setLoading(true);

    try {
      const endpoint = tab === "chat" ? "/chat" : "/qa";

      // IMPORTANT
      const body =
        tab === "chat"
          ? { message: userText }
          : { question: userText };

      const res = await fetch(API + endpoint, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      });

      if (!res.ok) {
        throw new Error(`HTTP Error ${res.status}`);
      }

      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: data.reply || "No response received",
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "bot",
          text: "Backend error. Check FastAPI logs.",
        },
      ]);
    }

    setLoading(false);
  };

  return (
    <>
      <button className="fab" onClick={() => setOpen(true)}>
        🤖
      </button>

      {open && (
        <div className="overlay" onClick={() => setOpen(false)}>
          <div
            className="panel"
            onClick={(e) => e.stopPropagation()}
          >
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
              </div>

              <button
                className="close"
                onClick={() => setOpen(false)}
              >
                ✕
              </button>
            </div>

            <div className="messages">
              {messages.length === 0 && (
                <div className="welcome">
                  {tab === "chat"
                    ? "Ask anything to VoltStream AI"
                    : "Ask questions from your PDF knowledge base"}
                </div>
              )}

              {messages.map((m, i) => (
                <div
                  key={i}
                  className={`msg ${m.role}`}
                >
                  {m.text}
                </div>
              ))}

              {loading && (
                <div className="msg bot">
                  Thinking...
                </div>
              )}
            </div>

            <div className="inputBox">
              <input
                value={input}
                onChange={(e) =>
                  setInput(e.target.value)
                }
                placeholder={
                  tab === "chat"
                    ? "Ask anything..."
                    : "Ask from PDF..."
                }
                onKeyDown={(e) =>
                  e.key === "Enter" && sendMessage()
                }
              />

              <button onClick={sendMessage}>
                Send
              </button>
            </div>
          </div>
        </div>
      )}

      <style>{`
        .fab{
          position:fixed;
          right:20px;
          bottom:20px;
          width:60px;
          height:60px;
          border:none;
          border-radius:50%;
          background:#00c2ff;
          color:black;
          font-size:24px;
          cursor:pointer;
          z-index:9999;
          box-shadow:0 0 20px rgba(0,194,255,.4);
        }

        .overlay{
          position:fixed;
          inset:0;
          background:rgba(0,0,0,.7);
          display:flex;
          justify-content:center;
          align-items:center;
          z-index:9998;
        }

        .panel{
          width:450px;
          height:650px;
          background:#111827;
          color:white;
          border-radius:18px;
          display:flex;
          flex-direction:column;
          overflow:hidden;
          border:1px solid #1f2937;
        }

        .header{
          display:flex;
          justify-content:space-between;
          align-items:center;
          padding:14px;
          border-bottom:1px solid #1f2937;
        }

        .tabs button{
          margin-right:8px;
          padding:8px 14px;
          border:none;
          border-radius:8px;
          background:#1f2937;
          color:white;
          cursor:pointer;
        }

        .tabs .active{
          background:#00c2ff;
          color:black;
          font-weight:600;
        }

        .close{
          border:none;
          background:none;
          color:white;
          cursor:pointer;
          font-size:18px;
        }

        .messages{
          flex:1;
          overflow-y:auto;
          padding:16px;
          display:flex;
          flex-direction:column;
          gap:10px;
        }

        .welcome{
          text-align:center;
          color:#94a3b8;
          margin-top:30px;
        }

        .msg{
          padding:10px 14px;
          border-radius:12px;
          max-width:80%;
          word-wrap:break-word;
        }

        .user{
          align-self:flex-end;
          background:#2563eb;
        }

        .bot{
          align-self:flex-start;
          background:#374151;
        }

        .inputBox{
          display:flex;
          border-top:1px solid #1f2937;
        }

        .inputBox input{
          flex:1;
          border:none;
          outline:none;
          padding:14px;
          background:#0f172a;
          color:white;
        }

        .inputBox button{
          border:none;
          padding:14px 18px;
          background:#00c2ff;
          color:black;
          cursor:pointer;
          font-weight:600;
        }
      `}</style>
    </>
  );
}