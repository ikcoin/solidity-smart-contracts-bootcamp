# Lessson12-Proxy

## Proxy Terminology

##### 1. The implementation contract
    - Which has all the code of our protocol. To upgrade the contract, a brand new implementation contract is deployed (v1 -> v2). 
##### 2. The proxy contract
    - Which point to which implementation is the "correct" one, and routes everyone's function calls to that contract. The proxy contract stores all the data.
##### 3. The user
    - Make calls to the proxy. 
##### 4. The admin
    - The user or group of users/voters who upgrade to new implementation contracts.


## Different Proxy Implementations

### 1. Transparent Proxy Pattern
    - Admins can't call implementation contract functions
    - Admin functions are functions that govern the upgrades
    - Users still powerless on admin functions

### 2. Universal Upgradeable Proxies
    Puts all the logic of upgrading in the implementation itself
    - AdminOnly Upgrade functions are in the implementation contracts instead of the proxy

### 3. Diamond pattern
    It allows multiple implementation contracts
    - If the contract is so big that does not fit into the contract maximum size, you can have multiple contracts through this multi-implementation.
    - Allows having more granular upgrades to not upgrade and deploy the entire smart contract but upgrade little pieces of the contract if it is chunked out. 