import RemindersPanel from "./reminders/RemindersPanel";

export default function Sidebar({ chats, activeChatId, onNewChat, onSelectChat }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-top">
        <div className="brand">
          <span className="brand-icon">✦</span>
          <span className="brand-name">AtoooZ AI</span>
        </div>
        <button className="new-chat-btn" onClick={onNewChat}>
          <span>+</span> New Chat
        </button>
      </div>

      <div className="chat-history">
        <p className="history-label">Recent</p>
        {chats.map((c) => (
          <button
            key={c.id}
            className={`history-item ${c.id === activeChatId ? "active" : ""}`}
            onClick={() => onSelectChat(c.id)}
          >
            💬 {c.title}
          </button>
        ))}
      </div>

      <RemindersPanel />

      <div className="sidebar-footer">
        <div className="user-info">
          <div className="user-avatar">M</div>
          <span>Muthu Manikandan</span>
        </div>
      </div>
    </aside>
  );
}