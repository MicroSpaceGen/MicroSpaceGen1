"""
Example demonstrating basic experiment functionality
"""

from datetime import datetime
from src.experiments.space_experiment import SpaceExperiment, ExperimentParameters
from src.analysis.gene_analyzer import GeneAnalyzer, GeneSequence
from src.blockchain.data_storage import BlockchainStorage

def run_basic_experiment():
    """Run a basic space experiment example"""
    
    # Initialize components
    blockchain = BlockchainStorage()
    gene_analyzer = GeneAnalyzer()
    
    # Create experiment parameters
    params = ExperimentParameters(
        experiment_id="example_001",
        microorganism_type="E. coli",
        duration=30,
        temperature=25.0,
        radiation_level=0.5,
        gravity_level=0.0,
        start_date=datetime.now()
    )
    
    # Create and start experiment
    experiment = SpaceExperiment(params)
    print(f"Starting experiment: {experiment.parameters.experiment_id}")
    experiment.start_experiment()
    
    # Record some observations
    observations = [
        {
            "temperature": 25.0,
            "growth_rate": 0.5,
            "cell_count": 1000
        },
        {
            "temperature": 25.5,
            "growth_rate": 0.6,
            "cell_count": 1500
        }
    ]
    
    for obs in observations:
        experiment.record_observation(obs)
        print(f"Recorded observation: {obs}")
    
    # Add some gene sequences
    sequences = [
        GeneSequence(
            sequence_id="seq_001",
            sequence="ATCGATCGATCG",
            organism="E. coli",
            metadata={"source": "control"}
        ),
        GeneSequence(
            sequence_id="seq_002",
            sequence="ATCGATCGATCC",
            organism="E. coli",
            metadata={"source": "experiment"}
        )
    ]
    
    for seq in sequences:
        gene_analyzer.add_sequence(seq)
        print(f"Added sequence: {seq.sequence_id}")
    
    # Compare sequences
    comparison = gene_analyzer.compare_sequences("seq_001", "seq_002")
    print(f"Sequence comparison: {comparison}")
    
    # Store experiment data on blockchain
    blockchain.add_data(experiment.get_experiment_summary())
    print("Stored experiment data on blockchain")
    
    # End experiment
    experiment.end_experiment()
    print(f"Experiment completed. Summary: {experiment.get_experiment_summary()}")

if __name__ == "__main__":
    run_basic_experiment() 