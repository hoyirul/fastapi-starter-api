# FASTAPI-STARTER

## Structure
```bash
accounting-backend/
├── docs/
│   ├── convention-id.md
│   ├── convention-en.md
├── src/
│   ├── modules/
│   │   ├── modules1/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── services.py
│   │   │   ├── routes.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       └── test_accounts.py
│   │   ├── logs/
│   │   │   ├── __init__.py
│   │   │   ├── models.py
│   │   │   ├── schemas.py
│   │   │   ├── services.py
│   │   │   ├── routes.py
│   │   │   └── tests/
│   │   │       ├── __init__.py
│   │   │       └── test_logs.py
│   │   └── __init__.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py
│   │   ├── redis.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── response.py
│   │   ├── dependency.py
│   │   ├── logger.py
│   │   └── security.py
│   ├── main.py
│   ├── routers.py
│   └── startup.py
├── sync/
│   ├── migrations/
│   │   ├── __init__.py
│   ├── seeders/
│   │   ├── __init__.py
│   ├── setup.py
├── templates/
│   ├── fastapi.svg
│   ├── index.html
├── .env
├── .env.example
├── .gitignore
├── app.py
├── docker-compose.yml
├── Dockerfile
├── madhai.py
├── README.md
└── requirements.txt
```

## Installation
1. Clone the Project
    ```bash 
    > git clone giturl
    ```
2. Setup Environment
    ```bash 
    > cd accounting-be
    > python -m venv venv
    > source venv/bin/activate # Linux/MacOS
    > venv\Scripts\Activate # Windows OS
    > pip install -r requirements.txt
    ```
3. Setup project
    ```bash 
    > cp .env.example .env
    ```
4. Setup database, update your env for connect to database
    ```bash 
    # REDIS
    REDIS_HOST=127.0.0.1 # or you ip address
    REDIS_PORT=6379 # your redis port
    REDIS_PASSWORD=secret # Change this value after step 5

    # PostgreSQL
    DB_SECRET_KEY=
    DB_DRIVER=asyncpg
    DB_CONNECTION=postgresql
    DB_USER=postgres
    DB_PASSWORD=your_password # Change this value after step 5
    DB_HOST=localhost
    DB_PORT=5432
    DB_NAME=your_db_name
    ```
5. Make SECRET KEY and JWT SECRET KEY
    ```bash
    > python madhai --generate --key 32 # byte_int -> 8, 16, 32, 64 etc (default 32) for generate secret key
    > python madhai --hash your_password --key from_DB_SECRET_KEY # You can get the key from the log output then copy and paste it to the DB_PASSWORD or DB_REDIS_PASSWORD value in the .env file

    # Then update your env for DB_PASSWORD value with log output 
    ```
6. Sync Database with Migrations and Seeders
    ```bash
    > python madhai --upgrade # for run all migrations
    > python madhai --seed # for run all seeders
    ```
7. Run Application
    ```bash
    > fastapi dev app.py # for run application with host=127.0.0.1 and port=8000
    
    # or

    > fastapi dev app.py --host 0.0.0.0 --port 8000 # for run application with host=your_ip_address and port=8000
    ```

## Run Project
1. Make a modules
    ```bash
    > python madhai --module modulename # for make a module like categories, roles, users etc. Then go to the module on src/module/modulename
    > python madhai --module yourdir/modulename
    ```
    <b>Important : </b> the folder name you should (`snake_case`) following the code convention [convention-id](/docs/convention-id.md) or [convention-en](/docs/convention-en.md) 
2. Make migrations
    ```bash
    > python madhai --make --migration your_migration_name # for make a migration file, (`snake_case`) for example `create_table_users` then file automatically created on `src/database/migrations` your_migration_name_migration.py (IMPORTANT: you should create a migration file with create_table_ prefix)
    ```
3. Run migrations
    ```bash
    > python madhai --upgrade --table your_migration_name # for specific migration
    > python madhai --upgrade # for all migration

    > python madhai --downgrade --table your_migration_name # for drop specific migration
    > python madhai --downgrade # for drop all migration

    > python madhai --make --alter --migration your_migration_name # for make a migration file with alter table, (`snake_case`) for example `alter_table_users` then file automatically created on `src/database/migrations` your_migration_name_migration.py (IMPORTANT: you should create a migration file with alter_table_ prefix)
    > python madhai --upgrade --alter --table your_migration_name # for specific migration with alter table
    > python madhai --downgrade --alter --table your_migration_name # for drop specific migration with alter table

    ```
    <b>IMPORTANT:</b> After you run the migration, you should modify the migration file to add the column, table, or anything you want to change
    - Docs Create Statement (PostgreSQL) : [PostgreSQL Docs](https://www.w3schools.com/postgresql/postgresql_create_table.php)
    - Docs Alter Statement (PostgreSQL) : [PostgreSQL Docs](https://www.w3schools.com/postgresql/postgresql_alter_column.php)
4. Make seeders
    ```bash
    > python madhai --make --seeder your_seeder_name # for make a seeder file, (`snake_case`) for example `users` or `categories` then file automatically created on `src/database/seeders` your_seeder_name_seeder.py
    ```
5. Run seeders
    ```bash
    > python madhai --seed --table your_seeder_name # for specific seeder
    > python madhai --seed # for all seeder

    > python madhai --rollback --table your_seeder_name # for truncate specific seeder
    > python madhai --rollback # for truncate all seeder
    ```

## References
- [FastAPI Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)
- [SQLAlchemy Documentation](https://fastapi.tiangolo.com/tutorial/first-steps/)

## License
[MIT](https://choosealicense.com/licenses/mit/) License

## Author
[CV. Ika Raya Sentausa - 2024](https://irasa.co.id)
