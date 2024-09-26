# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to install dependencies
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire TCC2 contents into the container
COPY . .

# Set environment variables for Flask
ENV FLASK_APP=app
ENV FLASK_ENV=development
ENV DATABASE_URL=postgresql+psycopg2://user:password@tcc2-db-1:5432/mydatabase

# Expose port 5000 to the world outside this container
EXPOSE 5000

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]