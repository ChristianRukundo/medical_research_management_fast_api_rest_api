# medical_research_management_fast_api_rest_api

This is a REST API for a medical research management project. The project helps manage medical research data, user profiles, and research project details. It is designed for institutions or organizations conducting medical research, providing an efficient and scalable platform for managing research data and interactions.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup](#setup)
- [Database](#database)
- [Data Generation](#data-generation)
- [Usage](#usage)
- [License](#license)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)

## Overview

This system provides a platform for managing medical research data. It is built using Python and FastAPI, with PostgreSQL as the database backend. The API supports functionalities for managing user profiles, research projects, and data import/export operations.

Key features include:
- User authentication and management
- Research project creation, modification, and deletion
- Data importation via APIs and SQL inserts
- Dynamic data generation for testing and demo purposes
- Exporting data to CSV or other formats for analysis or reporting

## Features

- **User Management**: Admins can add, update, and remove users from the system.
- **Research Project Management**: Users can manage their research projects, including editing details and categorizing them.
- **Data Import & Export**: The system supports importing data via APIs or SQL inserts, and exporting research data for analysis or reporting.
- **Dynamic Data Generation**: Automatically generate data for users and research projects, useful for testing purposes.

## Technologies Used

- **FastAPI**: Web framework for building the REST API.
- **PostgreSQL**: Database for storing user and research data.
- **SQLAlchemy**: ORM for interacting with the database.
- **Pandas**: For data processing and management.
- **Alembic**: For database migrations.
- **Docker**: Optional containerization of the app and database.
- **GitHub Actions**: For CI/CD pipeline automation.

## Setup

### Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- PostgreSQL
- Docker (optional but recommended for containerized deployment)

### Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/ChristianRukundo/medical_research_management_fast_api_rest_api.git
cd medical_research_management_fast_api_rest_api
