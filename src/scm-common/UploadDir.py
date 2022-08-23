import os

def get_upload_dir():
    cmn_dir = os.path.dirname(os.path.realpath(__file__))
    app_dir = os.path.dirname(cmn_dir)
    upload_dir = os.path.join(app_dir, 'uploads')
    os.makedirs(upload_dir, exist_ok=True)
    return upload_dir