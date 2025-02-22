# Use an official lightweight Python image
FROM python:3.10

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Expose the port Flask runs on
EXPOSE 5000

# Run database migrations and start the app
CMD ["sh", "-c", "flask db upgrade && python run.py"]
