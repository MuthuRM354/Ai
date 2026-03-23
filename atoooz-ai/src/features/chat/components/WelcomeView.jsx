const SUGGESTIONS = [
  "Explain Python decorators",
  "What is an AI agent?",
  "Write a REST API in FastAPI",
  "Difference between list and tuple",
];

export default function WelcomeView({ onPick }) {
  return (
    <div className="welcome-screen">
      <div className="welcome-icon">✦</div>
      <h1>How can I help you today?</h1>
      <p>Powered by Claude · Remembers your conversation</p>
      <div className="suggestions">
        {SUGGESTIONS.map((s) => (
          <button key={s} className="suggestion-card" onClick={() => onPick(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}