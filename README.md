


 python -m venv venv
 venv\Scripts\activate
 pip install -r requirements.txt
pip install --force-reinstall passlib[bcrypt]


uvicorn main:app --reload --host 0.0.0.0 --port 8000


## notes

https://www.youtube.com/watch?v=uy4TPngK-8c&list=PLsyeobzWxl7qF4ASwCZZDXor_Y0YJ3Qfc&index=7
https://www.youtube.com/watch?v=QkGqjPFIGCA
https://www.youtube.com/watch?v=J7SXGbShbj8

https://medium.com/@ChanakaDev/mongodb-with-fastapi-1d5440880520