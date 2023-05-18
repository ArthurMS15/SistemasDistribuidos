const runAtInterval = (callback, interval) => {
    callback();
    return setInterval(callback, interval);
};
  
module.exports = {
    runAtInterval,
};