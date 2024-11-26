/** @type import('hardhat/config').HardhatUserConfig */
// module.exports = {
//   solidity: "0.8.24",
// };
require("@nomiclabs/hardhat-waffle");

require('@nomiclabs/hardhat-ethers');

module.exports = {
  solidity: "0.8.0",
  networks: {
    localhost: {
      url: "http://127.0.0.1:8545", // This should match the port Hardhat node is running on
    },
  },
};


