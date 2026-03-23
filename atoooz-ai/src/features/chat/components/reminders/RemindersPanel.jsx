import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { addReminder, removeReminder, toggleReminder } from "../../../../store/slices/reminderSlice";

export default function RemindersPanel() {
  const dispatch = useDispatch();
  const { items } = useSelector((state) => state.reminders);

  const [title, setTitle] = useState("");
  const [dueAt, setDueAt] = useState("");

  const onAdd = (e) => {
    e.preventDefault();
    const trimmed = title.trim();
    if (!trimmed) return;
    dispatch(addReminder({ title: trimmed, dueAt: dueAt || null }));
    setTitle("");
    setDueAt("");
  };

  return (
    <section className="reminders-panel">
      <p className="history-label">Reminders</p>

      <form className="reminder-form" onSubmit={onAdd}>
        <input
          className="reminder-input"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          placeholder="Add reminder..."
        />
        <input
          className="reminder-date"
          type="datetime-local"
          value={dueAt}
          onChange={(e) => setDueAt(e.target.value)}
        />
        <button className="reminder-add-btn" type="submit">Add</button>
      </form>

      <div className="reminder-list">
        {items.length === 0 ? (
          <p className="reminder-empty">No reminders yet</p>
        ) : (
          items.map((r) => (
            <div key={r.id} className="reminder-item">
              <label>
                <input
                  type="checkbox"
                  checked={r.completed}
                  onChange={(e) =>
                    dispatch(toggleReminder({ id: r.id, completed: e.target.checked }))
                  }
                />
                <span className={r.completed ? "done" : ""}>{r.title}</span>
              </label>
              <div className="reminder-actions">
                {r.due_at && (
                  <small>{new Date(r.due_at).toLocaleString()}</small>
                )}
                <button onClick={() => dispatch(removeReminder(r.id))}>✕</button>
              </div>
            </div>
          ))
        )}
      </div>
    </section>
  );
}