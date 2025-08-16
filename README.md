Currency Quote Dashboard and Automation

This project is a solution for creating a currency quote dashboard with automated email notifications.

The project demonstrates a hybrid architecture, combining the flexibility of Python with the efficiency of low-code tools.
Key Features

    Real-time Currency Quotes: Displays real-time quotes for USD/BRL and EUR/BRL using the AwesomeAPI.

    Automated Email Notifications:

        Variation Alert: Sends an email notification if the USD/BRL rate varies by more than 2%.

        Weekly Summary: Sends a weekly email with a summary of the main currency quotes.

    Intuitive Dashboard: A simple and clear user interface built with Streamlit for easy visualization.

    Scalable Architecture: The solution uses Google Sheets as a data bridge, allowing for seamless communication between Python and N8N, making the project easily deployable in a cloud environment.

Technologies Used

    Python: The core language for data logic and API consumption.

    Streamlit: For building the interactive and user-friendly web dashboard.

    N8N: An open-source automation tool used to schedule and manage email workflows.

    Google Sheets: Acts as a central cloud database for data synchronization.

    SQLite: A lightweight, local database used for internal data persistence.

    AwesomeAPI: The public API used to retrieve currency quote data.
