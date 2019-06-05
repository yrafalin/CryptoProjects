# Crypto
Programs from my 9th Grade Crypto elective

Cryptographic Primitives:<br />
* hash_str.txt: string to be hashed by the md5<br />
* jsonMaker.py: makes fake transaction jsons<br />
* transactions.json: input to merkle tree<br />
* MakeMerkleTree.py: merkle tree making program<br />
* RecursiveMerkleTree.py: same as above, but with a recursive function<br />
* MakeMD5.py: initial version<br />
* SeMD5.py: second version<br />
* FrMD5.py: last version, but still doesn't work<br />
* OnlineMD5.py: online md5 example in python<br />

Mining and Wallets:<br />
* miner.py: creates blockchain and mines for new blocks<br />
* GenerateAddr.py: generates address for new public key or an inputted one (Update: and a ton of extra features)<br />
* jsonMaker.py: refactored for use as library<br />
* MakeMerkleTree.py: refactored for use as library<br />

Ethereum and Smart Contracts:<br />
* Rockpapsci.sol: original rock paper scissors, takes your choice, and emits result
* Weightedrps.sol: weighted so that higher transfers have higher chances of winning
* contract.js: js file which runs Rockpapsci.sol in truffle

Full Blockchain:
* MakeMerkleTree.py: updated merkle maker
* blockchain.py: full blockchain program, with a flask app inside

Final Project (Smart Contract Implementation):
* RunSmartContract.py: profiles and runs smart contract while accounting for gas allowance
