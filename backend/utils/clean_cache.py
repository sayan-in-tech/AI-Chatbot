import os
import shutil
import traceback
from pathlib import Path

def clean_pycache():
    """Clean all __pycache__ directories"""
    try:
        print("🔧 [utils/clean_cache.py:clean_pycache] Starting cache cleanup")
        
        try:
            project_root = Path(__file__).parent.parent.parent
            print(f"✅ [utils/clean_cache.py:clean_pycache] Project root: {project_root}")
        except Exception as e:
            print(f"❌ [utils/clean_cache.py:clean_pycache] Error getting project root: {str(e)}")
            traceback.print_exc()
            raise
        
        try:
            cache_count = 0
            for root, dirs, files in os.walk(project_root):
                for dir_name in dirs:
                    if dir_name == '__pycache__':
                        try:
                            cache_path = os.path.join(root, dir_name)
                            shutil.rmtree(cache_path)
                            cache_count += 1
                            print(f"✅ [utils/clean_cache.py:clean_pycache] Removed: {cache_path}")
                        except PermissionError as e:
                            print(f"❌ [utils/clean_cache.py:clean_pycache] Permission denied removing {cache_path}: {str(e)}")
                            traceback.print_exc()
                        except FileNotFoundError as e:
                            print(f"⚠️  [utils/clean_cache.py:clean_pycache] Cache directory already removed: {cache_path}")
                        except Exception as e:
                            print(f"❌ [utils/clean_cache.py:clean_pycache] Error removing {cache_path}: {str(e)}")
                            traceback.print_exc()
            
            if cache_count > 0:
                print(f"✅ [utils/clean_cache.py:clean_pycache] Cache cleaned successfully (removed {cache_count} directories)")
            else:
                print("✅ [utils/clean_cache.py:clean_pycache] No cache directories found")
        except Exception as e:
            print(f"❌ [utils/clean_cache.py:clean_pycache] Error during cache walk: {str(e)}")
            traceback.print_exc()
            raise
        
    except Exception as e:
        print(f"❌ [utils/clean_cache.py:clean_pycache] Unexpected error cleaning cache: {str(e)}")
        traceback.print_exc()
        raise