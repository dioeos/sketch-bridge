export default function formatTime (dateStr) => {
  try {
    const date = new Date(dateStr);
    return date.toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', hour12: true}).toLowerCase();
  } catch (e) {
    return new Date().toLocaleTimeString([], {hour: '2-digit', minute: '2-digit', hour12: true }).toLowerCase();
  }
};

