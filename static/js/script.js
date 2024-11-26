const web3 = new Web3(window.ethereum);
const contractAddress = "0xb36601688Bd76e938a40483f71D29C79e4533951";
const contractABI = [ /* ABI from the compiled contract */ ];
const contract = new web3.eth.Contract(contractABI, contractAddress);

async function registerPatient(name, email, disease) {
    const accounts = await ethereum.request({ method: 'eth_requestAccounts' });
    const transaction = await contract.methods
        .registerPatient(name, email, disease)
        .send({ from: accounts[0], value: web3.utils.toWei('0.0001', 'ether') });

    console.log('Transaction successful', transaction);
}
