import os
import shutil
from datetime import datetime
from website import DB_NAME

def backup_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    instance_dir = os.path.join(current_dir, 'instance')
    backups_dir = os.path.join(instance_dir, 'backups_db')
    db_file_path = os.path.join(instance_dir, DB_NAME) 
    if not os.path.exists(backups_dir):
        os.makedirs(backups_dir)
        
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    backup_file_name = f'databackup_{timestamp}.db'
    backup_file_path = os.path.join(backups_dir, backup_file_name)
    
    shutil.copy(db_file_path, backup_file_path)
    
    print(f"Database backed up to: {backup_file_path}")

if __name__ == "__main__":
    backup_database()