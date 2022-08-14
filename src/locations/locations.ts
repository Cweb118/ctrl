import District from "./district";
import Region from "./region";

// The City of Barheim
const theCore = new District('the_core', 'The Core');
const theThreshold = new District('the_threshold', 'The Threshold');

const theCityOfBarheim = new Region('the_city_of_barheim', 'The City of Barheim', [theCore, theThreshold]);

// Levyt Cliffside
const theShores = new District('the_shores', 'The Shores');

const levytCliffside = new Region('levyt_cliffside', 'Levyt Cliffside', [theShores]);

// Yavari Domain
const yavar = new District('yavar', 'Yavar');

const yavariDomain = new Region('yavari_domain', 'Yavari Domain', [yavar]);