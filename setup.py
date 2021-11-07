from setuptools import setup
import mp_logger

setup(
    name='mp_logger',
    version=mp_logger.__version__,
    description='Moon Package for logger(csv, slack, google, mongo, notion)',
    url='https://github.com/hopelife/mp_logger',
    author='Moon Jung Sam',
    author_email='monblue@snu.ac.kr',
    license='MIT',
    packages=['mp_logger'],
    # entry_points={'console_scripts': ['mp_logger = mp_logger.__main__:main']},
    keywords='logger(csv, google, mongo, notion, )',
    # python_requires='>=3.8',  # Python 3.8.6-32 bit
    # install_requires=[ # 패키지 사용을 위해 필요한 추가 설치 패키지
    #     'google-api-python-client',
    #     'google-auth-httplib2',
    #     'google-auth-oauthlib',
    #     'oauth2client', 
    #     'gspread'
    # ],
    # zip_safe=False
)

# - pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
# - pip install --upgrade oauth2client
# - pip install gspread