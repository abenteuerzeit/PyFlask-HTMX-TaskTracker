# PyFlask-HTMX-TaskTracker

## Introduction

PyFlask-HTMX-TaskTracker is a web-based task management application designed to offer a seamless and interactive user experience. Built with Flask, a lightweight yet powerful web framework, this application is ideal for those seeking efficient task management with real-time interactions. The project leverages HTMX to enhance user experiences, offering dynamic content without the need for bulky JavaScript frameworks. Additionally, it employs the HATEOAS (Hypermedia as the Engine of Application State) principle to ensure a scalable and maintainable RESTful architecture.

## Demo

<https://github.com/abenteuerzeit/PyFlask-HTMX-TaskTracker/assets/98088666/89448991-7d96-4917-a0cb-1093489774b9>

## Why HTMX?

HTMX allows us to bring interactivity to our web application without relying on complex JavaScript frameworks. This results in a lighter, more maintainable codebase while still providing the dynamic features typically associated with heavy client-side frameworks. With HTMX, we can update parts of a web page in response to user actions, reducing the need for full page reloads and enhancing the application's responsiveness.

## Why HATEOAS?

HATEOAS is a constraint of the REST application architecture that keeps the RESTful style architecture unique from most other network application architectures. The core principle of HATEOAS is that a client interacts with a network application entirely through hypermedia provided dynamically by application servers. This approach allows for a more decoupled architecture, making our application more adaptable to changes in the future.

## Features

- **Task Management**: Create, edit, delete, and view tasks seamlessly.
- **Real-time Interactivity**: Utilize HTMX for dynamic content updates without page reloads.
- **Modern UI**: Styled with Bootstrap for a responsive and intuitive user interface.
- **RESTful API Design**: Implementing HATEOAS principles for a scalable and robust back-end architecture.

## Installation

To set up and run PyFlask-HTMX-TaskTracker, follow these steps:

1. **Clone the Repository**:

   ```
   git clone https://github.com/abenteuerzeit/PyFlask-HTMX-TaskTracker.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd PyFlask-HTMX-TaskTracker
   ```

3. **Create a Virtual Environment** (optional but recommended):

   ```shell
   python -m venv venv
   ```

   Activate the virtual environment:

      - On Windows:

        ```shell
        venv\Scripts\activate
        ```

      - On macOS and Linux:

        ```shell
        source venv/bin/activate
        ```

4. **Install Dependencies**:

   ```shell
   pip install -r requirements.txt
   ```

5. **Run the Application**:

   ```shell
   python app.py
   ```

   The application will be available at `http://localhost:5000`.

## Contributing

We welcome contributions to the PyFlask-HTMX-TaskTracker project! To contribute, please fork the repository, make your changes, and then submit a pull request back to the main repository. If you have suggestions for improvements or encounter any issues, feel free to open an issue in the repository. We appreciate your input in making this project better!

## License

This project is licensed under the [European Union Public License (EUPL)](https://joinup.ec.europa.eu/collection/eupl/eupl-text-eupl-12).

## Contact

For any further queries or feedback, feel free to reach out to me at <v-adrianmroz@microsoft.com>
