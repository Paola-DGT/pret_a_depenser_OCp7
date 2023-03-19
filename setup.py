from setuptools import find_packages, setup

setup(
    name="risk_assesment_app",
    version="0.0.1",
    python_requires=">=3.8",
    packages=find_packages(),
    author="Paola DGT",
    author_email="paola.dgt@gmail.com",
    description="OC project 7",
    url="",
    install_requires=[
        "fastapi",
        "gunicorn",
        "pandas",
        "pydantic",
        "pytest",
        "starlette",
        "uvicorn",
        "scikit-learn",
        "streamlit",
        "streamlit_authenticator",
        "watchdog",
        "pyyaml",
    ],
)
