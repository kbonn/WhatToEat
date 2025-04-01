from flask import Flask, render_template

# Create the Flask app instance
app = Flask(__name__)
# Optional: Load configuration from config.py
# app.config.from_object('config.Config')

# Define a simple route
@app.route('/')
def index():
    # This will look for 'index.html' in the 'templates' folder
    return render_template('index.html', title='Welcome')

# Allows running the app directly using 'python app.py'
if __name__ == '__main__':
    # Use debug=True for development (auto-reloads on code changes)
    # Never use debug=True in production!
    app.run(debug=True)