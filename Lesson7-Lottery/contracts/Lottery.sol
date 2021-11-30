// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract Lottery is Ownable, VRFConsumerBase {
    address payable[] public players;
    address payable public winner;
    uint256 public randomness;
    uint256 public usdEntryFee;
    AggregatorV3Interface internal ethUsdPriceFeed;
    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    } // 0,1,2
    LOTTERY_STATE public lottery_state;
    uint256 public fee;
    bytes32 public keyhash;
    event RequestedRandomness(bytes32 requestId);

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash
    ) public VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * (10**18); //50 usd in wei
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        fee = _fee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        //50$ minimum entrance fee
        require(msg.value >= getEntranceFee(), "Not enough ETH");
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (
            uint80 roundID,
            int256 price,
            uint256 startedAt,
            uint256 timeStamp,
            uint80 answeredInRound
        ) = ethUsdPriceFeed.latestRoundData();

        //Solidity does not work with decimals, so we need to work with big numbers
        uint256 adjustedPrice = uint256(price) * 10**10; //18 decimals

        // 50 / 4000
        return ((usdEntryFee * 10**18) / adjustedPrice);
    }

    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSED);
        lottery_state = LOTTERY_STATE.OPEN;
    }

    function endLottery() public onlyOwner {
        //uint256(
        //    keccak256(
        //        abi.encodePacked(
        //            nonce,
        //            msg.sender,
        //            block.difficulty,
        //            block.timestamp
        //        )
        //    )
        //) % players.length;

        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        bytes32 requestId = requestRandomness(keyhash, fee); //When recieved a RequestId, the function fulfillRandomness is called
        emit RequestedRandomness(requestId);
    }

    function fulfillRandomness(bytes32 _requestId, uint256 _randomness)
        internal
        override
    {
        require(lottery_state == LOTTERY_STATE.CALCULATING_WINNER);
        require(_randomness > 0);
        randomness = _randomness;
        winner = players[_randomness % players.length];
        winner.transfer(address(this).balance);
        //Reset Lootery state
        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}
