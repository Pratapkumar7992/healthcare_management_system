// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatientData {
    struct Patient {
        string name;
        bytes32 email; // Change to bytes32 for gas efficiency
        string disease;
    }

    mapping(address => Patient) public patients;

    event PatientRegistered(address indexed patientAddress, string name, bytes32 email, string disease);

    function registerPatient(string memory _name, string memory _email, string memory _disease) public payable {
        require(msg.value == 0.00001 ether, "Transaction must include 0.00001 ETH");

        bytes32 emailHash = keccak256(abi.encodePacked(_email)); // Use a hash for email

        patients[msg.sender] = Patient({
            name: _name,
            email: emailHash,
            disease: _disease
        });

        emit PatientRegistered(msg.sender, _name, emailHash, _disease);
    }

    function getPatient(address _patient) public view returns (string memory name, string memory email, string memory disease) {
        Patient memory p = patients[_patient];
        return (p.name, string(abi.encodePacked(p.email)), p.disease);
    }
}
