pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

contract AdvancedCandy is AccessControl, ERC721 {
    uint256 public tokenCounter;

    // add other things
    mapping(bytes32 => address) public requestIdToSender;
    mapping(bytes32 => string) public requestIdToTokenURI;
    // mapping(uint256 => Element) public tokenIdToElement;
    mapping(bytes32 => uint256) public requestIdToTokenId;
    event requestedCollectible(bytes32 indexed requestId);

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");

    constructor() public ERC721("Atomic Candy", "AC") {
        tokenCounter = 0;

        _setupRole(DEFAULT_ADMIN_ROLE, _msgSender());
        _setupRole(MINTER_ROLE, _msgSender());
    }

    function createCandy(string memory tokenURI) public returns (bytes32) {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "ERC721PresetMinterPauserAutoId: must have minter role to mint"
        );
        bytes32 requestId = bytes32(
            keccak256(abi.encodePacked(
                msg.sender,
                now,
                tokenCounter)
            )
        );

        requestIdToSender[requestId] = msg.sender;
        requestIdToTokenURI[requestId] = tokenURI;

        uint256 newItemId = tokenCounter;
        requestIdToTokenId[requestId] = newItemId;
        tokenCounter = tokenCounter + 1;


        address CandyOwner = requestIdToSender[requestId];
        _safeMint(CandyOwner, newItemId);
        _setTokenURI(newItemId, tokenURI);

        emit requestedCollectible(requestId);
    }

    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        require(
            hasRole(MINTER_ROLE, _msgSender()),
            "ERC721PresetMinterPauserAutoId: must have minter role to mint"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    function setMinterRole(address account) public {
        require(
            hasRole(DEFAULT_ADMIN_ROLE, _msgSender()),
            "ERC721PresetMinterPauserAutoId: must have admin role to mint"
        );
        _setupRole(MINTER_ROLE, account);
    }
}
