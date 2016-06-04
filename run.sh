if [ -x "$(which pip)" ]; then
        echo '---'
else
        echo 'installing pip'
        curl -L 'https://bootstrap.pypa.io/get-pip.py' | python -
fi

python -m pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
