/**
 * Grace's Skill Library — form receiver.
 *
 * Paste this into Extensions → Apps Script of your Google Sheet, then Deploy → New deployment → Web app
 * (Execute as: Me · Who has access: Anyone). Put the Web app URL into data/site.yaml as form_endpoint.
 *
 * Every "Request a skill", feedback (the lamp) and custom-skill message becomes one row in the sheet,
 * on a tab named after its type, and you get an email for each one.
 */

const NOTIFY_EMAIL = 'graceguo2004@outlook.com';   // where the email alerts go
const HEADERS = ['Received', 'Type', 'Message', 'Email', 'Page'];
const MAX_LEN = 5000;                               // ignore anything absurdly long

function doPost(e) {
  try {
    const data = JSON.parse((e && e.postData && e.postData.contents) || '{}');
    const type = ['request', 'feedback', 'consult'].indexOf(data.type) >= 0 ? data.type : 'other';
    const message = String(data.message || '').trim().slice(0, MAX_LEN);
    if (!message) return reply({ ok: false, error: 'empty' });
    const email = String(data.email || '').trim().slice(0, 200);
    const page = String(data.page || '').slice(0, 300);

    const sheet = tab(type);
    sheet.appendRow([new Date(), type, message, email, page]);

    const subject = {
      request: '📮 New skill request',
      feedback: '💡 New feedback',
      consult: '🤝 New custom-skill enquiry',
    }[type] || 'New message from the Skill Library';
    MailApp.sendEmail({
      to: NOTIFY_EMAIL,
      subject: subject,
      body: message + '\n\nFrom: ' + (email || '(no email)') + '\nPage: ' + page +
            '\n\nAll messages: ' + SpreadsheetApp.getActiveSpreadsheet().getUrl(),
      replyTo: email && /@/.test(email) ? email : NOTIFY_EMAIL,
    });
    return reply({ ok: true });
  } catch (err) {
    return reply({ ok: false, error: String(err) });
  }
}

function tab(type) {
  const ss = SpreadsheetApp.getActiveSpreadsheet();
  const name = { request: 'Skill requests', feedback: 'Feedback', consult: 'Custom skills' }[type] || 'Other';
  let sheet = ss.getSheetByName(name);
  if (!sheet) {
    sheet = ss.insertSheet(name);
    sheet.appendRow(HEADERS);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, HEADERS.length).setFontWeight('bold');
  }
  return sheet;
}

function reply(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(ContentService.MimeType.JSON);
}

/** Run this once from the editor to check it works and to grant permissions. */
function testReceiver() {
  doPost({ postData: { contents: JSON.stringify({ type: 'feedback', message: 'Test from the Apps Script editor', page: '/test' }) } });
}
