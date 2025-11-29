function syncCalendar() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName("Sheet1");
  const calendar = CalendarApp.getCalendarById("primary");

  const data = sheet.getRange(2, 1, sheet.getLastRow() - 1, 9).getValues();

  data.forEach(row => {
    const [name, email, phone, wa, sub, start, expiry] = row;

    if (!expiry) return;

    const title = sub + " Expiry Reminder";
    const desc = `User: ${name}\nEmail: ${email}\nPhone: ${phone}\nWhatsApp: ${wa}`;

    calendar.createAllDayEvent(title, new Date(expiry), { description: desc });
  });
}
