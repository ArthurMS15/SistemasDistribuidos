const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const { printCard, printPlayers, printDraftedNumbers } = require('./print');
const { input } = require('./input');

const PROTO_PATH = './bingo.proto';
const options = {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
};
const packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const BingoService = grpc.loadPackageDefinition(packageDefinition).Bingo;

const bingoClient = new BingoService(
  'localhost:50051',
  grpc.credentials.createInsecure()
);

const state = {
  status: 0,
  username: '',
  token: '',
  card: [],
  numbers: [],
  playersLoggedIn: [],
  playersReady: [],
}

const updateScreen = () => {
  const { playersLoggedIn, playersReady, status, card, username, token } = state;

  console.clear();

  if (status === 0) {
    printPlayers(playersLoggedIn, playersReady);
    input('Are you ready? (y/n) ').then((answer) => {
      if (answer.toLowerCase() === 'y') {
        state.status = 1;
        bingoClient.ready({ username, token }, (err, response) => {
          if (err) throw new Error(err);
          if (response.status === 0) {
            state.status = 2;
            state.card = response.card;
          }
        });
      }
    });
  } else if (status === 1) {
    printPlayers(playersLoggedIn, playersReady);
    console.log('Waiting for other players to get ready...');
  } else if (status === 2) {
    const playCall = bingoClient.play({ username, token })
    playCall.on('data', (data) => {
      if (data.status === 0) {
        state.status = 3;
        state.numbers.push(data.number);
      } else if (data.status === 1) {
        console.log(data.message);
        process.exit();
      } else if (data.status === 2) {
        console.log('Game finished!');
        console.log(`Winner: ${data.winner}`);
        process.exit();
      }
    });
  } else if (status === 3) {
    console.log('Game started!');
    printCard(card);
    printDraftedNumbers(state.numbers);

    input('Claim win (y/n) ').then((answer) => {
      if (answer.toLowerCase() === 'y') {
        bingoClient.checkWin({ username, token }, (err, response) => {
          if (err) throw new Error(err);
          if (response.status === 0) {
            console.log('Game finished! You won!');
            process.exit();
          }
        });
      }
    });
  }
};

const main = async () => {
  state.username = await input('Username: ');

  const loginCall = bingoClient.login({ username: state.username });
  loginCall.on('data', (data) => {
    if (data.status === 0) {
      state.token = data.token;
      state.playersLoggedIn = data.playersLoggedIn;
      state.playersReady = data.playersReady;
    } else {
      console.log(data.message);
      process.exit();
    }
  });

  setInterval(() => {
    updateScreen();
  }, 100);
}

main();