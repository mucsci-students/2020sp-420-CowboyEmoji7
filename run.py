from app_package import app


if __name__ == "__main__":
    app.secret_key = 'the random and secure key'
    app.run(debug=True)