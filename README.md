# Project Name

Brief description of the project and its main functionality.

## Technologies Used

- Backend: Python 3.11, Django 4.1.5
- Frontend: HTML, CSS, Bootstrap, JS

## Description

The project consists of a web application that enables users to work with NFT collections and manage their wallet and tokens. The backend is implemented using Python 3.11 and Django 4.1.5, while the frontend is built with HTML, CSS, Bootstrap, and JS.

## Features

- Distributed business logic, CRUD, and data processing in Models and Views on the backend.
- Authentication and additional interactions for users.
- Web3 integration through web3auth.js to connect the user's wallet and retrieve wallet balance.
- Utilization of the `def get_balance(address)` function in Models to fetch wallet balance.
- Retrieval of NFT tokens on the user's wallet using the `get_token_list(address)` function through the debank service API.
- Automatic connection of users by their Web3 wallet.
- Displaying the user's tokens and portfolio information in the "Profile" section.
- Synchronization of all data with the database (MySQL or SQLite).

## Frontend Modifications

The frontend is built based on a pre-existing template with some customized changes. The structure has been modified to divide it into `base.html`, and templates have been moved to separate HTML sections for better frontend management.
