from app import create_app

app = create_app()

# If app.py is run directly start in debug mode
if __name__ == "__main__":
	app.run(debug=True)