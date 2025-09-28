# MedBotanica Server

MedBotanica Server is the backend API for the MedBotanica application, designed to manage and serve data related to medicinal plants, herbal remedies, and user interactions.

## Features

- RESTful API for plant and remedy data
- User authentication and authorization
- Search and filter functionality
- Secure data management

## Technologies Used

- Node.js
- Express.js
- MongoDB (Mongoose)
- JWT Authentication

## Getting Started

1. Clone the repository.
2. Install dependencies:  
    ```bash
    npm install
    ```
3. Set up environment variables (see `.env.example`).
4. Start the server:  
    ```bash
    npm start
    ```

## API Documentation

See the [API Docs](./docs/API.md) for detailed endpoints and usage.

## Contributing

Pull requests are welcome. For major changes, please open an issue first.

## License

This project is licensed under the MIT License.

 python -m venv venv
 venv\Scripts\activate
 pip install -r requirements.txt
uvicorn app.main:app --reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pip install --force-reinstall passlib[bcrypt]




## notes

https://www.youtube.com/watch?v=uy4TPngK-8c&list=PLsyeobzWxl7qF4ASwCZZDXor_Y0YJ3Qfc&index=7
https://www.youtube.com/watch?v=QkGqjPFIGCA
https://www.youtube.com/watch?v=J7SXGbShbj8

https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520