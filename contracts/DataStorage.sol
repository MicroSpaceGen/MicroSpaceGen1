// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DataStorage {
    struct Block {
        string blockId;
        string timestamp;
        string data;
        string previousHash;
        string hash;
        uint256 nonce;
    }
    
    mapping(string => bytes) private blocks;
    string[] private blockIds;
    
    event DataStored(string blockId, string timestamp);
    
    function storeData(string memory blockId, bytes memory data) public {
        require(bytes(blockId).length > 0, "Block ID cannot be empty");
        require(data.length > 0, "Data cannot be empty");
        
        blocks[blockId] = data;
        blockIds.push(blockId);
        
        emit DataStored(blockId, block.timestamp);
    }
    
    function getData(string memory blockId) public view returns (bytes memory) {
        require(bytes(blockId).length > 0, "Block ID cannot be empty");
        return blocks[blockId];
    }
    
    function getBlockCount() public view returns (uint256) {
        return blockIds.length;
    }
    
    function getBlockId(uint256 index) public view returns (string memory) {
        require(index < blockIds.length, "Index out of bounds");
        return blockIds[index];
    }
    
    function getLatestBlockId() public view returns (string memory) {
        require(blockIds.length > 0, "No blocks stored");
        return blockIds[blockIds.length - 1];
    }
} 