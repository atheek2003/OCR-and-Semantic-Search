# # Base image with Python 3.8
# FROM python:3.8-slim

# # Set environment variables
# ENV PYTHONDONTWRITEBYTECODE=1
# ENV PYTHONUNBUFFERED=1

# # Create and set the working directory
# WORKDIR /app

# # Copy the requirements.txt file to the working directory
# COPY requirements.txt /app/

# # Install dependencies
# RUN pip install --upgrade pip
# RUN pip install -r requirements.txt

# # Copy the entire project into the container
# COPY . /app/

# # Expose the port that the app will run on
# EXPOSE 5000

# # Set the default command to run the Flask app
# CMD ["python", "app.py"]
