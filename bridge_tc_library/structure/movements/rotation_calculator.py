# python
import importlib
import inspect
from typing import Dict, Type, Any, List, Tuple

from bridge_tc_library.structure import AbstractRotation
from bridge_tc_library.structure.movements.abstract_rotation import RotationParams


class RotationCalculator:
    """
    During initialization, dynamically imports all rotation classes from the
    'bridge_tc_library.structure.movements.rotations' module and stores them in a dictionary.
    """

    def __init__(self) -> None:
        module_name = "bridge_tc_library.structure.movements.rotations"
        try:
            mod = importlib.import_module(module_name)
        except Exception as e:
            raise ImportError(f"Couldn't import {module_name}: {e}") from e

        rotations: Dict[str, Type[Any]] = {}

        if hasattr(mod, "_rotation_classes") and isinstance(getattr(mod, "_rotation_classes"), dict):
            for name, cls in getattr(mod, "_rotation_classes").items():
                rotations[name] = cls
        else:
            for name in dir(mod):
                if name.startswith("_"):
                    continue
                attr = getattr(mod, name)
                if inspect.isclass(attr) and getattr(attr, "__module__", None) == mod.__name__:
                    rotations[name] = attr

        self.rotations = rotations

    def get(self, name: str):
        """Returns the rotation class by its name, or None if not found."""
        return self.rotations.get(name)

    def get_rotations(self, num_pairs: int, min_boards_amount: int, max_boards_amount: int, min_boards_per_boardgroup: int) -> List[Tuple[Type[AbstractRotation], RotationParams]]:
        """
        Returns a list of tuples containing the rotation class and possible rotation parameters.
        Each tuple contains (RotationClass, RotationParams) where RotationParams has
        (num_tables, num_board_groups, boards_per_board_group).
        """
        results: List[Tuple[Type[AbstractRotation], RotationParams]] = []
        for cls in self.rotations.values():
            if hasattr(cls, 'generate_possible_rotations'):
                possible_rotations = cls.generate_possible_rotations(
                    num_pairs, min_boards_amount, max_boards_amount, min_boards_per_boardgroup
                )
                for params in possible_rotations:
                    results.append((cls, params))
        return results