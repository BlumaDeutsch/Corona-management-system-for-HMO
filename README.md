# Corona-management-system-for-HMO
Corona management system for HMO

המערכת אחראית לקליטת נתונים אודות אדם חדש ע"י המשתמש ולצרופו של אותו אדם לבסיס הנתונים של קופת החולים. בנוסף, אחראית המערכת על שליפת נתונים בסיסיים על אדם שכבר נמצא במערכת באמצעות מספר תעודת זהות. 
המערכת מסוגלת גם להציג את מספר החולים הפעילים בכל יום בחודש האחרון את מספר האנשים שלא התחסנו כלל, ואת אחוזם ביחס למספר החברים בקופת החולים. 

על מנת להריץ אץ המערכת יש צורך: 
- להוריד פייתון בגרסה מעודכנת. 
- להוריד את החבילות הבאות: pymongo, flask, dateutils 
- להוריד mongoDB 
- ליצור חיבור ב localhost  פורט מספר 27017
- לאכסן את קבצי ה html בתיקיית templates באותו תיקייה של קובץ הפייתון

על מנת להריץ אץ המערכת, יש לגשת לכתובת http://127.0.0.1:5000/ (במקרה שכל הקבצים הורדו מכונה מקומית)
לקליטת פרטים על חבר חדש, יש ללחוץ על כפתור 'add new person' 
בדף הנפתח יש למלא את פרטי החבר, וללחוץ 'update'
לחיפוש אדם לפי תעודת זהות יש ללחוץ 'find person' 
בדף הנפתח יש למלא את השדה בתעודת הזהות, ולחוץ 'find person by id number' 
להצגת שאר פרטי המידע שהמערכת מספקת, יש ללחוץ 'show chart' 

דוגמא: 
לחץ 'add new person' 
בדף הנפתח הזן את הפרטים הבאים: 
name: levy
last name: lev
id numuber: 123456789
date of birth: 13.05.1995
phone: 0000000000
date of receiving first vaccination: 02.03.2022
manufacturer: pfizer
date of positive result: 16.04.2023
recovery date: 03.05.2023
לחץ על 'update' 
עכשיו לחץ על 'find person' 
הכנס מספר תעודת זהות 123456789 ולחץ על 'find person by id' 
פרטי המשתמש יעלו:![find person](https://github.com/BlumaDeutsch/Corona-management-system-for-HMO/assets/80222387/a738ecb3-7da6-4b46-8b35-c05b847fcc9a)
חזור פעמיים אחורה לדף הבית
לחץ על 'show chart' 
פרטים נוספים יוצגו: ![show chart](https://github.com/BlumaDeutsch/Corona-management-system-for-HMO/assets/80222387/23add99d-26e5-435f-b9e8-60ff91979aeb)
