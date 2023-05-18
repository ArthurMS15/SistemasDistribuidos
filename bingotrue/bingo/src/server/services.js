const { generateCard, checkBingo } = require('./card');
const { runAtInterval } = require('../utils');

const minPlayers = 1;
const draftNumberInterval = 2000;

const players = [];
const draftedNumbers = [];

let gameStarted = false;
let winner = '';
let draftNumberIntervalId;
let playerCount = 0;

const generateToken = () => (Math.random() + 1).toString(36).substring(2, 18);

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

    // const interval = runAtInterval(() => {
    //   if (winner) {
    //     call.write({ status: 2, message: 'Game finished', winner });
    //     call.end();
    //   }

    //   const draftedNumber = draftNumber();

    //   if (draftedNumber === -1) {
    //     call.write({ status: 2, message: 'Game finished', winner: 'No winner' });
    //     call.end();
    //   }

    //   call.write({ number: draftedNumber, winner, status: 0, message: 'Number drafted' });
    // }, draftNumberInterval);
    // if (winner) clearInterval(interval);
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

module.exports = {
  login,
  ready,
  play,
  checkWin,
};