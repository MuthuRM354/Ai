import { useCallback, useEffect, useMemo, useRef } from "react";
import { useDispatch, useSelector } from "react-redux";
import Sidebar from "./components/Sidebar";
import WelcomeView from "./components/WelcomeView";
import MessageList from "./components/MessageList";
import ChatInput from "./components/ChatInput";
import {
  createNewChat,
  sendMessage,
  setActiveChat,
} from "../../store/slices/chatSlice";
import { fetchReminders } from "../../store/slices/reminderSlice";
import "./ChatPage.css";

export default function ChatPage() {
  const dispatch = useDispatch();
  const bottomRef = useRef(null);

  const { chats, activeChatId, loading } = useSelector((state) => state.chat);
  const { status: remindersStatus } = useSelector((state) => state.reminders);

  const activeChat = useMemo(
    () => chats.find((c) => c.id === activeChatId) || chats[0],
    [chats, activeChatId]
  );

  const messages = useMemo(() => activeChat?.messages ?? [], [activeChat]);

  const handleNewChat = useCallback(() => {
    dispatch(createNewChat());
  }, [dispatch]);

  const handleSelectChat = useCallback(
    (id) => {
      dispatch(setActiveChat(id));
    },
    [dispatch]
  );

  const handleSend = useCallback(
    (text) => {
      dispatch(sendMessage(text));
    },
    [dispatch]
  );

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, loading]);

  useEffect(() => {
    if (remindersStatus === "idle") {
      dispatch(fetchReminders());
    }
  }, [dispatch, remindersStatus]);

  return (
    <div className="app-shell">
      <Sidebar
        chats={chats}
        activeChatId={activeChatId}
        onNewChat={handleNewChat}
        onSelectChat={handleSelectChat}
      />

      <main className="main">
        {messages.length === 0 ? (
          <WelcomeView onPick={handleSend} />
        ) : (
          <MessageList
            messages={messages}
            loading={loading}
            bottomRef={bottomRef}
          />
        )}

        <ChatInput loading={loading} onSend={handleSend} />
      </main>
    </div>
  );
}