import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-ethers";

const config: HardhatUserConfig = {
  solidity: "0.8.19",
  networks: {
    ganache: {
      type: "http",
      url: "http://127.0.0.1:7545", // Ganache RPC URL
      accounts: [
        "0xe0ee824c1f8844fff7aafdbe1d2d0753fcad18dc3bd1aa29ff7df5cac3f173b4"
      ],
    },
  },
};

export default config;



