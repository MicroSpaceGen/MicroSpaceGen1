"""
Main entry point for MicroSpaceGen application
"""

import logging
from src.utils.helpers import setup_logging, load_config
from src.experiments.space_experiment import SpaceExperiment, ExperimentParameters
from src.analysis.gene_analyzer import GeneAnalyzer, GeneSequence
from src.blockchain.data_storage import BlockchainStorage
from datetime import datetime

def main():
    """Main application entry point"""
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Load configuration
        config = load_config("config/config.json")
        logger.info(f"Starting {config['project']['name']} v{config['project']['version']}")
        
        # Initialize components
        blockchain = BlockchainStorage()
        gene_analyzer = GeneAnalyzer()
        
        # Example: Create and start an experiment
        params = ExperimentParameters(
            experiment_id="exp_001",
            microorganism_type="E. coli",
            duration=config["experiment"]["default_duration"],
            temperature=25.0,
            radiation_level=config["experiment"]["radiation_levels"]["medium"],
            gravity_level=0.0,
            start_date=datetime.now()
        )
        
        experiment = SpaceExperiment(params)
        experiment.start_experiment()
        
        # Example: Record some observations
        observation = {
            "temperature": 25.0,
            "growth_rate": 0.5,
            "cell_count": 1000
        }
        experiment.record_observation(observation)
        
        # Example: Store experiment data on blockchain
        blockchain.add_data(experiment.get_experiment_summary())
        
        logger.info("Application started successfully")
        
    except Exception as e:
        logger.error(f"Application failed to start: {str(e)}")
        raise

if __name__ == "__main__":
    main() 