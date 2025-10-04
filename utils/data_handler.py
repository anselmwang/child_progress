import json
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
import tempfile

class DataHandler:
    def __init__(self, data_file='data/progress.jsonl', backup_dir='data/backups', max_backups=10):
        self.data_file = data_file
        self.backup_dir = backup_dir
        self.max_backups = max_backups
        
        # Ensure directories exist
        os.makedirs(os.path.dirname(data_file), exist_ok=True)
        os.makedirs(backup_dir, exist_ok=True)
    
    def load_all_data(self) -> List[Dict[str, Any]]:
        """Load all progress data from JSONL file."""
        if not os.path.exists(self.data_file):
            return []
        
        data = []
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        data.append(json.loads(line))
        except (json.JSONDecodeError, FileNotFoundError):
            return []
        
        return data
    
    def get_data_by_date(self, date_str: str) -> Dict[str, Any]:
        """Get progress data for a specific date."""
        all_data = self.load_all_data()
        for record in all_data:
            if record.get('date') == date_str:
                return record
        return {}
    
    def create_backup(self):
        """Create a backup of the current data file."""
        if not os.path.exists(self.data_file):
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"progress_backup_{timestamp}.jsonl"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            shutil.copy2(self.data_file, backup_path)
            self._cleanup_old_backups()
        except Exception as e:
            print(f"Warning: Failed to create backup: {e}")
    
    def _cleanup_old_backups(self):
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = [f for f in os.listdir(self.backup_dir) if f.startswith('progress_backup_')]
            backup_files.sort(reverse=True)  # Most recent first
            
            # Remove excess backups
            for backup_file in backup_files[self.max_backups:]:
                backup_path = os.path.join(self.backup_dir, backup_file)
                os.remove(backup_path)
        except Exception as e:
            print(f"Warning: Failed to cleanup old backups: {e}")
    
    def save_data(self, all_data: List[Dict[str, Any]]):
        """Save all data using atomic write with backup."""
        # Create backup before writing
        self.create_backup()
        
        # Use atomic write: write to temp file first, then rename
        temp_file = None
        try:
            # Create temporary file in the same directory
            temp_dir = os.path.dirname(self.data_file)
            with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', 
                                           dir=temp_dir, delete=False) as f:
                temp_file = f.name
                for record in all_data:
                    json.dump(record, f, ensure_ascii=False)
                    f.write('\n')
            
            # Atomic rename
            shutil.move(temp_file, self.data_file)
            temp_file = None  # Successfully moved
            
        except Exception as e:
            # Cleanup temp file on error
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except:
                    pass
            raise e
    
    def update_date_record(self, date_str: str, problems: List[str], 
                          exercises: List[str], notes: str, book: str = "Introduction to Algebra"):
        """Update or create a record for a specific date."""
        all_data = self.load_all_data()
        
        # Find existing record or create new one
        record_found = False
        for i, record in enumerate(all_data):
            if record.get('date') == date_str:
                all_data[i] = {
                    'date': date_str,
                    'problems': problems,
                    'exercises': exercises,
                    'notes': notes,
                    'book': book
                }
                record_found = True
                break
        
        if not record_found:
            all_data.append({
                'date': date_str,
                'problems': problems,
                'exercises': exercises,
                'notes': notes,
                'book': book
            })
        
        # Sort by date
        all_data.sort(key=lambda x: x['date'])
        
        # Save all data
        self.save_data(all_data)
    
    def get_latest_problems_and_exercises(self, before_date: str = None) -> tuple:
        """Get the latest problems and exercises before a given date."""
        all_data = self.load_all_data()
        
        # Filter data before the given date if specified
        if before_date:
            all_data = [record for record in all_data if record['date'] < before_date]
        
        if not all_data:
            return [], []
        
        # Sort by date and get the latest record
        all_data.sort(key=lambda x: x['date'])
        latest_record = all_data[-1]
        
        return latest_record.get('problems', []), latest_record.get('exercises', [])
