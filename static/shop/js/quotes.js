const quotes = [
    "All you need is love and a pet ♡",
    "Purrfect deals for your pets!",
    "Happiness is a warm puppy ♡",
    "Dogs are our link to paradise ♡",
    "Pets make life pawsome ♡",
    "Fur-ever friends are the best kind ♡",
    "All pets deserve love and care ♡",
    "A house is not a home without a pet ♡",
    "Pets bring joy, one paw at a time ♡",
    "Pawsitivity starts with a pet ♡",
    "Life is better with furry friends ♡",
    "Love is a four-legged word ♡",
    "Who rescued who? ♡",
    "Paws and enjoy the little things ♡",
    "Furry friends, endless love ♡",
    "Every pet leaves pawprints on our hearts ♡",
    "You had me at woof ♡",
    "Cats rule the world, one purr at a time ♡",
    "Adopt, don't shop ♡",
    "Unconditional love is spelled p-e-t ♡",
    "Live, love, bark ♡",
    "Snuggle up with a pet today ♡",
    "Happiness is wet noses and wagging tails ♡",
    "Pets are family, too ♡",
    "Purrfect companions, forever friends ♡",
    "Pets fill our hearts with love ♡"
];

function updateQuote() {
    const randomIndex = Math.floor(Math.random() * quotes.length);
    const randomQuote = quotes[randomIndex];

    document.getElementById("random-quote").textContent = randomQuote;
}