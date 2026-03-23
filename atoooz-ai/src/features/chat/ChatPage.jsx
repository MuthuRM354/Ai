import { useEffect, useMemo, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import Sidebar from "./components/Sidebar";
import WelcomeView from "./components/WelcomeView";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import { createNewChat, sendMessage, setActiveChat } from "../../store/slices/chatSlice";
import { fetchReminders } from "../../store/slices/reminderSlice";
import "./ChatPage.css";

export default function ChatPage() {
  const dispatch = useDispatch();
  const bottomRef = useRef(null);

  const { chats, activeChatId, loading } = useSelector((state) => state.chat);

  const activeChat = useMemo(
    () => chats.find((c) => c.id === activeChatId) || chats[0],
    [chats, activeChatId]
  );

  const messages = activeChat?.messages || [];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    dispatch(fetchReminders());
  }, [dispatch]);

  return (
    <div className="app-shell">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={() => dispatch(createNewChat())}
        onSelectChat={(id) => dispatch(setActiveChat(id))}
      />

      <main className="main">
        {messages.length === 0 ? (
          <WelcomeView onPick={(text) => dispatch(sendMessage(text))} />
        ) : (
          <MessageList messages={messages} loading={loading} bottomRef={bottomRef} />
        )}

        <ChatInput loading={loading} onSend={(text) => dispatch(sendMessage(text))} />
      </main>
    </div>
  );
}