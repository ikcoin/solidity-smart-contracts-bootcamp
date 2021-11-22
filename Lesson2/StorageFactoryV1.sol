// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "./SimpleStorage.sol";

//Factory Pattern
contract StorageFactory {
    SimpleStorage[] public simpleStorageArray;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }

    function sFStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber)
        public
    {
        SimpleStorage(address(simpleStorageArray[_simpleStorageIndex])).store(
            _simpleStorageNumber
        );
    }

    function sFGet(uint256 _simpleStorageIndex) public view returns (uint256) {
        return (
            SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]))
                .retrieve()
        );
    }
}
