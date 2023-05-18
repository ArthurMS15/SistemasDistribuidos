const generateCard = () => {
  const card = [];
  while (card.length < 24) {
    const num = Math.floor(Math.random() * 100);
    if (!card.includes(num)) card.push(num);
  }
  return card;
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

module.exports = {
  generateCard,
  checkBingo,
};