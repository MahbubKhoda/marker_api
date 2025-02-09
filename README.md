# Market Data Web Application

This web application, built using Python's Flask framework, fetches and displays market data from the Marker API (https://markerapi.com/).  It provides a user-friendly interface to access various API endpoints, allowing users to search and retrieve information on trademarks.

## What is Marker API?

Marker API is a platform that provides access to comprehensive trademark data.  It offers a suite of APIs that enable developers to retrieve information about trademarks, including serial numbers, descriptions, owners, and expiration dates. This data can be used for various purposes, such as trademark research, competitive analysis, and brand monitoring.  For detailed information and documentation, please visit the official Marker API website: https://markerapi.com/.

## How the Application Works

This application utilizes asynchronous requests with `aiohttp` to fetch data from the Marker API efficiently. The backend, built with Flask, handles routing and API interaction. The frontend, using HTML, CSS, and JavaScript, provides a dynamic interface for users to interact with the API.

### Backend (Python - Flask)

1.  **Environment Variables:** The application uses the `python-dotenv` library to load sensitive API credentials (username and password) from a `.env` file.  This file should be in the same directory as the `app.py` file and **should not** be committed to version control.

2.  **API Authentication:** The application uses Basic Authentication with the Marker API, providing the username and password retrieved from the environment variables.

3.  **Asynchronous Requests:** The `aiohttp` library is used to make asynchronous requests to the Marker API. This allows the application to fetch data from multiple endpoints concurrently, improving performance.

4.  **Flask Routes:**
    *   `/`: This route renders the main HTML template (`index.html`), which displays the user interface.
    *   `/fetch_api_data`: This route handles POST requests from the frontend. It retrieves search terms from the form data, makes the necessary API calls using `fetch_all_data` function, and returns the data in JSON format.

5.  **API Endpoints:** The `API_ENDPOINTS` dictionary defines the available Marker API endpoints and their corresponding URLs and required parameters.  This makes it easy to add or modify endpoints. The application supports the following endpoints:

    *   Serial Number Search
    *   Trademark Search
    *   Description Search
    *   Owner Search
    *   Expiration Search

### Frontend (HTML, CSS, JavaScript)

1.  **User Interface:** The HTML (`index.html`) creates a user interface with separate boxes for each API endpoint. Each box includes a form to enter search terms (if required), and a button to trigger the API call.

2.  **Form Submission:** When the user clicks the "Fetch" button, the JavaScript `fetchData` function is called. This function:
    *   Collects the search terms from the form associated with the endpoint.
    *   Adds a "loading" class to the box and displays a "Fetching results..." message.
    *   Sends a POST request to the `/fetch_api_data` route with the form data.
    *   Receives the JSON response from the backend.
    *   Displays the results in the box, or an error message if the API call fails.
    *   Removes the "loading" class and hides the loading message.

3.  **Dynamic Content:** The HTML uses Jinja2 templating to dynamically generate the boxes for each API endpoint based on the `API_ENDPOINTS` dictionary in the Python code.

4.  **Styling:** CSS is used to style the web page and make it more visually appealing.

## How to Run the Application

1.  **Clone the repository:** (If applicable)

2.  **Install dependencies:**
    ```bash
    pip install Flask aiohttp requests python-dotenv
    ```

3.  **Create a `.env` file:** In the same directory as `app.py`, create a `.env` file and add your Marker API credentials:

    ```
    MARKER_API_USERNAME=your_marker_api_username
    MARKER_API_PASSWORD=your_marker_api_password
    ```

    **Important:** Do not commit this `.env` file to version control.

4.  **Run the Flask app:**
    ```bash
    python app.py
    ```

5.  **Open the web page:** Open your web browser and go to `http://127.0.0.1:5000/`.

## Additional Information

For more detailed information about the Marker API and its endpoints, please refer to the official Marker API documentation: https://markerapi.com/.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.