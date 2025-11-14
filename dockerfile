# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the Python path to include the src directory
ENV PYTHONPATH "${PYTHONPATH}:/app/src"

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the rest of the application code into the container
COPY src/ ./src/
COPY start.sh .

# Make the startup script executable (it's already copied)
RUN chmod +x start.sh

# Expose the ports the app runs on
EXPOSE 8000
EXPOSE 8501

# Run the startup script when the container launches
CMD ["./start.sh"]