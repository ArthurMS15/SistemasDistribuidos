const readline = require('readline');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

const input = (prompt) => (
  new Promise((resolve) => {
    rl.question(prompt, (answer) => {
      resolve(answer);
    });
  })
);

module.exports = {
    input,
};