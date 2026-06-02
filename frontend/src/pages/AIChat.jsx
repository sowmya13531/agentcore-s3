import { useState } from "react";
import axios from "axios";
import { MessageCircle, X, Send } from "lucide-react";

const API_BASE =
"http://127.0.0.1:8000/api/v1";

export default function AIChat() {

  const [isOpen, setIsOpen] = useState(false);

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([]);

  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {

    if (!message.trim()) return;

    const userMessage = {
      sender: "user",
      text: message
    };

    setMessages((prev) => [...prev, userMessage]);

    const currentMessage = message;

    setMessage("");

    try {

      setLoading(true);

      console.log("Sending:", currentMessage);

      const response = await axios.post(
        `${API_BASE}/chat`,
        {
          message: currentMessage
        }
      );

      console.log(response.data);

      const aiMessage = {
        sender: "ai",
        text: response.data.reply
      };

      setMessages((prev) => [...prev, aiMessage]);

    } catch (error) {

      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Unable to contact AI Assistant."
        }
      ]);

    } finally {

      setLoading(false);

    }
  };

  const handleKeyDown = (e) => {

    if (e.key === "Enter") {

      sendMessage();

    }

  };

  return (
    <>
      {/* Floating Button */}

      <button
        onClick={() => setIsOpen(!isOpen)}
        className="
        fixed
        bottom-6
        right-6
        z-50
        w-16
        h-16
        rounded-full
        bg-blue-600
        hover:bg-blue-700
        text-white
        shadow-xl
        flex
        items-center
        justify-center
        "
      >
        {isOpen ? <X size={26} /> : <MessageCircle size={26} />}
      </button>

      {/* Chat Window */}

      {isOpen && (
        <div
          className="
          fixed
          bottom-24
          right-6
          z-50
          w-[400px]
          h-[550px]
          bg-slate-900
          border
          border-slate-700
          rounded-2xl
          shadow-2xl
          flex
          flex-col
          overflow-hidden
          "
        >

          {/* Header */}

          <div className="bg-blue-600 p-4">

            <h2 className="text-white font-semibold">
              VoltStream AI Copilot
            </h2>

          </div>

          {/* Chat Messages */}

          <div className="flex-1 overflow-y-auto p-4 space-y-3">

            {messages.length === 0 && (

              <div className="text-slate-500 text-sm">
                Ask anything about energy usage, billing, devices, or solar generation.
              </div>

            )}

            {messages.map((msg, index) => (

              <div
                key={index}
                className={`flex ${
                  msg.sender === "user"
                    ? "justify-end"
                    : "justify-start"
                }`}
              >

                <div
                  className={`max-w-[80%] px-4 py-3 rounded-xl ${
                    msg.sender === "user"
                      ? "bg-blue-600 text-white"
                      : "bg-slate-800 text-slate-200"
                  }`}
                >
                  {msg.text}
                </div>

              </div>

            ))}

            {loading && (

              <div className="flex justify-start">

                <div className="bg-slate-800 px-4 py-3 rounded-xl">

                  <div
                    className="
                    w-5
                    h-5
                    border-2
                    border-white
                    border-t-transparent
                    rounded-full
                    animate-spin
                    "
                  />

                </div>

              </div>

            )}

          </div>

          {/* Input Area */}

          <div className="border-t border-slate-700 p-4">

            <div className="flex gap-2">

              <input
                type="text"
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Ask VoltStream AI..."
                className="
                flex-1
                bg-slate-800
                border
                border-slate-700
                rounded-xl
                px-4
                py-3
                text-white
                outline-none
                "
              />

              <button
                onClick={sendMessage}
                disabled={loading}
                className="
                bg-blue-600
                hover:bg-blue-700
                px-4
                rounded-xl
                text-white
                "
              >
                <Send size={18} />
              </button>

            </div>

          </div>

        </div>
      )}
    </>
  );
}