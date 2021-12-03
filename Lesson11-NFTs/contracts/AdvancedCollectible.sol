// SPDX-License-Identifier: MIT

//The tokenURI can be 3 different images, randomly selected

pragma solidity ^0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    enum Type {
        SHIBA_INU,
        CHARLES1,
        CHARLES2
    }

    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;
    mapping(uint256 => Type) tokenIdToType;
    mapping(bytes32 => address) requestIdToAddress;

    event requestedCollectable(bytes32 indexed requestId, address requester);
    event typeAssigned(uint256 indexed tokenId, Type nftType);

    constructor(
        string memory _nftName,
        string memory _nftSymbol,
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721(_nftName, _nftSymbol)
    {
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible() public returns (bytes32) {
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToAddress[requestId] = msg.sender; //save the address of the @requester
        emit requestedCollectable(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Type nftType = Type(randomNumber % 3); //3 diferent types
        tokenIdToType[tokenCounter] = nftType;

        emit typeAssigned(tokenCounter, nftType);

        address owner = requestIdToAddress[requestId];
        _safeMint(owner, tokenCounter);
        //_setTokenURI(tokenCounter, tokenURI);
        tokenCounter += 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        //Manually setting the URI
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "ERC721: caller is not owner no approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }
}
