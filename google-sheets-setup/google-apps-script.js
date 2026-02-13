// Google Apps Script для сохранения данных формы в Google Sheets
// Этот код нужно вставить в Apps Script вашей Google таблицы

function doPost(e) {
  try {
    // Получаем активную таблицу
    var sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
    
    // Парсим данные из запроса
    var data = JSON.parse(e.postData.contents);
    
    // Добавляем новую строку с данными
    sheet.appendRow([
      data.timestamp,     // Дата и время
      data.lastName,      // Фамилия
      data.firstName,     // Имя
      data.middleName     // Отчество
    ]);
    
    // Возвращаем успешный ответ
    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'success',
        'message': 'Данные успешно сохранены'
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    // Возвращаем ошибку
    return ContentService
      .createTextOutput(JSON.stringify({
        'status': 'error',
        'message': error.toString()
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

// Функция для GET запросов (опционально, для тестирования)
function doGet(e) {
  return ContentService
    .createTextOutput('API работает! Используйте POST запросы для отправки данных.')
    .setMimeType(ContentService.MimeType.TEXT);
}
