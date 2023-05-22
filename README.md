# Technical challenge

## Description
This project aims to create an API that allows execute several functionalities required by Globant including: Data migration, create backup from a database in avro format, restore a database from avro files, create reports.

## Arquitecture

![Architecture](/images/architecture.jpeg)

## API Features

- **Migrate data**: The API allows users migrate a database by csv files uploading to a google cloud storage bucket. Once a file is upload, a cloud function is triggered in order to build a payload and consume the API and execute the endpoint to migrate data to the company database.
- **Create database backup**: This endpoint helps users to create a backup on google Cloud Storage in avro format files. These wiil be created according the date that endopint was executed.
- **Restore database**: This feature restore a database from avro files that were storaged on the GCS bucket. Users wiil be able to do it according to a given date.
- **Create report**: Users will be able to create 2 reports by one only endpoint. this could be done indicating the report name and a year.



## Technologies Used

- **Backend**: The API is built using Python and FastAPI and after that deployed on Cloud Run
- **Database**: Data is stored in SQLLite3 database.
- **Backup**: Avro and csv files are storaged on Google Cloud Storage bucket.
- **Report Generation**: Reports are written on Bigquery
- **Dashboard**: The dashboard is built with Looker Studio.

## Installation and Setup

1. Clone the repository.
2. Create a Cloud run service
3. Set environemnt variables on github included in ci_cd.yaml
4. create a a gcs bucket, bigquery dataset on a GCP Project
5. Access the API endpoints and dashboard in your web browser.

## Usage

- Use the API endpoints to perform CRUD operations on the data.
- Generate reports based on the available data by invoking the report generation functionality.
- Access the dashboard to visualize and analyze the data through interactive charts and graphs.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

