from .base import BaseProblemGenerator
from .number_sense import NumberSenseGenerator
from .measurement import MeasurementGenerator
from .geometry import GeometryGenerator
from .patterning import PatterningGenerator
from .data_management import DataManagementGenerator

GENERATORS = {
    "number_sense": NumberSenseGenerator,
    "measurement": MeasurementGenerator,
    "geometry": GeometryGenerator,
    "patterning": PatterningGenerator,
    "data_management": DataManagementGenerator
}

def get_generator(topic):
    """Get the appropriate generator for a topic."""
    generator_class = GENERATORS.get(topic)
    if generator_class:
        return generator_class()
    raise ValueError(f"Unknown topic: {topic}")

def get_all_topics():
    """Get list of all available topics."""
    return list(GENERATORS.keys())
