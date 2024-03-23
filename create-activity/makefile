create-open-app: 
	docker build -t form --platform linux/amd64 .
	docker run -p 8501:8501 form

open-app:
	docker run -p 8501:8501 form

open-local:
	streamlit run app.py --server.port=8501 --server.address=0.0.0.0

open-login:
	streamlit run loginpage.py --server.port=8501 --server.address=0.0.0.0
