# FastAPI Backend Service

This is a simple FastAPI backend service designed to demonstrate a basic REST API setup with Docker. It includes a "Hello World" endpoint that greets users by name.

## Setup

To get started with this project, make sure you have Docker and Docker Compose installed on your machine.

1. **Clone the repository:**

   ```
   git clone <repository-url>
   ```

2. **Navigate to the backend directory:**

   ```
   cd backend
   ```

3. **Build the Docker container:**

   ```
   docker-compose build
   ```

## Running the Service

To run the service in development mode, use the following command:

```
docker-compose up
```

This command starts the FastAPI server inside a Docker container, making it accessible at \`http://localhost:8000\`.

## Endpoints

The service includes the following endpoints:

- **Hello World:**

  - \`GET /hello/{name}\`

    Returns a greeting message to the specified name.

    **Example Request:**

    ```
    GET /hello/John
    ```

    **Example Response:**

    ```json
    {
    	"message": "Hello World, John"
    }
    ```

## Stopping the Service

To stop the running Docker container, use the following command:

```
docker-compose down
```

This command stops and removes the container created by \`docker-compose up\`, effectively stopping the service.
