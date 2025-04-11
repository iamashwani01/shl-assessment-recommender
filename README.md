# Assessment
This project was created using FastAPI to build the backend. A basic HTML form is used to take input from the user for job role and competencies. When the form is submitted, the data is sent to the FastAPI backend.

The backend uses Hugging Face’s Mixtral-8x7B-Instruct model via their inference API to generate SHL assessment recommendations in real-time. The API response is parsed and displayed on the same page in a readable format.

The API key for Hugging Face is managed using environment variables, and the request to Hugging Face is made using httpx (an async HTTP client).

The application was deployed using Render, and the code was pushed from GitHub. The server runs using Uvicorn on port 10000, and Render detects this to make the service live.


