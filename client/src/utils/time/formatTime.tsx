export default function formatTime(dateStr) {
  const date = new Date(dateStr);

  if (isNaN(date.getTime())) {
    // handle invalid date value
    return new Date()
      .toLocaleTimeString([], {
        hour: "2-digit",
        minute: "2-digit",
        hour12: true,
      })
      .toLowerCase();
  }

  return date
    .toLocaleTimeString([], {
      hour: "2-digit",
      minute: "2-digit",
      hour12: true,
    })
    .toLowerCase();
}
