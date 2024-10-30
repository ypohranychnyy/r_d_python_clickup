# r_d_python_clickup
Автоматизація API з використанням Python та налаштування CI/CD
# README.md

# Python ClickUp API Automation Tests

This project contains automated tests for ClickUp API's list operations using Python. The tests include creating, retrieving, updating, and deleting lists using the ClickUp API. These tests are implemented with the help of the `pytest` framework and `pytest-steps` for step-based testing.

## Project Setup

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/ypohranychnyy/r_d_python_clickup.git
   cd r_d_python_clickup
   ```

2. **Create and Activate a Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # For macOS/Linux
   venv\Scripts\activate  # For Windows
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**
   Create a `.env` file in the root directory of your project with the following variables:
   ```
   BASE_URL=https://api.clickup.com/api/v2
   CLICKUP_API_TOKEN=<your_clickup_api_token>
   CLICKUP_FOLDER_ID=<your_clickup_folder_id>
   ```

## Running Tests

To run the tests and generate an HTML report:

```sh
pytest tests/ --html=report.html --self-contained-html
```

- The HTML report will be saved in the `report.html` file for detailed analysis.

## Test Description

The following CRUD operations are tested:

1. **Create List**: A new list is created in the given folder.
2. **Get List**: The created list is retrieved to verify its presence.
3. **Update List**: The list name is updated to verify the update functionality.
4. **Delete List**: The list is deleted, and the deletion is verified.

## Continuous Integration Setup

The project is configured for CircleCI to automatically run tests whenever changes are pushed to the repository.

### CircleCI Configuration

The `.circleci/config.yml` file contains the configuration for running the tests in CircleCI. To set up CircleCI for this project:

1. Make sure to connect your GitHub repository with CircleCI.
2. The configuration installs dependencies, runs tests, and generates reports.

```yaml
version: 2.1

jobs:
  python-job:
    docker:
      - image: circleci/python:3.12
    steps:
      - checkout
      - run:
          name: set up venv
          command: |
            python -m venv venv
            . venv/bin/activate
      - run:
          name: install dependencies
          command: |
            . venv/bin/activate
            pip install -r requirements.txt
      - run:
          name: run tests
          command: |
            . venv/bin/activate
            pytest --html=./report/report.html --self-contained-html
      - store_artifacts:
          path: report/
          destination: python-report

workflows:
  build-and-test:
    jobs:
      - python-job
```

## Notes

- Ensure you have proper permissions and API tokens to access the ClickUp API.
- The tests include preconditions and postconditions to ensure that each test can be run independently.

## License

This project is licensed under the MIT License.

## Author

Yuriy Pohranychnyy