import { createAsyncThunk, createSlice } from "@reduxjs/toolkit";
import {
  createReminderApi,
  deleteReminderApi,
  extractReminderApi,
  getRemindersApi,
  updateReminderApi,
} from "../../api/reminderApi";

const initialState = {
  items: [],
  loading: false,
  error: null,
};

export const fetchReminders = createAsyncThunk(
  "reminders/fetch",
  async (_, { rejectWithValue }) => {
    try {
      return await getRemindersApi();
    } catch (err) {
      return rejectWithValue(err?.message || "Failed to fetch reminders");
    }
  }
);

export const addReminder = createAsyncThunk(
  "reminders/add",
  async ({ title, dueAt }, { rejectWithValue }) => {
    try {
      return await createReminderApi({ title, due_at: dueAt || null });
    } catch (err) {
      return rejectWithValue(err?.message || "Failed to add reminder");
    }
  }
);

export const extractReminderFromMessage = createAsyncThunk(
  "reminders/extractFromMessage",
  async (message, { rejectWithValue }) => {
    try {
      return await extractReminderApi(message);
    } catch (err) {
      return rejectWithValue(err?.message || "Failed to extract reminder");
    }
  }
);

export const toggleReminder = createAsyncThunk(
  "reminders/toggle",
  async ({ id, completed }, { rejectWithValue }) => {
    try {
      return await updateReminderApi(id, { completed });
    } catch (err) {
      return rejectWithValue(err?.message || "Failed to update reminder");
    }
  }
);

export const removeReminder = createAsyncThunk(
  "reminders/remove",
  async (id, { rejectWithValue }) => {
    try {
      await deleteReminderApi(id);
      return id;
    } catch (err) {
      return rejectWithValue(err?.message || "Failed to delete reminder");
    }
  }
);

const reminderSlice = createSlice({
  name: "reminders",
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchReminders.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchReminders.fulfilled, (state, action) => {
        state.loading = false;
        state.items = action.payload;
      })
      .addCase(fetchReminders.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload || action.error.message;
      })
      .addCase(addReminder.fulfilled, (state, action) => {
        state.items.push(action.payload);
      })
      .addCase(extractReminderFromMessage.fulfilled, (state, action) => {
        if (action.payload?.matched && action.payload?.reminder) {
          const exists = state.items.some((item) => item.id === action.payload.reminder.id);
          if (!exists) {
            state.items.push(action.payload.reminder);
          }
        }
      })
      .addCase(toggleReminder.fulfilled, (state, action) => {
        const idx = state.items.findIndex((r) => r.id === action.payload.id);
        if (idx >= 0) state.items[idx] = action.payload;
      })
      .addCase(removeReminder.fulfilled, (state, action) => {
        state.items = state.items.filter((r) => r.id !== action.payload);
      });
  },
});

export default reminderSlice.reducer;