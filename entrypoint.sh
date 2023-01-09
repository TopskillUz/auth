if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."
    while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

pip install --upgrade pip
pip install -r requirements.txt
echo "Successfully installed requirements.txt"


alembic upgrade head
echo "Successfully created tables"

# Start server
echo "Starting server and client"
python client.py
python server.py



