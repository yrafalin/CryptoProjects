const RPS = artifacts.require('Rockpapsci')

contract('Rockpapsci', (accounts) => {
    //const [bob, alice] = accounts
    //it("test 1", async () => {
    const ssContract = await RPS.deployed()
        //const bobNum = await ssContract.balences.call(bob)
    ssContract.FightRPS('rock')
    var resultRet = ssContract.RoundResult()
    //resultRet.watch(function(err, result) {})
    // Alternately, to get the events all at once.
    voteCast.get((wl, winRes, id) => {
      console.log("The result is a", wl)
      console.log("The computer got a", winRes)
      console.log("The result on the contract is", ssContract.prevResults.call(id))
    })//function(err, result) /* some other callback* /)
        /*assert.equal(bobNum, 0, 'wrong')
        const aliceNum = await ssContract.balences.call(alice)
        assert.equal(aliceNum, 0, 'wrong')*/
    })

    /*it("test 2", async () => {
        const ssContract = await Betting.deployed()
        ssContract.deposit(2, { from: bob })
        ssContract.deposit(1, { from: alice })
        ssContract.createBet(2, 1, 33, { from: bob })
        ssContract.accept(0, {from: alice})
        let bobNum = await ssContract.balences.call(bob)
        console.log(bobNum)
        let aliceNum = await ssContract.balences.call(alice)
        console.log(aliceNum)
        assert.equal(parseInt(aliceNum) + parseInt(bobNum), 3, 'wrong')
    })*/
})
