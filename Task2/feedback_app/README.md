

&nbsp;Task 2 – Student Feedback Form





This project implements a simple web app where students can submit feedback and view all feedbacks.





&nbsp;Tech Stack \& Tools Used:

\- Python (Flask)

\- HTML / CSS for frontend

\- Local JSON file (`feedbacks.json`) for storing feedbacks



&nbsp;Features Implemented:

\- Submit student feedback (name + feedback).

\- View all feedbacks in a dashboard.

\- Edit/modify any feedback.

\- Delete feedback

\- Displays a summary:

&nbsp;   - Total feedback count.

&nbsp;   - Top keywords (automatically computed).

&nbsp;   - Overall sentiment (Positive / Neutral / Negative), intelligently calculated per feedback.

\- Modern, user-friendly frontend UI.



&nbsp;

How to Run the Feedback App



1\) Install dependencies:-



&nbsp;   ```bash

&nbsp;    pip install flask



2)Navigate to the folder -Start the Flask App:-



&nbsp;  bash

&nbsp;  python app.py





3\) Open in Browser:-



&nbsp;  Visit:http://127.0.0.1:5000/







Further Improvements:



Implement real admin authentication with passwords.(no real admin functionality in the existing from).



Store feedbacks in a database (e.g., SQLite) for better performance.



Add export option (CSV or PDF) for feedback reports.



Notes:



All feedbacks are stored in feedbacks.json.



Sentiment detection uses weighted negative words and per-feedback majority logic.



