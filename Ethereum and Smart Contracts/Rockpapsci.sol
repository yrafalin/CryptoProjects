pragma solidity ^0.5.0;

contract GenerateRPS {

    event RoundResult(string WinLose, string RandResult, uint id);

    string[] RPS = ['rock', 'paper', 'scissors'];

    mapping (string => uint) private revRPS;

    constructor() public {
        revRPS['rock'] = 1;
        revRPS['paper'] = 2;
        revRPS['scissors'] = 3;
    }

    struct RPSResult {
        string WinLose;
        string RandResult;
        address Challenger;
    }

    RPSResult[] public prevResults;

    function _doRPS(string memory _human, uint _dna) private {
        string memory WL = _findWinner(_human, _dna);
        string memory compRes = RPS(_dna);
        uint id = prevResults.push(RPSResult(WL, compRes, msg.sender)) - 1;
        emit RoundResult(WL, compRes, id);
    }

    function _generateRandomComp() private returns (uint) {
        uint rand = uint(keccak256(abi.encodePacked(blockhash, now)));
        return rand % 3;
    }

    function _findWinner(string memory _human, uint _comp) private view returns (string memory) {
        uint humanNum = revRPS(_human);
        if (humanNum == _comp + 1) {
           return 'Tie';
        } else if (humanNum == _comp + 2 || humanNum == (_comp + 2) % 3) {
            return 'Win';
        } else {
            return 'Lose';
        }
    }

    function FightRPS(string memory _human) public {
        uint randDna = _generateRandomComp();
        revRPS.rock = 1;
        revRPS.paper = 2;
        revRPS.scissors = 3;
        _doRPS(_human, randDna);
    }

}
