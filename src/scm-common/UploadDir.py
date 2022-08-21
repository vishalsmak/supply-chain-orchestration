import os

def get_upload_dir():
    api_dir = os.path.dirname(os.path.realpath(__file__))
    app_dir = os.path.dirname(api_dir)
    upload_dir = os.path.join(app_dir, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir