const net = require("net");
const fs = require("fs");
const process = require("process");

/*Importa o módulo net, necessário para criar um cliente de rede e se comunicar com o servidor.
Importa o módulo fs, usado para criar e manipular arquivos no sistema de arquivos local.
Importa o módulo process, usado para acessar argumentos da linha de comando e sair do programa.*/

if (process.argv.length !== 5) {
  console.log("Uso: node client.js <ip_servidor> <porta> <nome_arquivo>");  //quantidade correta de argumentos foi fornecia
  process.exit(1);
}

const serverIP = process.argv[2]; //armazena o segundo argumento
const serverPort = process.argv[3];
const fileName = process.argv[4];

const client = new net.Socket();  //cria um novo objeto de socket para o cliente.
client.connect(serverPort, serverIP, () => {
  console.log("Conectado ao servidor");
  client.write(fileName);
}); //conecta-se ao servidor no IP e porta especificados e define uma função de callback a ser chamada quando a conexão for estabelecida.

client.on("data", (data) => { //define uma função de callback para lidar com os dados recebidos do servidor.
  const response = data.toString(); //converte os dados recebidos em uma string.
  if (response.startsWith("EXIST")) {
    const fileSize = parseInt(response.split(" ")[1]);
    console.log(`Arquivo encontrado. Tamanho: ${fileSize}`);
    client.write("OK");

    const fileStream = fs.createWriteStream(fileName); //cria um novo arquivo usando o nome fornecido e cria um fluxo de gravação para o arquivo.
    let receivedBytes = 0;
    client.on("data", (chunk) => {
      receivedBytes += chunk.length;
      const progress = (receivedBytes / fileSize) * 100;
      console.log(`Recebendo arquivo... ${progress.toFixed(2)}%`); //Calcule e exibe o progresso da transferência do arquivo. 
      fileStream.write(chunk);

      if (receivedBytes === fileSize) {
        console.log("Arquivo recebido com sucesso.");
        client.destroy();
      }
    }); // Define uma função de callback para lidar com os dados recebidos (chunks) do servidor.
  } else {
    console.log("Arquivo não encontrado.");
    client.destroy();
  }
});

client.on("close", () => {
  console.log("Conexão encerrada.");
});
