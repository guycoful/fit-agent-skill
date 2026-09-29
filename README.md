# סוכן תזונה וחיטוב

מאמן תזונה קשוח שעובד בשיחה, בלי שרת ובלי חשבון. שאלון פתיחה חד-פעמי בונה פרופיל אישי, והפסיקה היומית ("יום מוצלח" או "יום כושל") מחושבת בקוד ולא על ידי המודל.

הסוכן הזה התחיל כאפליקציה ואחר כך כ-Gem בג'מיני של גיא כהן, והוא ארוז כסקיל כללי. היעדים שייכים למשתמש והסקיל לא מכיל אף מספר אישי.

## איך משתמשים

1. [הורדה ישירה של SKILL.md](https://raw.githubusercontent.com/guycoful/fit-agent-skill/main/SKILL.md). הקובץ נפתח כטקסט.
2. מורידים גם את שלושת הקבצים שבתיקיית `references`: `verdict.py`, `profile.example.json`, `day.example.json`.
3. שומרים הכל בתיקייה בשם `fit-agent`, כשקובץ SKILL.md בתוכה ותיקיית `references` לצידו.
4. מעלים לכלי שיש לכם. ב-Claude: Customize, Skills, Create skill, Upload a skill. ב-Gemini Spark: Skills, Upload.

הפסיקה מחושבת על ידי `references/verdict.py` ולכן הכלי צריך להריץ קוד פייתון. ב-Claude צריך להפעיל code execution.

מדריך ההמרה המלא: https://claude.ai/artifact/UKg2bkoJDCzECgs2C7zSen

הסקיל אינו תחליף לרופא או לתזונאי מוסמך.
