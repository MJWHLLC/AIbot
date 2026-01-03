from setuptools import setup, find_packages

setup(
    name="paralegal-agent",
    version="0.1.0",
    packages=find_packages(),
    py_modules=[
        'app',
        'app_new',
        'auth',
        'mail',
        'model_client',
        'model_client_real',
        'prompts',
        'prompts_full',
        'users'
    ],
    install_requires=[
        "Flask>=2.0",
        "python-dotenv>=0.21",
        "requests>=2.28",
        "Flask-WTF>=1.1",
        "Flask-Mail>=0.9",
    ],
    extras_require={
        'dev': [
            'pytest>=7.0',
            'pytest-cov',
            'flake8',
        ]
    },
    python_requires='>=3.9',
)
