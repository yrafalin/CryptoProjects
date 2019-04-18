pragma solidity ^0.5.0;

contract GenerateRPS {

    event RoundResult(string WinLose, string RandResult, uint id);

    string[] RPS = ['rock', 'paper', 'scissors'];

    mapping (string => uint) revRPS;

    constructor() public {
        revRPS.rock = 1;
        revRPS.paper = 2;
        revRPS.scissors = 3;
    }

    struct RPSResult {
        string WinLose;
        string RandResult;
        address Challenger;
    }

    RPSResult[] public prevResults;

    function _doRPS(string memory _human) private {
        uint rand = uint(keccak256(abi.encodePacked(blockhash, now)));
        string memory WL = _generateWinner(rand);
        string memory compRes = RPS(rand);
        uint id = prevResults.push(RPSResult(WL, compRes, msg.sender)) - 1;
        emit RoundResult(WL, compRes, id);
    }

    function _generateWinner(uint _dna) private returns (uint) {
        uint adjRand = (_dna % 55) + _getAdjuster();
        if (adjRand >= 40) {
           return 'Win';
        } else if (adjRand >= 20) {
            return 'Tie';
        } else {
            return 'Lose';
        }
    }

    function _getAdjuster() private view returns (uint) {
      uint value = 0;
      if (msg.value >= 1000000000000000) {
        uint value = (_log(msg.value) - 14) * 15;
      }
      return value;
    }

    function _log(uint exponent) private pure returns (uint) {
      // https://ethereum.stackexchange.com/questions/8086/logarithm-math-operation-in-solidity
      uint x = exponent;
      uint LOG = 0;
      while (x >= 1500000) {
        uint LOG = LOG + 405465;
        uint x = x * 2 / 3;
      }
      uint x = x - 1000000;
      uint y = x;
      uint i = 1;
      while (i < 10) {
        uint LOG = LOG + (y / i);
        uint i = i + 1;
        uint y = y * x / 1000000;
        uint LOG = LOG - (y / i);
        uint i = i + 1;
        uint y = y * x / 1000000;
      }
      return LOG;
    }

    function FightRPS(string memory _human) public {
        _doRPS(_human);
    }

}
