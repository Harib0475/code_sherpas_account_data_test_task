
# Bank Account

This is a Django REST API for managing bank accounts and transactions. The project includes endpoints for creating accounts, customers, depositing, withdrawing, transferring money, and retrieving transaction histories. Swagger documentation is provided for easy testing and interaction with the API.

## Features

- Create and manage bank accounts
- Deposit money into an account
- Withdraw money from an account
- Transfer money between accounts
- Retrieve transaction histories for accounts
- Create and Retrieve Customers
- Swagger documentation for API endpoints
![All Endpoints Image not Found](all_endpoints.png?raw=true "Title")

## Requirements

- Python 3.x
- Django 3.x or higher
- Django REST Framework
- drf-yasg
- Faker

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Harib0475/code_sherpas_account_data_test_task.git
   cd code_sherpas_account_data_test_task
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
    ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
    ```bash
   python manage.py migrate
   ```

5. Populate the database with dummy data:
   ```bash
   python manage.py populate_data
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the Swagger documentation:
   Open your browser and go to `http://127.0.0.1:8000/swagger/`

## Endpoints

### Accounts

- **List Accounts / Create Account**
  - `GET /api/accounts/`
  - `POST /api/accounts/`

- **Retrieve / Update / Delete Account**
  - `GET /api/accounts/{id}/`
  - `PUT /api/accounts/{id}/`
  - `DELETE /api/accounts/{id}/`

### Transactions

- **Deposit Money**
  - `POST /api/accounts/{id}/deposit/`
  - Request Body:
    ```json
    {
      "amount": 100.0
    }
    ```

- **Withdraw Money**
  - `POST /api/accounts/{id}/withdraw/`
  - Request Body:
    ```json
    {
      "amount": 50.0
    }
    ```

- **Transfer Money**
  - `POST /api/accounts/transfer/`
  - Request Body:
    ```json
    {
      "from_iban": "IBAN123",
      "to_iban": "IBAN456",
      "amount": 200.0
    }
    ```

- **List Transactions By Filters**
  - `GET /api/accounts/{id}/transactions/?end_date=2024-12-31&ordering=-date&page=2&page_size=1&start_date=2024-01-01&transaction_type=D`
    ![Transaction Image not Found](transactions.png?raw=true "Title")
  
- **Retrieve / Update / Delete Customers**
  - `GET /api/customers/{id}/`
  - `PUT /api/customers/{id}/`
  - `DELETE /api/customers/{id}/`
- 
## Running Tests

To run tests, use the following command:
```bash
python manage.py test
```
![Test Cases Image not Found](test_cases_results.png?raw=true "Title")


## Management Command

The project includes a management command to populate the database with dummy data. This can be run using:
```bash
python manage.py populate_data
```
![Populate Data Image not Found](populate_data.png?raw=true "Title")


## Acknowledgements

- Django REST Framework
- drf-yasg for Swagger documentation
- Faker for generating dummy data
