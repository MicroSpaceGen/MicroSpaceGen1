"""
Gene Analysis Module
Processes and analyzes genetic data from space experiments.
"""

import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from Bio import SeqUtils
from Bio.Seq import Seq
from Bio.SeqUtils import GC
from Bio import pairwise2
from Bio.pairwise2 import format_alignment
from datetime import datetime

@dataclass
class GeneSequence:
    """Represents a gene sequence with metadata"""
    sequence_id: str
    sequence: str
    organism: str
    metadata: Dict

class GeneAnalyzer:
    """Main class for gene sequence analysis"""
    
    def __init__(self):
        self.sequences: List[GeneSequence] = []
    
    def add_sequence(self, sequence: GeneSequence) -> None:
        """Add a new gene sequence to the analysis"""
        if not self._validate_sequence(sequence.sequence):
            raise ValueError("Invalid DNA sequence")
        self.sequences.append(sequence)
    
    def _validate_sequence(self, sequence: str) -> bool:
        """Validate if the sequence contains only valid DNA nucleotides"""
        valid_nucleotides = set('ATCG')
        return all(nucleotide in valid_nucleotides for nucleotide in sequence.upper())
    
    def analyze_mutations(self, sequence_id: str) -> Dict:
        """Analyze mutations in a specific sequence"""
        sequence = next((s for s in self.sequences if s.sequence_id == sequence_id), None)
        if not sequence:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        # Calculate basic sequence statistics
        gc_content = GC(Seq(sequence.sequence))
        sequence_length = len(sequence.sequence)
        
        # Analyze nucleotide composition
        nucleotide_counts = {
            'A': sequence.sequence.upper().count('A'),
            'T': sequence.sequence.upper().count('T'),
            'C': sequence.sequence.upper().count('C'),
            'G': sequence.sequence.upper().count('G')
        }
        
        # Calculate mutation potential based on GC content
        mutation_potential = 1 - (abs(50 - gc_content) / 50)
        
        return {
            "sequence_id": sequence_id,
            "gc_content": gc_content,
            "sequence_length": sequence_length,
            "nucleotide_composition": nucleotide_counts,
            "mutation_potential": mutation_potential,
            "mutation_positions": self._find_mutation_hotspots(sequence.sequence),
            "mutation_types": self._analyze_mutation_types(sequence.sequence)
        }
    
    def _find_mutation_hotspots(self, sequence: str) -> List[int]:
        """Find potential mutation hotspots in the sequence"""
        hotspots = []
        for i in range(len(sequence) - 2):
            # Look for repeated nucleotides or high GC content regions
            if (sequence[i] == sequence[i+1] == sequence[i+2] or
                sequence[i:i+3].upper().count('G') + sequence[i:i+3].upper().count('C') >= 2):
                hotspots.append(i)
        return hotspots
    
    def _analyze_mutation_types(self, sequence: str) -> Dict[str, int]:
        """Analyze potential mutation types in the sequence"""
        mutation_types = {
            "transitions": 0,
            "transversions": 0,
            "insertions": 0,
            "deletions": 0
        }
        
        # Count potential mutation sites
        for i in range(len(sequence) - 1):
            current = sequence[i].upper()
            next_nuc = sequence[i+1].upper()
            
            # Transitions (purine to purine or pyrimidine to pyrimidine)
            if ((current in 'AG' and next_nuc in 'AG') or
                (current in 'CT' and next_nuc in 'CT')):
                mutation_types["transitions"] += 1
            
            # Transversions (purine to pyrimidine or vice versa)
            elif ((current in 'AG' and next_nuc in 'CT') or
                  (current in 'CT' and next_nuc in 'AG')):
                mutation_types["transversions"] += 1
        
        return mutation_types
    
    def compare_sequences(self, sequence_id1: str, sequence_id2: str) -> Dict:
        """Compare two sequences for differences"""
        seq1 = next((s for s in self.sequences if s.sequence_id == sequence_id1), None)
        seq2 = next((s for s in self.sequences if s.sequence_id == sequence_id2), None)
        
        if not seq1 or not seq2:
            raise ValueError("One or both sequences not found")
        
        # Perform sequence alignment
        alignments = pairwise2.align.globalms(
            seq1.sequence,
            seq2.sequence,
            2,    # match score
            -1,   # mismatch score
            -0.5, # gap open
            -0.1  # gap extend
        )
        
        if not alignments:
            return {
                "similarity_score": 0.0,
                "differences": [],
                "alignment": ""
            }
        
        best_alignment = alignments[0]
        alignment_str = format_alignment(*best_alignment)
        
        # Calculate similarity score
        matches = sum(1 for a, b in zip(best_alignment[0], best_alignment[1]) if a == b)
        similarity_score = matches / max(len(best_alignment[0]), len(best_alignment[1]))
        
        # Find differences
        differences = []
        for i, (a, b) in enumerate(zip(best_alignment[0], best_alignment[1])):
            if a != b:
                differences.append({
                    "position": i,
                    "seq1_base": a,
                    "seq2_base": b,
                    "type": "mismatch" if a != '-' and b != '-' else "indel"
                })
        
        return {
            "similarity_score": similarity_score,
            "differences": differences,
            "alignment": alignment_str
        }
    
    def generate_report(self, sequence_id: str) -> Dict:
        """Generate a comprehensive analysis report"""
        sequence = next((s for s in self.sequences if s.sequence_id == sequence_id), None)
        if not sequence:
            raise ValueError(f"Sequence {sequence_id} not found")
        
        mutation_analysis = self.analyze_mutations(sequence_id)
        
        return {
            "sequence_id": sequence_id,
            "organism": sequence.organism,
            "sequence_length": len(sequence.sequence),
            "analysis_timestamp": datetime.now().isoformat(),
            "results": {
                "mutation_analysis": mutation_analysis,
                "statistics": {
                    "gc_content": mutation_analysis["gc_content"],
                    "sequence_complexity": self._calculate_sequence_complexity(sequence.sequence)
                }
            }
        }
    
    def _calculate_sequence_complexity(self, sequence: str) -> float:
        """Calculate sequence complexity using Shannon entropy"""
        sequence = sequence.upper()
        nucleotide_counts = {
            'A': sequence.count('A'),
            'T': sequence.count('T'),
            'C': sequence.count('C'),
            'G': sequence.count('G')
        }
        
        total = len(sequence)
        if total == 0:
            return 0.0
        
        entropy = 0.0
        for count in nucleotide_counts.values():
            if count > 0:
                probability = count / total
                entropy -= probability * np.log2(probability)
        
        return entropy 