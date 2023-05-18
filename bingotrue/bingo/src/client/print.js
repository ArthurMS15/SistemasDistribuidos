const printCard = (card) => {
  console.log('This is your bingo card:\n');
  let counter = 0;
  let grid = '';
  for (let i = 0; i < 5; i++) {
    for (let j = 0; j < 5; j++) {
      if (i === 2 && j === 2) {
        grid += '💥 ';
      } else {
        grid += String(card[counter++]).padStart(2, '0') + ' ';
      }
    }
    grid += '\n';
  }
  console.log(grid);
}

const printPlayers = (playersLoggedIn, playersReady) => {
  console.log(`Players logged in (${playersLoggedIn.length}): ${playersLoggedIn.join(', ')}.`);
  console.log(`Players ready (${playersReady.length}): ${playersReady.join(', ')}.`);
};

const printDraftedNumbers = (draftedNumbers) => {
  console.log(`Drafted numbers (${draftedNumbers.length}): ${draftedNumbers.join(', ')}.`);
};

module.exports = {
  printCard,
  printPlayers,
  printDraftedNumbers,
};