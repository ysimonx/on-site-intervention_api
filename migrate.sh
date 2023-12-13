export DEV_DATABASE_URL=mysql+pymysql://intervention_on_site:*@*.*.*.*:3306/intervention_on_site_dev
export FLASK_APP=api-intervention_on_site.py
export FLASK_DEBUG=1

sleep 3

flask db init

sleep 3

flask db migrate -m "Initial migration"

sleep 3

flask db upgrade

sleep 3

flask db check
