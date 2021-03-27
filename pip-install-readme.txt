Installing pandas on the M1 is a bitch - check this out https://stackoverflow.com/questions/65084318/trouble-installing-pandas-on-new-macbook-air-m1

#python3 -m pip install virtualenv
#virtualenv -p python3.8 venv

## already had a venv 
source venv/bin/activate
pip install --upgrade pip
pip install numpy cython
git clone https://github.com/pandas-dev/pandas.git
cd pandas
python3 setup.py install
