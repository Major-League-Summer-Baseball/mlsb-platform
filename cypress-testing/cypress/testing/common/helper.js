/**
 * Holds common helper functions.
 * @module common/helper
 */

/**
 * A function to get the current year
 * @return {number} - the current year
 * @example
 * const currentYear = getCurrentYear(); // 2019
 */
export function getCurrentYear() {
  return new Date().getFullYear();
}

/**
 * Creates a random name to use for testing.
 * @return {string} - a random name
 * @example
 * const firstName = randomName();
 */
export function randomName() {
  return 'xxxxxxxx'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}


/**
 * Creates a random email to use for testing.
 * @return {string} - a random email with domain of @mlsb.ca
 * @example
 * const firstName = randomEmail();
 */
export function randomEmail() {
  return 'xxxxxxxx-yyyyyyy@mlsb.ca'.replace(/[xy]/g, function(c) {
    var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

/**
 * Get the first positive integer in a string. Assumes the int
 * is seperate by whitespace
 * @param {string} phrase - the phrase to extract a integer from
 * @return {number} the first positive integer, if none are found then -1
 * @example <caption>Found Case</caption>
 * parseFirstPositiveInt('Hello there 1') // return 1
 * @example <caption>No positive numnber</caption>
 * parseFirstPositiveInt('My name is X') // return -1
 */
function parseFirstPositiveInt(phrase) {
  let i = -1;
  // loop through each part of the phrase and check if a number
  for (const s of phrase.split(' ')) {
    i = parseInt(s);
    if (i >= 0) {
      break;
    }
  }
  return i;
}

/**
 * Parse English to create a date object.
 * <p>The date Strings that are are parsed can be written. </p>
 * <ul>
 *   <li>
 *     Relative wording -
 *     E.g. today", "tomorrow at 12:00" "3 days from now at 13:00"
 *   </li>
 *   <li>
 *     ISO format YYYY-MM-DD or YYYY-MM-DDTHH:MM:SS
 *   </li>
 * @param {string} dateString -  the string version of the date
 * @return {Date} - the parse date
 */
export function parseDateString(dateString) {
  let parsedDate;
  dateString = dateString.trim().toLowerCase();
  if (dateString.startsWith('today')) {
    parsedDate = new Date();
  } else if (dateString.startsWith('tomorrow')) {
    parsedDate = new Date();
    date.setDate(date.getDate() + 1);
  } else if (dateString.startsWith('yeserday')) {
    parsedDate = new Date();
    date.setDate(date.getDate() - 1);
  } else if (dateString.includes('from today')) {
    parsedDate = new Date();
    date.setDate(date + parseFirstPositiveInt(dateString));
  } else if (dateString.includes('ago')) {
    parsedDate = new Date();
    date.setDate(date - parseFirstPositiveInt(dateString));
  } else {
    // assume ISO date
    parsedDate = new Date(dateString);
  }

  // check if a time was specified
  if (dateString.includes('at')) {
    const phrases = dateString.split(' ');
    const times = phrases[phrases.length - 1].split(':');
    // since hours start at zero need to subtract one
    parsedDate.setHours(times[0] - 1);
    parsedDate.setMinutes(times[1]);
  } else {
    parsedDate.setHours(11);
    parsedDate.setMinutes(0);
  }
  return parsedDate;
}
