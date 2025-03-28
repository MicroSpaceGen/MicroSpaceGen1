"""
Space Experiment Module
Handles the core functionality for space-based microbial experiments.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class ExperimentParameters:
    """Parameters for space experiments"""
    experiment_id: str
    microorganism_type: str
    duration: int  # in days
    temperature: float
    radiation_level: float
    gravity_level: float
    start_date: datetime
    end_date: Optional[datetime] = None

class SpaceExperiment:
    """Main class for managing space experiments"""
    
    def __init__(self, parameters: ExperimentParameters):
        self.parameters = parameters
        self.status = "initialized"
        self.data = {}
        self.observations = []
    
    def start_experiment(self) -> bool:
        """Start the space experiment"""
        try:
            self.status = "running"
            self.parameters.start_date = datetime.now()
            return True
        except Exception as e:
            self.status = "failed"
            raise Exception(f"Failed to start experiment: {str(e)}")
    
    def record_observation(self, observation: Dict) -> None:
        """Record an observation during the experiment"""
        self.observations.append({
            "timestamp": datetime.now(),
            "data": observation
        })
    
    def end_experiment(self) -> bool:
        """End the space experiment"""
        try:
            self.status = "completed"
            self.parameters.end_date = datetime.now()
            return True
        except Exception as e:
            self.status = "failed"
            raise Exception(f"Failed to end experiment: {str(e)}")
    
    def get_experiment_summary(self) -> Dict:
        """Get a summary of the experiment"""
        return {
            "experiment_id": self.parameters.experiment_id,
            "status": self.status,
            "duration": (self.parameters.end_date - self.parameters.start_date).days if self.parameters.end_date else None,
            "observations_count": len(self.observations)
        } 