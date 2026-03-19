# Online Property Rental Real Estate Platform

## Project Overview
This project is an online platform designed to facilitate property rentals in a streamlined manner. Users can easily browse listings, landlords can manage their properties, and potential tenants can find their ideal homes.

## Features
- **User Authentication:** Secure login and registration for landlords and tenants.
- **Property Listings:** Users can browse, filter, and search for properties based on various criteria.
- **Booking System:** Tenants can book properties directly through the platform.
- **Admin Dashboard:** An administrative interface for managing users and properties.
- **Feedback System:** Both landlords and tenants can provide feedback on their experiences.

## Tech Stack
- **Frontend:** React.js, Bootstrap 4
- **Backend:** Node.js, Express.js
- **Database:** MongoDB
- **Authentication:** JSON Web Token (JWT) for secure user authentication

## Installation Guide
### Prerequisites
- Node.js installed on your machine.
- MongoDB running locally or a cloud MongoDB service.

### Steps
1. Clone the repository: `git clone https://github.com/Sumannay/Online-Property-Rental-Real-Estate-Platform.git`
2. Navigate into the project directory: `cd Online-Property-Rental-Real-Estate-Platform`
3. Install backend dependencies: `cd backend && npm install`
4. Install frontend dependencies: `cd ../frontend && npm install`
5. Run the backend server: `cd backend && npm start`
6. Run the frontend application: `cd frontend && npm start`

## Database Models
- **User:** Stores user information including username, password, role (landlord/tenant).
- **Property:** Contains details of properties including location, price, availability, and landlord ID.
- **Booking:** Manages bookings with references to users and properties.
- **Feedback:** Captures feedback from tenants about properties and landlords.

## API Routes
| Method | Endpoint              | Description                      |
|--------|-----------------------|----------------------------------|
| GET    | /api/properties       | Retrieve all properties          |
| GET    | /api/properties/:id   | Retrieve specific property       |
| POST   | /api/properties       | Create new property             |
| PUT    | /api/properties/:id   | Update existing property         |
| DELETE | /api/properties/:id   | Delete a property               |
| POST   | /api/auth/login       | Authenticate user               |

## Usage Guide
1. Follow the installation guide to set up the project.
2. Use the frontend interface to browse and book properties.
3. Landlords can manage their listings through the admin dashboard.
4. Provide feedback after booking to help other users.

## Contributing Guidelines
- Fork the project and clone it to your local machine.
- Create a new branch for your feature: `git checkout -b feature/YourFeature`.
- Make your changes and commit them: `git commit -m 'Add some feature'`.
- Push to your branch: `git push origin feature/YourFeature`.
- Open a pull request detailing your changes.

## Acknowledgments
- Inspired by online rental platforms.
- Special thanks to contributors and users for their feedback and support.