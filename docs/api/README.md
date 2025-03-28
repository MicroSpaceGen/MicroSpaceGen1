# MicroSpaceGen API Documentation

## Overview
This document provides detailed API documentation for the MicroSpaceGen project.

## Core Modules

### Space Experiment Module
Located in `src/experiments/space_experiment.py`

#### Classes

##### ExperimentParameters
```python
@dataclass
class ExperimentParameters:
    experiment_id: str
    microorganism_type: str
    duration: int
    temperature: float
    radiation_level: float
    gravity_level: float
    start_date: datetime
    end_date: Optional[datetime] = None
```

##### SpaceExperiment
```python
class SpaceExperiment:
    def __init__(self, parameters: ExperimentParameters)
    def start_experiment(self) -> bool
    def record_observation(self, observation: Dict) -> None
    def end_experiment(self) -> bool
    def get_experiment_summary(self) -> Dict
```

### Gene Analysis Module
Located in `src/analysis/gene_analyzer.py`

#### Classes

##### GeneSequence
```python
@dataclass
class GeneSequence:
    sequence_id: str
    sequence: str
    organism: str
    metadata: Dict
```

##### GeneAnalyzer
```python
class GeneAnalyzer:
    def __init__(self)
    def add_sequence(self, sequence: GeneSequence) -> None
    def analyze_mutations(self, sequence_id: str) -> Dict
    def compare_sequences(self, sequence_id1: str, sequence_id2: str) -> Dict
    def generate_report(self, sequence_id: str) -> Dict
```

### Blockchain Storage Module
Located in `src/blockchain/data_storage.py`

#### Classes

##### DataBlock
```python
@dataclass
class DataBlock:
    block_id: str
    timestamp: datetime
    data: Dict
    previous_hash: Optional[str]
    hash: str
```

##### BlockchainStorage
```python
class BlockchainStorage:
    def __init__(self)
    def add_data(self, data: Dict) -> str
    def create_block(self, data: Dict) -> DataBlock
    def get_block(self, block_id: str) -> Optional[DataBlock]
    def verify_chain(self) -> bool
    def get_chain_summary(self) -> Dict
```

### Utility Functions
Located in `src/utils/helpers.py`

```python
def setup_logging(log_level: str = "INFO") -> None
def load_config(config_path: str) -> Dict[str, Any]
def save_data(data: Dict[str, Any], filepath: str) -> bool
def load_data(filepath: str) -> Optional[Dict[str, Any]]
def generate_timestamp() -> str
def validate_data(data: Dict[str, Any], required_fields: list) -> bool
```

## Usage Examples

### Starting an Experiment
```python
from datetime import datetime
from src.experiments.space_experiment import SpaceExperiment, ExperimentParameters

params = ExperimentParameters(
    experiment_id="exp_001",
    microorganism_type="E. coli",
    duration=30,
    temperature=25.0,
    radiation_level=0.5,
    gravity_level=0.0,
    start_date=datetime.now()
)

experiment = SpaceExperiment(params)
experiment.start_experiment()
```

### Analyzing Gene Sequences
```python
from src.analysis.gene_analyzer import GeneAnalyzer, GeneSequence

analyzer = GeneAnalyzer()
sequence = GeneSequence(
    sequence_id="seq_001",
    sequence="ATCGATCGATCG",
    organism="E. coli",
    metadata={"source": "control"}
)
analyzer.add_sequence(sequence)
```

### Storing Data on Blockchain
```python
from src.blockchain.data_storage import BlockchainStorage

blockchain = BlockchainStorage()
blockchain.add_data({"key": "value"})
``` 