// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EnergyTrading {
    struct Trade {
        address seller;
        address buyer;
        uint256 amount; // in kWh
        uint256 price; // in wei per kWh
        uint256 timestamp;
        bool executed;
    }

    mapping(uint256 => Trade) public trades;
    uint256 public tradeCount;

    event TradeProposed(uint256 tradeId, address seller, address buyer, uint256 amount, uint256 price);
    event TradeExecuted(uint256 tradeId);

    function proposeTrade(address _buyer, uint256 _amount, uint256 _price) public {
        tradeCount++;
        trades[tradeCount] = Trade(msg.sender, _buyer, _amount, _price, block.timestamp, false);
        emit TradeProposed(tradeCount, msg.sender, _buyer, _amount, _price);
    }

    function executeTrade(uint256 _tradeId) public payable {
        Trade storage trade = trades[_tradeId];
        require(!trade.executed, "Trade already executed");
        require(msg.sender == trade.buyer, "Only buyer can execute");
        require(msg.value == trade.amount * trade.price, "Incorrect payment amount");

        trade.executed = true;
        payable(trade.seller).transfer(msg.value);
        emit TradeExecuted(_tradeId);
    }

    function getTrade(uint256 _tradeId) public view returns (address, address, uint256, uint256, uint256, bool) {
        Trade memory trade = trades[_tradeId];
        return (trade.seller, trade.buyer, trade.amount, trade.price, trade.timestamp, trade.executed);
    }
}
