apt-get update
apt-get install python3-venv
apt-get install libgl1
apt-get install mysql-client

python3 -m venv ./env
source env/bin/activate

pip install opencv-python flask flask-sqlalchemy PyMySQL cryptography uuid flask-cors datetime flask_bcrypt flask_security email_validator flask_jwt_extended opencv-python numpy exif piexif
pip install tb_rest_client request
pip install jsonpickle
pip install tb_rest_client
pip install requests
pip install Flask-Migrate
pip install Pillow
pip install python-resize-image
pip install csv
pip install pandas


pip install -r requirements.txt --upgrade

# mysql -u root -e "create database if not exists intervention_on_site_dev"; 
 