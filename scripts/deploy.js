async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contracts with the account:", deployer.address);
  
    const PatientData = await ethers.getContractFactory("PatientData");
    const patientData = await PatientData.deploy();
    await patientData.deployed();
  
    console.log("PatientData contract deployed to:", patientData.address);
  }
  
  main().catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
  