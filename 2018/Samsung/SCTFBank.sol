pragma solidity ^0.4.18;

contract SCTFBank{
    event LogBalance(address addr, uint256 value);
    mapping (address => uint256) private balance;
    uint256 private donation_deposit;
    address private owner;
    bool private lockBalances;

    //constructor
    constructor() public{
        owner = msg.sender;
    }
    
    //logging balance of requested address
    function showBalance(address addr) public {

        emit LogBalance(addr, balance[addr]);
    }

    //withdraw my balance
    function withdraw(uint256 value) public{
        require(!lockBalances);
        lockBalances = true;
        require(balance[msg.sender] >= value);
        balance[msg.sender] -= value;
        require(msg.sender.call.value(value)());
        lockBalances = false;
    }
    
    //transfer my balance to other
    function transfer(address to, uint256 value) public {
        require(balance[msg.sender] >= value);
        require(!lockBalances);
        lockBalances = true;
        balance[msg.sender] -= value;
        balance[to]+=value;
        lockBalances = false;
    }

    //transfer my balance to others
    function multiTransfer(address[] to_list, uint256 value) public {
        require(balance[msg.sender] >= value*to_list.length);
        require(balance[msg.sender] >= value);
        require(to_list.length>=0);
        require(!lockBalances);
        lockBalances = true;
        balance[msg.sender] -= value*to_list.length;
        for(uint i=0; i < to_list.length; i++){
            balance[to_list[i]] += value;
        }
        lockBalances = false;
    }
    
    //donate my balance
    function donate(uint256 value) public {
        require(balance[msg.sender]  >= value);
        require(!lockBalances);
        lockBalances = true;
        balance[msg.sender] -= value;
        donation_deposit += value;
        lockBalances = false;
    }

    //Only bank owner can deliver donations to anywhere he want.
    function deliver(address to) public {
        require(tx.origin == owner);
        require(owner == msg.sender);
        require(!lockBalances);
        lockBalances = true;
        to.transfer(donation_deposit);
        donation_deposit = 0;
        lockBalances = false;
    }
    
    //balance deposit, simple fallback function
    function () payable public {
        require(!lockBalances);
        lockBalances = true;
        balance[msg.sender]+=msg.value;
        lockBalances = false;
    }
}
//END

'''
function multiTransfer(address[] to_list, uint256 value) public {
        require(balance[msg.sender] >= value*to_list.length);
        require(balance[msg.sender] >= value);

overflow 가능

https://consensys.github.io/smart-contract-best-practices/known_attacks/


GREAT! Time to open bank!
... Bank Robbers are coming!
WOW! Your SCTFBank is safe!
Flag: SCTF{sorry_this_transaction_was_sent_by_my_cat}
'''