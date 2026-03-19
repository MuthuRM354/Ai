import { useState } from "react";
import { sendChatMessage } from "../../api/chatApi";

export default function ChatPage() {
    const[input, setInput] = useState("");
    const [message, setMessage] = useState([]);
    const [loading, setLoading] = useState(false);

    const onSend = async () => {
        if (!input.trim()) return;

        const userText = input.trim();
        setMessage((prev) => [...prev, { text: userText, sender: "user" }]);
        setInput("");
        setLoading(true);

        try{
            const answer = await sendChatMessage(userText);
            setMessage((prev) => [...prev, { text: answer, sender: "bot" }]);   
        } catch (error) {
            setMessage((prev) => [...prev, { text: "Error: " + error.message, sender: "bot" }]);    
        } finally {
            setLoading(false);
        }
    };

    return (  
        <div className="chat-shell">
            <h2>Chat with AI</h2>
            <div className="chat-BOX">
                {message.map((m, i) => (
                    <p key={i}><b>{m.role === "user" ? "you" : "AI"}</b>: {m.text}</p>
                ))}
                {loading && <p><i>AI is typing...</i></p>}
            </div>
            <div className="chat-input-row">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder="Ask me Anythingggg........"
                    onKeyDown={(e) => e.key === "Enter" && onSend()}
                />
                <button onClick={onSend} disabled={loading}>{loading ? "Sending..." : "Send" }</button>
            </div>
        </div>
    );
}
