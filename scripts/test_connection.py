# FILE: test_connection.py
# PURPOSE: Validate Snowflake connectivity using environment variables
# PHASE: 1
# DEPENDS ON: .env populated with Snowflake credentials
# OUTPUTS: Prints connection status and Snowflake version
import os

from dotenv import load_dotenv
import snowflake.connector


def main() -> None:
    load_dotenv()  # Load local environment variables for connection settings

    conn = snowflake.connector.connect(
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        role=os.getenv("SNOWFLAKE_ROLE"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT CURRENT_VERSION()")  # Verify connectivity with a simple query
            version = cursor.fetchone()[0]
            print(f"SUCCESS: Connected to Snowflake version {version}")
    finally:
        conn.close()  # Always close the connection to avoid leaking sessions


if __name__ == "__main__":
    main()
