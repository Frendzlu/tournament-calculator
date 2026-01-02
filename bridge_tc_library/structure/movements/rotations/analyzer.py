"""
Analyzer for dynamically discovering and loading rotation classes from the rotations folder.
"""

import importlib
import inspect
import os
from typing import Dict, Type, Optional, List
from pathlib import Path


class RotationAnalyzer:
    """Analyzes rotation modules and discovers available rotation classes."""
    
    @staticmethod
    def get_rotations_dir() -> Path:
        """Get the path to the rotation directory."""
        return Path(__file__).parent
    
    @staticmethod
    def get_rotation_modules() -> List[str]:
        """
        Discover all Python modules in the rotations directory.
        
        Returns:
            List of module names (without .py extension)
        """
        rotations_dir = RotationAnalyzer.get_rotations_dir()
        modules = []
        
        for file in rotations_dir.glob('*.py'):
            if file.name.startswith('_'):
                continue
            if file.is_file():
                modules.append(file.stem)
        
        return sorted(modules)
    
    @staticmethod
    def load_rotation_module(module_name: str):
        """
        Dynamically load a rotation module.
        
        Args:
            module_name: Name of the module to load (without .py)
            
        Returns:
            The imported module or None if import fails
        """
        try:
            return importlib.import_module(f'.{module_name}', package='bridge_tc_library.structure.movements.rotations')
        except Exception as e:
            print(f"Failed to load rotation module '{module_name}': {e}")
            return None
    
    @staticmethod
    def get_rotation_classes() -> Dict[str, Optional[Type]]:
        """
        Discover and load all rotation classes from modules.
        
        Returns:
            Dictionary mapping class names to classes (or None if import failed)
        """
        rotations = {}
        
        for module_name in RotationAnalyzer.get_rotation_modules():
            module = RotationAnalyzer.load_rotation_module(module_name)
            if module is None:
                continue
            
            # Look for classes that end with 'Movement'
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if name.endswith('Movement') and obj.__module__ == module.__name__:
                    rotations[name] = obj
        
        return rotations
    
    @staticmethod
    def get_failed_imports() -> Dict[str, str]:
        """
        Get modules that failed to import.
        
        Returns:
            Dictionary mapping module names to error messages
        """
        failed = {}
        
        for module_name in RotationAnalyzer.get_rotation_modules():
            try:
                importlib.import_module(f'.{module_name}', package='bridge_tc_library.structure.movements.rotations')
            except Exception as e:
                failed[module_name] = str(e)
        
        return failed
