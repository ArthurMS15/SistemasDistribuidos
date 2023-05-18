const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');

const PROTO_PATH = './bingo.proto';
const host = '127.0.0.1:50051';

// Config
const minPlayers = 1;
const draftNumberInterval = 2000;

// Server State
let players = [];
let draftedNumbers = [];
let gameStarted = false;
let winner = '';
let draftNumberIntervalId;
let playerCount = 0;

// Utility Functions
const generateToken = () => (Math.random() + 1).toString(36).substring(2, 18);
const runAtInterval = (callback, interval) => {
  callback();
  return setInterval(callback, interval);
};

// Game Functions
const generateCard = () => {
  const card = Array.from({length: 24}, () => Math.floor(Math.random() * 100));
  return [...new Set(card)];
};

const checkBingo = (card, draftedNumbers) => {
  let card2D = [
    card.slice(0, 5),
    card.slice(5, 10),
    [...card.slice(10, 12), -1, ...card.slice(12, 14)],
    card.slice(14, 19),
    card.slice(19, 24)
  ];

  for (let i = 0; i < 5; i++) {
    if (
      card2D[i].every(num => num === -1 || draftedNumbers.includes(num)) ||
      card2D.map(row => row[i]).every(num => num === -1 || draftedNumbers.includes(num))
    ) {
      return true;
    }
  }

  if (
    [0, 1, 2, 3, 4].every(i => card2D[i][i] === -1 || draftedNumbers.includes(card2D[i][i])) ||
    [0, 1, 2, 3, 4].every(i => card2D[i][4 - i] === -1 || draftedNumbers.includes(card2D[i][4 - i]))
  ) {
    return true;
  }

  return false;
};
/*FIM CARD*/

const waitForReadyPlayers = () => {
  return new Promise((resolve) => {
    const checkInterval = setInterval(() => {
      const readyPlayers = players.filter((p) => p.ready);
      if (readyPlayers.length >= Math.max(minPlayers, players.length)) {
        clearInterval(checkInterval);
        resolve();
      }
    }, 1000);
  });
};

const draftNumber = () => {
  let draftedNumber;
  do {
    if (draftedNumbers.length === 100) return -1;
    draftedNumber = Math.floor(Math.random() * 100);
  } while (draftedNumbers.includes(draftedNumber));
  draftedNumbers.push(draftedNumber);
  return draftedNumber;
};

const startGame = () => {
  playerCount++;
  if (playerCount < players.length) return;
  if (!draftNumberIntervalId) {
    draftNumberIntervalId = setInterval(() => {
      const draftedNumber = draftNumber();
      if (draftedNumber === -1 || winner) {
        clearInterval(draftNumberIntervalId);
        draftNumberIntervalId = null;
        const status = { status: 2, message: 'Game finished', winner: draftedNumber === -1 ? 'No winner' : winner };
        players.forEach((p) => p.call.write(status));
      } else {
        players.forEach((p) => p.call.write({ number: draftedNumber, winner, status: 0, message: 'Number drafted' }));
      }
    }, draftNumberInterval);
  }
};

const login = (call) => {
  const { username } = call.request;

  if (gameStarted) {
    call.write({ status: 1, message: 'Game already started.' });
    call.end();
  }

  const playerExists = players.find((p) => p.username.toLowerCase() === username.toLowerCase());
  if (!playerExists) {
    const newPlayer = {
      username,
      token: generateToken(),
      ready: false,
    };
    players.push(newPlayer);
    const interval = runAtInterval(() => {
      if (gameStarted) call.end();
      call.write({
        token: newPlayer.token,
        playersLoggedIn: players.map((p) => p.username),
        playersReady: players.filter((p) => p.ready).map((p) => p.username),
        status: 0,
        message: 'Waiting to start.',
      });
    }, 2000);
    if (gameStarted) clearInterval(interval);
  } else {
    call.write({ status: 1, message: 'Username already taken.' });
    call.end();
  }
};

const ready = async (call, callback) => {
  const { username, token } = call.request;
  const player = players.find((p) => p.username.toLowerCase() === username.toLowerCase() && p.token === token);
  if (player) {
    player.ready = true;

    await waitForReadyPlayers();
    player.card = generateCard();

    callback(null, { status: 0, message: 'Game started', card: player.card });
  } else {
    callback(null, { status: 1, message: 'Player not found' });
  }
};

const play = (call) => {
  const { username, token } = call.request;
  const player = players.find((p) => p.username.toLowerCase() === username.toLowerCase() && p.token === token);
  if (player) {
    player.call = call;
    startGame();
  } else {
    call.write({ status: 1, message: 'Player not found' });
    call.end();
  }
};

const checkWin = (call, callback) => {
  const { username, token } = call.request;
  const player = players.find((p) => p.username.toLowerCase() === username.toLowerCase() && p.token === token);
  if (player) {
    const won = checkBingo(player.card, draftedNumbers);

    if (won) {
      winner = username;
      callback(null, { status: 0, message: 'You won!' });
    } else {
      callback(null, { status: 2, message: 'You didn\'t win' });
    }
  } else {
    callback(null, { status: 1, message: 'Player not found' });
  }
};
/*fim services*/

// Server Initialization
const options = {
  keepCase: true,
  longs: String,
  enums: String,
  defaults: true,
  oneofs: true,
};
const packageDefinition = protoLoader.loadSync(PROTO_PATH, options);
const bingoProto = grpc.loadPackageDefinition(packageDefinition);
const server = new grpc.Server();

server.addService(bingoProto.Bingo.service, {login, ready, play, checkWin});

server.bindAsync(
  host,
  grpc.ServerCredentials.createInsecure(),
  () => {
    console.log(`Server running at http://${host}`);
    server.start();
  }
);