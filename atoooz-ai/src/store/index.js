import { configureStore } from "@reduxjs/toolkit";
import chatReducer from "./slices/chatSlice";
import reminderReducer from "./slices/reminderSlice";

export const store = configureStore({
  reducer: {
    chat: chatReducer,
    reminders: reminderReducer,
  },
});