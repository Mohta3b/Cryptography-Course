# Cryptography Course Project
## Transaction in Bitcoin Testnet Network Using Python

- [Introduction](#introduction)
- [Methodology](#methodology)
- [Results](#results)
- [Conclusion](#conclusion)
- [References](#references)
- [License](#license)

## Introduction
Bitcoin is a cryptocurrency and a digital payment system invented by an unknown programmer, or a group of programmers, under the name Satoshi Nakamoto. It was released as open-source software in 2009. The system is peer-to-peer, and transactions take place between users directly, without an intermediary. These transactions are verified by network nodes and recorded in a public distributed ledger called a blockchain.

Due to the necessity of funds for transactions within the main blockchain, we opt to utilize the testnet network for conducting our transactions.. Testnet is an alternative Bitcoin blockchain, to be used for testing. Testnet coins are separate and distinct from actual bitcoins, and are never supposed to have any value.

## Methodology
The methodology for this project is as follows:
1. **Generation of Testnet Bitcoin Address:** The project initiates with the creation of a dedicated Bitcoin address tailored for the testnet network.

2. **Transaction Crafting with 'python-bitcoinlib' and Testnet Faucet:**
   * Step 1: Single-Input, Dual-Output Transaction Creation: A transaction is meticulously constructed, featuring a single input and two outputs. One output is designated for the intended recipient, while the other is designated for change, facilitated by the P2PKH script.
   * Step 2: Multisig Script Transaction with Three Addresses: The methodology extends to encompass the creation of three distinct addresses. This phase entails executing a transaction using a Multisig script, which mandates the consent of two out of three signatures.
   * Step 3: Complex Transaction Scenario: Building upon the prior steps, we delve into a more intricate transaction setup. Here, a single input and two outputs are employed. Notably, one of the outputs remains non-spendable, while the other is designed to be spendable by all.

3. **Mining a Block on the Testnet Network:** The project culminates with the critical task of mining a block on the testnet network. This is executed by duplicating the n+1 th block from the primary blockchain and appending it to the testnet blockchain, leveraging n as the input parameter.

## Results
Please refer to the "Report.pdf" document located in the "Docs" folder for detailed results and findings.

## Conclusion
The project was successfully executed, with the results being in line with the anticipated outcomes. The project was able to successfully generate a Bitcoin address for the testnet network, and execute a transaction with a single input and two outputs. The project was also able to execute a transaction with a multisig script, and a complex transaction scenario. Finally, the project was able to successfully mine a block on the testnet network.

## References
1. [Bitcoin Testnet](https://en.bitcoin.it/wiki/Testnet)
2. [Bitcoin Testnet Faucet](https://coinfaucet.eu/en/btc-testnet)
3. [Bitcoin Testnet Block Explorer](https://blockstream.info/testnet)
4. [Bitcoin Testnet Block Explorer](https://live.blockcypher.com/btc-testnet)

## License
```
MIT License
```
