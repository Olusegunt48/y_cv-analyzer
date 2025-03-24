import os

def save_uploaded_file(uploaded_file, save_path="uploads/"):
    """Saves an uploaded file to a specified directory."""
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    file_path = os.path.join(save_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path
