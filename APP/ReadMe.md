1. Create a database in pgAdmin and enable the postGIS extension
2. Create a .env file and add the var DATABASE_URL = 'posgresql://postgres:<your password>@localhost:<your port>/<db name>'
3. Run the fill_database.py file (if needed update the paths to the resources)
4. Run app.py
5. Run frontend dashboard notebook (if needed update the output path)