"""
Test cases for space experiment module
"""

import pytest
from datetime import datetime
from src.experiments.space_experiment import SpaceExperiment, ExperimentParameters

def test_experiment_initialization():
    """Test experiment initialization"""
    params = ExperimentParameters(
        experiment_id="test_001",
        microorganism_type="E. coli",
        duration=30,
        temperature=25.0,
        radiation_level=0.5,
        gravity_level=0.0,
        start_date=datetime.now()
    )
    
    experiment = SpaceExperiment(params)
    assert experiment.status == "initialized"
    assert experiment.parameters.experiment_id == "test_001"

def test_experiment_start():
    """Test experiment start"""
    params = ExperimentParameters(
        experiment_id="test_002",
        microorganism_type="S. cerevisiae",
        duration=15,
        temperature=30.0,
        radiation_level=0.3,
        gravity_level=0.0,
        start_date=datetime.now()
    )
    
    experiment = SpaceExperiment(params)
    assert experiment.start_experiment() is True
    assert experiment.status == "running"

def test_experiment_observation():
    """Test recording observations"""
    params = ExperimentParameters(
        experiment_id="test_003",
        microorganism_type="B. subtilis",
        duration=20,
        temperature=28.0,
        radiation_level=0.4,
        gravity_level=0.0,
        start_date=datetime.now()
    )
    
    experiment = SpaceExperiment(params)
    observation = {
        "temperature": 28.0,
        "growth_rate": 0.5,
        "cell_count": 1000
    }
    
    experiment.record_observation(observation)
    assert len(experiment.observations) == 1
    assert experiment.observations[0]["data"] == observation

def test_experiment_end():
    """Test experiment end"""
    params = ExperimentParameters(
        experiment_id="test_004",
        microorganism_type="P. aeruginosa",
        duration=25,
        temperature=32.0,
        radiation_level=0.6,
        gravity_level=0.0,
        start_date=datetime.now()
    )
    
    experiment = SpaceExperiment(params)
    assert experiment.end_experiment() is True
    assert experiment.status == "completed"
    assert experiment.parameters.end_date is not None 