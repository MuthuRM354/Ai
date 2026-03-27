import { createAsyncThunk, createSlice, nanoid } from "@reduxjs/toolkit";
import { sendChatMessage } from "../../api/chatApi";
import { extractReminderFromMessage } from "./reminderSlice";

const initialState = {
  chats: [{ id: "default", title: "New Chat", messages: [] }],
  activeChatId: "default",
  loading: false,
  error: null,
};

const getActiveChat = (state) =>
  state.chats.find((c) => c.id === state.activeChatId);

const createMessage = (role, content) => ({
  id: nanoid(),
  role,
  content,
});

export const sendMessage = createAsyncThunk(
  "chat/sendMessage",
  async (text, { getState, dispatch, rejectWithValue }) => {
    const message = (text || "").trim();
    if (!message) return rejectWithValue("Message is empty");

    const state = getState().chat;
    const activeChat = state.chats.find((c) => c.id === state.activeChatId);
    const previousMessages = activeChat?.messages || [];

    dispatch(addUserMessage(message));

    let reminderResult = null;
    try {
      reminderResult = await dispatch(extractReminderFromMessage(message)).unwrap();
    } catch {
      reminderResult = null;
    }

    if (reminderResult?.matched && reminderResult?.reminder) {
      const dueText = reminderResult.reminder.due_at
        ? ` for ${new Date(reminderResult.reminder.due_at).toLocaleString()}`
        : "";

      const confirmation = `✅ Reminder created: **${reminderResult.reminder.title}**${dueText}`;
      dispatch(addAssistantMessage(confirmation));
      return confirmation;
    }

    try {
      const history = previousMessages.map((m) => ({
        role: m.role,
        content: m.content,
      }));

      const answer = await sendChatMessage(message, history);
      dispatch(addAssistantMessage(answer));
      return answer;
    } catch (err) {
      const errorMessage = err?.message || "Request failed";
      dispatch(addAssistantMessage(`**Error:** ${errorMessage}`));
      return rejectWithValue(errorMessage);
    }
  }
);

const chatSlice = createSlice({
  name: "chat",
  initialState,
  reducers: {
    createNewChat(state) {
      const id = String(Date.now());
      state.chats.unshift({ id, title: "New Chat", messages: [] });
      state.activeChatId = id;
    },
    setActiveChat(state, action) {
      state.activeChatId = action.payload;
    },
    addUserMessage(state, action) {
      const chat = getActiveChat(state);
      if (!chat) return;

      chat.messages.push(createMessage("user", action.payload));

      if (chat.messages.length === 1) {
        const title = action.payload;
        chat.title = title.slice(0, 30) + (title.length > 30 ? "…" : "");
      }
    },
    addAssistantMessage(state, action) {
      const chat = getActiveChat(state);
      if (!chat) return;

      chat.messages.push(createMessage("assistant", action.payload));
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(sendMessage.fulfilled, (state) => {
        state.loading = false;
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || action.error.message;
      });
  },
});

export const { createNewChat, setActiveChat, addUserMessage, addAssistantMessage } =
  chatSlice.actions;

export default chatSlice.reducer;