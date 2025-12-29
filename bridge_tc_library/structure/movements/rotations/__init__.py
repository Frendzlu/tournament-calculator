from .analyzer import RotationAnalyzer

# Dynamically load all rotation classes from available modules
_rotation_classes = RotationAnalyzer.get_rotation_classes()

# Make rotation classes available at package level
for _class_name, _class_obj in _rotation_classes.items():
    if _class_obj is not None:
        globals()[_class_name] = _class_obj

"""# Maintain backward compatibility with explicit imports
try:
    from .howell import HowellMovement  # type: ignore
except Exception:
    HowellMovement = _rotation_classes.get('HowellMovement')  # type: ignore

try:
    from .mitchell import MitchellMovement  # type: ignore
except Exception:
    MitchellMovement = _rotation_classes.get('MitchellMovement')  # type: ignore
"""
# Export available rotation classes
__all__ = [name for name in _rotation_classes.keys() if _rotation_classes[name] is not None]
