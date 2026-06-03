import { useState, useEffect, useRef } from "react";
import axios from "axios";
import { Send, Bot, User } from "lucide-react";

const API_BASE = "http://127.0.0.1:8000/api/v1";

export default function AIChat() {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  const sendMessage = async () => {
    if (!message.trim()) return;

    const userMsg = { role: "user", text: message };
    setMessages((prev) => [...prev, userMsg]);

    const current = message;
    setMessage("");
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        message: current,
      });

      setMessages((prev) => [
        ...prev,
        { role: "ai", text: res.data.reply },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "⚠️ AI service not reachable" },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-slate-950 rounded-2xl border border-slate-800">

      {/* HEADER */}
      <div className="p-4 border-b border-slate-800 flex items-center gap-3">
        <div className="bg-blue-600 p-2 rounded-lg">
          <Bot size={18} />
        </div>
        <div>
          <h1 className="font-semibold">AI Energy Copilot</h1>
          <p className="text-xs text-slate-400">
            Ask anything about electricity, billing & devices
          </p>
        </div>
      </div>

      {/* CHAT AREA */}
      <div className="flex-1 overflow-y-auto p-5 space-y-4">

        {messages.length === 0 && (
          <div className="text-slate-500 text-center mt-10">
            💡 Try: "How to reduce my electricity bill?"
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            className={`flex items-end gap-2 ${
              m.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            {m.role === "ai" && (
              <div className="bg-blue-600 p-2 rounded-full">
                <Bot size={14} />
              </div>
            )}

            <div
              className={`px-4 py-3 rounded-2xl max-w-[70%] text-sm ${
                m.role === "user"
                  ? "bg-blue-600 text-white"
                  : "bg-slate-800 text-slate-200"
              }`}
            >
              {m.text}
            </div>

            {m.role === "user" && (
              <div className="bg-slate-700 p-2 rounded-full">
                <User size={14} />
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div className="text-slate-400 flex gap-2">
            <span>AI thinking</span>
            <span className="animate-bounce">...</span>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* INPUT */}
      <div className="p-4 border-t border-slate-800 flex gap-2">
        <input
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask VoltStream AI..."
          className="flex-1 bg-slate-900 border border-slate-700 rounded-xl px-4 py-3 text-white"
        />

        <button
          onClick={sendMessage}
          className="bg-blue-600 hover:bg-blue-700 px-4 rounded-xl"
        >
          <Send size={18} />
        </button>
      </div>
    </div>
  );
}