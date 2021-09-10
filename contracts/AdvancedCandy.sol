pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCandy is
    AccessControl,
    ERC721,
    VRFConsumerBase
{
    uint256 public tokenCounter;

    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    // mapping(uint256 => Element) public tokenIdToElement;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId);

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    bytes32 internal keyHash;
    uint256 internal fee;

    constructor(
        address _VRFCoordinator,
        address _LinkToken,
        bytes32 _keyhash
    )
        public
        VRFConsumerBase(_VRFCoordinator, _LinkToken)
        ERC721("Atomic Candy", "AC")
    {
        tokenCounter = 0;
        keyHash = _keyhash;
        fee = 0.1 * 10**18;

        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _setupRole(MINTER_ROLE, _msgSender());
    }

    function createCandy(string memory tokenURI)
        public
        returns (bytes32)
    {
        require(hasRole(MINTER_ROLE, _msgSender()), "ERC721PresetMinterPauserAutoId: must have minter role to mint");
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;
        emit requestedCollectible(requestId);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        address CandyOwner = requestIdToSender[requestId];
        string memory tokenURI = requestIdToTokenURI[requestId];
        uint256 newItemId = tokenCounter;
        _safeMint(CandyOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(hasRole(MINTER_ROLE, _msgSender()), "ERC721PresetMinterPauserAutoId: must have minter role to mint");
        _setTokenURI(tokenId, _tokenURI);
    }

    function setMinterRole(address account) public {
        require(hasRole(DEFAULT_ADMIN_ROLE, _msgSender()), "ERC721PresetMinterPauserAutoId: must have admin role to mint");
        _setupRole(MINTER_ROLE, account);
    }
}
