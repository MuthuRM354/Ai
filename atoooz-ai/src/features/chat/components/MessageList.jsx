import ReactMarkdown from "react-markdown";

export default function MessageList({ messages, loading, bottomRef }) {
  return (
    <div className="messages">
      {messages.map((m, i) => (
        <div key={i} className={`message-row ${m.role}`}>
          <div className="avatar">{m.role === "user" ? "M" : "✦"}</div>
          <div className="message-content">
            <ReactMarkdown
              components={{
                code({ inline, children, ...props }) {
                  return inline ? (
                    <code className="inline-code" {...props}>{children}</code>
                  ) : (
                    <pre className="code-block"><code {...props}>{children}</code></pre>
                  );
                },
              }}
            >
              {m.content}
            </ReactMarkdown>
          </div>
        </div>
      ))}

      {loading && (
        <div className="message-row assistant">
          <div className="avatar">✦</div>
          <div className="message-content typing">
            <span className="dot" />
            <span className="dot" />
            <span className="dot" />
          </div>
        </div>
      )}
      <div ref={bottomRef} />
    </div>
  );
}