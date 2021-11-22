// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";

contract FundMe {
    mapping(address => uint256) public addressToAmountFunded;
    address contractOwner;

    constructor() public {
        contractOwner = msg.sender;
    }

    function fund() public payable {
        uint256 minimimUSD = 50 * 10**18; //50$ == 50*10^18

        require(msg.value >= minimumUSD, "Not enough ETH. ");

        addressToAmountFunded[msg.sender] += msg.value;
    }

    function getVersion() public view returns (uint256) {
        // ETH/USD AggregatorV3Interface deployed on Rinkeby Network --> /0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        return (priceFeed.version());
    }

    function getPrice() public view returns (uint256) {
        AggregatorV3Interface priceFeed = AggregatorV3Interface(
            0x8A753747A1Fa494EC906cE90E9f37563A8AF630e
        );
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return (uint256(answer) * 10000000000);
    }

    //Eth amount to usd
    function getConversionRate(uint256 _ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        return ((ethPrice * _ethAmount) / 1000000000000000000);
    }

    modifier onlyOwner() {
        require(msg.sender == contractOwner);
        _;
    }

    function withdraw() public payable onlyOwner {
        msg.sender.transfer(address(this).balance);
    }
}
